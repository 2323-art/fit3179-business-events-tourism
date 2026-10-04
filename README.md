# Beyond the conference badge

An original FIT3179 DV2 data story about Australia's business-event visitors, created by Jack (Wong Jing Yuan), Monash University Malaysia, 5 October 2026.

**Website:** https://2323-art.github.io/fit3179-business-events-tourism/

The main question is who generates visitor spending, where it lands, and how international markets changed between 2024 and 2025. The audience is a general Malaysian readership interested in Australian tourism and business events. The page is a single scrolling story, with four chapters, twelve charts and three distinct map idioms.

## Review refinements (5 October 2026)

Eight keyboard-accessible origin buttons identify map routes. Scatter commentary follows the selected year and any of eighteen markets. The heatmap retains mean-change ordering, one-decimal percentages and a Malaysia outline. The waterfall has cumulative connectors; the activity slope has direct labels and distinct line patterns. National table previews show 2025 only and warn against comparing historical domestic rows across the survey break. Statistical inputs are unchanged.

Responsive checks cover 1440, 1024, 390 and 320px, all twelve charts/tables and preservation of selections on resize. Rebuild readable specifications with `reproduce/build_specs.py`.

## Run locally

Serve this directory with any static HTTP server and open `index.html` through that server. Opening the file directly can prevent browsers from loading JSON. All libraries and fonts are included locally. No account, API key, build system or remote chart service is needed to view the page.

## Chart guide

| Figure | Specification | Question and encoding | Classification used for audit |
|---|---|---|---|
| 01 | `specs/01-waffle.json` | Which traveller types generate trips versus spending? Two 100-cell part-to-whole views, counted as one chart. Largest-remainder rounding conserves 100 squares; tooltips show exact shares. | Advanced waffle |
| 02 | `specs/02-spend-per-trip.json` | How much is spent per trip? Aligned lengths with a zero baseline. | Basic bar |
| 03 | `specs/03-sankey.json` | How much total trip spending stays in Australia? Conserved ribbon thickness links three traveller groups to two spending locations. | Advanced Sankey |
| 04 | `specs/04-choropleth.json` | Where is spending large relative to population? Sequential colour shows spending divided by midyear residents. | Advanced choropleth map |
| 05 | `specs/05-symbol-map.json` | Where are visitor volumes largest? Circle area, rather than radius, represents state visits. | Advanced proportional symbol map |
| 06 | `specs/06-treemap.json` | How do destination regions contribute within states? Nested rectangle areas show regional spending. | Advanced treemap |
| 07 | `specs/07-flow-map.json` | Which origins connect to Australia? Width of schematic capital-to-capital lines represents visitor trips for the top eight published origins. | Advanced origin–destination flow map |
| 08 | `specs/08-market-scatter.json` | Do volume and value identify the same leading markets? Position compares visitor trips with spending; fixed axes and a year selector support comparison. | Basic scatterplot |
| 09 | `specs/09-change-heatmap.json` | Do visitor, night and spending changes move together? Signed colour plus labels in an ordered matrix. | Advanced heatmap |
| 10 | `specs/10-waterfall.json` | Which changes compose the national international-spending decline? Floating increments connect national endpoints; a residual ensures reconciliation. | Advanced waterfall |
| 11 | `specs/11-activity-slope.json` | How did selected participation rates change? Slopes join 2024 and 2025 percentages. | Additional slope graph |
| 12 | `specs/12-per-night.json` | Is spending also higher after accounting for nights? Paired positions compare business-event and other international visitors. | Basic dumbbell |

Eight advanced families are counted without relying on the slope graph or dumbbell. If those two paired-comparison charts are grouped together by the assessor, eleven remain. The judgement of effective use and final grading belongs to the assessor.

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
| `waterfall` | contribution | start/end/value are AUD billions; “Other + rounding” reconciles all excluded/unpublished origins and source rounding |
| `activities` | selected activity × year | `share`: fraction of international event attendees, not all business-event visitors; multiple responses permitted |
| `per-night` | year | `business` / `other`: published rounded AUD spent within Australia per international visitor night |

## Limitations

- Visitor trips are not unique people. State visits can count the same multi-state trip more than once. Do not sum state visits to obtain national unique trips.
- All monetary comparisons are nominal, not adjusted for inflation or converted to Malaysian ringgit.
- Most local attendees and some event-industry spending are outside survey scope. These figures do not estimate the entire business-events industry's economic impact.
- Source rounding causes small differences between national, state and regional spending totals. Regional “other/unknown” A$1m is disclosed and omitted from the treemap. Suppressed/unavailable values are never silently replaced with zero.
- No confidence intervals are available in the extracted report tables. Neither significance nor causation is asserted. Small market changes may reflect sampling variability.
- A market called “Scandinavia” is retained as the report's regional category in tables, not relabelled as a country. It is not one of the top-eight flow endpoints.
- Activity participation uses attendees only. Attendance and accompanying-person groups can overlap, so they are not added.
- Two source tables were deliberately excluded: spending-item totals did not reconcile to the headline and event-duration rows contained an anomalous category. These do not affect the selected published totals.
- Schematic origin links are not flight paths or exact itineraries. Their representative capital endpoints are explicitly identified.

## Implementation and accessibility

Vega 5.33.0, Vega-Lite 5.23.0 and Vega-Embed 6.29.0 render the charts. Figure 06 uses Vega's hierarchy/treemap transform; the others use Vega-Lite. Specifications are readable JSON, created for this story. No finished visualisation has been copied or reskinned. `app.js` adjusts sizes for the available column width and preserves selector values on resize. Source data remain unchanged.

The Australia maps use an Albers-style conic equal-area projection with standard parallels −18° and −36°. The international map uses a Pacific-centred Equal Earth projection. GeoJSON input is supported by current Vega-Lite; it need not be converted to TopoJSON.

Controls are keyboard accessible. Each chart has a separate data table and downloadable CSV; the dialog closes with its button or Escape. Charts have visible headings, explanatory captions and source labels. Colour is reinforced with position, labels and explicit signs. Local fonts are Barlow Condensed and IBM Plex Sans, used under their included SIL Open Font Licences.

All displayed chart data and geometry total about 0.33 MB before compression. Optional source snapshots for reproduction are not fetched by the webpage. Screenshots are also not downloaded during normal page viewing.

## Reproduction and acknowledgement

`reproduce/build_data.py` rebuilds derived tables from the included statistical snapshots, downloading the three public Natural Earth inputs when needed. It requires Python and openpyxl. `reproduce/build_specs.py` regenerates the JSON specifications. The original public dashboard extraction method is documented in `reproduce/fetch_tra.py`; that retrieval uses only the publicly available report resource key, not private credentials.

Statistical content: © Commonwealth of Australia, licensed CC BY 4.0, except excluded third-party material and branding. Natural Earth data are public domain. No institutional endorsement is implied. Vendor licence notices are included in `vendor/`.

**AI acknowledgement:** OpenAI Codex assisted extensively with source review, data processing, analysis, narrative, visualisation specifications, web implementation and testing. The student must review and understand the work, check its accuracy and acknowledge this assistance in the submission. No tutor feedback, hand sketch or interview attendance is claimed.
