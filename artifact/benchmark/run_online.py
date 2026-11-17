#!/usr/bin/env python3
"""Run the frozen A/B queries against a specified two-stage search API."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import gzip
import http.client
import json
from pathlib import Path
import statistics
import time
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent


def read_json(path):
    data = path.read_bytes()
    return json.loads(gzip.decompress(data) if path.suffix == '.gz' else data)


def save_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def now():
    return datetime.now(timezone.utc).isoformat()


def select_tasks(tasks, limit):
    groups = {'A': [], 'B': []}
    for task in tasks:
        if task.get('kind') == 'online' and task.get('group') in groups:
            groups[task['group']].append(task)

    selected = []
    for group, rows in groups.items():
        ids = [row['case']['id'] for row in rows]
        if len(ids) != len(set(ids)):
            raise ValueError(f'Duplicate query in group {group}')
        if not ids or (limit is not None and len(ids) < limit):
            raise ValueError(f'Too few queries in group {group}')
        selected.extend(rows[:limit])
    return selected


def post_stage(base_url, payload, deadline, directory, stages):
    stage = payload['stage']
    entry = {'stage': stage, 'status': 'failed', 'started_at': now(),
             'request_file': f'{directory.name}/{stage}.request.json',
             'response_file': f'{directory.name}/{stage}.response.txt'}
    stages.append(entry)
    request_bytes = json.dumps(payload, ensure_ascii=False).encode()
    (directory / f'{stage}.request.json').write_bytes(request_bytes)
    url = urlsplit(base_url)
    connection_type = http.client.HTTPSConnection if url.scheme == 'https' else http.client.HTTPConnection
    started = time.monotonic()
    connection = connection_type(url.hostname, url.port, timeout=max(0.001, deadline - started))
    try:
        if started >= deadline:
            raise TimeoutError('Full-query deadline reached')
        connection.request('POST', url.path.rstrip('/') + '/api/evidence-search',
                           body=request_bytes,
                           headers={'Content-Type': 'application/json',
                                    'Accept': 'application/x-ndjson',
                                    'Origin': f'{url.scheme}://{url.netloc}'})
        response = connection.getresponse()
        entry['http_status'] = response.status
        entry['content_type'] = response.getheader('content-type', '')
        streamed = 'application/x-ndjson' in entry['content_type'].lower()
        chunks, pending, terminal = [], b'', None
        with (directory / f'{stage}.response.txt').open('wb') as raw:
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError('Full-query deadline reached')
                sock = connection.sock or getattr(getattr(response.fp, 'raw', None), '_sock', None)
                if sock is not None:
                    sock.settimeout(remaining)
                chunk = response.read1(65536)
                if not chunk:
                    break
                raw.write(chunk)
                raw.flush()
                if streamed:
                    pending += chunk
                    while b'\n' in pending:
                        line, pending = pending.split(b'\n', 1)
                        if line.strip():
                            event = json.loads(line)
                            if event.get('type') == 'result':
                                terminal = event
                    if terminal is not None:
                        break
                else:
                    chunks.append(chunk)
        if not 200 <= response.status < 300:
            raise ValueError(f'HTTP {response.status}')
        if streamed:
            if pending.strip() and terminal is None:
                event = json.loads(pending)
                if event.get('type') == 'result':
                    terminal = event
            if terminal is None:
                raise ValueError('Stream ended without a result')
            entry['status_code'] = terminal['status']
            body = terminal['body']
        else:
            entry['status_code'] = response.status
            body = json.loads(b''.join(chunks))
        if not 200 <= entry['status_code'] < 300 or body.get('ok') is not True:
            raise ValueError(json.dumps(body.get('error', body), ensure_ascii=False)[:1500])
        if body.get('stage') != stage:
            raise ValueError('Response stage differs from request')
        if body.get('channels', {}).get('relation', {}).get('status') == 'degraded':
            raise ValueError('Relation analysis returned degraded status')
        entry['status'] = 'ok'
        entry['result_status'] = body.get('resultStatus')
        return body
    except Exception as error:
        entry['error'] = {'type': type(error).__name__, 'message': str(error)}
        raise
    finally:
        connection.close()
        entry['elapsed_seconds'] = time.monotonic() - started
        entry['finished_at'] = now()


def evaluate_task(task, base_url, timeout, output, protocol):
    started = time.monotonic()
    case = task['case']
    directory = output / task['task_id']
    directory.mkdir()
    record = {'task_id': task['task_id'], 'group': task['group'], 'repetition': task['repetition'],
              'case_id': case['id'], 'experiment_attempt': 1, 'started_at': now(),
              'status': 'failed', 'stage': 'preview', 'stages': [],
              'accepted_relation_and_direction': False, 'target_in_final': False}
    base = {'search_protocol': protocol['search_protocol'], 'query': case['query'],
            'intent': 'claim_search', 'corpus': 'cross_paper', 'limit': protocol['limit']}
    try:
        preview = post_stage(base_url, {**base, 'stage': 'preview'}, time.monotonic() + timeout, directory, record['stages'])
        record['result_status'] = preview.get('resultStatus')
        if preview.get('resultStatus') in {'clarification_required', 'needs_context'}:
            record['status'] = 'incomplete'
            return record
        candidates = preview['previewResults']
        record['preview_candidate_count'] = len(candidates)
        if not candidates:
            if preview.get('resultStatus') != 'no_direct_answer':
                raise ValueError('Preview has no candidates without a no_direct_answer result')
            record['status'] = 'incomplete'
            return record
        if not preview.get('queryPlanHandoff'):
            raise ValueError('Preview did not supply a query-plan handoff')
        record['stage'] = 'ai_rerank'
        final = post_stage(base_url, {**base, 'stage': 'ai_rerank',
                           'query_plan_handoff': preview['queryPlanHandoff'],
                           'candidate_refs': [{'snapshot_id': item['snapshotId'],
                                               'claim_id': item['claim']['id']} for item in candidates]},
                           time.monotonic() + timeout, directory, record['stages'])
        record['result_status'] = final.get('resultStatus')
        if final.get('resultStatus') not in {'matches', 'no_direct_answer', 'degraded'}:
            raise ValueError('Final response lacks a terminal result status')
        for cluster in final['clusters']:
            for member in [cluster['representative'], *cluster.get('members', [])]:
                if member['snapshotId'] == case['snapshot_id'] and member['claim']['id'] == case['claim_id']:
                    relation = member['queryRelation']
                    record.update(target_in_final=True, relation=relation['relation'], direction=relation['direction'])
                    record['accepted_relation_and_direction'] = (
                        relation['relation'] in case['accepted_relations'] and relation['direction'] == case['direction'])
                    break
            if record['target_in_final']:
                break
        record['status'] = 'complete'
    except Exception as error:
        record['error'] = {'type': type(error).__name__, 'message': str(error)}
    finally:
        record['finished_at'] = now()
        record['elapsed_seconds'] = time.monotonic() - started
    return record


def summarize(tasks, records):
    summary = {}
    for group in ('A', 'B'):
        scheduled = [task for task in tasks if task['group'] == group]
        rows = [row for row in records if row['group'] == group]
        completed = [row for row in rows if row['status'] == 'complete']
        times = [row['elapsed_seconds'] for row in completed]
        correct = sum(row['accepted_relation_and_direction'] for row in completed)
        summary[group] = {'queries': len({task['case']['id'] for task in scheduled}),
                          'attempts': len(scheduled), 'completed': len(completed),
                          'failed_or_missing': len(scheduled) - len(completed),
                          'relation_and_direction_correct': correct,
                          'accuracy_all_attempts': correct / len(scheduled),
                          'mean_completed_seconds': statistics.mean(times) if times else None,
                          'median_completed_seconds': statistics.median(times) if times else None}
    return summary


def main(argv=None):
    protocol = read_json(ROOT / 'online/protocol.json.gz')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True, help='New output directory')
    parser.add_argument('--base-url', required=True, help='URL of the service to evaluate')
    parser.add_argument('--limit-per-group', type=int, help='Queries per group (default: all retained queries)')
    args = parser.parse_args(argv)
    url = urlsplit(args.base_url)
    if url.scheme not in {'http', 'https'} or not url.hostname or url.username or url.password or url.query or url.fragment:
        parser.error('--base-url must be an HTTP(S) service URL without credentials, query or fragment')
    max_balanced_limit = min(protocol['group_sizes'].values())
    if args.limit_per_group is not None and not 1 <= args.limit_per_group <= max_balanced_limit:
        parser.error('Limit must fit both retained groups')
    tasks = select_tasks(read_json(ROOT / 'online/tasks.frozen.json.gz')['tasks'],
                         args.limit_per_group)
    output = args.out.resolve()
    output.mkdir(parents=True, exist_ok=False)
    save_json(output / 'tasks.json', {'tasks': tasks})
    save_json(output / 'run.json', {'started_at': now(), 'base_url': args.base_url,
                                   'timeout_seconds': protocol['timeout_seconds'],
                                   'concurrency': protocol['logical_concurrency'], 'attempts': len(tasks)})
    records = []
    try:
        with ThreadPoolExecutor(max_workers=protocol['logical_concurrency']) as pool, (output / 'records.jsonl').open('w') as log:
            pending = {pool.submit(evaluate_task, task, args.base_url, protocol['timeout_seconds'], output, protocol): task for task in tasks}
            for future in as_completed(pending):
                record = future.result()
                records.append(record)
                log.write(json.dumps(record, ensure_ascii=False) + '\n')
                log.flush()
                print(record['task_id'] + ': ' + record['status'], flush=True)
    finally:
        summary = summarize(tasks, records)
        save_json(output / 'summary.json', summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return int(any(row['status'] != 'complete' for row in records) or len(records) != len(tasks))


if __name__ == '__main__':
    raise SystemExit(main())
