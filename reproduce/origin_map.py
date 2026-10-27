"""Build all individually located 2025 origin markets from preserved sources."""
import argparse
import csv
import io
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def great_circle(a, b):
    def vec(p):
        lon, lat = map(math.radians, p)
        return [math.cos(lat)*math.cos(lon), math.cos(lat)*math.sin(lon), math.sin(lat)]
    va, vb = vec(a), vec(b)
    omega = math.acos(max(-1, min(1, sum(x*y for x, y in zip(va, vb)))))
    points = []
    for i in range(61):
        t = i / 60
        v = [(math.sin((1-t)*omega)*x+math.sin(t*omega)*y)/math.sin(omega)
             for x, y in zip(va, vb)]
        points.append([round(math.degrees(math.atan2(v[1], v[0])), 3),
                       round(math.degrees(math.atan2(v[2], math.hypot(v[0], v[1]))), 3)])
    return points


def outputs():
    source = json.loads((ROOT/'data/source/tra-international-markets.json').read_text())
    places = json.loads((ROOT/'data/source/origin-map-places.json').read_text())
    coords = {r['country']: r['coordinates'] for r in places['places']}
    aliases = {'United States of America': 'USA', 'United Kingdom': 'UK'}
    counts = {aliases.get(r['Country of origin'], r['Country of origin']): round(r['Value']*1000)
              for r in source if r['Year'] == 2025 and r['Attribute'] == 'Visitors (000)'}
    assert set(counts)-set(coords) == {'Scandinavia'}, 'Review origins without individual locations'
    origins, routes = [], []
    for country in sorted(set(counts)&set(coords), key=lambda c: (-counts[c], c)):
        coord = coords[country]
        origins.append(dict(country=country, visitors=counts[country], longitude=coord[0], latitude=coord[1]))
        routes.append(dict(type='Feature', properties=dict(country=country, visitors=counts[country]),
                           geometry=dict(type='LineString', coordinates=great_circle(coord, coords['Australia']))))
    assert len(origins) == len(routes) == 17
    assert sum(r['visitors'] for r in origins) == sum(counts.values())-counts['Scandinavia']
    result = {'origins.json': json.dumps(origins, ensure_ascii=False, separators=(',', ':'))+'\n',
              'routes.json': json.dumps(dict(type='FeatureCollection', features=routes), separators=(',', ':'))+'\n'}
    buf = io.StringIO(newline='')
    writer = csv.DictWriter(buf, fieldnames=list(origins[0]), lineterminator='\n')
    writer.writeheader()
    writer.writerows(origins)
    result['origins.csv'] = buf.getvalue()
    return result


def build(check=False):
    for name, content in outputs().items():
        path = ROOT/'data'/name
        if check:
            assert path.read_text(encoding='utf-8') == content, 'Stale output: '+name
        else:
            path.write_text(content, encoding='utf-8')
    print('Verified 17 individual origins and matching routes; Scandinavia remains unlocated.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    build(parser.parse_args().check)
