/* Local Vega/Vega-Lite specifications; viewport changes preserve control values. */
const charts=['01-waffle','02-spend-per-trip','03-sankey','04-choropleth','05-symbol-map','06-treemap','07-flow-map','08-market-scatter','09-change-heatmap','10-waterfall','11-activity-slope','12-per-night'];
window.chartViews={};window.chartFailures=[];
let marketRows=[];
const formatTrips=n=>new Intl.NumberFormat('en-AU').format(n);
const formatMoney=n=>'A$'+new Intl.NumberFormat('en-AU',{maximumFractionDigits:1}).format(n/1e6)+'m';
function updateMarketSummary(){
 const view=window.chartViews['08-market-scatter'];if(!view||!marketRows.length)return;
 const year=Number(view.signal('year')),focus=view.signal('focus'),rows=marketRows.filter(r=>r.year===year);
 const spendLeader=rows.reduce((a,b)=>a.spend>b.spend?a:b),tripLeader=rows.reduce((a,b)=>a.visitors>b.visitors?a:b);
 const row=rows.find(r=>r.country===focus);
 document.getElementById('market-heading').textContent=year+' · '+(row?row.country+' in focus':spendLeader.country+' leads on spending');
 document.getElementById('market-summary').textContent=row?`${row.country}: about ${formatTrips(row.visitors)} visitor trips and ${formatMoney(row.spend)} spent in Australia in ${year}. The faded dots retain the other markets for comparison.`:`In ${year}, ${spendLeader.country} led spending with ${formatMoney(spendLeader.spend)}; ${tripLeader.country} led visitor volume with about ${formatTrips(tripLeader.visitors)} trips. Choose a year or any of the 18 markets below.`;
}
async function renderChart(name,index){
 const el=document.getElementById('chart'+String(index+1).padStart(2,'0'));
 try{
  const spec=await (await fetch('specs/'+name+'.json')).json();
  const width=Math.max(230,el.clientWidth);
  if(index===0){spec.hconcat.forEach(p=>{p.width=Math.floor((width-38)/2);p.height=p.width});delete spec.width;delete spec.height;spec.config.legend.disable=true}
  else if(index===5){spec.width=width;spec.height=width<500?460:380}
  else if(index===6){spec.height=width<500?260:440;if(width<600)spec.layer[4].transform=[{filter:"originFocus == 'All origins' ? (datum.country == 'Malaysia' || datum.country == 'New Zealand') : datum.country == originFocus"}]}
  else if(index===9&&width<500){spec.layer[1].mark.size=22;spec.layer[2].mark.fontSize=10;spec.encoding.x.axis.labelAngle=-45;spec.height=280}
  else if(index===10&&width<500){spec.height=310;if(width<300){spec.transform[1].calculate='datum.year == 2024 ? 0.06 : 0.42';spec.layer[3].data.values[1].position=.42}}
  if(index===3||index===4)spec.height=Math.min(380,width*.88);
  const result=await vegaEmbed(el,spec,{actions:false,renderer:'svg',tooltip:{theme:'light'},loader:vega.loader({baseURL:document.baseURI})});
  window.chartViews[name]=result.view;
  if(index===7){result.view.addSignalListener('year',updateMarketSummary);result.view.addSignalListener('focus',updateMarketSummary);updateMarketSummary()}
 }catch(error){window.chartFailures.push({name,message:error.message});el.innerHTML='<p class="chart-error">This chart could not load. Please use its data table or CSV below.</p>';console.error(name,error)}
}
async function showTable(name){
 let rows=await (await fetch('data/'+name+'.json')).json();
 if(name==='national')rows=rows.filter(r=>r.year===2025);
 if(name==='regions')rows=rows.filter(r=>r.value>0).map(r=>({region:r.name,state:r.parent,spend:r.value}));
 const labels={spend:'Spending in Australia (AUD)',total_spend:'Total trip spending (AUD)',spend_per_trip:'Spending per trip (AUD)',population:'Residents (June 2025)',spend_per_resident:'AUD per resident',visitors:name==='states'?'State visits':'Visitor trips',share:'Participation',change:'Change (%)',other:'Other visitors (AUD/night)',business:'Business-event visitors (AUD/night)',value:'Change / total (AUD billions)',start:'Start (AUD billions)',end:'End (AUD billions)',nights:'Visitor nights'};
 const hidden=new Set(['longitude','latitude','label_lon','label_lat','order']);
 const table=document.createElement('table');const head=document.createElement('thead'),body=document.createElement('tbody');
 const keys=Object.keys(rows[0]||{}).filter(k=>!hidden.has(k));const hr=document.createElement('tr');keys.forEach(key=>{const th=document.createElement('th');th.textContent=labels[key]||key.replaceAll('_',' ');th.scope='col';hr.append(th)});head.append(hr);
 rows.forEach(row=>{const tr=document.createElement('tr');keys.forEach(key=>{const td=document.createElement('td');td.textContent=row[key]===null?'Not available':typeof row[key]==='number'?new Intl.NumberFormat('en-AU',{maximumFractionDigits:['share','change'].includes(key)?1:4,...(['share','change'].includes(key)?{style:'percent'}:{})}).format(row[key]):row[key];tr.append(td)});body.append(tr)});table.append(head,body);
 document.getElementById('data-note').textContent=(name==='national'?'2025 snapshot only. The downloadable source also contains 2024 domestic estimates, which cannot be compared directly because the survey changed. ':name==='activities'?'Includes all five supplied activities; the chart selects four to keep the comparison readable. ':name==='regions'?'Destination regions only; parent groups are not added again. ':'')+'Use the CSV link for the full reusable dataset. All monetary values are nominal Australian dollars.';
 document.getElementById('table-wrap').replaceChildren(table);document.getElementById('data-title').textContent=name.replaceAll('-',' ')+' · chart data';document.getElementById('data-dialog').showModal();
}
document.querySelectorAll('.chart-tools').forEach(el=>{const b=document.createElement('button');b.textContent='Read data table';b.addEventListener('click',()=>showTable(el.dataset.table));const csv=document.createElement('a');csv.href='data/'+el.dataset.table+'.csv';csv.textContent='CSV';csv.setAttribute('download','');const spec=document.createElement('a');spec.href='specs/'+el.dataset.chart+'.json';spec.textContent='Chart specification';el.append(b,csv,spec)});
document.getElementById('close-dialog').addEventListener('click',()=>document.getElementById('data-dialog').close());
document.getElementById('data-dialog').addEventListener('click',e=>{if(e.target===e.currentTarget)e.currentTarget.close()});
async function start(){
 await document.fonts.ready;
 try{
  marketRows=await (await fetch('data/markets.json')).json();
  const origins=await (await fetch('data/origins.json')).json();
  for(const row of [{country:'All origins'},...origins]){
   const button=document.createElement('button');button.type='button';button.dataset.origin=row.country;button.setAttribute('aria-pressed',String(row.country==='All origins'));button.textContent=row.country+(row.visitors?' · '+formatTrips(row.visitors):'');
   button.addEventListener('click',async()=>{const view=window.chartViews['07-flow-map'];if(!view)return;await view.signal('originFocus',row.country).runAsync();document.querySelectorAll('#origin-key button').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));});document.getElementById('origin-key').append(button);
  }
 }catch(error){console.error('Could not load comparison controls',error)}
 await Promise.all(charts.map(renderChart));document.documentElement.dataset.chartsReady='true';
}
start();let resizeTimer,previousWidth=innerWidth,renderQueue=Promise.resolve();
addEventListener('resize',()=>{if(Math.abs(innerWidth-previousWidth)<20)return;clearTimeout(resizeTimer);resizeTimer=setTimeout(()=>{
 renderQueue=renderQueue.then(async()=>{
  previousWidth=innerWidth;const prior=window.chartViews['08-market-scatter'];const year=prior?.signal('year'),focus=prior?.signal('focus'),originFocus=window.chartViews['07-flow-map']?.signal('originFocus');
  Object.values(window.chartViews).forEach(v=>v.finalize());await Promise.all(charts.map(renderChart));
  if(year!==undefined&&window.chartViews['08-market-scatter'])await window.chartViews['08-market-scatter'].signal('year',year).signal('focus',focus).runAsync();
  if(originFocus!==undefined&&window.chartViews['07-flow-map'])await window.chartViews['07-flow-map'].signal('originFocus',originFocus).runAsync();
  updateMarketSummary();
 }).catch(console.error);
 },200)});
