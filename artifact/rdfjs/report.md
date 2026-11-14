# Independent JavaScript JSON-LD consumer: one F2 record

Executed 2026-10-27 with Node v26.3.0, npm 11.16.0 and jsonld 9.0.0. The sole record input is `../recipient-check/input-record.jsonld`. No PDF or other record was supplied.

Official package: https://registry.npmjs.org/jsonld and https://github.com/digitalbazaar/jsonld.js . Registry metadata, exact package lock and installation output are included. Only `jsonld` is a direct dependency; its transitive dependencies are pinned by the lockfile. Installation used `--ignore-scripts --no-audit --no-fund`; no production or global dependencies were modified. The npm web page returned HTTP 403 during documentation lookup; the official registry lookup and installation succeeded.

`consume.cjs` invokes jsonld.js `toRDF` and matches the resulting RDF terms by subject/predicate/type. It independently obtained **57 default-graph quads / 6 subjects**, without hardcoding that count or consuming RDFLib output. It queried record → preparation, imported-result derivation, preparation inputs, selected observation/anchor, the explicitly exported groundsObservation link, and source version. It recovered prepared value **55–57 MPa**, conditions and **qualified_reuse** operator reading. Historical source-file state is **verified**; current-file state remains **not_rechecked**.

The `ds:originalExport` RDF string was written as **214323 UTF-8 bytes**, preserving the input literal. Node crypto SHA-256 of `canonical_payload` matched `record_id`; `assert.deepStrictEqual` confirmed the parsed canonical payload and payload had the same JSON values and types. `verify_reuse.py` passed integrity, structure and internal source-identity checks using the record alone.

| Item | SHA-256 |
|---|---|
| Input JSON-LD bytes | 2ec791cc957e08d9f2d4b586abb6024612852d067166f65c0c500ba5352a3694 |
| Recovered originalExport UTF-8 | ea03972266cc720c7b52706f76bd1fed542fc17de88b31f438a034f36c54d26d |
| canonical_payload | 54ac83a1ddad95f7e179d64b636ce9e97da1c37fc4dd34173da3c29b79fa6463 |
| Recorded source version (not rehashed here) | f87d7cdcf0d08a7557993c1966b56183882c0b87c68809d0519ea8060382de99 |

Together with the Python RDFLib run, this checks two implementations reading one serialized record. Scientific paths remain JSON literal content except for relations present in the RDF input.

The JavaScript consumer and standard-library verifier exited 0. See [README.md](README.md) for isolated installation and rerun commands.
