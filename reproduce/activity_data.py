"""Build/check the six-activity 2023-2025 comparison using preserved TRA sources.

2023 is the rounded attendee column in State of the Industry 2023, printed p41.
2024/25 retain Percentage_attend from the public business-events dashboard.
Ranks are calculated ONLY within the same six activities in every year.
"""
import argparse
import csv
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAMES = {
    'Dine out': 'Dining',
    'Go shopping': 'Shopping',
    'Sightseeing': 'Sightseeing',
    'Botanical / public gardens': 'Gardens',
    'National parks / state parks': 'National/state parks',
    'Museums or art galleries': 'Museums & galleries',
}


def build_activities():
    source = ROOT / 'data' / 'source'
    report = json.loads((source / 'tra-activities-2023.json').read_text(encoding='utf-8'))
    dashboard = json.loads((source / 'tra-international-be-actitivies.json').read_text(encoding='utf-8'))
    rows = []
    for r in report['rows'] + dashboard:
        if r['Activity'] not in NAMES:
            continue
        year, share = r['Year'], r['Percentage_attend']
        assert year in (2023, 2024, 2025) and share is not None and 0 <= share <= 1
        rows.append(dict(activity=NAMES[r['Activity']], year=year, share=share,
                         rank=0, participation=(f'About {share:.0%}' if year == 2023 else f'{share:.1%}'),
                         source=('TRA State of the Industry 2023, p. 41' if year == 2023 else 'TRA business-events dashboard'),
                         precision=('Published whole percentage' if year == 2023 else 'Dashboard estimate')))
    assert len(rows) == 18 and len({(r['activity'], r['year']) for r in rows}) == 18
    for year in (2023, 2024, 2025):
        group = [r for r in rows if r['year'] == year]
        assert {r['activity'] for r in group} == set(NAMES.values())
        for r in group:
            r['rank'] = 1 + sum(other['share'] > r['share'] for other in group)
    return sorted(rows, key=lambda r: (r['year'], r['rank'], r['activity']))


def output_text(rows):
    stream = io.StringIO(newline='')
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)
    return json.dumps(rows, indent=2, ensure_ascii=False) + '\n', stream.getvalue()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    rows = build_activities()
    texts = output_text(rows)
    for suffix, text in zip(('json', 'csv'), texts):
        path = ROOT / 'data' / f'activities.{suffix}'
        if args.check:
            assert path.read_text(encoding='utf-8') == text, f'{path.name} differs from source-derived values'
        else:
            path.write_text(text, encoding='utf-8')
    print('Verified 18 observations: six identical activities in 2023, 2024 and 2025; ranks within that set.')


if __name__ == '__main__':
    main()
