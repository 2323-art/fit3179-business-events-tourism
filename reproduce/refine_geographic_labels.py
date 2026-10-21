"""Idempotently refine only the ACT and international-origin annotations.

Apply to the current authored specifications. The older build_specs.py does not
recreate the current authored site. Source data, numeric encodings,
projections and unrelated chart specifications are not modified.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def refine():
    path = ROOT / 'specs/04-choropleth.json'
    spec = json.loads(path.read_text(encoding='utf-8'))
    # Retain the NT label; give ACT a dedicated offshore callout.
    nt = spec['layer'][1]
    nt['transform'][0]['filter'] = "datum.code == 'NT'"
    nt['mark']['dx'] = -5
    spec['layer'] = spec['layer'][:2]
    spec['layer'].extend([
        {
            'data': {'values': [{'longitude': 148.983, 'latitude': -35.4618,
                                  'lon2': 158, 'lat2': -42.5}]},
            'mark': {'type': 'rule', 'color': '#162B4D', 'strokeWidth': 1.4},
            'encoding': {
                'longitude': {'field': 'longitude', 'type': 'quantitative'},
                'latitude': {'field': 'latitude', 'type': 'quantitative'},
                'longitude2': {'field': 'lon2'}, 'latitude2': {'field': 'lat2'}}
        },
        {
            'data': {'values': [{'longitude': 148.983, 'latitude': -35.4618}]},
            'mark': {'type': 'circle', 'filled': False, 'size': 70,
                     'stroke': '#162B4D', 'strokeWidth': 1.6, 'opacity': 1},
            'encoding': {'longitude': {'field': 'longitude', 'type': 'quantitative'},
                         'latitude': {'field': 'latitude', 'type': 'quantitative'}}
        },
        {
            'data': {'url': 'data/states.json'},
            'transform': [
                {'filter': "datum.code == 'ACT'"},
                {'calculate': "'Australian Capital\\nTerritory\\n$' + format(datum.spend_per_resident, ',.0f')", 'as': 'callout'}],
            'mark': {'type': 'text', 'align': 'right', 'baseline': 'top', 'dx': 0, 'dy': 7,
                     'fontSize': 15, 'fontWeight': 'bold', 'lineBreak': '\n',
                     'lineHeight': 18, 'color': '#162B4D'},
            'encoding': {'longitude': {'datum': 158}, 'latitude': {'datum': -42.5},
                         'text': {'field': 'callout'},
                         'tooltip': [{'field': 'state', 'title': 'State'},
                                     {'field': 'spend_per_resident', 'type': 'quantitative', 'title': 'AUD per resident', 'format': '$,.0f'}]}
        }
    ])
    path.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    path = ROOT / 'specs/07-flow-map.json'
    spec = json.loads(path.read_text(encoding='utf-8'))
    labels = spec['layer'][4]
    labels['transform'][0]['filter'] = "originFocus == 'All origins' || datum.country == originFocus"
    labels['mark']['align'] = {'expr': "datum.country == 'USA' || datum.country == 'India' || datum.country == 'Malaysia' || datum.country == 'Singapore' ? 'right' : 'left'"}
    labels['mark']['dx'] = {'expr': "datum.country == 'USA' || datum.country == 'India' || datum.country == 'Malaysia' || datum.country == 'Singapore' ? -8 : 8"}
    labels['mark']['dy'] = {'expr': "datum.country == 'UK' ? -24 : datum.country == 'Singapore' ? 20 : datum.country == 'Malaysia' ? -10 : datum.country == 'Japan' ? -4 : -12"}
    path.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

if __name__ == '__main__':
    refine()


