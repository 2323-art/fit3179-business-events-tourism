"""Bounded, offline rebuild/check for the narrative revision. Standard library only."""
import argparse
import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TYPES = ['Domestic day', 'Domestic overnight', 'International']
STATES = {'New South Wales':'NSW','Victoria':'VIC','Queensland':'QLD','South Australia':'SA','Western Australia':'WA','Tasmania':'TAS','Northern Territory':'NT','ACT':'ACT'}
UNION = 'Attended or accompanied someone else to business event total'

def read(name):
    return json.loads((ROOT/'data/source'/f'{name}.json').read_text(encoding='utf-8'))

def build_outputs():
    summary = read('tra-summary-dashboard')
    international = [r for r in summary if r['Year']==2025 and r['Type']=='International' and r['Category']==UNION]
    assert len(international)==1
    r=international[0]
    total=r['Total trip spend ($000)']*1000
    inside=r['Spend in Australia ($000)']*1000
    outside=total-inside
    assert 0 < inside < total
    # Conserved international-only Sankey: thickness is AUD / 1bn at every x.
    flows=[]
    nodes=[dict(label='International trip spending',x=0,y=.35,y2=.35+total/1e9,value=total,share=1)]
    source_y=.35
    for destination,value,dest_y in [('In Australia',inside,0),('Outside Australia',outside,inside/1e9+.7)]:
        h=value/1e9
        for step in range(31):
            t=step/30; smooth=t*t*(3-2*t); y=source_y+(dest_y-source_y)*smooth
            flows.append(dict(link='International → '+destination,traveller='International',destination=destination,value=value,share=value/total,x=t,y=y,y2=y+h))
        nodes.append(dict(label=destination,x=1,y=dest_y,y2=dest_y+h,value=value,share=value/total))
        source_y+=h
    assert inside+outside==total
    state_source=read('tra-state-summary')
    mix=[]
    for state,code in STATES.items():
        rows=[r for r in state_source if r['Year']==2025 and r['State/Territory']==state and r['Category']=='Total' and r['Type'] in TYPES]
        assert len(rows)==3 and {r['Type'] for r in rows}==set(TYPES),state
        assert all(r['Sample In/Out']==1 and r['Visitors (000)'] is not None and r['Expenditure ($M)'] is not None for r in rows),state
        # Shares use the three published components, not State Total (all tourism).
        visits=sum(r['Visitors (000)'] for r in rows)*1000
        spend=sum(r['Expenditure ($M)'] for r in rows)*1000000
        for typ in TYPES:
            r=next(r for r in rows if r['Type']==typ)
            mix.append(dict(state='Australian Capital Territory' if state=='ACT' else state,code=code,year=2025,traveller=typ,visitors=r['Visitors (000)']*1000,spend=r['Expenditure ($M)']*1000000,visitor_share=r['Visitors (000)']*1000/visits,spend_share=r['Expenditure ($M)']*1000000/spend,order=TYPES.index(typ)))
        for key in ['visitor_share','spend_share']:
            assert math.isclose(sum(r[key] for r in mix if r['code']==code),1,abs_tol=1e-12)
    return {'flows':flows,'flow-nodes':nodes,'state-mix':mix}

def save_outputs(outputs):
    for name,rows in outputs.items():
        (ROOT/'data'/f'{name}.json').write_text(json.dumps(rows,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
        with (ROOT/'data'/f'{name}.csv').open('w',encoding='utf-8-sig',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)

def check_outputs(outputs):
    for name,expected in outputs.items():
        actual=json.loads((ROOT/'data'/f'{name}.json').read_text(encoding='utf-8'))
        assert actual==expected,f'{name} JSON differs from preserved sources'
        with (ROOT/'data'/f'{name}.csv').open(encoding='utf-8-sig',newline='') as f: actual=list(csv.DictReader(f))
        assert len(actual)==len(expected),name
        for got,want in zip(actual,expected):
            assert all(got[k]==v if isinstance(v,str) else float(got[k])==v for k,v in want.items()),name
    print('PASS: international Sankey conserves source spending; 24 state/traveller rows match published union estimates; all eight share pairs sum to 100%; JSON and CSV agree.')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true',help='Verify without writing')
    args=parser.parse_args()
    outputs=build_outputs()
    if args.check: check_outputs(outputs)
    else: save_outputs(outputs);check_outputs(outputs)
