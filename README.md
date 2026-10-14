# Beyond the conference badge

An original FIT3179 DV2 data story about Australia's business-event visitors, created by Jack (Wong Jing Yuan), Monash University Malaysia, 5 October 2026.

**Website:** https://2323-art.github.io/fit3179-business-events-tourism/

The main question is who generates visitor spending, where it lands, and how international markets changed between 2024 and 2025. The audience is a general Malaysian readership interested in Australian tourism and business events. The page is a single scrolling story, with four chapters, twelve charts and three distinct map idioms.

## Review refinements

### Presentation fixes — 14 October 2026

Smaller state circles draw above larger ones, keeping the Australian Capital Territory visible. The scatterplot labels each year’s spending and visit leaders alongside Malaysia. The treemap wraps key region names, the Sankey labels source totals and its international split, and the slopegraph names activities directly. The waterfall retains an honest zero-based overview and adds enlarged floating changes with signed values. AUD, bn and m are introduced in the opening definitions. Readability, data tables, linked controls, keyboard operation and selection retention are verified across desktop and mobile widths.


### Consistent colour meanings and legends — 14 October 2026

**User rule: never pair red and green.** The red, rose and red-brown category colours have been retired: New South Wales uses deep violet, Western Australia uses sand, and national/state park activities use steel blue. Legends and linked charts use these replacements consistently. Future palette changes must preserve this rule; colour alone must not be the only way to identify a series.

`data/colour-semantics.json` records the category colours used by the charts and their legends. Each category colour has one meaning across the story: visitor classes retain gold/teal/blue; states have a separate shared palette in the symbol map and treemap; activities have their own colours and redundant line patterns; purple/orange consistently show increases/decreases. Slate grey identifies other international visitors. The choropleth retains a separate ordered greyscale for spending per resident. Text, outlines and basemaps are structural elements, not additional category encodings.

Colour legends retain the category key. Direct source totals and the international split annotate the Sankey; wrapped region names and selected values annotate the treemap; activity names sit beside their lines. Essential geographic labels and headline comparisons remain visible without interaction. State legend buttons highlight the same state in both views and show its destination spending below the treemap; keyboard selection and resize retention are supported.

Course guidance: `FIT2179 Course Notes 8 Colour.pdf`, PDF pages 5–8 and 10–11; `FIT2179 Course Notes 3 Marks and Channels.pdf`, PDF pages 3 and 6; `Munzner - Chapter 6 - Rules of Thumb.pdf`, PDF page 24. The eight-state palette is supported by selection and textual detail rather than requiring colour memorisation. No claim is made that all hues remain distinguishable under every colour-vision deficiency.

### White space and chart hierarchy — updated 14 October 2026

Captions follow their own charts instead of occupying forced shared rows. Detail, figure and chapter spacing follow a consistent progression; panel tops and column edges retain common sight-lines. Surplus minimum heights were removed.

On wide screens, related charts occupy equal-width columns with aligned chart starts. Chart heights reflect their content; the detailed treemap, flow map and waterfall retain a full row. The primary comparison pairs stack below 1,101 pixels. The waterfall combines zero-based national totals with an explicitly enlarged cumulative-change scale and signed contribution labels. These layout and scale choices serve the reading tasks; they are not numerical course requirements.

Source guidance: `FIT2179 Course Notes 9 Layout.pdf`, PDF pages 2 and 4–6; `FIT3179_Week04 – Visual hiearchy and figure-ground.pdf`, PDF pages 3 and 6; `Munzner - Chapter 7 - Arrange Tables.pdf`, PDF pages 31–32. Private course originals are not distributed in this repository.

### Font size and hierarchy — updated 14 October 2026

The original course typography guidance recommends 11–12 point text for digital displays and a clear hierarchy of titles, headings, annotations and secondary labels. The website uses a 16 pixel body size, a 15 pixel supporting-text minimum, 24 pixel chart headings, 36 pixel section headings and a 64–80 pixel main title. These particular heading ratios are design choices; the notes do not prescribe a fixed numerical scale. Body leading is 1.6 and supporting text 1.5. Prose measures adapt to their columns, with two-column captions under wide desktop figures.

Chart text uses the same readable minimum at every viewport. Paired figures stack earlier on narrower screens, long labels wrap, and legends receive more space. Secondary chart text has a quieter colour while annotations remain prominent. Source data and existing colour meanings are unchanged.

Sources: `FIT2179 Course Notes 11 Typography.pdf`, PDF file pages 6–9 and 11–12; `FIT2179 Course Notes 9 Layout.pdf`, pages 4–6; `FIT3179_Week04 – Visual hiearchy and figure-ground.pdf`, page 6. These original course documents are retained in the private knowledge base, not redistributed with the website.

### Readability — updated 14 October 2026

Paragraphs and captions use IBM Plex Sans. The marking-review fixes replace the earlier iterative ten-word line shrinking with responsive CSS measures and aligned chart starts. Country, state and source names remain explicit. Australian dollars (AUD), billion (bn) and million (m) are defined near the opening and abbreviated in crowded chart labels; underlying values and dataset keys remain unchanged.

Gold means domestic day visitors, teal domestic overnight visitors, and blue international business-event visitors. Purple consistently means increase and orange decrease in both change diagrams. The spending-per-resident map uses a sequential grey scale. Other charts use neutral marks, position, area, outlines or line patterns without assigning unrelated meanings to the visitor-category colours. Labels focus on key findings and selected markets, with exact details retained in tooltips and tables.

Five-width browser checks cover 1440, 1024, 768, 390 and 320 pixels, all thirty-six market/year combinations, nine origin controls including the overview, all twelve data tables, mobile callout bounds and selection retention on resize. Statistical input files are unchanged. This revision does not carry forward an earlier estimated grade as a new assessment.

Eight keyboard-accessible origin buttons identify map routes. Scatter commentary follows the selected year and any of eighteen markets. The heatmap retains mean-change ordering, one-decimal percentages and a Malaysia outline. The waterfall has cumulative connectors; the activity slope has direct labels and distinct line patterns. National table previews show 2025 only and warn against comparing historical domestic rows across the survey break. Statistical inputs are unchanged.

Responsive checks cover 1440, 1024, 390 and 320px, all twelve charts/tables and preservation of selections on resize. The checked-in `specs/` files are the reviewed presentation. `reproduce/build_specs.py` generates the earlier base specifications; review its output before replacing the refined specifications.

A subsequent independent review added high-contrast Sankey amounts and an explicit international-spending split, direct NT/ACT/NSW map values, compact wide-caption text and shared caption/action alignment across paired figures. These refinements preserve every statistical input and all twelve chart types.

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

Updated 12 October 2026 after reviewing relevant original course material across indexed Weeks 2–10 and the unconfirmed-week foundations. Figure 08 now keeps both 2024 and 2025 values visible for the chosen market. Its selector also outlines the same market in Figure 09 without replacing the heatmap's change colours. The default overview uses Malaysia as an explicitly labelled starting example; Reset market view restores 2025 / all markets. The separately labelled top-eight origin map remains a local 2025 view. The waffle key includes numeric trip/spending shares for reading without colour.

All 36 market/year combinations were checked at 1440, 1024, 768, 390 and 320px, including comparison values, linked selection, keyboard reset and resize retention. Existing table, route, alignment and annotation checks also passed. Opening, market and activity views were inspected in greyscale. These checks do not constitute formal accessibility certification or a guaranteed assignment grade.

Vega 5.33.0, Vega-Lite 5.23.0 and Vega-Embed 6.29.0 render the charts. Figure 06 uses Vega's hierarchy/treemap transform; the others use Vega-Lite. Specifications are readable JSON, created for this story. No finished visualisation has been copied or reskinned. `app.js` adjusts sizes for the available column width and preserves selector values on resize. Source data remain unchanged.

The Australia maps use an Albers-style conic equal-area projection with standard parallels −18° and −36°. The international map uses a Pacific-centred Equal Earth projection. GeoJSON input is supported by current Vega-Lite; it need not be converted to TopoJSON.

Controls are keyboard accessible. Each chart has a separate data table and downloadable CSV; the dialog closes with its button or Escape. Charts have visible headings, explanatory captions and source labels. Colour is reinforced with position, labels and explicit signs. Local fonts are Barlow Condensed and IBM Plex Sans, used under their included SIL Open Font Licences.

All displayed chart data and geometry total about 0.33 MB before compression. Optional source snapshots for reproduction are not fetched by the webpage. Screenshots are also not downloaded during normal page viewing.

## Reproduction and acknowledgement

`reproduce/build_data.py` rebuilds derived tables from the included statistical snapshots, downloading the three public Natural Earth inputs when needed. It requires Python and openpyxl. `reproduce/build_specs.py` regenerates the JSON specifications. The original public dashboard extraction method is documented in `reproduce/fetch_tra.py`; that retrieval uses only the publicly available report resource key, not private credentials.

Statistical content: © Commonwealth of Australia, licensed CC BY 4.0, except excluded third-party material and branding. Natural Earth data are public domain. No institutional endorsement is implied. Vendor licence notices are included in `vendor/`.

**AI acknowledgement:** OpenAI Codex assisted extensively with source review, data processing, analysis, narrative, visualisation specifications, web implementation and testing. The student must review and understand the work, check its accuracy and acknowledge this assistance in the submission. No tutor feedback, hand sketch or interview attendance is claimed.
