"""Rebuild the six-origin Sankey from the preserved TRA market snapshot."""
import argparse
import csv
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def outputs():
    source = json.loads((ROOT / 'data/source/tra-international-markets.json').read_text(encoding='utf-8'))
    markets = {}
    for row in source:
        if row['Year'] == 2025:
            attrs = markets.setdefault(row['Country of origin'], {})
            assert row['Attribute'] not in attrs
            attrs[row['Attribute']] = row['Value']
    rows = []
    for country, attrs in markets.items():
        total = round(attrs['Total trip spend ($000)'] * 1000)
        inside = round(attrs['Spend in Australia ($000)'] * 1000)
        assert 0 <= inside <= total
        rows.append(dict(country=country, year=2025, total_trip_spend=total,
                         in_australia=inside, outside_australia=total-inside, share=inside/total))
    rows = sorted(rows, key=lambda r: (-r['total_trip_spend'], r['country']))[:6]
    assert len(rows) == 6
    rows = [dict(rank=i+1, **r) for i, r in enumerate(rows)]
    # All ribbon endpoints use AUD coordinates and the same vertical scale.
    source_gap, target_gap = 100000000, 120000000
    inside_total = sum(r['in_australia'] for r in rows)
    outside_total = sum(r['outside_australia'] for r in rows)
    extent = inside_total + outside_total + 5 * source_gap
    offset = (5 * source_gap - target_gap) / 2
    destinations = [('in_australia', 'Retained in Australia', offset, inside_total),
                    ('outside_australia', 'Spent outside Australia', offset+inside_total+target_gap, outside_total)]
    nodes, links = [], []
    target_positions = {key: start for key, _, start, _ in destinations}
    source_position = 0
    for row in rows:
        country = row['country']
        label = country.replace('United States of America', 'United States')
        nodes.append(dict(kind='source', country=country, label=label, amount=row['total_trip_spend'],
                          y0=source_position, y1=source_position+row['total_trip_spend'], extent=extent))
        source_split = source_position
        for key, location, _, _ in destinations:
            amount = row[key]
            target_start = target_positions[key]
            links.append(dict(country=country, location=location, amount=amount,
                              total=row['total_trip_spend'], share=amount/row['total_trip_spend'],
                              sy0=source_split, sy1=source_split+amount,
                              ty0=target_start, ty1=target_start+amount, extent=extent))
            source_split += amount
            target_positions[key] += amount
        assert source_split == source_position+row['total_trip_spend']
        source_position = source_split+source_gap
    for key, location, start, amount in destinations:
        assert target_positions[key] == start+amount
        nodes.append(dict(kind='target', country='', label=location, amount=amount,
                          y0=start, y1=start+amount, extent=extent))
    assert sum(l['amount'] for l in links) == sum(r['total_trip_spend'] for r in rows)
    assert all(l['sy1']-l['sy0'] == l['ty1']-l['ty0'] == l['amount'] for l in links)
    result = {}
    for name, data in [('origin-spending', rows), ('origin-spending-links', links), ('origin-spending-nodes', nodes)]:
        result[name+'.json'] = json.dumps(data, indent=2, ensure_ascii=False)+'\n'
    buf = io.StringIO(newline='')
    writer = csv.DictWriter(buf, fieldnames=list(rows[0]), lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)
    result['origin-spending.csv'] = buf.getvalue()
    return result


def build(check=False):
    for name, content in outputs().items():
        path = ROOT / 'data' / name
        if check:
            assert path.read_text(encoding='utf-8') == content, 'Stale output: '+name
        else:
            path.write_text(content, encoding='utf-8')
    print('Verified six ranked origins, twelve conserved flows and two destination totals.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    build(parser.parse_args().check)
