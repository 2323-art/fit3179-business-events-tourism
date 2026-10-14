import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'specs';OUT.mkdir(exist_ok=True)
BLUE='#2457D6';TEAL='#007F78';GOLD='#B47716';INK='#162B4D'
types=['Domestic day','Domestic overnight','International'];colors=[GOLD,TEAL,BLUE]
config={'font':'IBM Plex Sans','view':{'stroke':None},'axis':{'labelFontSize':12,'titleFontSize':12,'titleFontWeight':'normal','gridColor':'#DFE6EE','domain':False,'tickColor':'#B3C2D3','labelColor':INK,'titleColor':INK,'titlePadding':12,'labelLimit':150},'legend':{'labelFontSize':12,'titleFontSize':12,'orient':'bottom','title':None},'title':{'fontSize':14,'anchor':'start','color':INK}}
def save(n,s,vega=False):
 s={'$schema':'https://vega.github.io/schema/vega/v5.json' if vega else 'https://vega.github.io/schema/vega-lite/v5.json',**s}
 if not vega:s={'width':'container','height':300,'config':config,**s}
 (OUT/(n+'.json')).write_text(json.dumps(s,indent=2,ensure_ascii=False),encoding='utf-8')
def data(n,geo=False):return {'url':'data/'+n+'.json',**({'format':{'type':'json','property':'features'}} if geo else {})}
def f(field,t='Q',**kw):return {'field':field,'type':{'Q':'quantitative','N':'nominal','O':'ordinal','T':'temporal'}[t],**kw}
def typcol():return f('traveller','N',scale={'domain':types,'range':colors})
def tip(field,title=None,fmt=None,t='Q'):return f(field,t,**({'title':title} if title else {}),**({'format':fmt} if fmt else {}))
panels=[]
for metric in ['Visitor trips','Spending in Australia']:
 panels.append({'width':180,'height':180,'title':metric,'data':data('waffle'),'transform':[{'filter':f'datum.metric === "{metric}"'}],'mark':{'type':'rect','cornerRadius':2,'stroke':'white','strokeWidth':2},'encoding':{'x':f('x','O',axis=None),'y':f('y','O',axis=None),'color':typcol(),'tooltip':[tip('traveller','Traveller',t='N'),tip('share','Exact share','.1%')]}})
save('01-waffle',{'hconcat':panels,'spacing':28,'resolve':{'scale':{'color':'shared'}},'height':180})
save('02-spend-per-trip',{'data':data('national'),'transform':[{'filter':'datum.year == 2025'}],'height':220,'layer':[{'mark':{'type':'bar','cornerRadiusEnd':3},'encoding':{'x':f('spend_per_trip',title='AUD spent in Australia per visitor trip',axis={'format':'$,.0f'},scale={'domain':[0,3800]}),'y':f('traveller','N',sort=['International','Domestic overnight','Domestic day'],title=None),'color':{**typcol(),'legend':None},'tooltip':[tip('traveller',t='N'),tip('spend_per_trip','AUD per trip','$,.0f')]}},{'mark':{'type':'text','align':'left','dx':7,'fontSize':13,'color':INK},'encoding':{'x':f('spend_per_trip'),'y':f('traveller','N',sort=['International','Domestic overnight','Domestic day']),'text':f('spend_per_trip',format='$,.0f')}}]})
save('03-sankey',{'height':300,'layer':[{'data':data('flows'),'mark':{'type':'area','opacity':.8},'encoding':{'x':f('x',axis=None,scale={'domain':[-.03,1.03]}),'y':f('y',axis=None,scale={'domain':[21,0]}),'y2':{'field':'y2'},'detail':f('link','N'),'color':{**typcol(),'legend':None},'tooltip':[tip('link','Flow',t='N'),tip('value','AUD','$,.0f')]}},{'data':data('flow-nodes'),'mark':{'type':'rule','strokeWidth':7,'color':INK},'encoding':{'x':f('x'),'y':f('y'),'y2':{'field':'y2'}}},{'data':data('flow-nodes'),'transform':[{'filter':'datum.x == 1'},{'calculate':'(datum.y + datum.y2)/2','as':'mid'}],'mark':{'type':'text','align':'right','dx':-10,'color':'white','stroke':INK,'strokeWidth':.2,'fontWeight':'bold','fontSize':12},'encoding':{'x':f('x'),'y':f('mid'),'text':f('label','N')}}]})
projection={'type':'conicEqualArea','parallels':[-18,-36],'rotate':[-134,0,0],'center':[0,-28]}
base={'data':data('australia',True),'mark':{'type':'geoshape','stroke':'white','strokeWidth':1},'encoding':{'tooltip':[tip('properties.state','State',t='N'),tip('properties.spend_per_resident','AUD per resident','$,.0f'),tip('properties.spend','Spending (AUD)','$,.0f'),tip('properties.population','Residents',',.0f')]}}
save('04-choropleth',{'height':380,'projection':projection,'layer':[{**base,'encoding':{**base['encoding'],'color':f('properties.spend_per_resident',scale={'domain':[0,1600],'range':['#EDF4FA','#193D91']},legend={'title':'AUD per resident','format':'$,.0f','gradientLength':220})}},{'data':data('states'),'mark':{'type':'text','fontWeight':'bold','fontSize':12,'color':INK,'stroke':'white','strokeWidth':2},'encoding':{'longitude':f('label_lon'),'latitude':f('label_lat'),'text':f('code','N')}},{'data':{'values':[{'longitude':148.983,'latitude':-35.4618,'lon2':153,'lat2':-36.7}]},'mark':{'type':'rule','color':INK},'encoding':{'longitude':f('longitude'),'latitude':f('latitude'),'longitude2':{'field':'lon2'},'latitude2':{'field':'lat2'}}}]})
save('05-symbol-map',{'height':380,'projection':projection,'layer':[{'data':data('australia',True),'mark':{'type':'geoshape','fill':'#EDF1F5','stroke':'white'}},{'data':data('states'),'mark':{'type':'circle','fill':BLUE,'fillOpacity':.55,'stroke':BLUE,'strokeWidth':1.5},'encoding':{'longitude':f('longitude'),'latitude':f('latitude'),'size':f('visitors',scale={'domain':[0,7500000],'range':[0,4400]},legend={'title':'State visits','format':'.1s','values':[1000000,4000000,7000000]}),'tooltip':[tip('state',t='N'),tip('visitors','State visits',',.0f')]}},{'data':data('states'),'mark':{'type':'text','dy':-3,'fontWeight':'bold','color':INK,'stroke':'white','strokeWidth':2},'encoding':{'longitude':f('label_lon'),'latitude':f('label_lat'),'text':f('code','N')}}]})
save('06-treemap',{'width':1000,'height':380,'padding':0,'autosize':'none','data':[{'name':'tree','url':'data/regions.json','transform':[{'type':'stratify','key':'id','parentKey':'parent'},{'type':'treemap','field':'value','sort':{'field':'value','order':'descending'},'method':'squarify','size':[{'signal':'width'},{'signal':'height'}],'paddingInner':3,'paddingOuter':3,'paddingTop':22}]},{'name':'leaves','source':'tree','transform':[{'type':'filter','expr':'!datum.children'}]},{'name':'parents','source':'tree','transform':[{'type':'filter','expr':'datum.depth == 1'}]}],'scales':[{'name':'color','type':'ordinal','domain':['NSW','VIC','QLD','WA','SA','ACT','NT','TAS'],'range':['#2457D6','#007F78','#426BA0','#4F6D58','#A06C20','#805C89','#377E8C','#6A779C']}],'marks':[{'type':'rect','from':{'data':'leaves'},'encode':{'enter':{'x':{'field':'x0'},'y':{'field':'y0'},'x2':{'field':'x1'},'y2':{'field':'y1'},'fill':{'scale':'color','field':'parent'},'tooltip':{'signal':"{'Region':datum.name, 'Spending (AUD)':format(datum.value,'$,.0f')}"}},'update':{'fillOpacity':{'value':1}},'hover':{'fillOpacity':{'value':.7}}}},{'type':'text','from':{'data':'leaves'},'encode':{'update':{'x':{'signal':'datum.x0+7'},'y':{'signal':'datum.y0+16'},'text':{'field':'name'},'limit':{'signal':'max(0, datum.x1-datum.x0-14)'},'opacity':{'signal':'datum.y1-datum.y0>27 && datum.x1-datum.x0>55 ? 1:0'},'font':{'value':'IBM Plex Sans'},'fontSize':{'value':12},'fill':{'value':'white'}}}},{'type':'text','from':{'data':'leaves'},'encode':{'update':{'x':{'signal':'datum.x0+7'},'y':{'signal':'datum.y0+33'},'text':{'signal':"format(datum.value/1e9,'$.2f')+'b'"},'opacity':{'signal':'datum.y1-datum.y0>45 && datum.x1-datum.x0>75 ? 1:0'},'font':{'value':'IBM Plex Sans'},'fontSize':{'value':12},'fill':{'value':'white'}}}},{'type':'text','from':{'data':'parents'},'encode':{'update':{'x':{'signal':'datum.x0+5'},'y':{'signal':'datum.y0+16'},'text':{'field':'name'},'font':{'value':'IBM Plex Sans'},'fontWeight':{'value':'bold'},'fill':{'value':INK}}}}]},True)
save('07-flow-map',{'height':440,'projection':{'type':'equalEarth','rotate':[-150,0,0]},'layer':[{'data':data('world',True),'mark':{'type':'geoshape','fill':'#E8EFF5','stroke':'white','strokeWidth':.5}},{'data':data('routes',True),'mark':{'type':'geoshape','filled':False,'strokeOpacity':.6},'encoding':{'strokeWidth':f('properties.visitors',scale={'domain':[0,165000],'range':[0,12]},legend={'title':'Visitor trips','values':[50000,100000,150000],'format':'.0s'}),'stroke':{'condition':{'test':"datum.properties.country == 'Malaysia'",'value':TEAL},'value':BLUE},'tooltip':[tip('properties.country','Origin',t='N'),tip('properties.visitors','Visitor trips',',.0f')]}},{'data':data('origins'),'mark':{'type':'circle','size':50,'color':INK},'encoding':{'longitude':f('longitude'),'latitude':f('latitude'),'tooltip':[tip('country','Origin',t='N'),tip('visitors','Visitor trips',',.0f')]}},{'data':{'values':[{'longitude':149.129,'latitude':-35.283,'label':'Australia'},{'longitude':101.689,'latitude':3.14,'label':'Malaysia'}]},'mark':{'type':'text','dy':18,'fontWeight':'bold','color':INK},'encoding':{'longitude':f('longitude'),'latitude':f('latitude'),'text':f('label','N')}}]})
save('08-market-scatter',{'data':data('markets'),'params':[{'name':'year','value':2025,'bind':{'input':'select','options':[2024,2025],'name':'Year: '}},{'name':'focus','value':'All markets','bind':{'input':'select','options':['All markets','Malaysia','China','New Zealand','Singapore','USA','UK'],'name':'Highlight: '}}],'transform':[{'filter':'datum.year == year'}],'height':360,'layer':[{'mark':{'type':'circle','size':110,'stroke':'white','strokeWidth':1},'encoding':{'x':f('visitors',title='Visitor trips',axis={'format':'~s'},scale={'domain':[0,185000]}),'y':f('spend',title='Spending in Australia (AUD)',axis={'format':'$~s'},scale={'domain':[0,400000000]}),'color':{'condition':{'test':"datum.country == 'Malaysia'",'value':TEAL},'value':BLUE},'opacity':{'condition':{'test':"focus == 'All markets' || datum.country == focus",'value':.85},'value':.12},'tooltip':[tip('country','Origin',t='N'),tip('visitors','Visitor trips',',.0f'),tip('spend','Spending (AUD)','$,.0f')]}},{'transform':[{'filter':"datum.country == 'Malaysia' || datum.visitors > 70000 || datum.country == focus"}],'mark':{'type':'text','dx':6,'dy':-9,'align':'left','fontSize':11,'color':INK},'encoding':{'x':f('visitors'),'y':f('spend'),'text':f('country','N')}}]})
save('09-change-heatmap',{'data':data('changes'),'height':420,'encoding':{'x':f('metric','O',sort=['Visitors','Nights','Spend'],title=None,axis={'orient':'top','labelAngle':0}),'y':f('country','N',sort={'field':'change','op':'mean','order':'descending'},title=None)},'layer':[{'mark':{'type':'rect','stroke':'white','strokeWidth':2},'encoding':{'color':f('change',scale={'domain':[-.65,0,.65],'range':['#915114','#FFFFFF','#2457D6'],'clamp':True},legend={'title':'Change, 2024 → 2025','format':'+.0%','gradientLength':190}),'tooltip':[tip('country',t='N'),tip('metric',t='N'),tip('change','Change','+.1%'),tip('before','2024',',.0f'),tip('after','2025',',.0f')]}},{'mark':{'type':'text','fontSize':12},'encoding':{'text':f('change',format='+.0%'),'color':{'condition':{'test':'abs(datum.change) > 0.35','value':'white'},'value':INK}}}]})
save('10-waterfall',{'data':data('waterfall'),'height':300,'encoding':{'x':f('label','O',sort={'field':'order','order':'ascending'},title=None,axis={'labelAngle':-25,'labelLimit':160})},'layer':[{'mark':{'type':'bar','size':46},'encoding':{'y':f('start',title='Spending in Australia (AUD billions)',scale={'domain':[0,2.95]}),'y2':{'field':'end'},'color':f('kind','N',scale={'domain':['Total','Increase','Decrease'],'range':[INK,BLUE,GOLD]},legend=None),'tooltip':[tip('label','Contribution',t='N'),tip('value','AUD billions','+.3f')]}},{'transform':[{'calculate':'max(datum.start,datum.end)','as':'top'},{'calculate':"datum.kind == 'Total' ? format(datum.value,'$.2f')+'b' : format(datum.value*1000,'+,.0f')+'m'",'as':'display'}],'mark':{'type':'text','dy':-8,'fontSize':12,'color':INK},'encoding':{'y':f('top'),'text':f('display','N')}}]})
save('11-activity-slope',{'data':data('activities'),'height':360,'encoding':{'x':f('year','O',title=None,axis={'labelAngle':0},scale={'padding':.25}),'y':f('share',title='Share of international event attendees',axis={'format':'.0%'},scale={'domain':[.1,1]})},'layer':[{'mark':{'type':'line','point':{'filled':True,'size':55},'strokeWidth':2},'encoding':{'detail':f('activity','N'),'color':f('activity','N',scale={'range':[BLUE,TEAL,GOLD,'#805C89','#576D84']},legend={'labelLimit':200,'columns':1}),'tooltip':[tip('activity',t='N'),tip('year',t='O'),tip('share','Participation','.1%')]}},{'mark':{'type':'text','dy':-11,'fontSize':11,'color':INK},'encoding':{'text':f('share',format='.1%'),'detail':f('activity','N')}}]})
save('12-per-night',{'data':data('per-night'),'height':240,'encoding':{'y':f('year','O',title=None),'x':f('other',title='Spending in Australia per visitor night (AUD)',scale={'domain':[0,180]},axis={'format':'$,.0f'})},'layer':[{'mark':{'type':'rule','strokeWidth':4,'color':'#B3C2D3'},'encoding':{'x2':{'field':'business'}}},{'mark':{'type':'circle','size':150,'color':'#576D84','opacity':1},'encoding':{'tooltip':[tip('other','Other international visitors','$,.0f')]}},{'mark':{'type':'circle','size':150,'color':BLUE,'opacity':1},'encoding':{'x':f('business'),'tooltip':[tip('business','Business-event visitors','$,.0f')]}},{'mark':{'type':'text','dy':-18,'color':INK},'encoding':{'text':f('other',format='$,.0f')}},{'mark':{'type':'text','dy':-18,'color':INK},'encoding':{'x':f('business'),'text':f('business',format='$,.0f')}}]})
# Refinements after inspecting the rendered figures.
for path in OUT.glob('*.json'):
 s=json.loads(path.read_text(encoding='utf-8'))
 if path.name.startswith('01-'):
  for panel in s['hconcat']:panel['encoding']['color']['legend']=None
 if path.name.startswith(('02-','08-','12-')):
  s['config']['axis']['tickCount']=5
 if path.name.startswith(('04-','05-')):
  label=s['layer'][1 if path.name.startswith('04-') else 2]
  label['mark'].pop('stroke',None);label['mark'].pop('strokeWidth',None)
  label['mark']['fontSize']=12
  if path.name.startswith('04-'):label['encoding']['color']={'condition':{'test':"datum.code == 'NT'",'value':'white'},'value':INK}
 if path.name.startswith('07-'):
  s['layer'][1]['encoding']['strokeWidth']['legend']['symbolType']='stroke'
  s['layer'][1]['encoding']['strokeWidth']['legend']['format']='~s'
 if path.name.startswith('08-'):
  s['layer'][1]['mark']['align']={'expr':"datum.country == 'New Zealand' ? 'right' : 'left'"}
  s['layer'][1]['mark']['dx']={'expr':"datum.country == 'New Zealand' ? -6 : 6"}
 if path.name.startswith('09-'):
  s['layer'][0]['encoding']['color']['scale']['interpolate']='rgb'
  s['layer'][1]['encoding']['color']['condition']['test']='abs(datum.change) > 0.48'
 if path.name.startswith('11-'):
  s['transform']=[{'filter':"datum.activity != 'Go shopping'"}]
 if path.name.startswith('03-'):
  s['layer'].append({'data':data('flow-nodes'),'transform':[{'filter':'datum.x == 0'},{'calculate':"(datum.y + datum.y2)/2 - (datum.label == 'International' ? 0.6 : 0)",'as':'mid'}],'mark':{'type':'text','align':'left','dx':10,'color':'white','fontSize':11,'fontWeight':'bold'},'encoding':{'x':f('x'),'y':f('mid'),'text':f('label','N')}})
 path.write_text(json.dumps(s,indent=2,ensure_ascii=False),encoding='utf-8')
# Strict rubric review: make the intended comparisons visible without hovering.
def revise(name, change):
 path=OUT/(name+'.json');s=json.loads(path.read_text(encoding='utf-8'));change(s)
 path.write_text(json.dumps(s,indent=2,ensure_ascii=False),encoding='utf-8')

def spending_labels(s):
 s['height']=360
 for layer in [s['layer'][2],s['layer'][3]]:
  layer['transform'].append({'calculate':"datum.label + '\\nA$' + format(datum.value / 1e9, '.2f') + 'b'",'as':'direct_label'})
  layer['mark'].update({'color':'#07101C','fontSize':12,'fontWeight':'bold','lineBreak':'\n','lineHeight':14,'baseline':'middle','dy':-7})
  layer['mark'].pop('stroke',None);layer['mark'].pop('strokeWidth',None)
  layer['encoding']['text']=f('direct_label','N')
revise('03-sankey',spending_labels)
revise('02-spend-per-trip',lambda s:s.update(height=300))

def territory_callout(s):
 s['layer'][1]['transform']=[{'calculate':"indexof(['ACT','NT','NSW'], datum.code) >= 0 ? datum.code + '\\nA$' + format(datum.spend_per_resident, ',.0f') : datum.code",'as':'map_label'}]
 s['layer'][1]['mark'].update({'lineBreak':'\n','lineHeight':14,'align':'center','dx':{'expr':"datum.code == 'ACT' ? -4 : 0"}})
 s['layer'][1]['encoding']['text']=f('map_label','N')
 # Keep the value callout in bounds without enlarging the ACT geography.
 s['layer'][1]['encoding']['longitude']={'field':'label_lon','type':'quantitative'}
 s['layer'][1]['encoding']['tooltip']=[tip('state','State',t='N'),tip('spend_per_resident','AUD per resident','$,.0f')]
revise('04-choropleth',territory_callout)

def flow_review(s):
 s['params']=[{'name':'originFocus','value':'All origins'}]
 s['layer'][1]['mark']['strokeOpacity']=1
 s['layer'][1]['encoding']['opacity']={'condition':{'test':"originFocus == 'All origins' || datum.properties.country == originFocus",'value':.8},'value':.1}
 s['layer'][1]['encoding']['strokeWidth']['legend'].update({'symbolSize':700,'symbolStrokeColor':BLUE})
 # The destination is always named. Origins receive labels and a keyboard-accessible key.
 s['layer'][3]['data']['values']=s['layer'][3]['data']['values'][:1]
 s['layer'].append({'data':data('origins'),'mark':{'type':'text','fontSize':12,'fontWeight':'bold','color':INK,'align':{'expr':"datum.country == 'UK' || datum.country == 'India' || datum.country == 'Malaysia' ? 'right' : 'left'"},'dx':{'expr':"datum.country == 'UK' || datum.country == 'India' || datum.country == 'Malaysia' ? -8 : 8"},'dy':{'expr':"datum.country == 'Singapore' ? 18 : datum.country == 'Malaysia' ? -8 : -10"}},'encoding':{'longitude':f('longitude'),'latitude':f('latitude'),'text':f('country','N'),'opacity':{'condition':{'test':"originFocus == 'All origins' || datum.country == originFocus",'value':1},'value':.25}}})
revise('07-flow-map',flow_review)

def scatter_review(s):
 markets=json.loads((OUT.parent/'data/markets.json').read_text(encoding='utf-8'))
 s['params'][1]['bind']['options']=['All markets']+sorted({r['country'] for r in markets})
 # A named selection takes precedence over the default labels in the crowded lower left.
 s['layer'][1]['transform'][0]['filter']="focus == 'All markets' ? (datum.country == 'Malaysia' || datum.visitors > 70000) : datum.country == focus"
 s['layer'][1]['encoding']['tooltip']=s['layer'][0]['encoding']['tooltip']
revise('08-market-scatter',scatter_review)

def heatmap_review(s):
 changes=json.loads((OUT.parent/'data/changes.json').read_text(encoding='utf-8'))
 s['encoding']['y']['sort']=sorted({r['country'] for r in changes},key=lambda c:-sum(r['change'] for r in changes if r['country']==c))
 s['transform']=[{'calculate':"abs(datum.change) < 0.0005 ? '0.0%' : format(datum.change, '+.1%')",'as':'change_label'}]
 s['layer'][1]['encoding']['text']=f('change_label','N')
 s['layer'].insert(1,{'transform':[{'filter':"datum.country == 'Malaysia'"}],'mark':{'type':'rect','fillOpacity':0,'stroke':TEAL,'strokeWidth':2}})
revise('09-change-heatmap',heatmap_review)

def waterfall_review(s):
 s['layer'].insert(0,{'transform':[{'window':[{'op':'lead','field':'label','as':'next_label'}],'sort':[{'field':'order'}]},{'filter':'datum.next_label != null'}],'mark':{'type':'rule','strokeDash':[3,3],'color':'#8292A7'},'encoding':{'x2':{'field':'next_label'},'y':f('end')}})
revise('10-waterfall',waterfall_review)

# Two named endpoints, direct activity labels, and redundant line patterns make
# this a readable slope graph even when category hues cannot be distinguished.
save('11-activity-slope',{'data':data('activities'),'height':320,
 'transform':[{'filter':"datum.activity != 'Go shopping'"},{'calculate':"datum.year == 2024 ? 0.06 : 0.53",'as':'position'}],
 'encoding':{'x':f('position',axis=None,scale={'domain':[0,1],'nice':False}),'y':f('share',axis=None,scale={'domain':[.12,1.08],'nice':False})},
 'layer':[
 {'mark':{'type':'line','point':{'filled':True,'size':55},'strokeWidth':2},'encoding':{'detail':f('activity','N'),'color':f('activity','N',scale={'range':[BLUE,TEAL,GOLD,'#805C89']},legend=None),'strokeDash':f('activity','N',legend=None),'tooltip':[tip('activity',t='N'),tip('year',t='O'),tip('share','Participation','.1%')]}},
 {'mark':{'type':'text','dy':-12,'fontSize':12,'color':INK},'encoding':{'text':f('share',format='.1%'),'detail':f('activity','N')}},
 {'transform':[{'filter':'datum.year == 2025'}],'mark':{'type':'text','align':'left','dx':10,'fontSize':12,'fontWeight':'bold','color':INK},'encoding':{'text':f('activity','N')}},
 {'data':{'values':[{'position':.06,'share':1.065,'year':'2024'},{'position':.53,'share':1.065,'year':'2025'}]},'mark':{'type':'text','fontSize':13,'fontWeight':'bold','color':INK},'encoding':{'text':f('year','N')}}]})
print('Wrote',len(list(OUT.glob('*.json'))),'readable chart specifications')

# Week 10: outline the selected market without replacing the heatmap's magnitude colours.
p=OUT/'09-change-heatmap.json';s=json.loads(p.read_text(encoding='utf-8'))
s['params']=[{'name':'marketFocus','value':'Malaysia'}]
s['layer'][1]['transform']=[{'filter':'datum.country == marketFocus'}]
s['layer'][1]['mark']['stroke']=INK
s['layer'][1]['mark']['strokeWidth']=3
p.write_text(json.dumps(s,indent=2,ensure_ascii=False),encoding='utf-8')

# User feedback, 13 October: full wording, selective labels and stable colour semantics.
INCREASE='#762A83';DECREASE='#C45118';NEUTRAL='#59626D'
names={'USA':'United States','UK':'United Kingdom','NSW':'New South Wales','VIC':'Victoria','QLD':'Queensland','WA':'Western Australia','SA':'South Australia','ACT':'Australian Capital Territory','NT':'Northern Territory','TAS':'Tasmania'}
def full_name(expr):
 return ' : '.join(f'{expr} == {json.dumps(k)} ? {json.dumps(v)}' for k,v in names.items())+' : '+expr
def full_region(expr):
 for short,long in names.items():expr='replace('+expr+','+json.dumps(short)+','+json.dumps(long)+')'
 return expr

def wording(node):
 if isinstance(node,dict):
  for k,v in list(node.items()):
   if k in ('title','label') and isinstance(v,str):
    node[k]=v.replace('AUD','Australian dollars').replace('Spend (','Spending (')
   elif k=='format' and isinstance(v,str) and 's' in v:node[k]=',.0f'
   else:wording(v)
 elif isinstance(node,list):
  for item in node:wording(item)

for path in OUT.glob('*.json'):
 s=json.loads(path.read_text(encoding='utf-8'));n=path.name[:2]
 wording(s)
 if n=='02':
  s['layer'][0]['encoding']['x']['title']=['Spending per visitor trip','(Australian dollars)']
  s['layer'][1]['transform']=[{'filter':"datum.traveller == 'International'"}]
 if n=='03':
  for layer in s['layer'][2:]:
   layer['transform'][-1]['calculate']="datum.label + '\\n' + format(datum.value / 1e9, '.2f') + ' billion'"
 if n=='04':
  s['layer'][0]['encoding']['color']['scale']['range']=['#F0F0F0','#343434']
  s['layer'][0]['encoding']['color']['legend']['title']=['Australian dollars','per resident']
  layer=s['layer'][1]
  layer['transform']=[{'filter':"datum.code == 'NT' || datum.code == 'ACT'"},{'calculate':"datum.code == 'NT' ? 'Northern\\nTerritory\\n$' + format(datum.spend_per_resident, ',.0f') : 'Australian\\nCapital Territory\\n$' + format(datum.spend_per_resident, ',.0f')",'as':'map_label'}]
  layer['mark'].update({'fontSize':11,'dx':{'expr':"datum.code == 'ACT' ? -30 : 0"},'dy':-10})
 if n=='05':
  s['layer'][1]['mark'].update(fill=NEUTRAL,stroke=NEUTRAL)
  s['layer'][1]['encoding']['size']['legend'].update(title=['State visits','(millions)'],labelExpr="format(datum.value / 1e6, '.0f')")
  s['layer'][2]['transform']=[{'filter':"indexof(['NSW','VIC','QLD'], datum.code)>=0"},{'calculate':"datum.code == 'NSW' ? 'New South\\nWales' : datum.code == 'QLD' ? 'Queensland' : 'Victoria'",'as':'state_label'}]
  s['layer'][2]['encoding']['text']=f('state_label','N')
  s['layer'][2]['mark'].update(fontSize=11,lineBreak='\n',lineHeight=12)
 if n=='06':
  s['scales']=[]
  s['marks'][0]['encode']['enter']['fill']={'value':NEUTRAL}
  s['marks'][0]['encode']['enter']['tooltip']={'signal':"{'Region':"+full_region('datum.name')+", 'State or territory':"+full_name('datum.parent')+", 'Spending (Australian dollars)':format(datum.value,'$,.0f')}"}
  # Region identity and enclosing group carry the hierarchy; hue adds no extra variable.
  s['data'].append({'name':'labelled','source':'leaves','transform':[{'type':'filter','expr':'datum.value >= 1.9e9'}]})
  s['marks'][1]['from']['data']='labelled'
  s['marks'][1]['encode']['update']['text']={'signal':full_region('datum.name')}
  s['marks'][3]['encode']['update'].update(text={'signal':full_name('datum.name')},limit={'signal':'max(0,datum.x1-datum.x0-10)'},opacity={'signal':'datum.x1-datum.x0 > length(('+full_name('datum.name')+'))*7 ? 1:0'},fontSize={'value':12})
  s['marks'].pop(2)
 if n=='07':
  s['layer'][1]['encoding']['stroke']={'value':BLUE}
  s['layer'][1]['encoding']['strokeWidth']['legend'].update(title='Visitor trips',format=',.0f')
  s['layer'][4]['transform']=[{'filter':"originFocus == 'All origins' ? (datum.country == 'Malaysia' || datum.country == 'New Zealand') : datum.country == originFocus"},{'calculate':full_name('datum.country'),'as':'country_name'}]
  s['layer'][4]['encoding']['text']=f('country_name','N')
 if n=='08':
  s['params'][1]['bind']['labels']=[names.get(v,v) for v in s['params'][1]['bind']['options']]
  s['layer'][0]['encoding']['color']={'value':BLUE}
  s['layer'][0]['encoding']['y']['axis']={'labelExpr':"format(datum.value / 1e6, '.0f')",'tickCount':4}
  s['layer'][0]['encoding']['y']['title']=['Spending in Australia','(million Australian dollars)']
  s['layer'][0]['encoding']['x']['axis']={'format':',.0f','tickCount':3}
  s['layer'][1]['transform'][0]['filter']="focus == 'All markets' ? datum.country == 'Malaysia' : datum.country == focus"
  s['layer'][1]['transform'].append({'calculate':full_name('datum.country'),'as':'country_name'})
  s['layer'][1]['encoding']['text']=f('country_name','N')
 if n=='09':
  s['encoding']['y']['axis']={'labelExpr':full_name('datum.label'),'labelLimit':160}
  s['layer'][0]['encoding']['color']['scale']['range']=[DECREASE,'#FFFFFF',INCREASE]
  s['layer'][2]['transform']=[{'filter':'datum.country == marketFocus'}]
  s['layer'][2]['encoding']['color']['condition']['test']='abs(datum.change) > 0.45'
 if n=='10':
  s['encoding']['x']['axis'].update(labelExpr=full_name("datum.label == 'Other + rounding' ? 'Other markets and rounding' : datum.label"),labelLimit=200)
  s['layer'][1]['encoding']['color']['scale']['range']=[NEUTRAL,INCREASE,DECREASE]
  s['layer'][1]['encoding']['y']['title']=['Spending in Australia','(billion Australian dollars)']
  s['layer'][1]['transform']=[{'calculate':full_name("datum.label == 'Other + rounding' ? 'Other markets and rounding' : datum.label"),'as':'contribution_label'}]
  s['layer'][1]['encoding']['tooltip'][0]['field']='contribution_label'
  s['layer'][2]['transform'].insert(0,{'filter':"datum.kind == 'Total' || datum.label == 'China'"})
  s['layer'][2]['transform'][1]['calculate']="max(datum.start,datum.end) + (datum.kind == 'Total' ? 0.18 : 0)"
  s['layer'][2]['transform'][-1]['calculate']="datum.kind == 'Total' ? format(datum.value,'.2f')+' billion' : format(datum.value*1000,'+,.0f')+' million'"
  s['layer'][2]['mark']['align']={'expr':"datum.label == '2025' ? 'right' : datum.label == '2024' ? 'left' : 'center'"}
 if n=='11':
  s['layer'][0]['encoding']['color']={'value':NEUTRAL}
  s['layer'][0]['transform']=[{'calculate':"datum.activity == 'National/state parks' ? 'National and state parks' : datum.activity",'as':'activity_full'}]
  s['layer'][0]['encoding']['tooltip'][0]['field']='activity_full'
  s['layer'][1]['transform']=[{'filter':"datum.activity == 'Sightseeing'"}]
  s['layer'][2]['transform'].append({'calculate':"datum.activity == 'National/state parks' ? 'National and\\nstate parks' : datum.activity",'as':'activity_label'})
  s['layer'][2]['encoding']['text']=f('activity_label','N')
  s['layer'][2]['mark'].update(lineBreak='\n',lineHeight=14)
 if n=='12':
  s['encoding']['x']['title']=['Spending per visitor night','(Australian dollars)']
  s['layer'][1]['mark']['color']=NEUTRAL
  for layer in s['layer'][3:]:layer['transform']=[{'filter':'datum.year == 2025'}]
 # Expand country names in tooltips without changing source keys or interactive signals.
 def country_tips(node):
  if isinstance(node,dict):
   enc=node.get('encoding',{})
   for t in enc.get('tooltip',[]) if isinstance(enc.get('tooltip'),list) else []:
    if t.get('field') in ('country','properties.country'):
     raw=t['field'];field='country_full';node.setdefault('transform',[]).append({'calculate':full_name('datum.'+raw),'as':field});t['field']=field
   for v in list(node.values()):country_tips(v)
  elif isinstance(node,list):
   for v in node:country_tips(v)
 country_tips(s)
 path.write_text(json.dumps(s,indent=2,ensure_ascii=False),encoding='utf-8')

# Typography course notes: the 11–12 point screen recommendation is applied
# as a 15 pixel minimum, with 16 pixel chart titles and explanatory annotations.
def readable_type(node):
 if isinstance(node,dict):
  for key,value in list(node.items()):
   if key.endswith('FontSize') or key=='fontSize':
    if isinstance(value,(int,float)):node[key]=max(15,value)
    elif isinstance(value,dict) and isinstance(value.get('value'),(int,float)):value['value']=max(15,value['value'])
   elif key=='lineHeight' and isinstance(value,(int,float)):node[key]=max(18,value)
   else:readable_type(value)
 elif isinstance(node,list):
  for value in node:readable_type(value)
for path in OUT.glob('*.json'):
 s=json.loads(path.read_text(encoding='utf-8'));readable_type(s);n=path.name[:2]
 if n!='06':
  s['config']['text']={'fontSize':16,'lineHeight':20,'color':INK}
  s['config']['axis'].update(labelFontSize=15,titleFontSize=15,labelColor='#4E6078',labelPadding=7,titlePadding=14,labelOverlap=True)
  s['config']['legend'].update(labelFontSize=15,titleFontSize=15,labelLimit=240)
  s['config']['title'].update(fontSize=16,lineHeight=20)
 if n=='01':s['hconcat'][1]['title']=['Spending in','Australia']
 if n=='02':
  s['layer'][0]['encoding']['x']['axis']['tickCount']=3
  s['layer'][0]['encoding']['x']['title']=['Spending per trip','in Australian dollars']
  s['layer'][0]['encoding']['y']['axis']={'labelExpr':"datum.label == 'Domestic overnight' ? ['Domestic', 'overnight'] : datum.label",'labelLineHeight':18}
  s['layer'][1]['mark'].update(align='right',dx=-8,color='white',fontWeight='bold')
 if n=='03':
  s['height']=420
  for layer in s['layer'][2:]:
   layer['mark'].update(fontSize=16,lineHeight=20)
   layer['transform'][-1]['calculate']="(datum.label == 'Domestic overnight' ? 'Domestic\\novernight' : datum.label == 'Outside Australia' ? 'Overseas' : datum.label) + '\\n' + format(datum.value/1e9,'.2f') + ' billion'"
 if n=='04':
  s['layer'][1]['mark'].update(fontSize=15,lineHeight=18,dx={'expr':"datum.code == 'ACT' ? -46 : -5"},dy=-16)
  s['layer'][1]['transform'][1]['calculate']="datum.code == 'NT' ? 'Northern\\nTerritory\\n$' + format(datum.spend_per_resident, ',.0f') : 'Australian\\nCapital Territory\\n$' + format(datum.spend_per_resident, ',.0f')"
 if n=='05':s['layer'][2]['mark'].update(fontSize=15,lineHeight=18)
 if n=='06':
  s['marks'][1]['encode']['update']['y']={'signal':'datum.y0+20'}
  s['marks'][2]['encode']['update']['opacity']={'signal':'datum.x1-datum.x0 > length(('+full_name('datum.name')+'))*9 ? 1:0'}
 if n=='07':
  s['layer'][4]['mark']['align']={'expr':"datum.country == 'USA' || datum.country == 'India' || datum.country == 'Malaysia' ? 'right' : 'left'"}
  s['layer'][4]['mark']['dx']={'expr':"datum.country == 'USA' || datum.country == 'India' || datum.country == 'Malaysia' ? -8 : 8"}
 if n=='08':s['layer'][0]['encoding']['x']['axis']['tickCount']=3
 if n=='09':
  s['height']=520
  s['encoding']['y']['axis']['labelLimit']=180
  s['layer'][0]['encoding']['color']['legend'].update(gradientLength=120,title=['Change,','2024 to 2025'])
 if n=='10':s['encoding']['x']['axis']['labelOverlap']=False
 if n=='11':
  s['layer'][1]['mark']['dy']=-22
  s['layer'][2]['mark'].update(fontSize=16,lineHeight=20)
  s['layer'][2]['transform'][-1]['calculate']="datum.activity == 'National/state parks' ? 'National and\\nstate parks' : datum.activity == 'Go to the beach' ? 'Go to the\\nbeach' : datum.activity"
 path.write_text(json.dumps(s,indent=2,ensure_ascii=False),encoding='utf-8')

# Colour roles are shared with the HTML legends; no data colour has two meanings.
STATE_COLOURS={'NSW':'#443675','VIC':'#795637','QLD':'#748128','WA':'#D2BA68','SA':'#5E608B','ACT':'#386453','NT':'#9A8468','TAS':'#4F7F91'}
ACTIVITY_COLOURS={'Dine out':'#008B9C','Sightseeing':'#6E3D60','Go to the beach':'#526F24','National/state parks':'#3F667B'}
ACTIVITY_DASHES=[[],[8,4],[3,3],[10,3,2,3]]
semantics={
 'travellers':[{'key':k,'label':k,'colour':c} for k,c in zip(types,colors)],
 'states':[{'key':k,'label':names[k],'colour':c} for k,c in STATE_COLOURS.items()],
 'activities':[{'key':k,'label':'National and state parks' if k=='National/state parks' else k,'colour':c,'dash':ACTIVITY_DASHES[i]} for i,(k,c) in enumerate(ACTIVITY_COLOURS.items())],
 'change':[{'key':'Increase','label':'Increase','colour':INCREASE},{'key':'Decrease','label':'Decrease','colour':DECREASE}],
 'otherVisitors':[{'key':'Other','label':'Other international visitors','colour':NEUTRAL}],
 'quantitative':{'spendingPerResident':['#F0F0F0','#343434']},
 'note':'UI text, basemaps, borders and selection outlines are structural, not category colours.'}
(OUT.parent/'data/colour-semantics.json').write_text(json.dumps(semantics,indent=2),encoding='utf-8')
for path in OUT.glob('*.json'):
 s=json.loads(path.read_text(encoding='utf-8'));n=path.name[:2]
 if n=='02':s['layer']=s['layer'][:1] # The headline already states the key value.
 if n=='03':
  # Traveller colours move to a legend; destination labels still explain ribbon endpoints.
  s['layer']=[layer for layer in s['layer'] if not any(t.get('filter')=='datum.x == 0' for t in layer.get('transform',[]))]
 if n=='05':
  s['params']=[{'name':'stateFocus','value':'All states'}]
  layer=s['layer'][1];layer['mark'].pop('fill',None);layer['mark'].pop('stroke',None)
  layer['mark'].update(fillOpacity=1,strokeWidth=1.5)
  layer['encoding']['color']=f('code','N',scale={'domain':list(STATE_COLOURS),'range':list(STATE_COLOURS.values())},legend=None)
  layer['encoding']['opacity']={'condition':{'test':"stateFocus == 'All states' || datum.code == stateFocus",'value':1},'value':.18}
  layer['encoding']['stroke']={'value':'#FFFFFF'}
  layer['encoding']['size']['legend'].update(symbolFillColor='#FFFFFF',symbolStrokeColor=INK,symbolStrokeWidth=1.5)
  s['layer']=s['layer'][:2]
 if n=='06':
  s['signals']=[{'name':'stateFocus','value':'All states'}]
  s['scales']=[{'name':'stateColour','type':'ordinal','domain':list(STATE_COLOURS),'range':list(STATE_COLOURS.values())}]
  s['data'][0]['transform'][1].update(paddingTop=4,paddingInner=4,paddingOuter=5)
  s['marks'][0]['encode']['enter']['fill']={'scale':'stateColour','field':'parent'}
  s['marks'][0]['encode']['update']['fillOpacity']={'signal':"stateFocus == 'All states' || datum.parent == stateFocus ? 1 : .18"}
  s['marks'][0]['encode'].pop('hover',None)
  # Retain only region identities that fit; the legend replaces all state headings.
  s['data'][3]['transform']=[{'type':'filter','expr':'datum.y1-datum.y0 > 28 && datum.x1-datum.x0 > length(('+full_region('datum.name')+'))*9+16'}]
  s['marks']=s['marks'][:2]
  label=s['marks'][1]['encode']['update'];label.pop('limit',None)
  label['opacity']={'signal':"stateFocus == 'All states' || datum.parent == stateFocus ? 1 : 0"}
  label['fill']={'signal':"indexof(['QLD','WA','NT'], datum.parent) >= 0 ? '#101820' : '#FFFFFF'"}
 if n=='10':s['layer'][1]['encoding']['color']['scale']['range']=[BLUE,INCREASE,DECREASE]
 if n=='11':
  s['transform'][1]['calculate']='datum.year == 2024 ? 0.08 : 0.92'
  layer=s['layer'][0]
  layer['encoding']['color']=f('activity','N',scale={'domain':list(ACTIVITY_COLOURS),'range':list(ACTIVITY_COLOURS.values())},legend=None)
  layer['encoding']['strokeDash']=f('activity','N',scale={'domain':list(ACTIVITY_COLOURS),'range':ACTIVITY_DASHES},legend=None)
  s['layer'][3]['data']['values'][0]['position']=.08;s['layer'][3]['data']['values'][1]['position']=.92
  s['layer'].pop(2) # Activity identities are carried by the colour-and-pattern legend.
 path.write_text(json.dumps(s,indent=2,ensure_ascii=False),encoding='utf-8')
