# One-record recipient reconstruction check

This format-retention illustration uses one saved F2 record. The minimal CSV projection contains `prepared_value`, `unit` and DOI. The released exporter produces JSON-LD from the same record.

A fresh AI recipient is asked to recover six concrete items from only each input: (1) prepared value/unit; (2) original selected-observation numeric/raw/unit; (3) prepared quantity/conditions; (4) selected observation/claim identity and actual directed terminal relation; (5) source-version SHA and recorded/corrected locator information; (6) operator conclusion and qualification. Missing information must remain unavailable, without external source lookup or guessing. Queries or parsing commands and exact input locators must support every answer.

One automated recipient reconstructs retained information. The CSV fields and input selection are fixed before the reconstruction.
