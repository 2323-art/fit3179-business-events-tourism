# Beyond the conference badge

An original FIT3179 DV2 data story about Australia's business-event visitors, created by Jack (Wong Jing Yuan), Monash University Malaysia, 5 October 2026.

**Website:** https://2323-art.github.io/fit3179-business-events-tourism/

The main question is who generates visitor spending, where it lands, and how international markets changed between 2024 and 2025. The audience is a general Malaysian readership interested in Australian tourism and business events. The page is a single scrolling story, with four chapters, twelve charts and three distinct map idioms.

## Project preferences

Do not pair red and green. The category palette and shared state colours are defined in `data/colour-semantics.json`; activity lines also use distinct patterns.

## Run locally

Serve this directory with any static HTTP server and open `index.html` through that server. Opening the file directly can prevent browsers from loading JSON. All libraries and fonts are included locally. No account, API key, build system or remote chart service is needed to view the page.

## Domain, audience and What / Why / How

**Domain.** This story concerns tourism associated with attending or accompanying someone to a business event in Australia. Its scope is visitor trips, nights, participation and expenditure during the whole trip. It does not estimate every event attendee, the entire events industry or an event's causal economic impact.

**Who.** The intended reader is an average Malaysian reader interested in tourism, travel or business events, without specialist knowledge of Australian geography or statistics. The page defines business-event visitors, expands state names, labels money as Australian dollars and explains percentages and per-resident measures in ordinary language. Malaysia is an explicitly labelled starting example in the international comparison; the story retains all available markets so this audience connection does not become a claim that Malaysia is the largest market.

**Why.** The explanatory goal is to help readers distinguish visitor volume from spending, recognise how geography changes the comparison, and understand how international-market changes differ. In Munzner's action-target terms, readers compare traveller-group shares and spending rates; locate geographic concentrations; compare origin-market attributes; and identify changes between 2024 and 2025. Derived per-trip and per-night rates separate the arithmetic contributions to total spending without asserting causes. The main sequence presents these questions in that order, while selection and tooltips support specific follow-up questions. The framework distinguishes an explanatory purpose from whether the page is interactive. [L1]

**What.** TRA supplies aggregate survey estimates, arranged as tables keyed by year and traveller type, jurisdiction, origin market or activity. Categories identify groups; time is ordered; trips, nights, AUD amounts and derived rates are quantitative. State-to-region nesting supplies a shallow hierarchy, and Natural Earth supplies geographic shapes and representative positions. ABS residents are joined to state expenditure for the per-resident comparison. Data authors, creation methods, reference dates and transformations are documented separately below. Domestic data are a 2025 snapshot; only international data support the two-year comparison.

**How.** The page combines twelve figures in one scrolling sequence: value, places, international origins and activity beyond the event. Each figure has a specific comparison task, stated below. Headlines and selective annotations identify the intended evidence; definitions and limitations prevent stronger interpretations than the data supports. Short captions retain the essential encoding, scope caveat and source, with optional native disclosure panels for secondary methods. This hierarchy reduces reading density without concealing the caveats needed to interpret a chart. This is the project's application of the course guidance, not a claim that the lectures prescribe these exact charts. [L1, L2, L10, L11]

### Chart rationale

| Figure / specification | Reader task: action + target | Idiom, marks and channels | Why this choice helps | Limitation and response |
| --- | --- | --- | --- | --- |
| 01 · `01-waffle.json` | Compare traveller groups' shares of trips and spending. | Two waffle panels; equal cells use categorical hue and count to represent shares. | The same 100-cell whole exposes the contrast between trip share and spending share. The pair counts as one chart. [L3] | Whole-cell rounding limits precision; largest-remainder rounding conserves 100 cells, while the numeric key and tooltips retain exact shares. |
| 02 · `02-spend-per-trip.json` | Compare spending per trip across traveller groups. | Horizontal bars; aligned zero-based length encodes AUD per trip. | Common position/length supports more precise magnitude comparison than area. [L4] | Trip duration differs; the caption makes clear this is not spending per day, and figure 12 adds a per-night comparison for international visitors. |
| 03 · `03-sankey.json` | Trace total trip spending from traveller groups to spending locations. | Sankey ribbons; conserved thickness encodes AUD, with hue identifying traveller group. | The international split makes the difference between total trip spend and spend within Australia visible. | These are aggregate spending allocations, not tracked transactions. Exact labels and the national data table support close reading. |
| 04 · `04-choropleth.json` | Compare geographic spending scale relative to residents. | Choropleth; ordered brightness encodes AUD per resident on equal-area state shapes. | A stated denominator makes jurisdictions comparable for this question, while the projection avoids area distortion. [L5] | The ratio is not residents' income or benefit. The caption explicitly limits its interpretation; absolute volume appears separately in figure 05. |
| 05 · `05-symbol-map.json` | Locate and compare concentrations of state visits. | Proportional-symbol map; circle area encodes visits, categorical hue identifies state. | Magnitude is carried by symbols rather than the land area of each state; linked selection preserves geographic context. [L6] | Area is less precise than aligned position, and state visits can overlap across trips. Tooltips and the table expose values; the caption forbids treating their sum as unique national trips. |
| 06 · `06-treemap.json` | Compare destination spending within the state hierarchy. | Treemap; nested rectangle area encodes spending and hue identifies the parent state. | Containment suits the shallow state-to-region structure and makes dominant destinations evident. [L7] | Close areas and small regions are harder to compare. State selection supplies a destination list; the table retains regions too small to label. |
| 07 · `07-flow-map.json` | Locate the largest published international origins and compare their connections to Australia. | Origin-destination map; line width encodes trips, with geographic position locating origins. | Geographic links answer where the visitors originate; selection reduces overlapping connections. [L8] | Representative capitals and Canberra are schematic endpoints, not airports or itineraries. The top-eight scope and the unshown remainder are stated. |
| 08 · `08-market-scatter.json` | Compare origin-market volume and spending; inspect small markets; derive spending-per-trip changes. | Scatterplot; horizontal/vertical position encode trips/AUD. Highlight selects a market, while two labelled scale presets control the plotted extent. | All markets supplies context; Smaller markets separates the crowded cluster. Each preset stays fixed across years, and a persistent table and rate summary retain both years. [L1, L4, L9] | Detail omits markets above 40,000 trips or AUD 120m; its count and an out-of-view reminder make this explicit. Return to All markets for the full comparison. Rate identities describe arithmetic, not causes. |
| 09 · `09-change-heatmap.json` | Identify whether visitor, night and spending changes agree within and across markets. | Heatmap; signed diverging colour encodes percentage change, with a selected-row outline and numeric labels. | A compact matrix reveals contrasting directions across three measures; linked selection connects it to figure 08. [L3, L9] | Colour supports approximate comparison; selected values, tooltips and the data table supply precision. Row ordering is an organising aid, not a performance index. |
| 10 · `10-waterfall.json` | Decompose the change in national international-visitor spending. | Waterfall; floating bar lengths encode signed contributions along a running-total axis. | National endpoints and additive contributions reconcile the total change. Six named origins, other published origins and the unpublished-origin/rounding residual remain distinct. | The residual cannot identify individual unpublished markets or explain causes. Zero-based endpoint bars accompany the explicitly enlarged cumulative detail scale. |
| 11 · `11-activity-slope.json` | Compare participation in selected activities between two years. | Slopegraph; vertical position encodes share, while line slope shows change and colour/dash identify activity. | Two dated endpoints directly communicate direction and relative change; the sightseeing annotation supports the headline. [L3] | The lines do not track the same people or intermediate changes. Activities overlap, so shares are not summed; tooltips and the table provide values beyond the selected annotation. |
| 12 · `12-per-night.json` | Compare spending per night for business-event and other international visitors. | Connected-dot plot; paired positions on one AUD scale expose the gap. | A common scale supports direct comparison with little ink and complements the per-trip comparison. [L4] | The comparison is descriptive and uses rounded published averages. It does not control for visitor mix or establish that attending an event caused extra spending. |

Specification names in the table are in `specs/`. The three map idioms are choropleth, proportional symbol and origin-destination flow; repeated panels or layers are not counted as additional charts. Custom elements include the conserved Sankey layout, linked state highlighting, the scatterplot's overview/detail presets, the persistent market-comparison table and derived-rate explanation, and the waterfall's separate total/detail scales. These controls and summaries do not add to the twelve-chart count. Each serves a reader task rather than increasing complexity for its own sake.

### Course-method evidence

These are design references, separate from the statistical data provenance. Locators are **physical PDF pages**, not inferred teaching weeks. The originals are in the local parent workspace at `../Lecture Notes/01 Sources/Originals/`; they are not bundled or republished with this public website. The corresponding topic notes provide navigation and caveats; the older consolidated master notes are secondary evidence.

| Key | Original lecture / reading and locator | Applied principle |
| --- | --- | --- |
| L1 | S1 · `S1 - Course notes 1 Data Visualisation What Why How (1).pdf`, pp. 6–10 | Domain/users, data and action-target tasks precede idiom choices; explanatory purpose and interactivity are distinct. |
| L2 | S9 · `S9 - FIT3179 -S2-2026 - Course Notes 7 Storytelling with Data.pdf`, pp. 2–4 | A specific goal, suitable charts, reduced clutter and selective annotations guide attention. |
| L3 | S10 · `S10 - Table Idioms - Part 2 - Kirk 2019 Data Visualisation.pdf`, pp. 5, 6 and 9 | Waffle wholes and rounding limits; heatmap magnitude and ordering; two-checkpoint slopegraphs and selective labels. Scanned pages have a page-specific OCR trail in the vault. |
| L4 | S5 · `S5 - FIT2179 Course Notes 3 Marks and Channels (1).pdf`, pp. 7–9; S2 · `S2 - Course notes 4 Visualisation of Table Datasets.pdf`, pp. 8–10 and 18–20 | Position/length support quantitative comparison; connected-dot endpoints, ordered line positions, scatterplot relationships and their limits. |
| L5 | S19 · `S19 - FIT2179 Course Notes Choropleth.pdf`, pp. 2–4 | Ordered brightness, question-specific standardisation and area-preserving projections. |
| L6 | S22 · `S22 - FIT2179 Course Notes Proportional Symbol Maps.pdf`, pp. 2 and 4–5 | Quantities represented by proportional symbols; manage size and overlap. |
| L7 | S60 · `S60 - Munzner - Networks  Trees - Chapter 9 .pdf`, pp. 14–15 (printed pp. 213–214) | Treemaps encode hierarchy through containment and support queries of leaf attributes. |
| L8 | S21 · `S21 - FIT2179 Course Notes Flow Maps.pdf`, pp. 2–3 and 6 | Origin-destination link geometry need not follow real routes; quantitative width and overlap management. |
| L9 | S46 · `S46 - FIT3179 Week 9 Studio.pdf`, pp. 11–15 and 21–29; S39 · `S39 - FIT3179 Week 10 Studio (1).pdf`, pp. 9–17 | Details on demand, menu/threshold filtering and highlighting extend to coordinated views. |
| L10 | S3 · `S3 - FIT2179 Course Notes 11 Typography.pdf`, pp. 6–7 and 10–12 | Legibility, hierarchy and label spacing guide compact scatter ticks, retained heatmap values and readable captions. |
| L11 | S8 · `S8 - FIT2179 Course Notes 9 Layout.pdf`, pp. 2–6 | Grouping, alignment and purposeful whitespace guide the opening, captions and adjacent definition. Optional method disclosures apply these principles; the lectures do not prescribe that control. |

## Statistical sources and transformations

1. [Tourism Research Australia, Business events data](https://www.tra.gov.au/en/tourism-statistics/business-events-data), 2024 and 2025, public report refreshed 21 May 2026. Source authors are Tourism Research Australia/Austrade. Read-only public dashboard data were retrieved 5 October 2026. The published attendance-or-accompaniment union is used; overlapping subgroups are not summed. Source dollars in thousands and state dollars in millions are converted to nominal AUD.
2. [ABS National, state and territory population, March 2026](https://www.abs.gov.au/statistics/people/population/national-state-and-territory-population/mar-2026), released 17 September 2026. Population is the June 2025 reference in Table 4 (`310104.xlsx`), Data1 row 187, columns T–AA, matching the tourism year. State names are standardised for the join. Spending / resident population is a market-scale measure, not household income or per-person benefit.
3. [Natural Earth](https://www.naturalearthdata.com/): 1:110m countries and populated places, 1:50m states. Australian jurisdictions and useful properties are retained; coordinates are rounded to three decimals. ACT has a label callout. The map source contains Jervis Bay separately; it is not presented as a ninth state with an invented statistic. No claims are made about disputed boundaries.

The two statistical sources are combined in figure 04. The other figures use different views of TRA's dataset; twelve charts do not mean twelve unrelated datasets.

### Why domestic comparisons stop at 2025

TRA changed from the National Visitor Survey to Domestic Tourism Statistics in January 2025. Collection and coverage changed. Unqualified 2024–2025 domestic growth rates would be misleading. The first two chapters therefore use 2025 snapshots. The time comparisons use the International Visitor Survey. [TRA methodology explanation](https://www.tra.gov.au/en/about-us/changes-to-the-australian-resident-tourism-statistics-collection-in-2025).

### Data dictionary

Every displayed data table has JSON and CSV versions in `data/`. `provenance.json` records source URLs, reference periods, licences and transformations. The tables contain estimates, not fabricated observations.

| File | Grain | Units and important fields |
|---|---|---|
| `national` | year × traveller type | `visitors`: visitor trips; `nights`: visitor nights, null for day trips; `spend`: AUD within Australia; `total_spend`: AUD total trip; `spend_per_trip`: spend/visitors |
| `waffle` | one cell in a 100-cell panel | `share`: fraction 0–1; x/y are layout positions; rounded cell count is not the exact percentage |
| `flows`, `flow-nodes` | ribbon sample / node | `value`: nominal AUD; y/y2 are proportional layout coordinates in billions; x is 0–1 horizontal position |
| `states` | state or territory, 2025 | visits, nights, spending in AUD; population persons; `spend_per_resident` AUD/resident; coordinates decimal degrees |
| `regions` | hierarchy node | leaves have `value` in AUD; parent nodes have zero own value and aggregate children through Vega; `parent` supplies the hierarchy |
| `markets` | published origin × year | visitor trips, visitor nights, spending and total spending in AUD; UK/USA are shortened source names |
| `origins`, `routes` | top-eight origin, 2025 | rounded source visitor trips; representative capital coordinates / great-circle schematic geometry |
| `changes` | origin × measure | `change` is fractional change (2025/2024 − 1); before/after are trips, nights or AUD according to metric |
| `waterfall` | contribution | start/end/value are AUD billions; six named markets are followed by “Other published markets” (the remaining published origins) and “Unpublished + rounding” (the national change minus all published-origin changes) |
| `activities` | selected activity × year | `share`: fraction of international event attendees, not all business-event visitors; multiple responses permitted |
| `per-night` | year | `business` / `other`: published rounded AUD spent within Australia per international visitor night |

The selected-market explanation, placed immediately after the scatterplot/heatmap pair, derives spending per trip (`spend / visitors`), nights per trip (`nights / visitors`) and spending per night (`spend / nights`) directly from the selected rows of `markets`. These are ratios of aggregate estimates, not individual visitor records. Total spending equals trips × spending per trip, or trips × nights per trip × spending per night. Across years the corresponding change factors multiply; percentage changes must not simply be added. The displayed values are rounded only after calculation. The default Malaysia example therefore connects approximately +31.3% trips and −20.7% spending per trip to +4.1% total spending; it does not identify a cause or follow the same people over time. This use of derived task-relevant quantities applies S1 p. 10 [L1].

## Limitations

- Visitor trips are not unique people. State visits can count the same multi-state trip more than once. Do not sum state visits to obtain national unique trips.
- All monetary comparisons are nominal, not adjusted for inflation or converted to Malaysian ringgit.
- Most local attendees and some event-industry spending are outside survey scope. These figures do not estimate the entire business-events industry's economic impact.
- Source rounding causes small differences between national, state and regional spending totals. Regional “other/unknown” A$1m is disclosed and omitted from the treemap. Suppressed/unavailable values are never silently replaced with zero.
- No confidence intervals are available in the extracted report tables. Neither significance nor causation is asserted. Small market changes may reflect sampling variability.
- The waterfall separates the remaining published markets (−AUD 14.758m) from the unpublished-origin/rounding residual (−AUD 133.815m). The latter is calculated by subtraction, not directly measured as rounding, and does not reveal which unpublished origins changed.
- A market called “Scandinavia” is retained as the report's regional category in tables, not relabelled as a country. It is not one of the top-eight flow endpoints.
- Activity participation uses attendees only. Attendance and accompanying-person groups can overlap, so they are not added.
- Two source tables were deliberately excluded: spending-item totals did not reconcile to the headline and event-duration rows contained an anomalous category. These do not affect the selected published totals.
- Schematic origin links are not flight paths or exact itineraries. Their representative capital endpoints are explicitly identified.

## Implementation and accessibility

Figure 08 keeps both 2024 and 2025 values visible for the chosen market, with compact visitor-axis labels defined in the axis title. Its **All markets** preset spans 0–200,000 trips and AUD 0–400m; **Smaller markets** spans 0–40,000 trips and AUD 0–120m and excludes records outside those bounds. Both presets use fixed domains across years. The visible note reports how many of the 18 markets remain, and prompts readers to return to the overview if their selected market is outside the detail. The table and rate summary still describe the selected market even when its dot is out of view.

Highlighting a market also outlines its row in Figure 09 without replacing the heatmap's change colours; signed selected values remain in the chart. Malaysia is an explicitly labelled starting example. Reset market view restores 2025, All markets as the highlighted group, and the All markets scale; resize logic retains year, highlighted market and scale. The separately labelled top-eight origin map remains a local 2025 view. The waffle key includes numeric trip/spending shares for reading without colour.

Earlier project notes reported checks across 36 market/year combinations and five viewport widths, including greyscale inspection. These are historical reports, not evidence that every combination has been re-tested for the current revision. The first 27 October 2026 revision, before the new detail preset and caption disclosures, was inspected directly in Chrome at 1920, 958, 639 and 383 CSS-pixel widths (window resizing and browser zoom): all 12 charts rendered without horizontal page overflow. The revised opening, compact scatter ticks, signed selected heatmap values and split waterfall labels were visually checked. Canada / 2024 selection updated the linked table and heatmap and survived resizing; Reset restored 2025 / all markets and the Malaysia example. The waterfall data dialog opened with both residual groups and closed successfully. No browser warnings or errors were recorded in that run. Source-derived waterfall JSON/CSV checks, extractor schema/decoder tests and all six live source-table comparisons passed. These checks are not a claim of formal accessibility compliance or testing on physical mobile devices. The subsequent detail preset, rate summary and shortened captions were checked in Chrome at 1920 CSS pixels: all 12 charts rendered, there was no horizontal page overflow, both years retained the detail bounds, Canada updated its heatmap/rates, China produced the explicit outside-detail notice, and Scandinavia correctly showed unchanged trip volume. Reset restored all three controls and the Malaysia analysis. All eight disclosures opened and closed through the keyboard. No browser warnings or errors were recorded. The Malaysian and national rate calculations were independently checked against the preserved data using exact rational arithmetic. All 12 specifications compiled and parsed; a separate non-browser Vega render at 230 chart pixels verified both scale presets in both years. This narrow-chart check does not establish the final whole-page layout or actual resize retention at narrower browser widths; those latest checks remain unverified.

Vega 5.33.0, Vega-Lite 5.23.0 and Vega-Embed 6.29.0 render the charts. Figure 06 uses Vega's hierarchy/treemap transform; the others use Vega-Lite. Specifications are readable JSON, created for this story. No finished visualisation has been copied or reskinned. `app.js` adjusts sizes for the available column width and preserves selector values on resize. The source snapshots are retained separately from the derived chart tables.

The Australia maps use an Albers-style conic equal-area projection with standard parallels −18° and −36°. The international map uses a Pacific-centred Equal Earth projection. GeoJSON input is supported by current Vega-Lite; it need not be converted to TopoJSON.

Controls are keyboard accessible. Each chart has a separate data table and downloadable CSV; the dialog closes with its button or Escape. Charts have visible headings, explanatory captions and source labels. Colour is reinforced with position, labels and explicit signs. Local fonts are Barlow Condensed and IBM Plex Sans, used under their included SIL Open Font Licences.

All displayed chart data and geometry total about 0.33 MB before compression. Optional source snapshots for reproduction are not fetched by the webpage. Screenshots are also not downloaded during normal page viewing.

## Reproduction and acknowledgement

`reproduce/build_data.py` rebuilds derived tables from the included statistical snapshots, downloading the three public Natural Earth inputs when needed. It requires Python and openpyxl. The checked-in `specs/` files contain the current presentation. `reproduce/build_specs.py` generates an earlier base; inspect its output before replacing them. The original public dashboard extraction method is documented in `reproduce/fetch_tra.py`; that retrieval uses only the publicly available report resource key, not private credentials.

Statistical content: © Commonwealth of Australia, licensed CC BY 4.0, except excluded third-party material and branding. Natural Earth data are public domain. No institutional endorsement is implied. Vendor licence notices are included in `vendor/`.

**AI acknowledgement:** OpenAI Codex assisted extensively with source review, data processing, analysis, narrative, visualisation specifications, web implementation and testing. The student must review and understand the work, check its accuracy and acknowledge this assistance in the submission. No tutor feedback, hand sketch or interview attendance is claimed.
