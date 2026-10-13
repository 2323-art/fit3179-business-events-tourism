/* Local Vega/Vega-Lite specifications; viewport changes preserve control values. */
const charts=['01-waffle','02-spend-per-trip','03-sankey','04-choropleth','05-symbol-map','06-treemap','07-flow-map','08-market-scatter','09-change-heatmap','10-waterfall','11-activity-slope','12-per-night'];
window.chartViews={};window.chartFailures=[];
let marketRows=[];
let colourSemantics,regionRows=[],selectedState='All states';
const formatTrips=n=>new Intl.NumberFormat('en-AU').format(n);
const formatMoney=n=>new Intl.NumberFormat('en-AU',{maximumFractionDigits:1}).format(n/1e6)+' million Australian dollars';
const displayName=value=>typeof value==='string'?value.replace(/\b(USA|UK|NSW|VIC|QLD|WA|SA|NT|ACT|TAS)\b/g,key=>({'USA':'United States','UK':'United Kingdom','NSW':'New South Wales','VIC':'Victoria','QLD':'Queensland','WA':'Western Australia','SA':'South Australia','NT':'Northern Territory','ACT':'Australian Capital Territory','TAS':'Tasmania'}[key])).replace('National/state parks','National and state parks').replace('Other + rounding','Other markets and rounding'):value;
const formatChange=n=>new Intl.NumberFormat('en-AU',{style:'percent',maximumFractionDigits:1,signDisplay:'exceptZero'}).format(Math.abs(n)<.0005?0:n);
function updateComparison(focus){
 const country=focus==='All markets'?'Malaysia':focus;
 const before=marketRows.find(r=>r.country===country&&r.year===2024),after=marketRows.find(r=>r.country===country&&r.year===2025);
 if(!before||!after)return;
 document.getElementById('comparison-title').textContent=displayName(country)+' · 2024 and 2025';
 document.getElementById('comparison-context').textContent=focus==='All markets'?'Malaysia is the starting example. Choose a market above to compare both years here.':'Both years stay visible while you switch the scatterplot year.';
 const body=document.getElementById('comparison-rows');body.replaceChildren();
 for(const [key,label] of [['visitors','Visitor trips'],['nights','Visitor nights'],['spend','Spending (million Australian dollars)']]){
  const tr=document.createElement('tr'),th=document.createElement('th');th.scope='row';th.textContent=label;tr.append(th);
  for(const row of [before,after]){const td=document.createElement('td');td.textContent=key==='spend'?(row[key]/1e6).toLocaleString('en-AU',{minimumFractionDigits:1,maximumFractionDigits:1}):formatTrips(row[key]);tr.append(td)}body.append(tr);
 }
 document.getElementById('change-summary').textContent=`${displayName(country)}, 2024 → 2025: visitor trips ${formatChange(after.visitors/before.visitors-1)}, nights ${formatChange(after.nights/before.nights-1)} and spending ${formatChange(after.spend/before.spend-1)}. The outlined row follows the market selector; all other rows remain visible.`;
 const heatmap=window.chartViews['09-change-heatmap'];
 if(heatmap&&heatmap.signal('marketFocus')!==country)heatmap.signal('marketFocus',country).runAsync().catch(console.error);
}
function updateMarketSummary(){
 const view=window.chartViews['08-market-scatter'];if(!view||!marketRows.length)return;
 const year=Number(view.signal('year')),focus=view.signal('focus'),rows=marketRows.filter(r=>r.year===year);
 const spendLeader=rows.reduce((a,b)=>a.spend>b.spend?a:b),tripLeader=rows.reduce((a,b)=>a.visitors>b.visitors?a:b);
 const row=rows.find(r=>r.country===focus);
 document.getElementById('market-heading').textContent=year+' · '+(row?displayName(row.country)+' in focus':displayName(spendLeader.country)+' leads on spending');
 document.getElementById('market-summary').textContent=row?`${displayName(row.country)}: about ${formatTrips(row.visitors)} visitor trips and ${formatMoney(row.spend)} spent in Australia in ${year}. The faded dots retain the other markets for comparison.`:`In ${year}, ${displayName(spendLeader.country)} led spending with ${formatMoney(spendLeader.spend)}; ${displayName(tripLeader.country)} led visitor volume with about ${formatTrips(tripLeader.visitors)} trips. Choose a year or any of the 18 markets below.`;
 updateComparison(focus);
}
async function renderChart(name,index){
 const el=document.getElementById('chart'+String(index+1).padStart(2,'0'));
 el.setAttribute('aria-busy','true');
 if(!el.querySelector('svg'))el.innerHTML='<p class="chart-status" role="status">Loading chart…</p>';
 try{
  const spec=await (await fetch('specs/'+name+'.json')).json();
  const width=Math.max(230,el.clientWidth);
  if(index===1&&width<500)spec.layer[0].encoding.x.title=['Spending per trip','in Australian','dollars'];
  if(index===6&&width<500)spec.layer[1].encoding.strokeWidth.legend.columns=1;
  if(index===8&&width<500)spec.layer[2].transform=[{filter:'false'}];
  if(index===0){spec.hconcat.forEach(p=>{p.width=Math.floor((width-38)/2);p.height=p.width});delete spec.width;delete spec.height;spec.config.legend.disable=true}
  else if(index===5){spec.width=width;spec.height=width<500?460:380}
  else if(index===6){spec.height=width<500?260:440;if(width<600)spec.layer[4].transform=[{filter:"originFocus == 'All origins' ? (datum.country == 'Malaysia' || datum.country == 'New Zealand') : datum.country == originFocus"},...spec.layer[4].transform.filter(t=>!t.filter)]}
  else if(index===9&&width<500){spec.layer[1].mark.size=16;spec.layer[2].transform[0].filter="datum.kind == 'Total'";spec.layer[2].transform[1].calculate='2.85';spec.layer[2].transform[2].calculate="format(datum.value,'.2f') + '\\nbillion'";spec.layer[2].mark.lineBreak='\n';spec.layer[2].mark.lineHeight=18;spec.encoding.x.axis.labelAngle=-60;spec.height=360}
  // Give the explanatory idioms more area than their contextual comparisons.
  if(index===1)spec.height=240;
  if(index===3)spec.height=Math.min(400,width*.98);
  if(index===4)spec.height=Math.min(280,width*.78);
  if(index===10)spec.height=360;
  if(index===11)spec.height=200;
  const result=await vegaEmbed(el,spec,{actions:false,renderer:'svg',tooltip:{theme:'light'},loader:vega.loader({baseURL:document.baseURI})});
  window.chartViews[name]=result.view;
  if(index===4||index===5)await result.view.signal('stateFocus',selectedState).runAsync();
  if(index===7){result.view.addSignalListener('year',updateMarketSummary);result.view.addSignalListener('focus',updateMarketSummary);updateMarketSummary()}
 }catch(error){window.chartFailures.push({name,message:error.message});el.innerHTML='<p class="chart-error">This chart could not load. Please use its data table or downloadable data below.</p>';console.error(name,error)}
 finally{el.setAttribute('aria-busy','false')}
}
async function showTable(name){
 let rows=await (await fetch('data/'+name+'.json')).json();
 if(name==='national')rows=rows.filter(r=>r.year===2025);
 if(name==='regions')rows=rows.filter(r=>r.value>0).map(r=>({region:r.name,state:r.parent,spend:r.value}));
 const labels={spend:'Spending in Australia (Australian dollars)',total_spend:'Total trip spending (Australian dollars)',spend_per_trip:'Spending per trip (Australian dollars)',population:'Residents (June 2025)',spend_per_resident:'Australian dollars per resident',visitors:name==='states'?'State visits':'Visitor trips',share:'Participation',change:'Change (%)',other:'Other visitors (Australian dollars per night)',business:'Business-event visitors (Australian dollars per night)',value:'Change / total (Australian dollars billions)',start:'Start (Australian dollars billions)',end:'End (Australian dollars billions)',nights:'Visitor nights'};
 const hidden=new Set(['longitude','latitude','label_lon','label_lat','order']);
 const table=document.createElement('table');const head=document.createElement('thead'),body=document.createElement('tbody');
 const keys=Object.keys(rows[0]||{}).filter(k=>!hidden.has(k));const hr=document.createElement('tr');keys.forEach(key=>{const th=document.createElement('th');th.textContent=labels[key]||key.replaceAll('_',' ');th.scope='col';hr.append(th)});head.append(hr);
 rows.forEach(row=>{const tr=document.createElement('tr');keys.forEach(key=>{const td=document.createElement('td');td.textContent=row[key]===null?'Not available':typeof row[key]==='number'?new Intl.NumberFormat('en-AU',{maximumFractionDigits:['share','change'].includes(key)?1:4,...(['share','change'].includes(key)?{style:'percent'}:{})}).format(row[key]):displayName(row[key]);tr.append(td)});body.append(tr)});table.append(head,body);
 document.getElementById('data-note').textContent=(name==='national'?'2025 snapshot only. The downloadable source also contains 2024 domestic estimates, which cannot be compared directly because the survey changed. ':name==='activities'?'Includes all five supplied activities; the chart selects four to keep the comparison readable. ':name==='regions'?'Destination regions only; parent groups are not added again. ':'')+'Use the downloadable data link for the full reusable dataset. All monetary values are nominal Australian dollars.';
 document.getElementById('table-wrap').replaceChildren(table);document.getElementById('data-title').textContent=name.replaceAll('-',' ')+' · chart data';document.getElementById('data-dialog').showModal();
}
document.querySelectorAll('.chart-tools').forEach(el=>{const b=document.createElement('button');b.textContent='Read data table';b.addEventListener('click',()=>showTable(el.dataset.table));const csv=document.createElement('a');csv.href='data/'+el.dataset.table+'.csv';csv.textContent='Download data';csv.setAttribute('download','');const spec=document.createElement('a');spec.href='specs/'+el.dataset.chart+'.json';spec.textContent='Chart specification';el.append(b,csv,spec)});
document.getElementById('close-dialog').addEventListener('click',()=>document.getElementById('data-dialog').close());
document.getElementById('data-dialog').addEventListener('click',e=>{if(e.target===e.currentTarget)e.currentTarget.close()});
document.getElementById('reset-market').addEventListener('click',async()=>{
 const view=window.chartViews['08-market-scatter'];if(!view)return;
 await view.signal('year',2025).signal('focus','All markets').runAsync();updateMarketSummary();
});
async function start(){
 await document.fonts.ready;
 try{
  marketRows=await (await fetch('data/markets.json')).json();
  [colourSemantics,regionRows]=await Promise.all(['colour-semantics','regions'].map(async name=>(await fetch('data/'+name+'.json')).json()));
  buildColourLegends();
  const origins=await (await fetch('data/origins.json')).json();
  for(const row of [{country:'All origins'},...origins]){
   const button=document.createElement('button');button.type='button';button.dataset.origin=row.country;button.setAttribute('aria-pressed',String(row.country==='All origins'));button.textContent=displayName(row.country)+(row.visitors?' · '+formatTrips(row.visitors):'');
   button.addEventListener('click',async()=>{const view=window.chartViews['07-flow-map'];if(!view)return;await view.signal('originFocus',row.country).runAsync();document.querySelectorAll('#origin-key button').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));});document.getElementById('origin-key').append(button);
  }
 }catch(error){console.error('Could not load comparison controls',error)}
 await Promise.all(charts.map(renderChart));updateMarketSummary();document.documentElement.dataset.chartsReady='true';
}
function buildColourLegends(){
 for(const host of document.querySelectorAll('[data-legend]')){
  const kind=host.dataset.legend;
  const entries=kind==='international'?[colourSemantics.travellers[2]]:kind==='waterfall'?[{...colourSemantics.travellers[2],label:'International spending total'},...colourSemantics.change]:colourSemantics[kind];
  if(kind==='states'){
   const reset=document.createElement('button');reset.type='button';reset.textContent='All states and territories';reset.dataset.state='All states';reset.setAttribute('aria-pressed',String(selectedState==='All states'));reset.addEventListener('click',()=>selectState('All states'));host.append(reset);
  }
  for(const entry of entries){
   const item=document.createElement(kind==='states'?'button':'span');item.className='legend-item';item.dataset.colour=entry.colour;item.dataset.meaning=entry.label;
   const swatch=document.createElement('span');swatch.className='legend-swatch';swatch.setAttribute('aria-hidden','true');
   if(entry.dash){
    const svg=document.createElementNS('http://www.w3.org/2000/svg','svg');svg.setAttribute('viewBox','0 0 44 12');svg.setAttribute('width','44');svg.setAttribute('height','12');
    const line=document.createElementNS(svg.namespaceURI,'line');for(const [k,v] of Object.entries({x1:0,x2:44,y1:6,y2:6,stroke:entry.colour,'stroke-width':3,'stroke-dasharray':entry.dash.join(' ')}))line.setAttribute(k,v);svg.append(line);swatch.append(svg);swatch.classList.add('line-swatch');
   }else swatch.style.backgroundColor=entry.colour;
   item.append(swatch,document.createTextNode(entry.label));
   if(kind==='states'){item.type='button';item.dataset.state=entry.key;item.setAttribute('aria-pressed','false');item.addEventListener('click',()=>selectState(entry.key));}
   host.append(item);
  }
 }
}
async function selectState(state){
 selectedState=state;
 await Promise.all(['05-symbol-map','06-treemap'].map(name=>window.chartViews[name]?.signal('stateFocus',state).runAsync()));
 document.querySelectorAll('[data-state]').forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.state===state)));
 const detail=document.getElementById('state-detail');detail.replaceChildren();
 const intro=document.createElement('p');intro.textContent=state==='All states'?'Select a state in the legend to see its destinations and spending.':displayName(state)+' · destination spending in 2025';detail.append(intro);
 if(state!=='All states'){
  const list=document.createElement('ul');
  for(const row of regionRows.filter(r=>r.parent===state).sort((a,b)=>b.value-a.value)){
   const item=document.createElement('li');item.textContent=displayName(row.name).replace('Hobart & south','Hobart and the South')+': '+formatMoney(row.value);list.append(item);
  }detail.append(list);
 }
 scheduleProse();
}
// Measure real word positions, preserving inline links and emphasis. A character
// width alone cannot guarantee ten words when a sentence contains short words.
function proseWordLines(element){
 const lines=new Map(),walker=document.createTreeWalker(element,NodeFilter.SHOW_TEXT);
 let node;
 while(node=walker.nextNode()){
  for(const match of node.textContent.matchAll(/\S+/g)){
   const range=document.createRange();range.setStart(node,match.index);range.setEnd(node,match.index+match[0].length);
   const rect=range.getClientRects()[0];if(!rect||!rect.width)continue;
   const top=Math.round(rect.top);lines.set(top,(lines.get(top)||0)+1);
  }
 }
 return [...lines.values()];
}
function fitProse(){
 for(const el of document.querySelectorAll('p:not(.methods-links),figcaption,.methods li')){
  if(!el.getClientRects().length)continue;
  el.style.removeProperty('max-width');
  let width=el.getBoundingClientRect().width;
  for(let i=0;i<50&&Math.max(0,...proseWordLines(el))>10;i++){
   width*=.96;el.style.maxWidth=width+'px';
  }
 }
}
let proseFrame;
function scheduleProse(){cancelAnimationFrame(proseFrame);proseFrame=requestAnimationFrame(fitProse)}
const proseObserver=new MutationObserver(records=>{if(records.some(r=>r.target.closest?.('p,figcaption,.methods li')))scheduleProse()});
proseObserver.observe(document.body,{childList:true,characterData:true,subtree:true});
document.fonts.ready.then(scheduleProse);addEventListener('resize',scheduleProse);
start().then(scheduleProse);let resizeTimer,previousWidth=innerWidth,renderQueue=Promise.resolve();
addEventListener('resize',()=>{if(Math.abs(innerWidth-previousWidth)<20)return;clearTimeout(resizeTimer);resizeTimer=setTimeout(()=>{
 renderQueue=renderQueue.then(async()=>{
  previousWidth=innerWidth;const prior=window.chartViews['08-market-scatter'];const year=prior?.signal('year'),focus=prior?.signal('focus'),originFocus=window.chartViews['07-flow-map']?.signal('originFocus');
  Object.values(window.chartViews).forEach(v=>v.finalize());await Promise.all(charts.map(renderChart));
  if(year!==undefined&&window.chartViews['08-market-scatter'])await window.chartViews['08-market-scatter'].signal('year',year).signal('focus',focus).runAsync();
  if(originFocus!==undefined&&window.chartViews['07-flow-map'])await window.chartViews['07-flow-map'].signal('originFocus',originFocus).runAsync();
  updateMarketSummary();
 }).catch(console.error);
 },200)});
