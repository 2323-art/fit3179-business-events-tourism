"""Apply only the two chart-label contrast refinements to existing specifications.

Apply to the current authored specifications; this never regenerates other
charts or data and does not make the older generator reproduce this version.
Vega-Lite's shared quantitative colour scale is named ``color``. Comparing its
actual RGB output avoids assuming equal luminance on both diverging-scale arms.
"""

import json
from pathlib import Path


SITE = Path(__file__).resolve().parents[1]


def update(filename, refine):
    path = SITE / "specs" / filename
    spec = json.loads(path.read_text(encoding="utf-8"))
    refine(spec)
    content = json.dumps(spec, ensure_ascii=False, indent=2) + "\n"
    if path.read_text(encoding="utf-8") != content:
        path.write_text(content, encoding="utf-8")


def sankey(spec):
    labels = [layer for layer in spec["layer"]
              if layer.get("data", {}).get("values", [{}])[0].get("label") == "AUD 2.34bn"]
    if len(labels) != 1:
        raise ValueError("Expected exactly one international-spending amount label")
    # Same foreground as the other node labels, including over translucent blue.
    labels[0]["mark"]["color"] = "#07101C"


def heatmap(spec):
    labels = [layer for layer in spec["layer"]
              if layer.get("mark", {}).get("type") == "text"
              and layer.get("encoding", {}).get("text", {}).get("field") == "change_label"]
    if len(labels) != 1:
        raise ValueError("Expected exactly one selected-value label layer")
    labels[0]["encoding"]["color"] = {
        "condition": {
            "test": "contrast('white', scale('color', datum.change)) > contrast('black', scale('color', datum.change))",
            "value": "white",
        },
        "value": "black",
    }


if __name__ == "__main__":
    update("03-sankey.json", sankey)
    update("09-change-heatmap.json", heatmap)
