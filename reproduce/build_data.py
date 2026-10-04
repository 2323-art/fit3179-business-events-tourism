"""Rebuild derived display data from preserved official source tables."""
import json, csv, math, hashlib
from pathlib import Path
from collections import defaultdict
import openpyxl

ROOT=Path(__file__).resolve().parents[1]; R=ROOT/'data'/'source'; D=ROOT/'data'
D.mkdir(parents=True,exist_ok=True)
import urllib.request
for filename,remote in [('world-original.geojson','ne_110m_admin_0_countries.geojson'),('states-original.geojson','ne_50m_admin_1_states_provinces.geojson'),('places-original.geojson','ne_110m_populated_places.geojson')]:
 if not (R/filename).exists(): urllib.request.urlretrieve('https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/'+remote,R/filename)
def read(n): return json.loads((R/(n+'.json')).read_text(encoding='utf-8'))
def save(n,v): (D/(n+'.json')).write_text(json.dumps(v,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
def table(n,v):
 save(n,v)
 if v:
  with (D/(n+'.csv')).open('w',newline='',encoding='utf-8-sig') as f:
   w=csv.DictWriter(f,fieldnames=list(v[0]));w.writeheader();w.writerows(v)

union='Attended or accompanied someone else to business event total'
summary=[r for r in read('tra-summary-dashboard') if r['Category']==union]
types={'Daytrips':'Domestic day','Overnight':'Domestic overnight','International':'International'}
national=[]
for r in summary:
 if r['Type'] not in types:continue
 national.append(dict(year=r['Year'],traveller=types[r['Type']],visitors=r['Visitors'],nights=r['Visitor nights'],spend=r['Spend in Australia ($000)']*1000,total_spend=r['Total trip spend ($000)']*1000,spend_per_trip=r['Spend in Australia ($000)']*1000/r['Visitors']))
for year in [2024,2025]:
 total=next(r for r in summary if r['Year']==year and r['Type']=='Combined')
 for field,source in [('visitors','Visitors'),('spend','Spend in Australia ($000)'),('total_spend','Total trip spend ($000)')]:
  assert sum(r[field] for r in national if r['year']==year)==total[source]*(1000 if 'spend' in field else 1)
table('national',national)
latest=[r for r in national if r['year']==2025]
waffle=[]
for metric,key in [('Visitor trips','visitors'),('Spending in Australia','spend')]:
 total=sum(r[key] for r in latest); shares=[r[key]/total*100 for r in latest]
 counts=[math.floor(s) for s in shares]
 for i in sorted(range(3),key=lambda i:shares[i]-counts[i],reverse=True)[:100-sum(counts)]:counts[i]+=1
 index=0
 for r,pct,count in zip(latest,shares,counts):
  for _ in range(count):
   waffle.append(dict(metric=metric,traveller=r['traveller'],share=pct/100,x=index%10,y=9-index//10));index+=1
 assert index==100
table('waffle',waffle)

# Continuous ribbons have conserved dollar thickness at both ends.
scale=1e9; gap=.55; flows=[]; nodes=[]; source_y=0; dest_y={'In Australia':0,'Outside Australia':18.3}
for r in sorted(latest,key=lambda r:['Domestic day','Domestic overnight','International'].index(r['traveller'])):
 height=r['total_spend']/scale
 nodes.append(dict(label=r['traveller'],x=0,y=source_y,y2=source_y+height,value=r['total_spend']))
 local_offset=0
 for destination,value in [('In Australia',r['spend']),('Outside Australia',r['total_spend']-r['spend'])]:
  if value==0:continue
  h=value/scale;y0=source_y+local_offset;y1=dest_y[destination]
  for step in range(31):
   t=step/30;smooth=t*t*(3-2*t)
   flows.append(dict(link=r['traveller']+' → '+destination,traveller=r['traveller'],destination=destination,value=value,x=t,y=y0+(y1-y0)*smooth,y2=y0+(y1-y0)*smooth+h))
  local_offset+=h;dest_y[destination]+=h
 source_y+=height+gap
for dest,start in [('In Australia',0),('Outside Australia',18.3)]:nodes.append(dict(label=dest,x=1,y=start,y2=dest_y[dest],value=(dest_y[dest]-start)*scale))
table('flows',flows);table('flow-nodes',nodes)

abbr={'New South Wales':'NSW','Victoria':'VIC','Queensland':'QLD','South Australia':'SA','Western Australia':'WA','Tasmania':'TAS','Northern Territory':'NT','ACT':'ACT','Australian Capital Territory':'ACT'}
popcols=dict(zip(['NSW','VIC','QLD','SA','WA','TAS','NT','ACT'],range(20,28)))
wb=openpyxl.load_workbook(R/'abs-population-mar-2026.xlsx',read_only=True,data_only=True);ws=wb['Data1']
population={k:ws.cell(187,col).value for k,col in popcols.items()}
assert str(ws.cell(187,1).value).startswith('2025-06')
states=[]
geometry=json.loads((R/'states-original.geojson').read_text(encoding='utf-8'))
features=[]
def round_coords(v):return [round_coords(i) for i in v] if isinstance(v,list) else round(v,3) if isinstance(v,float) else v
for feature in geometry['features']:
 p=feature['properties'];name=p.get('name')
 if p.get('adm0_a3')!='AUS' or name not in abbr:continue
 code=abbr[name]
 candidates=[r for r in read('tra-state-summary') if r['Year']==2025 and r['Type']=='Total' and r['Category']=='Total' and abbr.get(r['State/Territory'])==code]
 assert len(candidates)==1,(name,candidates)
 r=candidates[0];assert r['Sample In/Out']==1
 item=dict(state=name,code=code,visitors=r['Visitors (000)']*1000,spend=r['Expenditure ($M)']*1e6,nights=r['Nights (000)']*1000,population=population[code],spend_per_resident=r['Expenditure ($M)']*1e6/population[code],longitude=p['longitude'],latitude=p['latitude'])
 # ACT is too small to find without a clearly labelled callout.
 item['label_lon']=153 if code=='ACT' else p['longitude'];item['label_lat']=-36.7 if code=='ACT' else p['latitude']
 states.append(item);features.append(dict(type='Feature',properties=item,geometry=dict(type=feature['geometry']['type'],coordinates=round_coords(feature['geometry']['coordinates']))))
assert len(states)==8
table('states',states);save('australia',dict(type='FeatureCollection',features=features))

regions=[dict(id='Australia',parent=None,name='Australia',value=0)]
for code in popcols:regions.append(dict(id=code,parent='Australia',name=code,value=0))
for r in read('tra-cap-city-regional'):
 if r['Year']!=2025 or r['Region ID'] not in [1,2] or r['Sample In/Out']!=1:continue
 code=abbr.get(r['State/Territory'])
 if not code:continue
 regions.append(dict(id=r['Region'],parent=code,name=r['Region'].replace('Canberra - Regional ACT','ACT (all)').replace(' and the South',' & south').replace('Destination Perth','Perth region'),value=r['Expenditure ($M)']*1e6))
table('regions',regions)

markets={}
metric_names={'Visitors (000)':'visitors','Visitor nights (000)':'nights','Spend in Australia ($000)':'spend','Total trip spend ($000)':'total_spend'}
for r in read('tra-international-markets'):
 country={'United States of America':'USA','United Kingdom':'UK'}.get(r['Country of origin'],r['Country of origin'])
 key=(country,r['Year']);markets.setdefault(key,dict(country=key[0],year=key[1]))
 markets[key][metric_names[r['Attribute']]]=r['Value']*1000
market=list(markets.values());assert len(market)==36
table('markets',market)
changes=[]
for country in sorted(set(r['country'] for r in market)):
 before=markets[(country,2024)];after=markets[(country,2025)]
 for key,label in [('visitors','Visitors'),('nights','Nights'),('spend','Spend')]:
  changes.append(dict(country=country,metric=label,change=after[key]/before[key]-1,before=before[key],after=after[key]))
table('changes',changes)
before=next(r for r in national if r['year']==2024 and r['traveller']=='International')['spend']
after=next(r for r in national if r['year']==2025 and r['traveller']=='International')['spend']
drivers=sorted([(c,markets[c,2025]['spend']-markets[c,2024]['spend']) for c in set(r['country'] for r in market)],key=lambda x:abs(x[1]),reverse=True)[:6]
drivers=sorted(drivers,key=lambda x:-x[1]);drivers.append(('Other + rounding',after-before-sum(v for c,v in drivers)))
waterfall=[dict(label='2024',start=0,end=before/1e9,value=before/1e9,kind='Total',order=0)];running=before/1e9
for i,(country,delta) in enumerate(drivers,1):
 waterfall.append(dict(label=country,start=running,end=running+delta/1e9,value=delta/1e9,kind='Increase' if delta>=0 else 'Decrease',order=i));running+=delta/1e9
waterfall.append(dict(label='2025',start=0,end=after/1e9,value=after/1e9,kind='Total',order=len(waterfall)))
assert abs(running-after/1e9)<1e-8
table('waterfall',waterfall)
activities=[]
for r in read('tra-international-be-actitivies'):
 if r['Activity'] in ['Dine out','Go shopping','Sightseeing','Go to the beach','National parks / state parks']:
  activities.append(dict(activity=r['Activity'].replace('National parks / state parks','National/state parks'),year=r['Year'],share=r['Percentage_attend']))
assert len(activities)==10
table('activities',activities)
night=[]
for r in read('tra-per-person-night-spend'):
 night.append(dict(year=str(r['Year']),other=r['Did not attend or accompany anyone to a business event'],business=r[union]))
table('per-night',night)

world=json.loads((R/'world-original.geojson').read_text(encoding='utf-8'))
save('world',dict(type='FeatureCollection',features=[dict(type='Feature',properties={'name':f['properties']['ADMIN']},geometry=dict(type=f['geometry']['type'],coordinates=round_coords(f['geometry']['coordinates']))) for f in world['features'] if f['properties']['ADMIN']!='Antarctica']))
places=json.loads((R/'places-original.geojson').read_text(encoding='utf-8'))
def location(prefix):
 found=[f for f in places['features'] if f['properties'].get('NAME','').startswith(prefix)]
 assert len(found)==1,(prefix,len(found))
 return found[0]['geometry']['coordinates']
capital={'New Zealand':'Wellington','China':'Beijing','USA':'Washington','Singapore':'Singapore','UK':'London','India':'New Delhi','Japan':'Tokyo','Malaysia':'Kuala Lumpur'}
dest=location('Canberra');origins=[];links=[]
def great_circle(a,b):
 def vec(p):
  lon,lat=map(math.radians,p);return [math.cos(lat)*math.cos(lon),math.cos(lat)*math.sin(lon),math.sin(lat)]
 va,vb=vec(a),vec(b);omega=math.acos(sum(x*y for x,y in zip(va,vb)));out=[]
 for i in range(61):
  t=i/60;v=[(math.sin((1-t)*omega)*x+math.sin(t*omega)*y)/math.sin(omega) for x,y in zip(va,vb)]
  out.append([round(math.degrees(math.atan2(v[1],v[0])),3),round(math.degrees(math.atan2(v[2],math.hypot(v[0],v[1]))),3)])
 return out
for r in sorted([r for r in market if r['year']==2025],key=lambda r:-r['visitors'])[:8]:
 coord=location(capital[r['country']]);origins.append(dict(country=r['country'],visitors=r['visitors'],longitude=coord[0],latitude=coord[1]))
 links.append(dict(type='Feature',properties={'country':r['country'],'visitors':r['visitors']},geometry={'type':'LineString','coordinates':great_circle(coord,dest)}))
save('routes',dict(type='FeatureCollection',features=links));table('origins',origins)

sources=[dict(id='TRA',title='Tourism Research Australia: Business events data',url='https://www.tra.gov.au/en/tourism-statistics/business-events-data',reference='Calendar years 2024 and 2025; public report refreshed 21 May 2026',retrieved='2026-10-05',licence='Commonwealth of Australia, CC BY 4.0',transform='Selected union totals; monetary source units converted to AUD; domestic comparisons excluded across 2025 method break.'),dict(id='ABS',title='ABS National, state and territory population, March 2026',url='https://www.abs.gov.au/statistics/people/population/national-state-and-territory-population/mar-2026',reference='June 2025 population from Table 4, Data1 row 187 columns T:AA',retrieved='2026-10-05',licence='Commonwealth of Australia, CC BY 4.0',transform='Joined eight jurisdictions to TRA spending; spending divided by residents.'),dict(id='NE',title='Natural Earth vector map data',url='https://www.naturalearthdata.com/',reference='1:110m countries and populated places; 1:50m Australian states',retrieved='2026-10-05',licence='Public domain',transform='Selected features; coordinates rounded to three decimals; representative capitals used for schematic flows.')]
save('provenance',sources)
checks=dict(national_reconciled=True,states_joined=len(states),market_rows=len(market),waffle_cells=len(waffle),waterfall_reconciled=True,data_bytes=sum(p.stat().st_size for p in D.glob('*')),excluded=['Spending items: inconsistent aggregate with headline','Days at events: anomalous row and incompatible bins'],caveats=['State visits count a multi-state trip more than once.','Survey estimates and published rounding; no claim of statistical significance.','Amounts are nominal AUD, not inflation adjusted.','2024/2025 domestic data are not directly comparable.'])
(ROOT/'data-checks.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
print(json.dumps(checks,indent=2))
