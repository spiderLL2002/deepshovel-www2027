# Evaluation and research reproduction

| Material | What the reproduction checks |
| --- | --- |
| [Evaluation](../artifact/benchmark/README.md) | Retrieval, argument comparison, online search, F2, and source-audit scores from the published records |
| [Argument inspection](../artifact/arguments/README.md) | The production expander follows 18 premise edges and three assumption edges for F2. Seven full claim expansions agree with an independent traversal of the Asmari graph. |
| [GP15 research](../artifact/gp15/README.md) | Ten analysis stages reproduce the four RMSEs and six layerwise error contrasts. |
| [Research trace](../artifact/research-trace/README.md) | File and identifier links connect the recorded queries, source evidence, and research decisions. |

The [paper reproduction command](../README.md#reproduce-the-evaluation-and-gp15-research) writes its completion status to `report.json` and the output of each step to a separate log.
