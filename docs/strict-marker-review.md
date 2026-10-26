# Independent strict-marker review — 27 October 2026

## Verdict and scope

No remaining actionable website defect was found in the current working revision reviewed after the independent auditor passed its source/specification gate. The website supports the assessment's HD descriptors. This is an evidence-based review, not an official mark, a numerical grade prediction or a guarantee of full marks.

The marker independently read the supplied `FIT3179 Data Visualisation 2_v1.2.pdf`, physical pages 1–6, consulted the lecture-vault topic and prerequisite trails, inspected the final chart specifications and narrative, and conducted a fresh browser review of the current local website. The earlier grade estimate and old screenshots were not used as evidence of current quality. Lecture-vault status reported no pending uploads, changed sources, unavailable files or indexing gaps.

## Criterion-by-criterion evidence

| Criterion | Evidence and judgement |
| --- | --- |
| Idioms and complexity — 8% | Twelve numbered figures remain when waffle panels and the waterfall's companion totals are counted within their respective figures. The supporting state-composition bars are not needed to reach the chart threshold. A conservative eight advanced set is waffle, Sankey, choropleth, proportional-symbol map, treemap, origin-destination flow map, heatmap and waterfall. The slopegraph is an additional defensible advanced idiom under the brief and S10 p.9; the threshold does not depend on its classification. Figure 12 is treated as a basic connected-dot plot. All three maps have distinct tasks and appropriate projections. Final encodings correspond to exclusive shares, conserved expenditure allocations, population-normalised geography, symbol area, hierarchical leaf magnitude, geographic connection width, quantitative relationships, signed changes and additive contributions. Meeting counts alone was not treated as sufficient. |
| Storytelling, annotations, grammar and style — 5% | The opening establishes the difference between visitor volume and spending. The sequence develops trip composition/rates and spending location, geography and traveller mix, regional composition, international changes and the Malaysian example, then activity participation and a distinct per-night comparator. Message titles, selected values and explanatory text guide attention. The conclusion follows the evidence. Relevant limitations are visible beside the comparison: domestic survey break, whole-trip scope, attendee-only activities, overlapping state visits, population-normalised scale versus benefit, nominal spending, survey estimates and the unpublished-origin remainder. No post-event timing or causal conclusion is asserted. Source, author, date and AI metadata are present. |
| Layout, colour and figure-ground — 3% | Fresh rendered inspection showed clear chapters, consistent sight-lines, balanced columns/stacked views, useful white space, readable legends and purposeful emphasis. Traveller colours are consistent across the opening, bars and supporting state composition; state colours coordinate the symbol map and treemap; signed change colours agree between heatmap and waterfall. Supporting backgrounds and inactive marks provide context. |
| Typography — 2% | Distinctive headings, consistent body typography, readable line lengths and spacing, and legible chart labels support the hierarchy. Checked compact axis labels, selected heatmap values, Sankey labels, activity names and per-night premium annotations in the inspected layouts. |
| Description of domain, who, what, why and how — 2% | README explicitly describes business-event visitor tourism, general Malaysian readers, data structures and sources, reader tasks, idiom rationales and limitations. The visible story expands geographic names, explains AUD and derived measures, and uses Malaysia as a labelled starting example. This verifies the repository description, not the actual Moodle submission text. |
| Vega/Vega-Lite and readable specifications | Individual readable JSON specifications exist and are linked from the figures. The treemap uses Vega; the other charts use Vega-Lite. The independent auditor records compilation/parsing checks. The marker inspected the final encodings and their rendered results. |
| Single URL/page and small-laptop format | The inspected local website is one scrolling page. Navigation scrolls to chapters; controls do not replace major sections. The complete page was visually reviewed at 966 CSS pixels, with no horizontal page overflow. Selected two-column layouts were additionally checked at 1366 pixels. |
| Reliable data, combined sources and suitable recency | TRA tourism estimates are combined with ABS resident population in the choropleth; Natural Earth supplies geometry. Current source/calculation checking is documented separately in `auditor-review.md`. The source-aligned 2025 domestic snapshot and 2024–2025 international comparison avoid the domestic method break. The auditor records 287,259 bytes across seventeen current chart/control data files, below the brief's data-download limit. The marker did not independently repeat live official-source retrieval. |
| Meaningful interaction | State selection links geographic emphasis, traveller mix and destination details; origin selection makes a connection traceable; market selection links comparison values and change rows. Fixed overview/detail domains support comparison across years, with explicit out-of-view handling documented in the implementation and auditor/root checks. The tested controls and disclosures serve specific reading tasks. |
| Public availability and submission | Current local rendering does not prove that this revision is publicly deployed. Public GitHub page and embedded-resource availability require a separate post-publication check. Moodle submission, submission timing and the actual submitted description were not inspected. |
| Sketch — 2%; interview — 3% | Unassessed. The user's exclusion of sketch work does not waive the brief's sketch requirement. No marks are awarded for an unseen sketch or unobserved interview, and no claim of sketch adherence is made. |

## Actual independent browser inspection

The marker used a separate Chrome review tab on `http://127.0.0.1:8765/`, rather than relying on the parent's screenshots or the repository's historical screenshots. The local files were the current post-auditor revision.

- **966 × 785 CSS pixels:** visually traversed the entire page from opening through footer, including all twelve numbered figures and the supporting state-composition view. Reviewed titles, introductory text, legends, axes, direct annotations, captions, chapter transitions, conclusion, sources and acknowledgement. Thirteen chart SVGs rendered; the measured page width was 951 pixels, with no horizontal page overflow.
- **1366 × 768 CSS pixels:** inspected the settled two-column opening, paired spending bars/Sankey, and paired market scatterplot/heatmap. Checked compact labels, chart alignment and the source-data dialog. Thirteen chart SVGs rendered; measured page width was 1351 pixels, with no horizontal page overflow. This was a targeted paired-layout check, not a second complete page sweep.
- **386 × 844 CSS pixels:** inspected the activity chapter, complete slopegraph labels and visible per-night comparison/premium labels. Thirteen SVGs remained rendered; measured page width was 371 pixels, with no horizontal page overflow. This was a targeted narrow-layout check, not a full mobile-page review or physical-device test.
- Exercised Victoria selection and its destination detail, then reset the state view; Malaysia origin selection and origin reset; the Smaller markets scale with Malaysia focus; the 2024 year selection; and Reset market view. The expected visible summaries/selection states updated. These were representative independent checks, not an exhaustive test of every market/year/state combination.
- Opened all eight explanation disclosures and verified each actual `open` state; then closed them. Read the supporting explanations, including the derived-rate arithmetic and remainder definitions.
- Opened the per-night data dialog, inspected its displayed values and readable table, and closed it.
- Browser warning/error logs were empty for this review session.
- Temporary viewport overrides were reset before browser control returned to the parent reviewer.

The parent's broader resize-retention and all-state checks are separate evidence and are not represented as the marker's own actions. The independent auditor's source calculations and compilation checks are also attributed separately.

## Lecture basis and interpretive limits

Significant review decisions used actual page-specific lecture extracts and their original-source locators, rather than treating index entries or the older consolidated notes as primary evidence:

- S1 pp.6–10: domain, data/task abstraction, derived attributes and idiom choice.
- S5 pp.3–9: channel semantics and quantitative comparison accuracy.
- S2 pp.8–10 and 18–20: connected-dot, line and scatterplot conditions.
- S10 pp.5–6 and 9: exclusive waffle wholes, heatmap ordering/colour and two-checkpoint slopegraphs.
- S19 pp.2–4; S15 pp.3–6: question-specific map normalisation and appropriate projections.
- S22 pp.2–5: proportional symbols, size and overlap.
- S21 p.2: schematic origin-destination geometry and quantitative line width.
- S60 pp.14–16: containment and leaf magnitude in shallow treemap hierarchies.
- S7 pp.5–11: consistent colour semantics, contrast and colour-vision considerations.
- S3 pp.6–10; S8 pp.2–6: readable typography, hierarchy, alignment and white space.
- S9 pp.2–4: explanatory goal, suitable charts, reduced clutter and selective annotations.
- S56 pp.2–3; S39 pp.9–17: purposeful interaction and coordinated views.

The international-only Sankey is the least data-rich advanced figure, but its conserved spending-location split serves a clear explanatory purpose. This does not justify inventing a rubric penalty or demanding more branches solely to increase complexity. Repeated measurements are acceptable where a subsequent figure answers a distinct reader task; they are not independent corroborating datasets. Two annual endpoints and the large unpublished-origin remainder remain substantive source limits, not evidence of a longer trend or its causes. No additional dataset, longer series or causal model is imposed as an invented assessment requirement.
