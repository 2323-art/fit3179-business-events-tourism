"""Retrieve the six public TRA tables used by this story into a separate directory.

The included source snapshots supply the explicit column contract: no missing
research/schema.json dependency. Retrieval never replaces displayed data.
Run --check-only or --self-test for offline validation without network or writes.
"""
import argparse
import json
import urllib.request
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KEY = '1a9ff311-b70d-4152-9d89-11058df44fe7'
API = 'https://wabi-australia-southeast-b-primary-api.analysis.windows.net/public/reports/querydata?synchronous=true'
# Entity names from the original public model; filenames are preserved snapshots.
TABLES = {
    'Summary Dashboard': 'tra-summary-dashboard.json',
    'State summary': 'tra-state-summary.json',
    'cap city regional': 'tra-cap-city-regional.json',
    'International markets': 'tra-international-markets.json',
    'International BE Actitivies': 'tra-international-be-actitivies.json',
    'Per person night spend': 'tra-per-person-night-spend.json',
}


def source_contracts():
    """Check included rows before reusing their published column names."""
    contracts = {}
    for entity, filename in TABLES.items():
        rows = json.loads((ROOT / 'data' / 'source' / filename).read_text(encoding='utf-8'))
        if not rows or not isinstance(rows[0], dict):
            raise ValueError(f'{filename}: expected a non-empty table')
        props = list(rows[0])
        if any(set(row) != set(props) for row in rows):
            raise ValueError(f'{filename}: inconsistent column schema')
        if 'Year' not in props:
            raise ValueError(f'{filename}: missing comparison-year column')
        contracts[entity] = props
    return contracts


def fetch(entity, props):
    query = {
        'Version': 2,
        'From': [{'Name': 't', 'Entity': entity, 'Type': 0}],
        'Select': [{'Column': {'Expression': {'SourceRef': {'Source': 't'}},
                               'Property': p}, 'Name': f't.{p}'} for p in props],
    }
    command = {'SemanticQueryDataShapeCommand': {
        'Query': query,
        'Binding': {'Primary': {'Groupings': [{'Projections': list(range(len(props)))}]},
                    'DataReduction': {'DataVolume': 4, 'Primary': {'Window': {'Count': 30000}}},
                    'Version': 1},
        'ExecutionMetricsKind': 1,
    }}
    body = {'version': '1.0.0', 'queries': [{'Query': {'Commands': [command]},
             'QueryId': '', 'ApplicationContext': {'DatasetId': '17ce0b91-6143-4a3b-9698-de3904c772c0'}}],
            'cancelQueries': [], 'modelId': 100530}
    request = urllib.request.Request(API, data=json.dumps(body).encode(), headers={
        'Content-Type': 'application/json', 'X-PowerBI-ResourceKey': KEY,
        'ActivityId': str(uuid.uuid4()), 'RequestId': str(uuid.uuid4()),
    })
    return urllib.request.urlopen(request, timeout=60).read()


def decode(props, response):
    """Decode dictionaries/null/repetition flags without guessing column order."""
    try:
        ds = response['results'][0]['result']['data']['dsr']['DS'][0]
        rows = ds['PH'][0]['DM0']
    except (KeyError, IndexError, TypeError) as exc:
        raise ValueError('Public response changed or returned an error; inspect the raw response') from exc
    if not rows:
        raise ValueError('Public report returned no rows')
    schema = rows[0].get('S', [])
    if len(schema) != len(props):
        raise ValueError('Response column count differs from preserved source contract')
    names = [column.get('N', '') for column in schema]
    if set(names) != {f'G{i}' for i in range(len(props))}:
        raise ValueError(f'Unexpected response column identifiers: {names}')
    output_names = [props[int(name[1:])] for name in names]
    dictionaries = ds.get('ValueDicts', {})
    previous = None
    output = []
    sentinel = object()
    for row in rows:
        if 'S' in row and row['S'] != schema:
            raise ValueError('Response changes schema between rows')
        cells = iter(row.get('C', []))
        current = []
        for i, column in enumerate(schema):
            if row.get('R', 0) & (1 << i):
                if previous is None:
                    raise ValueError('First row cannot repeat a preceding value')
                value = previous[i]
            elif row.get('Ø', 0) & (1 << i):
                value = None
            else:
                value = next(cells, sentinel)
                if value is sentinel:
                    raise ValueError('Response row has too few cells')
            current.append(value)
        if next(cells, sentinel) is not sentinel:
            raise ValueError('Response row has extra cells')
        decoded = []
        for column, value in zip(schema, current):
            if 'DN' in column and isinstance(value, int):
                try:
                    if value < 0:
                        raise IndexError('Negative dictionary index')
                    value = dictionaries[column['DN']][value]
                except (KeyError, IndexError) as exc:
                    raise ValueError('Invalid response dictionary reference') from exc
            elif column.get('T') == 3 and isinstance(value, str):
                value = float(value)
            decoded.append(value)
        output.append(dict(zip(output_names, decoded)))
        previous = current
    if len(output) >= 30000 or ds.get('RT'):
        raise ValueError('Response may be truncated; do not publish a partial table')
    return output


def self_test():
    """Exercise compressed response cases and reject malformed/schema-drift rows."""
    def wrap(rows):
        return {'results': [{'result': {'data': {'dsr': {'DS': [{
            'PH': [{'DM0': rows}], 'ValueDicts': {'D0': ['Malaysia', 'China']},
        }]}}}}]}
    schema = [{'N': 'G1', 'T': 3}, {'N': 'G0', 'T': 1, 'DN': 'D0'}, {'N': 'G2', 'T': 7}]
    response = wrap([{'S': schema, 'C': ['10.5', 0, 2024]},
                     {'R': 2, 'Ø': 1, 'C': [2025]},
                     {'R': 4, 'C': ['20', 1]}])
    expected = [{'Value': 10.5, 'Country': 'Malaysia', 'Year': 2024},
                {'Value': None, 'Country': 'Malaysia', 'Year': 2025},
                {'Value': 20.0, 'Country': 'China', 'Year': 2025}]
    assert decode(['Country', 'Value', 'Year'], response) == expected
    for invalid in [wrap([{'S': schema, 'C': ['10.5', 0]}]),
                    wrap([{'S': schema, 'R': 2, 'C': ['10.5', 2024]}]),
                    wrap([{'S': schema[:-1], 'C': ['10.5', 0]}]),
                    wrap([{'S': schema, 'C': ['10.5', 0, 2024, None]}])]:
        try:
            decode(['Country', 'Value', 'Year'], invalid)
        except ValueError:
            pass
        else:
            raise AssertionError('Malformed response was accepted')
    print('Decoder checks passed: reordered columns, dictionaries, decimals, nulls, repeated values and malformed rows')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-only', action='store_true', help='Validate local column contracts without network or writes')
    parser.add_argument('--self-test', action='store_true', help='Run offline decoder checks without network or writes')
    parser.add_argument('--table', choices=list(TABLES), help='Retrieve only one table')
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'research' / 'tra-refresh')
    args = parser.parse_args()
    contracts = source_contracts()
    if args.self_test:
        self_test()
        return
    if args.check_only:
        for entity, props in contracts.items():
            print(f'{entity}: {len(props)} columns verified against {TABLES[entity]}')
        return
    destination = args.output_dir.resolve()
    protected = (ROOT / 'data').resolve()
    if destination == protected or protected in destination.parents:
        raise ValueError('Choose a directory outside data/; never overwrite published snapshots')
    destination.mkdir(parents=True, exist_ok=True)
    for entity, props in contracts.items():
        if args.table and entity != args.table:
            continue
        filename = TABLES[entity]
        raw = fetch(entity, props)
        (destination / filename.replace('.json', '-raw.json')).write_bytes(raw)
        rows = decode(props, json.loads(raw))
        (destination / filename).write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding='utf-8')
        print(f'{entity}: {len(rows)} rows saved separately; review definitions and periods before adoption')


if __name__ == '__main__':
    main()
