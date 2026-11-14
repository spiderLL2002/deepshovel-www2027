# From a retrieved scientific argument to a research decision

These records trace the Codex research workflow from the 25–27 October 2026 investigation, including candidate screening, the GP15 source and the execution of the reviewed protocol.

## 1. A retrieved prior argument strengthened a candidate rejection

**Question actually submitted.** Candidate REE-R7-02 asked whether hydrothermal bottle measurements could distinguish conservative seawater mixing from element-selective REY loss within a vent orifice. The recorded query explicitly requested the nearest prior studies, methods, sampling support and limitations. See the complete request in [hongo-retrieval.json](records/hongo-retrieval.json).

**What DeepShovel returned.** The saved `ai_rerank` result included a Hongo et al. (2007) claim about REE fractionation during fluid–seawater mixing, with the method field specifying REE versus Mg and a simple dilution model. The service labeled the result `supports` for the source-screening question, with overlapping scope.

**What the agent checked.** The library → graph → visuals → original PDF chain recovered the exact original version, SHA-256 `5aecf1722cf777a13fc8d9bf2617f2d40ae76515e9894ac7de2fdd3fc9e8eced`. The source check found that the proposed REE–Mg / early-mixing contrast substantially overlapped Figures 10–12. It also retained a consequential sampling difference: the vent-fluid measurements were unfiltered and acidified, whereas water-column samples were filtered. A Ce-conflict interpretation in the graph was **not adopted** as a scientific finding. See [historical source-check excerpts](records/historical-source-check-excerpts.json).

**What changed in the research record.** The updated candidate explicitly cites the “New DeepShovel-bound Hongo2007 original PDF” as evidence of direct overlap, and the round decision rejects the current question form. The source overlap strengthened the rejection, which also depended on missing reaction and sampling controls. See [candidate and final disposition](records/hongo-decision.json).

| Recorded stage | UTC on 25 October 2026 | Inspectable evidence |
|---|---|---|
| Preview request issued | 14:51:44.958852 | Original research query, bounded limit 12 |
| `ai_rerank` request issued | 14:52:05.635273 | Saved Hongo claim, scope and source anchors |
| Source-chain requests issued | 14:59:42–14:59:47 | Library, graph, visuals, PDF hash receipt |
| Candidate record updated | 15:07:23.824691 | Direct prior-work overlap recorded |
| Round closed | 15:46:16.075738 | REE-R7-02 rejected in its current form |

Request timestamps are in [hongo-receipts.json](records/hongo-receipts.json). The source is [Hongo et al., Geochemical Journal 41, 1–15 (2007)](https://doi.org/10.2343/geochemj.41.1). Its copyrighted full PDF and long quotations are not redistributed here.

## 2. Trace a source argument into the GP15 research inputs and new claims

[gp15-source-lineage.json](gp15-source-lineage.json) joins existing identities through the following chain:

1. The DeepShovel Lin–Catling source snapshot identifies the original paper, the calibration-related claim and the Figure 3 page anchor.
2. Its artifact PDF SHA-256 equals the `author_paper` SHA-256 in the actual research source-input file.
3. The frozen protocol binds that exact source-input file by SHA-256; the source-chain PDF request predates protocol freezing.
4. The final research claim–source map binds **C01** to the fixed implementation and protocol, **C03** to the empirical layer/aggregate results, and **C12** to the layerwise squared-error differences used in the nonnegative-weight deduction.
5. These exact source and result bytes are available in the [GP15 reproduction package](../gp15/README.md).

The inherited material is the published model definition and calibration scope. The GP15 sampling rules, layer comparisons and C03/C12 are outputs of the subsequent analysis. The cited source is [Lin and Catling (2024)](https://doi.org/10.2475/001c.118215).

## 3. Eight rounds, 48 screened candidates and one research manuscript

[eight-round-screening.json](records/eight-round-screening.json) contains every candidate ID, original question and final root disposition from the author's saved research state, with the complete state-file SHA-256. It derives eight rounds of six questions each, split equally between REE and OAE. The final dispositions are **35 rejected current forms, six rejected after frozen analysis, six not selected because data/novelty gates remained incomplete, and one eligible to draft**.

The one advanced candidate is `REE-R8-01`. Its round-close and manuscript-delivery events are retained, and the later p20 manuscript hash resolves to the public GP15 scientific manuscript.

## 4. Reviewed uncertainty rules, frozen protocol and actual execution

[rsi-protocol-execution.json](records/rsi-protocol-execution.json) exposes the recorded preexecution AI check of revised rules: at least six station labels, at least 90% complete-support bootstrap draws, and no aggregate comparison when a station deletion loses an originally populated layer. The review's recorded time is **15:55:43 UTC on 25 October 2026**. The protocol binds its exact hash at **15:57:54**, and the recorded execution begins at **15:58:00**, using the same protocol and reviewed code hashes.

The outputs report **975/1,000** and **978/1,000** complete-support bootstrap draws with six and eight station labels. All **14** station deletions retained the originally populated layers. The suppression rule is present in the frozen protocol and executable code, but that failure branch was not triggered by these observations. The public verifier checks the actual fields, chronology, code locators and hashes against the GP15 files; its full reproduction workflow separately regenerates the numerical outputs.

## Reproduce the record checks

Python 3 standard library only; no account, service, API key or live network is required:

```sh
python3 -B verify_trace.py
```

When the sibling `gp15/reproduction/payload/` is present, this also checks the public source, protocol and C01/C03/C12 result bytes against their recorded hashes. An explicit payload path can be supplied with `--gp15-payload PATH`.

The [verification report](runs/2026-10-29-census-rsi/public-verification.json) records the checks against the published data and GP15 package. The cited Hongo paper is available from its [publisher](https://doi.org/10.2343/geochemj.41.1). See [references.bib](references.bib) for the bibliographic references.
