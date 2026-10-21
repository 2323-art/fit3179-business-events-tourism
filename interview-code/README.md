# Annotated visualisation code

These study companions explain the chart specifications used by **Beyond the conference badge**. Prepared from the local source on 21 October 2026.

## Start here

1. Read [app.js](../app.js), searching for `INTERVIEW:`. Follow `start`, `renderChart`, `updateComparison` and `selectState` to understand loading and linked controls.
2. Open [the annotated scatterplot](08-market-scatter.jsonc) to understand data, filters, marks, encodings and parameters.
3. Open [the annotated treemap](06-treemap.jsonc) for the Vega hierarchy and layout transforms.
4. Read the comments in [build_data.py](../reproduce/build_data.py) for source preparation and calculations, [index.html](../index.html) for structure and [style.css](../style.css) for layout.

## All charts

- [01 — Paired waffles](01-waffle.jsonc)
- [02 — Spending per trip](02-spend-per-trip.jsonc)
- [03 — Sankey spending flows](03-sankey.jsonc)
- [04 — Spending-per-resident choropleth](04-choropleth.jsonc)
- [05 — State-visit symbol map](05-symbol-map.jsonc)
- [06 — Destination treemap](06-treemap.jsonc)
- [07 — International origin flow map](07-flow-map.jsonc)
- [08 — Market scatterplot](08-market-scatter.jsonc)
- [09 — Change heatmap](09-change-heatmap.jsonc)
- [10 — Spending-change waterfall](10-waterfall.jsonc)
- [11 — Activity slopegraph](11-activity-slope.jsonc)
- [12 — Per-night dumbbell](12-per-night.jsonc)

The site loads the original valid JSON in [specs](../specs/), not these JSONC companions. JSONC allows explanatory comments for reading. Removing comment lines from each companion produces the same JSON object as the corresponding source specification. [Source hashes](source-hashes.json) record the exact source bytes used; refresh companions after future specification edits.

These comments explain implementation, not assessment results. See [reproduction notes](../reproduce/README.md) before running any scripts. The current authored specifications are authoritative; the older specification generator must not overwrite them.
