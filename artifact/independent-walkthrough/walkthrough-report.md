> Public copy: personal machine path prefixes have been normalized; scientific input/export files are unchanged.

# Functional walkthrough

Date: 2026-10-27. One automated operator read the source PDF, inspected a supplied retrieval result and complete graph, and used an isolated localhost interface. The workflow used `server.py` to establish isolation.

## Actual execution

The first clock observation was 12:35:55 UTC (20:35:55 Beijing). The PDF was read before importing the retrieval and graph inputs. Source identity was checked at 12:38:10.441; the decision was saved at 12:38:18.516, after 143.516 seconds. The export was retrieved by 12:39:13, after 198 seconds. These elapsed times include tool use and recovery. Raw file timestamps are in `verification.json`.

1. Inspected server.py: fixed port 8137, no port argument. Parent supplied isolated origin http://localhost:8137/generic-reuse.html, separate from its http://127.0.0.1:8137. Created new IAB tab. Initial page showed no imported result and no saved record. Did not Reset.
2. Read original source.pdf with pypdf after discovering default Python and bundled Python lacked PyMuPDF. Rendered complete PDF pages 10 and 11 with pdftoppm and visually inspected both. Read source text on pages 3, 4, 8–13 relevant to assumptions, models and F2 interpretation.
3. Task B: imported `retrieved-result-only.json` through the Retrieval JSON chooser. The UI reported “Path lacks observations or source anchors; saving is unavailable.” The shortest path was the only path, the observation/anchor menus had no options, and Save/Download were disabled. `B-shortest-only.jpg` and `B-shortest-only-dom.txt` record this failure; B produced no decision export.
4. Continued as Task A: imported full-graph.json through Stored graph JSON file chooser and clicked Build observation branch. UI reported 33 nodes and 33 edges, preserved shortest path, with scientific fields still blank. Chose Recorded full-graph observation branch, obs.f2.assessed, and anchor.text.f2.stability. UI showed linked graph status and the original quote and selector.
5. Independently typed source-derived scientific fields. Selected Interpretation and Reuse with qualification. Chose source.pdf in Local source PDF chooser. UI reported Verified file identity with SHA-256 f87d7cdcf0d08a7557993c1966b56183882c0b87c68809d0519ea8060382de99.
6. Clicked Save reuse decision. UI showed a saved premise, qualified reading conclusion, linked graph and verified file identity. Captured A-saved.jpg and A-saved-dom.txt.
7. First combined save/download attempt timed out after 30 seconds; save and screenshots had succeeded. Rebound the same tab, saw two Download saved JSON buttons (toolbar and saved summary), then targeted the button in Saved premise summary. Browser download succeeded at <author-workspace>/Downloads/observation-reuse-d5ec6f9d439e.json. Copied this actual downloaded file to A-final-export.json. No export was manufactured from application internals.
8. Verified exported canonical-payload SHA-256 against record ID and checked every original input-result field equals its export counterpart. All passed; original_result adds observation_evidence_path. Original shortest path and composite scope are preserved.

## Independently prepared reading

Quantity: estimated maximum sustainable total pore pressure, value 55–57 MPa, for F2 under the paper’s analytical gas-injection/fault-reactivation models. This is not the pressure increase. The paper’s prose summary is approximate and model dependent, not a statistical confidence interval; no statistical uncertainty level is stated.

Source locator: PDF page 11 of 14, section 6, right-column continuation paragraph immediately above section 7, final F2 sentence. Cross-check PDF p10 Table 3 F2 rows: Eq.3/Eq.5 Ppmax = 57.4/57.3 MPa, initial Ppi = 22.04 MPa, increments = 35.4/35.3 MPa. PDF p11 Table 4 F2 rows: Pc = 55.03/55.31 MPa; PCr = 57.58/57.81 MPa. Thus the prose 55–57 is not an exact envelope containing all tabulated outputs.

Conditions: normal faulting regime; cohesion zero and friction coefficient 0.6 assumed; F2 dip 80°, dip direction 8°, strike 278° (p4 Table 1); stresses taken within specified intervals (example 10 m) near the middle of fault planes (p11). Elastic-modulus alternatives and 3D Mohr/slip-tendency/modified-slip-tendency methods must remain attached. No general operational injection limit or new physical-safety validation follows.

## Obstacles, corrections and unresolved limits

- Source-location issue: anchor page 11 and its quote agree, but rectangle x=.07899, y=.79873, width=.41008, height=.11139 covers the left lower column. The F2 sentence is in the right column. The operator recorded a corrected verbal locator and the discrepancy; the original anchor remains unchanged.
- Source prose and table numeric precision differ. Preserved prose summary and stated table values rather than silently replacing it or treating spread as uncertainty.

- IAB visible:true is unsupported in a subagent; creating background IAB tab succeeded.

- Two visible Download saved JSON buttons made an unscoped download attempt ambiguous; scoped saved-summary control worked. The original timeout is preserved as a recovery step.
- Source inspection used external PDF extraction/rendering, followed by an in-app selected-file hash check.
- Task B’s structural deficiency remains unresolved without a complete graph; this is deliberately retained as failure.

## Outputs and interpretation boundary

`A-final-export.json` is the browser export; `operator-fields.json` records entered text. `A-saved.jpg` and `B-shortest-only.jpg` are full-page captures; `source-10.png` and `source-11.png` are PDF renders. `verification.json` contains file checks and timestamps. The walkthrough produced one qualified record and one blocked shortest-only input.
