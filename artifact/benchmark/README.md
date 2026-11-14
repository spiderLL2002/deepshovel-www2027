# Evaluation data

| Evaluation | Inputs and recorded executions |
| --- | --- |
| Retrieval | 430 questions, 12,541 reference judgments, and four saved rankings per question |
| Semantic comparison | 264 test cases from 65 papers and 79 development cases from 17 papers, with four model inputs per case |
| Online comparison | 87 Group A queries and 88 Group B queries, with one attempt per query |
| Interactive condition check (F2) | Two queries at friction coefficients 0.6 and 0.4 |
| Source audit | 129 scientific nodes and 124 dependencies |

[Results](results.json) · [Download the evaluation data and execution logs](https://github.com/spiderLL2002/deepshovel-www2027/releases/download/www2027-artifact/deepshovel-evaluation.zip)

From the extracted package, run `python3 recompute.py`. From the repository root, run `python3 artifact/benchmark/recompute.py`. The command verifies file hashes and computes scores from the packaged inputs, rankings, reference labels, and recorded outputs. The two raw execution archives are available in the download.

- `retrieval/` contains the questions, candidate pools, judgments, and rankings. Top-three hit rates use all 430 questions and the original reference grades. nDCG@10 uses the 119 questions with fully graded pools, including supplementary AI grades. The hybrid ranking is the preview before final model reranking.
- `datasets/` contains the semantic queries, accepted relations and directions, and source anchors. `semantic-test/` and `semantic-dev/` contain the model inputs and outputs for the published scores. The fixed comparisons requested GPT-6-Luna and also used DeepSeek V4 Flash fallback outputs. The per-input model counts are in `results.json`. The expert review and reference-label agreement are in [expert-review.json](expert-review.json).
- `online/` contains the fixed queries and the November 14, 2026 run. Accuracy uses all assigned queries. Mean and median times use completed queries. The [F2 0.6](online/f2-p01-original/) and [F2 0.4](online/f2-p01-changed/) directories contain the original preview and rerank requests and responses. The full download contains the A/B request and response logs. To run A/B against a deployment, use `python3 run_online.py --base-url https://YOUR-DEPLOYMENT --out runs/online-new` from the evaluation directory.
- `source-audit/` contains the item-level evidence and judgments. `sources/` contains the referenced graphs and source identifiers.
