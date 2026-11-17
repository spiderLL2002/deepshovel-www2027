# Evaluation data

| Evaluation | Inputs and recorded executions |
| --- | --- |
| Retrieval | 430 questions, 12,541 reference judgments, and four saved rankings per question |
| [Semantic comparison](#semantic-test-scoring) | 264 test cases from 65 papers and 79 development cases from 17 papers, with four model inputs per case |
| Online comparison | 87 Group A queries and 88 Group B queries, with one attempt per query |
| Interactive condition check (F2) | Two queries at friction coefficients 0.6 and 0.4 |
| [Source audit](#source-audit) | Four papers: 129 scientific nodes, 124 scientific dependencies, and 128 source or data links |

[Results](results.json) · [Download the evaluation data and execution logs](https://github.com/spiderLL2002/deepshovel-www2027/releases/download/www2027-artifact/deepshovel-evaluation.zip)

From the extracted package, run `python3 recompute.py`. From the repository root, run `python3 artifact/benchmark/recompute.py`. The command verifies file hashes and computes scores from the packaged inputs, rankings, reference labels, and recorded outputs. The two raw execution archives are available in the download.

- `retrieval/` contains the questions, candidate pools, judgments, and rankings. The rankings were computed on the November 4, 2026 snapshot of the library (9,506 papers and 41,092 claims; see `retrieval/baseline_manifest.json.gz`); the public library has since grown to 10,714 papers. Top-three hit rates use all 430 questions and the original reference grades. nDCG@10 uses the 119 questions with fully graded pools, including supplementary AI grades. The hybrid ranking is the preview before final model reranking.
- `online/` contains the fixed queries and the November 14, 2026 run. Accuracy uses all assigned queries. Mean and median times use completed queries. The full download contains the A/B request and response logs. To run A/B against a deployment, use `python3 run_online.py --base-url https://YOUR-DEPLOYMENT --out runs/online-new` from the evaluation directory.
- Both F2 requests returned the expected relation: [0.6 returned equivalent](online/f2-p01-original/ai_rerank.response.txt) and [0.4 returned qualifies](online/f2-p01-changed/ai_rerank.response.txt). In both cases, the comparison stage reused a validated model result from an identical earlier request. The [0.6](online/f2-p01-original/) and [0.4](online/f2-p01-changed/) directories contain the original preview and rerank requests and responses.

## Semantic test scoring

The paper reports accepted relations. The stricter score also requires the predicted direction to match the reference direction, including for equivalence and contradiction. Among the 46 expanded-argument predictions with an accepted relation but a different direction, 38 were equivalence, 7 were contradiction, and 1 was qualification.

| Comparison input | Relation correct | Relation and direction correct |
| --- | ---: | ---: |
| Claim and conditions | 217/264 | 184/264 |
| Expanded argument | 241/264 | 195/264 |
| Source passages | 221/264 | 187/264 |
| Flat argument | 229/264 | 188/264 |

### Model breakdown

The semantic test ran across two model backends, GPT-6 Luna and DeepSeek V4 Flash, and each record stores the model that answered (`model`). Across the 1,056 judgments, GPT-6 Luna answered 569 and DeepSeek V4 Flash answered 487.

| Comparison input | All cases | Answered by GPT-6 Luna | Answered by DeepSeek V4 Flash |
| --- | ---: | ---: | ---: |
| Claim and conditions | 217/264 | 117/143 | 100/121 |
| Expanded argument | 241/264 | 135/140 | 106/124 |
| Source passages | 221/264 | 127/144 | 94/120 |
| Flat argument | 229/264 | 129/142 | 100/122 |

The paper reports the "All cases" column. On cases where the same model answered both inputs, the expanded argument compares as follows:

| Expanded argument versus | GPT-6 Luna on both inputs | DeepSeek V4 Flash on both inputs |
| --- | ---: | ---: |
| Claim and conditions | 134 versus 114 of 138 | 102 versus 99 of 119 |
| Source passages | 134 versus 121 of 138 | 101 versus 92 of 118 |
| Flat argument | 133 versus 124 of 137 | 102 versus 98 of 119 |

On the 28 queries that omit a needed premise, the four inputs score 13 (claim and conditions), 23 (expanded argument), 16 (source passages), and 21 (flat argument).

See the [scoring code](recompute.py#L81-L114), [results and model counts](results.json#L74-L125), [test outputs](semantic-test/records.json.gz), [development outputs](semantic-dev/records.json.gz), [reference labels and source anchors](datasets/), and [expert review and label agreement](expert-review.json).

## Source audit

The AI-assisted audit covered four papers. Scientific nodes and dependencies were assessed for support in the source. Source or data links were assessed for the evidence supplied by the specific linked passage, figure, table, or data entry.

| Audited item | Total | Fully supported | Partially supported | Unsupported | Uncertain |
| --- | ---: | ---: | ---: | ---: | ---: |
| Scientific nodes | 129 | 129 | 0 | 0 | 0 |
| Scientific dependencies | 124 | 120 | 4 | 0 | 0 |
| Source or data links | 128 | 91 | 28 | 6 | 3 |

Two separately counted data nodes were fully supported. See the [audit totals](results.json#L211-L228), item-level evidence and judgments for [q16](source-audit/q16.json), [q17](source-audit/q17.json), [q18](source-audit/q18.json), and [q19](source-audit/q19.json), and the [referenced graphs and source identifiers](sources/).
