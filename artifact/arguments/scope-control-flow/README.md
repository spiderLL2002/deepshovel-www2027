# Interactive scope-control regression (v1.1 repair)

The **29 October 2026 public-source repair** applies the existing scope-normalization functions to single-proposition interactive and noninteractive tasks. Earlier interactive retrieval attached model decisions directly and skipped the scope guard, allowing contradiction or equivalence with unknown or disjoint scope. Missing query scope now also prevents direct equivalence. This package records a local source-code check; the October 25 service used the earlier code.

Interactive multi-question/non-propositional tasks retain model `supports`, `refines` and `qualifies` relations and their directions. They have no single reference proposition whose scope could establish whole-task contradiction or equivalence, so those two labels become `related` with unknown scope. Single-proposition checks retain compatible support and in-scope relation behavior, model confidence, model ranking and the existing one-planning-call preview/final handoff.

## Reproduce

From the repository root, use Python 3.12 and the existing small replay environment:

```sh
python3.12 -m venv .scope-venv
.scope-venv/bin/python -m pip install -r repro/requirements.lock pytest==8.4.2
PYTHONPATH=compiler .scope-venv/bin/python -B -m pytest \
  compiler/tests/test_retrieval_relation_reference_service.py \
  compiler/tests/test_retrieval_service.py::test_relation_blockers_and_geologic_time_units_are_conservative \
  compiler/tests/test_interactive_relation_ranking.py -o addopts= -q
```

The recorded run passes **92 tests**. The first two selections form the **86-test** CI scope check; the additional file verifies the existing interactive model wire. No Qdrant, GPU packages, live model calls or production credentials are needed for these selections.

The parameterized regression executes `RetrievalService._apply_relation_decisions`: interactive/noninteractive × context/legacy protocol × five scope states × three proposed relations = **60 synthetic contract cases**. Five further cases retain interactive non-propositional relevance while rejecting direct contradiction/equivalence. A local preview-to-final service test checks scope validation without an extra planning call. Before the repair, the targeted selection had 36 failures and 30 passes.

The existing scope/admission replay also remains executable without changing its expectations:

```sh
.scope-venv/bin/python -B artifact/replays/scope_contract/run.py \
  --repo . --out runs/scope-contract-new
```

It passed nine query cases and 18 full-pool channel-parity checks against the repaired public source. `--out` must be a new directory. Its constructed vectors/labels measure contract behavior, not retrieval quality.

[verification.json](verification.json) records the commands, outcomes and hashes of the tested source/test files. Free-text scientific mismatches remain conservatively unknown; the existing checker establishes disjointness only when supported by interpretable non-overlapping numeric intervals.
