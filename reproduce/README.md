# Reproducing the current website

The readable JSON files in `../specs/` are the current authored chart definitions. The website loads these files directly; it has no chart-generation build step.

`build_data.py` processes the preserved statistical snapshots into the derived data used by the site. This is separate from recreating the visual design.

## Verify or rebuild the narrative/state-mix data

`python reproduce/story_data.py --check` compares the saved Sankey and state-mix JSON/CSV with the preserved official snapshots without writing. `python reproduce/story_data.py` rebuilds only those three tables. This standard-library script is also called by the full data rebuild.

The Sankey now isolates the 2025 international total-trip spending split. The state mix selects `Year = 2025`, `Category = Total`, the three traveller `Type` rows and `Sample In/Out = 1` for each of eight jurisdictions. It does not add Attend/Accompany or use `State Total` (all tourism). Shares divide by the sum of the three published components in each jurisdiction; separate state totals differ slightly through source rounding. No states are summed into national unique trips.

## Verify or rebuild chart 10 only

From the repository root, these commands use Python's standard library and the included snapshots:

```powershell
python reproduce/build_data.py --check-waterfall
python reproduce/build_data.py --waterfall-only
```

The first compares the checked-in JSON and CSV with source-derived results without writing. The second rewrites only `data/waterfall.json` and `data/waterfall.csv`. A complete `python reproduce/build_data.py` run also needs `openpyxl` and downloads missing Natural Earth inputs; it rebuilds all derived data.

Chart 10 retains the six largest absolute changes among the 18 published origin markets, with increases before decreases. It now distinguishes:

- **Other published markets:** the combined change among the remaining 12 published origins: AUD -14.758 million.
- **Unpublished + rounding:** the difference between the 2024 and 2025 national amounts not represented in the 18-market table: AUD -133.815 million. This includes origin markets absent from that table and source rounding; it is not an estimate of rounding error alone.

The 18 published markets sum to AUD 2,025.405 million in 2024 and AUD 1,986.791 million in 2025. Subtracting those amounts from national totals gives AUD 486.503 million and AUD 352.688 million respectively. The six named changes, other published markets and the unrepresented-origin residual together equal the national AUD -172.429 million change. Calculations accumulate whole AUD before converting to display billions.

## Retrieve the original public tables separately

`fetch_tra.py` uses the public Power BI report resource key and the six entity names documented in the script. Its column contracts come from the preserved `data/source/tra-*.json` snapshots, including the original source's spelling `International BE Actitivies`. No `research/schema.json`, credentials or separately installed Python packages are required.

Offline checks do not contact the server or write files:

```powershell
python reproduce/fetch_tra.py --check-only
python reproduce/fetch_tra.py --self-test
```

The schema check verifies column consistency across all preserved rows. Decoder checks exercise column reordering, dictionary values, decimal values, nulls and repeated values, and reject malformed or changed schemas. The decoder also refuses potentially truncated results.

To retrieve all six tables, or just one:

```powershell
python reproduce/fetch_tra.py
python reproduce/fetch_tra.py --table "Per person night spend"
```

Raw responses and decoded tables go to `research/tra-refresh/`, created automatically. Use `--output-dir` to select another directory outside `data/`. The script refuses output inside `data/` so it cannot silently replace published snapshots. These report identifiers refer to the source report used by the project; if TRA changes the model or service, the explicit validation error requires inspecting the new response and reviewing definitions before adopting it.

During the 27 October 2026 repair, both offline checks passed. All six public tables were then retrieved and decoded in memory: 72 summary rows, 288 state rows, 52 regional rows, 144 market rows, 113 activity rows and two per-night rows. Every decoded row matched its preserved snapshot after normalising row order. No source or displayed data was refreshed. This verifies the current retrieval path and snapshot fidelity, not future service compatibility or the underlying survey estimates themselves.

`build_specs.py` is an older chart-generation script. An isolated comparison on 14 October 2026 found that nine of its twelve outputs differ from the authored specifications. Do not run it over the current `specs` directory. Keep any experimental regeneration in a separate copy.

The following scoped helpers apply the current refinements to the existing authored specifications and can be run repeatedly:

- `refine_geographic_labels.py`: ACT callout and international-origin labels.
- `refine_text_contrast.py`: older Sankey/heatmap foreground helper; do not run it over the reshaped international-only Sankey.
- `refine_story_annotations.py`: state-visit map callouts.

These helpers preserve the existing data and quantitative encodings. They are not a migration from the older generator's output. Preview and inspect the charts after any later design or source-data change.
