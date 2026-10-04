"""Read the public data model underlying TRA's published business-events report.
No login or private endpoints. Preserve the public response for reproducibility.
"""
import json, urllib.request, uuid, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
KEY='1a9ff311-b70d-4152-9d89-11058df44fe7'
API='https://wabi-australia-southeast-b-primary-api.analysis.windows.net/public/reports/querydata?synchronous=true'
SCHEMA=json.loads((ROOT/'research/schema.json').read_text())['schemas'][0]['schema']['Entities']

def fetch(entity):
    props=[p['Name'] for p in entity['Properties'] if 'Column' in p]
    query={'Version':2,'From':[{'Name':'t','Entity':entity['Name'],'Type':0}],
           'Select':[{'Column':{'Expression':{'SourceRef':{'Source':'t'}},'Property':p},'Name':f't.{p}'} for p in props]}
    command={'SemanticQueryDataShapeCommand':{'Query':query,'Binding':{'Primary':{'Groupings':[{'Projections':list(range(len(props)))}]},'DataReduction':{'DataVolume':4,'Primary':{'Window':{'Count':30000}}},'Version':1},'ExecutionMetricsKind':1}}
    body={'version':'1.0.0','queries':[{'Query':{'Commands':[command]},'QueryId':'','ApplicationContext':{'DatasetId':'17ce0b91-6143-4a3b-9698-de3904c772c0'}}],'cancelQueries':[],'modelId':100530}
    req=urllib.request.Request(API,data=json.dumps(body).encode(),headers={'Content-Type':'application/json','X-PowerBI-ResourceKey':KEY,'ActivityId':str(uuid.uuid4()),'RequestId':str(uuid.uuid4())})
    raw=urllib.request.urlopen(req,timeout=90).read()
    slug=re.sub(r'[^a-z0-9]+','-',entity['Name'].lower()).strip('-')
    (ROOT/f'research/tra-{slug}-raw.json').write_bytes(raw)
    return props,json.loads(raw),slug

def decode(props,d):
    ds=d['results'][0]['result']['data']['dsr']['DS'][0]
    rows=ds['PH'][0]['DM0']; dictionaries=ds.get('ValueDicts',{})
    schema=rows[0]['S']; previous=[None]*len(schema); output=[]
    for row in rows:
        cells=iter(row.get('C',[])); current=[]
        for i,col in enumerate(schema):
            if row.get('R',0)&(1<<i): value=previous[i]
            elif row.get('Ø',0)&(1<<i): value=None
            else: value=next(cells)
            current.append(value)
        decoded=[dictionaries[c['DN']][v] if 'DN' in c and isinstance(v,int) else float(v) if c['T']==3 and isinstance(v,str) else v for c,v in zip(schema,current)]
        output.append(dict(zip(props,decoded)));previous=current
    assert len(output)<30000,'Result may be truncated'
    return output

if __name__=='__main__':
    from concurrent.futures import ThreadPoolExecutor
    names=['Summary Dashboard','State summary','cap city regional','International markets','International BE Actitivies','Spend items','Days at convention/conference/trade fair/exhibition/seminar','Per person night spend','Venue','Type of traveller']
    entities=[e for e in SCHEMA if e['Name'] in names]
    def process(e):
        props,d,slug=fetch(e);rows=decode(props,d)
        (ROOT/f'research/tra-{slug}.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
        return e['Name'],len(rows),rows[:1]
    with ThreadPoolExecutor(max_workers=4) as pool:
        for result in pool.map(process,entities): print(result)
