# GP15 research case: public data, fixed protocol and executable claim checks

The GP15 case applies a fixed published REE–pH model and a fixed depth reference to the same matched samples. It reports four primary RMSE values and the six layerwise error contrasts supporting claim C12.

## Reproduce the analysis

From this directory, use Python 3.12:

```sh
python3.12 -B fetch_external_sources.py
python3.12 -B verify_demo.py
```

The first command verifies and restores the two inputs from their original providers. The second checks the claim-to-source bindings and recalculates the primary errors and six exact layerwise contrasts.

The complete analysis regenerates all ten stages, including sensitivities and figures:

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r reproduction/requirements-research.lock
.venv/bin/python -B run_portable.py --out ../../runs/gp15
```

The [research package](reproduction/README.md) documents the ten stages. The portable runner compares scientific data and vector figures byte for byte, reports runtime metadata separately and checks decoded PNG pixels against the declared thresholds. The [saved execution report](verification-2026-10-29-png-policy/portable-verification.json) contains the stage results and file comparisons.

## Primary results

|Primary result|Leg 1|Leg 2|
|---|---:|---:|
|Fixed model RMSE|0.07021355937856119|0.21827126240140987|
|Fixed depth-reference RMSE|0.17008381101696987|0.11029509536786561|
|Model minus reference RMSE|−0.09987025163840868|+0.10797616703354426|
|Unique parent bottle IDs|24|55|
|Layer memberships|28|63|
|Layer counts, shallow to deep|5, 6, 6, 3, 5, 3|16, 14, 17, 7, 5, 4|

RMSE is the square root of the mean of six squared **layer-mean** errors. It is not bottle-level RMSE. Primary layers use the inclusive intervals 200–300, 300–400, 400–500, 500–600, 600–700 and 700–800 m, with the pH table's reported sampling depth. A sample exactly on an internal boundary contributes to both adjacent layers, explaining why membership counts exceed unique bottle counts. Half-open bins, REE-reported depths and equal station weights are retained as sensitivities.

For Leg 2, define `d[k] = model_error[k]^2 - reference_error[k]^2` for the unchanged six primary layer means. The fresh exact-contrast checker yields:

|Depth interval (m)|d[k] (pH units squared)|
|---|---:|
|200–300|0.07284603963469431|
|300–400|0.053675103676973125|
|400–500|0.053196753808448675|
|500–600|0.020764537693458113|
|600–700|0.00693500760912255|
|700–800|0.005446573145896173|

All six contrasts are strictly positive. Thus, for any nonnegative weights summing to one **on these same six unchanged means**, `MSE_model - MSE_reference = sum(w[k] * d[k]) >= min(d) > 0`; the increasing square-root function preserves the RMSE ordering. This is C12. Exact fractions are in the fresh JSON. It does not cover changing samples within a layer, geographical weighting, simultaneous REE perturbations or all possible calibration uncertainty. Leg 1 has two positive and four negative contrasts and does not have this weight-invariant ordering.

## Exact model and fixed comparator

The [frozen protocol](reproduction/payload/ree/round8/protocol-frozen-v1.json) binds the source-manifest and analysis-code hashes and specifies matching, flags, depth conventions, weights, constants and sensitivities. It was frozen at `2026-10-25T15:57:54.693118+00:00`. Its presence records a frozen protocol; claims about response exposure additionally depend on the preserved exposure/acquisition record.

For `Sm, Gd, Dy, Er`, the released procedure normalizes concentrations by the original PAAS constants and molar masses, computes the ordinary least-squares slope `alpha` against atomic numbers `62, 64, 66, 68`, then uses:

```text
pH = (alpha - 3.339192211653703e-07) / (-3.9879452461785675e-08)
```

The raw REE concentrations are in pmol/kg. Multiplication by `1e-15` converts them to mol/g; the PAAS conversion is `PAAS_ug_per_g * 1e-6 / (molar_mass_mg_per_mol * 1e-3)`. The code, original coefficient CSVs and author implementation are preserved. Neither coefficients nor comparator values are fitted to GP15.

The six fixed depth-reference pH values, in the interval order above, are:

```text
7.73087871249336, 7.6898707001764945, 7.658636222030023,
7.6315530378663246, 7.606188333846088, 7.584325607003087
```

These are the original global calibration-layer pH means saved in the author's notebook. The original calibration relates separately averaged global REE and pH data; it is not a set of same-bottle calibration pairs. The comparator uses the same target means and layer weights as the transferred model. Arithmetic means are computed on the reported pH scale; no hydrogen-ion mixing calculation is claimed.

## pH scale, temperature, pressure and sample identity

The GP15 target is **total-scale pH measured at 25°C and ambient pressure**, not in-situ pH at the sample's ocean depth. Both BCO-DMO pH dataset methods describe a 25°C bath and measurement at 25 ± 0.1°C, and their attached intercalibration reports specify the total scale: [Leg 1, version 2](https://www.bco-dmo.org/dataset/838157) and [Leg 2, version 2](https://www.bco-dmo.org/dataset/838173).

The original proxy code explicitly selects GLODAPv2.2022 `G2phts25p0`, whose official definition is **total-scale pH at 25°C and 0 dbar (surface pressure)**. The depth reference is derived from the same field. Therefore the target, calibration response and depth reference share the reported scale/temperature/pressure basis; no additional temperature or pressure conversion was applied or required to align those stated bases. The field definition is in Table 1 of the [GLODAPv2.2022 data paper](https://essd.copernicus.org/articles/14/5543/2022/), with the release identified by [NOAA](https://www.ncei.noaa.gov/access/ocean-carbon-acidification-data-system/oceans/GLODAPv2_2022/). This alignment does not remove laboratory offsets or turn the comparison into an in-situ speciation test. The original code selects nonmissing product pH rather than measured-only pH; the exact calculated-pH fraction of its selected calibration subset was not reconstructed.

Joins require exact parent sample ID and matching station/event, finite responses, allowed bottle quality flags and the prescribed depth rules. pH was measured in an unfiltered aliquot and REE in a 0.2 µm filtered aliquot from the same parent Go-Flo bottle. The match therefore establishes parent bottle identity, not identical analytical aliquots. One source depth conflict remains explicit: sample 14984 is listed at 360 m in the REE table and 261 m in the pH table. The primary convention uses the latter; the alternative-depth sensitivity is retained without adjudicating the conflicting metadata.

## Files and claim tracing

- [claim-source-map.json](claim-source-map.json) selects C01 (fixed implementation), C02 (matched support), C03 (four RMSEs) and C12 from the final research map. It retains original file hashes and adds resolving export paths; nine file bindings are checked by `verify_demo.py`.
- [Scientific manuscript](scientific-manuscript.en.md) and [scientific supplement](scientific-supplementary.en.md) are the unchanged p20 texts identified by that source map.
- [transfer-source-input.json](reproduction/payload/ree/round8/transfer-source-input.json) binds the 17 original input/supporting files to source URLs, SHA-256 values, roles and locators.
- [pairing_audit.csv](reproduction/payload/results/ree_ph_fixed_transfer_v1/pairing_audit.csv), [sample_predictions.csv](reproduction/payload/results/ree_ph_fixed_transfer_v1/sample_predictions.csv) and [layer_summary.csv](reproduction/payload/results/ree_ph_fixed_transfer_v1/layer_summary.csv) expose selection decisions, sample IDs and calculations.
- [layer_squared_error_difference.csv](reproduction/payload/iteration-2026-10-27/analysis/selection-weight-domain-v1/layer_squared_error_difference.csv) supplies the C12 contrasts; the preserved checker reconstructs their signs with exact rational arithmetic.
- [table-source-map-v2.public.json](reproduction/payload/iteration-2026-10-27/reproducibility/public-lineage/table-source-map-v2.public.json) resolves the larger research table/method index and records unavailable historical context explicitly.


## Attribution and redistribution scope

The four original measurement CSVs are retained unchanged under the dataset providers' CC BY 4.0 terms, with method reports and versioned identifiers:

|Content|Creators / source|Versioned identifier|
|---|---|---|
|GP15 Leg 1 REE|Alan M. Shiller and Melissa Gilbert, BCO-DMO|[10.26008/1912/bco-dmo.932161.1](https://doi.org/10.26008/1912/bco-dmo.932161.1)|
|GP15 Leg 2 REE|Alan M. Shiller and Melissa Gilbert, BCO-DMO|[10.26008/1912/bco-dmo.932559.1](https://doi.org/10.26008/1912/bco-dmo.932559.1)|
|GP15 Leg 1 pH|Gregory Cutter and Nicole Buckley, BCO-DMO|[10.26008/1912/bco-dmo.838157.2](https://doi.org/10.26008/1912/bco-dmo.838157.2)|
|GP15 Leg 2 pH|Gregory Cutter and Nicole Buckley, BCO-DMO|[10.26008/1912/bco-dmo.838173.2](https://doi.org/10.26008/1912/bco-dmo.838173.2)|

Credit Ping-Chun Lin and David C. Catling (2024), [10.2475/001c.118215](https://doi.org/10.2475/001c.118215), for the original model. Author software is pinned to repository commit `99ebf142d6787361c7720b7a3e7c213fd213eddb`, with its [unchanged MIT notice](reproduction/payload/ree/round8/raw/Lin2024-LICENSE). The article states CC BY 4.0 on PDF page 17; its unchanged PDF/text and source identity are included. Cite the original source and preserve the applicable notices when reusing these materials.

Two supporting items are **downloaded from their providers instead of committed**: the author's compiled `REE_seawater_all_pmol.csv` and the GLODAPv2.2022 `Dataset_DOIs.csv` catalogue. The software MIT notice is not used to assign a blanket license to all upstream compiled measurements. `fetch_external_sources.py` obtains these exact source bytes, verifies the frozen hashes and restores their required paths; `.gitignore` excludes the local copies. The full GLODAP merged data product is not distributed here. The source manifest retains the original URLs and attribution.
