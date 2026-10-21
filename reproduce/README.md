# Reproducing the current website

The readable JSON files in `../specs/` are the current authored chart definitions. The website loads these files directly; it has no chart-generation build step.

`build_data.py` processes the preserved statistical snapshots into the derived data used by the site. This is separate from recreating the visual design.

`build_specs.py` is an older chart-generation script. An isolated comparison on 14 October 2026 found that nine of its twelve outputs differ from the authored specifications. Do not run it over the current `specs` directory. Keep any experimental regeneration in a separate copy.

The following scoped helpers apply the current refinements to the existing authored specifications and can be run repeatedly:

- `refine_geographic_labels.py`: ACT callout and international-origin labels.
- `refine_text_contrast.py`: Sankey and heatmap label foregrounds.
- `refine_story_annotations.py`: state-visit map callouts.

These helpers preserve the existing data and quantitative encodings. They are not a migration from the older generator's output. Preview and inspect the charts after any later design or source-data change.
