# Recorded-input completeness and scope evidence

This package runs the **DeepShovel claim-detail expander** on a saved Asmari graph and checks its output against recorded dependencies.

## Run

Use Node.js 22.13 or newer. No package installation, credentials, model calls, database, or network access is required.

```sh
node --experimental-strip-types --no-warnings verify.mjs --out runs/local
```

The command checks the vendored modules against the corresponding released source files and verifies the [shared Asmari graph](../second-case/full-graph.json). It compares the expander with an independent fixed-point reference and writes `report.json`, `f2-full-evidence-path.json`, and `f2-depth-2.json` under the requested output directory. The checked execution is saved in `runs/verified/`.

## What the real F2 example shows

The recorded conclusion is the approximate **55–57 MPa maximum sustainable pore pressure for F2 under the paper's modeled conditions**. The source is Taghipour et al. (2019), *Petroleum Science*, [DOI 10.1007/s12182-019-0331-9](https://doi.org/10.1007/s12182-019-0331-9), licensed CC BY 4.0, on page 11.

`reason.f2.evidence` needs the recorded pressure/stability observation **and** agreement of the three analytical methods. It also has three assumption inputs: zero cohesion, friction 0.6, and stress-sampling location. The downstream `reason.f2.safety` depends on that step, current-stress synthesis, and critical-pressure transition. The full backward dependency set contains 18 `premise_for` and 3 `assumption_for` edges.

On the recorded Asmari graph, the claim-detail expander returns 41 entities and 37 edges for F2, including all 18 premise edges and three assumption edges. The full paths for all seven claims agree with an independently constructed reference. At depth limits of 1, 2, and 3, every bounded traversal reports truncation. Nineteen traversals omit a premise or assumption edge; the other two omit deeper provenance links.

## Missing-input and depth controls

Three controlled mutations of the real input are rejected by the unchanged structural validator: removing a referenced observation, removing a referenced assumption, and removing an observation's premise edge. Each actual error code is saved in the report.

A draft with an omitted internal reasoning edge can pass structural validation. Comparing the draft against the reference graph detects that missing edge. `truncated=false` means the traversal reached its configured endpoint.

## How this corresponds to the application

The [module manifest](module-provenance.json) lists the paths and SHA-256 values of the vendored AGPL-3.0-only modules and the CC BY 4.0 Asmari graph:

- `lib/evidence-graph/paths.ts`: validates and indexes the source graph, then expands incoming derivation edges and structural source references.
- `app/api/evidence-graphs/[snapshotId]/route.ts`: serves the expanded claim paths for the claim-detail API.
- `app/components/evidence-synthesis.tsx` and `app/components/evidence-search.tsx`: display partial evidence chains and direct the reader to full paper details when a preview is truncated.
