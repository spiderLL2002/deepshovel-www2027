# Reproduction environment

- Evaluation score calculation uses the Python 3.9+ standard library and the published records.
- The combined paper command uses Python 3.12 and Node.js 22.13 or later. It installs the dependencies in `requirements-paper.lock` into an environment under the requested run directory.
- The GP15 source fetcher downloads two supporting inputs from their providers when absent and verifies their SHA-256 values. The computation then runs locally using the pinned packages in `artifact/gp15/reproduction/requirements-research.lock`.
- The GP15 strict runner checks reference file bytes. The [portable runner](../artifact/gp15/README.md) preserves scientific outputs and reports its narrowly defined runtime metadata and image rendering allowances.

Run commands from the [repository instructions](../README.md#reproduce-the-evaluation-and-gp15-research). Give each run a new output directory under `runs/`.
