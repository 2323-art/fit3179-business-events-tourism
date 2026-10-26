# Independent audit — 27 October 2026

Scope: current working revision after `faf4a42`, reviewed independently of the implementation author. This is a review of source files, calculations and specifications. Browser appearance, actual browser interactions, public deployment, Moodle submission, sketch and interview are not certified by this document.

## Acceptance criteria

The current assessment brief governs these criteria: `FIT3179 Data Visualisation 2_v1.2.pdf`, physical pages 1–6, read from the supplied local PDF. Requirements are distinguished from quality judgements.

| Criterion | Evidence and outcome |
| --- | --- |
| Vega/Vega-Lite; readable individual specifications | All 13 current JSON specifications compile/parse using the bundled libraries. The treemap uses Vega; others use Vega-Lite. |
| At least 3 different map idioms; appropriate projections | Choropleth, proportional-symbol and origin-destination flow maps. Australian maps use conic equal-area; world links use Pacific-centred Equal Earth. Actual legibility requires browser inspection. |
| At least 10 charts; HD requires more than 10 and at least 8 advanced idioms | Twelve numbered figures remain when repeated panels count once and the supporting state bars are excluded. Conservative advanced set: waffle, Sankey, choropleth, proportional-symbol map, treemap, flow map, heatmap, waterfall. Slope classification is not needed to reach eight. The threshold alone does not guarantee full idiom marks. |
| Meaningful advanced idioms, accurate marks/channels (8 marks) | Source and specification inspection found meaningful part-to-whole, geographic, hierarchical, relationship, change and reconciliation tasks. The state mix adds a substantive traveller-type comparison. Area/width/length mappings, waterfall cumulative amounts and fixed comparison domains are consistent with the stated tasks. Browser overlap and readability remain separate gates. |
| Structured explanatory story and informative annotations (5 marks) | The current text connects trip mix, stay length, spending scope, destination composition, regional shares, international volume/spend differences, Malaysian rate decomposition, incomplete origin coverage, activities and a distinct international comparator. It states limits beside the relevant charts rather than treating arithmetic as causation. |
| At least two reliable sources combined; latest suitable data; data download under a few MB | TRA estimates are combined with ABS June 2025 residents in the choropleth. Natural Earth supplies geometry. Seventeen current chart/control data files total 287,259 bytes. The business-events source is calendar 2025; 2024 is used only for international comparisons. |
| Single scrolling page, small-laptop readability, no horizontal page scroll or major-section swaps | Code supplies one continuous page with local controls. Current browser verification is required; source inspection alone cannot pass this criterion. |
| Layout/colour/figure–ground (3), typography (2) | Consistent semantic colours and local fonts are configured. A mark requires current rendered evidence, not only specification inspection. |
| Domain/audience/what/why/how (2) | README identifies business-event visitor tourism, general Malaysian readers, attributes, reader tasks, choices and their limitations. This does not certify the actual Moodle description. |
| Author, date, source links, acknowledgement; public GitHub and embedded charts | Present in the files; all 13 chart tool groups link to existing specification/JSON/CSV files. Public availability must be verified after deployment. The brief's zero-mark availability condition is not satisfied merely by local success. |
| Sketch (2), interview (3), submission/timing | Outside this implementation audit. The user excluded sketch work; that does not waive the brief's requirement. No marks are invented for unobserved assessment components. |

## Independent calculation checks

- Matched every new state-mix record to its preserved source row: 2025, `Category = Total`, each of the three traveller types, published sample flag. Checked 24 amounts and 48 shares independently. Each share uses the sum of its three components within that jurisdiction; it does not divide by separately rounded state totals or sum overlapping attendee/accompanying groups.
- Checked all 62 Sankey ribbon samples and three nodes: thickness equals the corresponding spending amount divided by one billion. AUD 3,955,405,000 equals AUD 2,339,479,000 in Australia plus AUD 1,615,926,000 outside Australia (40.85%).
- Verified mean nights per trip: international 20.04935; domestic overnight 3.13682. These are aggregate descriptive means, not estimates of an event's causal effect.
- Verified displayed regional fractions: NSW 1,800 / (1,800 + 4,048) = 30.77975%; Victoria 600 / (600 + 3,112) = 16.16379%.
- Verified the five shown Asian origins total 222,000 trips, or 30.38773% of the national international total; New Zealand 165,000 / 730,558 = 22.58548%. All eight shown origins cover 70.22030% of national international trips.
- Verified national international spending falls AUD 172.429m; unpublished-origin/rounding remainder falls AUD 133.815m, 77.60586% of the net decline. Other published markets account for a separate AUD 14.758m fall. The checked-in waterfall reconciles exactly.
- Verified Malaysia: trips +31.25%; spending per trip −20.66339%; total spending +4.12930%. Multiplicative change factors reconcile. Rates derive from rounded survey totals and do not follow the same people.
- Verified the per-night premium: 153 / 96 − 1 = 59.375%; 160 / 107 − 1 = 49.53271%. The comparator is other international visitors, different from the domestic comparisons earlier.
- Ran `story_data.py --check`, `build_data.py --check-waterfall`, JavaScript syntax checking and diff whitespace checks successfully. Independently compiled/parsed all specifications; verified every reader-facing chart-data/specification link points to an existing local file.

## Findings and disposition

1. The README's L12 reference was separated from its table by a blank line. The fixer removed the separation; rechecked.
2. The dynamic market leader heading could be read beyond the available published origins. The fixer qualified both the initial and dynamic heading/summary; rechecked in source. Browser wrapping is still to be inspected.

No remaining blocking source-level calculation or specification defect was found in this pass. This finding does not certify rendered layout or deployment and is not a guarantee of an official HD.

## Data limits that remain limits, not invented requirements

Two annual endpoints do not show seasonality, a longer recovery trajectory or event-by-event behaviour. National, state and regional views often reuse aggregates rather than supplying independent evidence. The 18 published origins cover 85.8% of 2025 international trips and 84.9% of in-Australia spending; the residual prevents identification of most of the net spending decline. The activity tables do not establish when activities happened relative to an event. Population-normalised spending measures scale relative to residents, not economic importance, local income or benefit. The current text acknowledges these limits. The brief does not impose a larger dataset, longer time series or causal model, so those absences alone are not marking violations.

## Course evidence

Lecture-vault status was clean: no pending, changed, missing or incomplete indexed sources. The topic index/prerequisite trails were used to locate original-source sections, not as independent evidence. Relevant physical PDF locators include S1 pp. 6–10 (data/task/idiom and derived attributes); S5 pp. 7–9 (quantitative channel accuracy); S9 pp. 2–4 (specific explanatory goal, appropriate charts and annotations); S10 pp. 5, 6, 9 (waffle, heatmap, two-endpoint slope); S19 pp. 2–4 (normalisation and choropleths); S21 pp. 2–3 (schematic origin–destination links); S22 pp. 2, 4–5 (proportional symbols); S60 pp. 14–15 (treemap leaf queries and shallow hierarchies); S2 pp. 8–10, 18–20 (connected comparisons and scatter relationships); S49 pp. 6–8, 19–25 (relative comparison and limits of association). These support methods and interpretation; the current brief supplies the assessment thresholds.
