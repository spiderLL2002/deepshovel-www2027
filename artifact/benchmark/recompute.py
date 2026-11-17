#!/usr/bin/env python3
"""Recompute the published results. Uses the Python standard library."""
import argparse
from collections import Counter, defaultdict
import gzip
import hashlib
import json
import math
from pathlib import Path
import statistics

ROOT = Path(__file__).resolve().parent
VARIANTS = ("claim_scope", "full_argument", "source_passages", "flat_argument")


def read(name):
    path = ROOT / name
    return json.loads(gzip.decompress(path.read_bytes()) if path.suffix == ".gz" else path.read_bytes())


def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def retrieval():
    queries = [q["query_id"] for q in read("retrieval/queries.json.gz")["queries"]]
    runs = read("retrieval/runs_baselines.json.gz")
    runs["hybrid"] = read("retrieval/runs_hybrid.json.gz")
    ranked = {
        name: {row["query_id"]: [doc["document_id"] for doc in row["results"][:12]]
               for row in rows}
        for name, rows in runs.items()
    }
    assert all(rows.keys() == set(queries) for rows in ranked.values())
    pools = read("retrieval/pools.json.gz")
    assert pools.keys() == set(queries)
    assert all(set(pools[q]) == set().union(*(rows[q] for rows in ranked.values()))
               for q in queries)
    labels = {row["query_id"]: {j["document_id"]: j["relevance"] for j in row["judgments"]}
              for row in read("retrieval/judgments_retrieval.json.gz")}
    supplements = {row["query_id"]: {j["document_id"]: j["relevance"] for j in row["judgments"]}
                   for row in read("retrieval/supplemental-judgments.json.gz")}
    assert all(not (grades.keys() & labels.get(q, {}).keys()) for q, grades in supplements.items())
    combined = {q: {**labels.get(q, {}), **supplements.get(q, {})} for q in queries}

    def dcg(grades):
        return sum((2**g - 1) / math.log2(i + 2) for i, g in enumerate(grades[:10]))

    ideal = {q: dcg(sorted((combined[q][d] for d in pools[q]), reverse=True))
             for q in queries if set(pools[q]) <= combined[q].keys()}
    eligible = [q for q, value in ideal.items() if value]
    methods = {}
    for method, results in ranked.items():
        scores = {"complete": 0, "complete_or_partial": 0}
        for q in queries:
            grades = [labels.get(q, {}).get(d) for d in results[q][:3]]
            for name, threshold in (("complete", 3), ("complete_or_partial", 2)):
                hit = any(g is not None and g >= threshold for g in grades)
                assert hit or (len(grades) == 3 and None not in grades), (method, q, name)
                scores[name] += hit
        methods[method] = {
            "top3_complete": {"hits": scores["complete"], "questions": len(queries),
                              "rate": scores["complete"] / len(queries)},
            "top3_complete_or_partial": {"hits": scores["complete_or_partial"], "questions": len(queries),
                                         "rate": scores["complete_or_partial"] / len(queries)},
            "ndcg_at_10": {"questions": len(eligible),
                           "score": round(statistics.mean(
                               dcg([combined[q][d] for d in results[q]]) / ideal[q]
                               for q in eligible), 12)},
        }
    return {"questions": len(queries), "original_judgments": sum(map(len, labels.values())),
            "supplemental_graded_judgments": sum(map(len, supplements.values())),
            "fully_graded_questions": len(eligible), "methods": methods}


def semantic(split):
    cases = {c["id"]: c for c in read(f"datasets/semantic-{split}.frozen.json")["cases"]}
    manifest = read(f"semantic-{split}/manifest.json.gz")
    rows = read(f"semantic-{split}/records.json.gz")
    assert len(cases) == manifest["case_count"] and len(rows) == manifest["logical_judgments"]
    prompt = read("semantic-prompt-schema.json.gz")["system_prompt"]
    assert hashlib.sha256(prompt.encode()).hexdigest() == manifest["prompt_sha256"]
    assert all(r["repetition"] == manifest["repetition"] and r["experiment_attempt"] == 1 for r in rows)
    first = {(r["id"], r["condition"]): r for r in rows}
    assert len(first) == len(rows)
    assert all(cid in cases and condition in VARIANTS for cid, condition in first)
    scores = {}
    for variant in VARIANTS:
        counts = Counter(total=len(cases), failed_or_missing=0, relation_correct=0,
                         relation_and_direction_correct=0)
        models = Counter()
        for cid, case in cases.items():
            row = first.get((cid, variant))
            if row is None or row["status"] != "ok":
                counts["failed_or_missing"] += 1
                continue
            assert hashlib.sha256(row["user_content"].encode()).hexdigest() == row["user_content_sha256"]
            assert json.loads(row["user_content"])["query"] == case["query"]
            assert row["system_prompt_sha256"] == manifest["prompt_sha256"]
            assert any(isinstance(attempt.get("text"), str)
                       and hashlib.sha256(attempt["text"].encode()).hexdigest() == row["output_content_sha256"]
                       and json.loads(attempt["text"]) == row["output"] for attempt in row["raw_attempt_outputs"])
            decision = row["output"]["decisions"][0]
            accepted = decision["relation"] in case["accepted_relations"]
            counts["relation_correct"] += accepted
            counts["relation_and_direction_correct"] += accepted and decision["direction"] == case["direction"]
            models[row["model"]] += 1
        scores[variant] = {**counts, "model_counts": dict(models)}
    return {"cases": len(cases), "papers": len({c.get("paper_id") or c["source"] for c in cases.values()}),
            "categories": dict(Counter(c["paper_category"] for c in cases.values())), "variants": scores}


def online():
    tasks = read("online/tasks.frozen.json.gz")["tasks"]
    rows = read("online/records.json.gz")
    assert all(r["experiment_attempt"] == 1 for r in rows)
    records = {r["task_id"]: r for r in rows}
    task_ids = {task["task_id"] for task in tasks}
    assert len(records) == len(rows) and len(task_ids) == len(tasks) and records.keys() <= task_ids
    groups = defaultdict(list)
    for task in tasks:
        key = task["group"] if task["kind"] == "online" else "F2"
        groups[key].append((task, records.get(task["task_id"])))
    result = {}
    for key, rows in groups.items():
        completed = [r for _, r in rows if r is not None and r["status"] == "complete"]
        times = [r["elapsed_seconds"] for r in completed]
        correct = 0
        for task, record in rows:
            if record is not None and record["status"] == "complete":
                case = task["case"]
                accepted = (record.get("relation") in case["accepted_relations"]
                            and record.get("direction") == case["direction"])
                assert accepted == record.get("accepted_relation_and_direction", False), task["task_id"]
                correct += accepted
        result[key] = {"queries": len({task["case"]["id"] for task, _ in rows}), "attempts": len(rows),
                       "completed": len(completed), "failed_or_missing": len(rows) - len(completed),
                       "relation_and_direction_correct": correct,
                       "mean_completed_seconds": statistics.mean(times) if times else None,
                       "median_completed_seconds": statistics.median(times) if times else None}
    return result


def audit():
    tally = defaultdict(Counter)
    for path in sorted((ROOT / "source-audit").glob("q*.json")):
        for item in json.loads(path.read_text())["items"]:
            tally[item["audit_category"]][item["decision"]] += 1
    return {key: dict(value) for key, value in tally.items()}


def calculate():
    return {"retrieval": retrieval(), "semantic_test": semantic("test"), "semantic_development": semantic("dev"),
            "online": online(), "source_audit": audit()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Write results.json after intentionally updating the dataset")
    args = parser.parse_args()
    actual = calculate()
    if args.write:
        (ROOT / "results.json").write_text(json.dumps(actual, indent=2, ensure_ascii=False) + "\n")
    else:
        assert actual == read("results.json"), "Published results differ from itemwise records"
        manifest = ROOT / "SHA256SUMS"
        optional_raw = {"retrieval/execution-records.json.gz", "online/request-response-files.json.gz"}
        for line in manifest.read_text().splitlines():
            expected, name = line.split("  ", 1)
            if name in optional_raw and not (ROOT / name).exists():
                print("Raw archive is in the complete release download:", name)
                continue
            assert sha256_file(ROOT / name) == expected, name
    print(json.dumps(actual, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
