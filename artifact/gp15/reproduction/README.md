# GP15 fixed REE–pH data and code

This package contains the public inputs, frozen programs and plans, reference results, independent numerical checkers and five figures for a reanalysis of the published fixed REE–pH implementation along GEOTRACES GP15. All 17 original analytical/supporting source files are retained unchanged, with the original author-code MIT notice and saved notebook output. Derived training-domain annotations, later exposed-data diagnostics and their provenance are distinguished from original measurements. The companion main manuscript and scientific supplementary information are delivered separately; their p20 version and caption identity are recorded as metadata in the export plan.

## Run

Use Python 3.12 and the pinned dependency lock:

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements-research.lock
.venv/bin/python -B run_reproduction.py
```

The reference environment is Python 3.12.13, Matplotlib 3.10.7 and NumPy 2.5.4; all transitive research dependencies are listed in `requirements-research.lock`. No network access, DeepShovel session, model fitting or source download is used during reproduction after dependencies are installed. In the parent research repository, the existing research environment supplies these dependencies.

The wrapper verifies the export manifest, creates a new temporary task tree and runs ten stages. Every generated directory or receipt is deleted only from that disposable copy before its stage runs. Exported originals are checked again at the end. An optional `--out NEW_DIRECTORY` selects a new working directory outside the export; existing paths are rejected. The printed local receipt and logs provide the actual execution outcome. No complete-run PASS is inferred from the presence of reference outputs.

|Stage|Actual calculation or check|Reference comparison scope|
|---|---|---|
|1|Original fixed analysis, including declared resampling and sensitivities|11 output files|
|2|Independent original raw-source recomputation|15,276 numeric comparisons; 5,034 identity/status comparisons; 962 audit rows|
|3|Earlier reviewer diagnostics|14 output files|
|4|Independent earlier reviewer diagnostics|6,357 numeric and 10,785 identity/status comparisons|
|5|Existing-result SI/QC display export|12 output files|
|6|Exact declared-decimal continuous-box calculation|8 output files; 6,108 required comparisons with preserved legacy quantities|
|7|Independent continuous-box checker C|12,750 categorized comparisons; complete category map and zero-mismatch requirement|
|8|Selection, fixed depth-weight argument and domain display|10 output files|
|9|Independent selection/weight/domain checker B|12,526 categorized comparisons; complete category map and zero-difference requirement|
|10|Five publication figures|15 PNG/SVG/PDF images, five coordinate CSVs and one figure manifest|

The six output-generating stages compare 76 reference files. Fresh receipts are checked using comparison-count maps, success/mismatch fields and declared scientific/support values. Receipt timestamps are excluded from byte comparisons. Categorized totals cover numerical, identity, coverage and source-binding checks.

Strict file-byte comparisons refer to the reference environment. A different Python patch/build, platform or plotting stack can change recorded runtime strings or image bytes. Such differences are reported rather than silently normalized. Original scientific constants, source decimals, frozen code and source hashes are never rewritten to make a run pass. The raw receipt may contain the local temporary working path; it belongs outside a public submission packet. A path-neutral public summary must retain the actual comparison results and raw-receipt SHA without copying private paths or service sessions.

## Data, source roles and figures

The payload preserves task-relative paths. The resolving public table/method index is:

```text
payload/iteration-2026-10-27/reproducibility/public-lineage/table-source-map-v2.public.json
```

Every `groups[].bindings[].path` resolves within the payload. Original v1/v2 maps and the original v2 SHA are retained as provenance references.

The original measurement archives are BCO-DMO REE datasets [932161 version 1](https://doi.org/10.26008/1912/bco-dmo.932161.1) and [932559 version 1](https://doi.org/10.26008/1912/bco-dmo.932559.1), and pH datasets [838157 version 2](https://doi.org/10.26008/1912/bco-dmo.838157.2) and [838173 version 2](https://doi.org/10.26008/1912/bco-dmo.838173.2). The four original CSV SHAs are unchanged. The other original sources retain analytical methods, normalization constants, author implementation, saved calibration outputs, the original REE compilation and release-specific GLODAP catalogue. The source manifest preserves public URLs, versions, roles, hashes and original column/page/table locators. Additional derived annotations do not increase the 17-source original-input count.

The directory `payload/iteration-2026-10-27/figures/final_v1` contains three main and two supplementary figures, their plan, code, coordinates, captions, source manifest and PDF QA. Its five coordinate tables match the frozen v3 tables byte for byte. Figure S2 identifies six global calibration means. PDFs use embedded TrueType fonts and vector cell paths; QA records zero raster XObjects and no creation/modification dates. The renderer reads `CAPTIONS.md` and creates 21 files.

The novelty report contains dated queries, 102 title/DOI screening records, nearest-study comparisons and coverage gaps. Source DOI/URL/locators and original file identities are retained. The adjacent DeepShovel coverage summary records seven itemwise comparisons, all incomplete and with no accepted relations. External full texts follow their source redistribution permissions.

## Scientific scope

The primary estimand is six means of actual eligible samples on each leg under the original inclusive pH-depth bins. The original 24/55 unique bottles and 28/63 memberships are retained. Adjacent layers can contain different stations; equal station weights cannot recover missing stations or yield area-weighted regional means. The two legs share cruise and laboratory dependencies, and bottle identity joins distinct analytical aliquots.

All target responses were exposed before the later diagnostics. Common-station restriction, mean-offset decomposition, abundance–shape descriptions and domain annotations are descriptive checks. Centered errors are not validated bias-corrected performance or pure vertical-shape errors. The unresolved 99 m reported-depth conflict remains disclosed, with the original alternative-depth sensitivity retained. The algebraic abundance–shape relation does not identify a physical residual mechanism.

The continuous-box certificates concern the original equal-weight layer means, four shared coherent REE coordinates and nine discrete pH-offset pairs interpreted through declared decimal constants. They do not supply real measurement-error hard bounds, continuous pH-error coverage or full joint-coefficient uncertainty. The separate arbitrary nonnegative depth-weight statement concerns unchanged point errors; it is not a joint arbitrary-weights-plus-REE theorem. The fixed model and fixed depth reference are not fitted to GP15. These finite modern comparisons do not establish global failure, regional representativeness, causation or failure of the original coarse approximately 1–2 pH-unit Precambrian objective.

## Attribution and licenses

Credit Shiller and Gilbert for REE measurements and Cutter and Buckley for pH, retaining CC BY 4.0 attribution and versioned DOIs. Credit Ping-Chun Lin and David C. Catling (2024), DOI [10.2475/001c.118215](https://doi.org/10.2475/001c.118215), for the model and paper. The author repository commit and MIT notice remain in the source records. The article carries CC BY 4.0 on PDF page 17; its PDF/text, attribution, SHA and license record are retained. The GLODAP catalogue is attributed to v2.2022. Compiled measurements and supporting materials retain their source licenses.
