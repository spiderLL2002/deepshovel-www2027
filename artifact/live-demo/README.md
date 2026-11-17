# Demonstration walkthrough

Open the [public workspace](https://deepshovel.iiot-shxt.xyz/workspace) or use a [configured local instance](../../README.md#run-the-application-locally). The [offline F2 example](../README.md) and the captured screens below can be inspected without a live query.

## F2: Trace the pressure estimate

1. In **Claim verification**, search for the query below.
2. Expand the result's evidence chain and open the representative paper.
3. In **Claims and evidence**, select **CLAIM 04** and expand the three assumptions: zero cohesion, friction coefficient 0.6, and stress-sampling location.
4. Under the pressure observation, select **Open original page**. The viewer highlights the pressure statement on PDF page **11 of 14**, in the right column below Figure 12.

> For fault F2 in the Asmari reservoir, the estimated maximum sustainable pore pressure during gas injection is 55–57 MPa under the assessed stress state, assuming zero cohesion and a friction coefficient of 0.6.

## F2: Change a condition

In the query above, change the friction coefficient to 0.4 and compare the result. The 55–57 MPa estimate is conditional on the modeled stress state and the original assumptions.

## F2: Captured screens

The [claim inspector](en-f2-claim.png), [source page](en-f2-source.png), and [assumptions](en-f2-assumptions.png) are used in the paper. Full views show the [search results](01-results.jpg), [expanded evidence](02-expanded-evidence.jpg), [claim detail](03-claim-detail.jpg), [assumptions](04-assumptions.jpg), and [original PDF page](06-source-page.jpg).

The original is Taghipour et al. (2019), *Petroleum Science* 16, 513–526, CC BY 4.0. [Source PDF](../second-case/source.pdf) · [Article DOI](https://doi.org/10.1007/s12182-019-0331-9)

## Fiskegrav: Compare the evidence across two papers

On a configured instance with both papers indexed, enter this query in **Claim verification** and expand the evidence for the two papers:

> At Fiskegrav, the late Permian marine and terrestrial ecosystem collapse is estimated at 1.6–8 kyr using revised sedimentation rates, substantially shorter than the earlier 10–60 kyr estimate.

1. Open [van Soelen et al. (2018), Section 5.1, p. 447](https://cp.copernicus.org/articles/14/441/2018/cp-14-441-2018.pdf#page=7). Identify the duration estimate and the event it describes.
2. Open [Mettam et al. (2017), Section 2.2, p. 211](https://discovery.ucl.ac.uk/10067098/1/Mettam_-s2.0-S0031018217302109-main.pdf#page=2) and [Figure 2](https://discovery.ucl.ac.uk/10067098/1/Mettam_-s2.0-S0031018217302109-main.pdf#page=3). Compare the last appearance of Permian macrofossils with the later loss of bioturbation, which marks the final marine ecosystem collapse in this section.

For the public walkthrough, use the two linked passages for a side-by-side reading.

## GP15: Extend the investigation with an agent

1. In the configured Codex session, ask: “Search DeepShovel for literature that could challenge the transfer of the published REE–pH predictor to the GP15 Pacific transect. Identify relevant sources and outline a test using matched samples.” The live step runs the initial literature search and planning.
2. Open the [saved GP15 study](../gp15/README.md#primary-results) to inspect the completed comparison, the six layerwise squared-error contrasts for Leg 2 and the inference about depth weights. The [research trace](../research-trace/README.md#2-trace-a-source-argument-into-the-gp15-research-inputs-and-new-claims) connects the source argument to the protocol, data and recorded claims.
