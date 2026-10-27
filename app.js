/* Local Vega/Vega-Lite specifications; viewport changes preserve control values. */
// INTERVIEW: START HERE: HTML provides chart01 to chart12 containers; each name below selects a JSON specification.
// INTERVIEW: The order matters: array index 0 goes into chart01, index 7 into chart08 (the scatterplot).
// INTERVIEW: Vega-Lite describes the marks and encodings; Vega renders them. The destination treemap uses rectangle area for AUD spending.
const charts=['01-waffle','02-spend-per-trip','03-spending-icons','04-choropleth','05-symbol-map','06-treemap','07-flow-map','08-market-scatter','09-change-heatmap','10-waterfall','11-activity-slope','12-per-night'];
// Vega appends data paths, so its base must exclude the page filename, query and chapter hash.
const chartBaseURL=new URL('.',document.baseURI).href;
// INTERVIEW: Keep each running chart View so other controls can change its signals later. chartFailures records caught loading errors.
window.chartViews={};window.chartFailures=[];
// INTERVIEW: Cache data used by the HTML summaries and controls. selectedState persists across chart redraws.
let marketRows=[];
let colourSemantics,regionRows=[],stateMixRows=[],selectedState='All states',referenceState='NSW',comparisonState='VIC';
// INTERVIEW: These helpers format numbers and expand abbreviations for readers; they do not change the underlying observations.
const formatTrips=n=>new Intl.NumberFormat('en-AU').format(n);
const formatMoney=n=>new Intl.NumberFormat('en-AU',{maximumFractionDigits:1}).format(n/1e6)+' million Australian dollars';
const displayName=value=>typeof value==='string'?value.replace(/\b(USA|UK|NSW|VIC|QLD|WA|SA|NT|ACT|TAS)\b/g,key=>({'USA':'United States','UK':'United Kingdom','NSW':'New South Wales','VIC':'Victoria','QLD':'Queensland','WA':'Western Australia','SA':'South Australia','NT':'Northern Territory','ACT':'Australian Capital Territory','TAS':'Tasmania'}[key])).replace('National/state parks','National and state parks').replace('Other + rounding','Other markets and rounding'):value;
const formatChange=n=>new Intl.NumberFormat('en-AU',{style:'percent',maximumFractionDigits:1,signDisplay:'exceptZero'}).format(Math.abs(n)<.0005?0:n);
// INTERVIEW: LINKED DETAIL TABLE: show both years for the selected origin so readers do not need to memorise the previous view.
// INTERVIEW: All markets is an overview state; Malaysia is explicitly the starting example for the table.
function updateComparison(focus){
 const country=focus==='All markets'?'Malaysia':focus;
// INTERVIEW: find() retrieves one record for each year; these records are already prepared in data/markets.json.
 const before=marketRows.find(r=>r.country===country&&r.year===2024),after=marketRows.find(r=>r.country===country&&r.year===2025);
 if(!before||!after)return;
 document.getElementById('comparison-title').textContent=displayName(country)+' · 2024 and 2025';
 document.getElementById('comparison-context').textContent=focus==='All markets'?'Malaysia is the starting example. Choose a market above to compare both years here.':'Both years stay visible while you switch the scatterplot year.';
// INTERVIEW: Replace the previous table rows. textContent inserts text safely; createElement builds HTML nodes.
 const body=document.getElementById('comparison-rows');body.replaceChildren();
// INTERVIEW: Build three rows (trips, nights, spending), with a value column for each year. Spending is displayed in millions only.
 for(const [key,label] of [['visitors','Visitor trips'],['nights','Visitor nights'],['spend','Spending (AUD millions)']]){
  const tr=document.createElement('tr'),th=document.createElement('th');th.scope='row';th.textContent=label;tr.append(th);
  for(const row of [before,after]){const td=document.createElement('td');td.textContent=key==='spend'?(row[key]/1e6).toLocaleString('en-AU',{minimumFractionDigits:1,maximumFractionDigits:1}):formatTrips(row[key]);tr.append(td)}body.append(tr);
 }
// INTERVIEW: Percentage change = after / before - 1. formatChange turns a fraction such as 0.3125 into +31.3%.
 // Derived rates connect visitor volume to spending without claiming causes (S1 p.10; S9 pp.2–4).
 const tripBefore=before.spend/before.visitors,tripAfter=after.spend/after.visitors;
 const money=n=>'AUD '+Math.round(n).toLocaleString('en-AU');
 document.getElementById('market-insight-title').textContent=displayName(country)+' · volume and spending per trip';
 document.getElementById('market-insight').textContent=`Trips changed ${formatChange(after.visitors/before.visitors-1)}, while spending per trip changed ${formatChange(tripAfter/tripBefore-1)} (${money(tripBefore)} → ${money(tripAfter)}). Together, these changes give ${formatChange(after.spend/before.spend-1)} in total spending.`;
 document.getElementById('market-rate-detail').textContent=`Average nights per trip: ${(before.nights/before.visitors).toFixed(1)} → ${(after.nights/after.visitors).toFixed(1)}. Spending per night: ${money(before.spend/before.nights)} → ${money(after.spend/after.nights)}. Total spending = trips × nights per trip × spending per night. Ratios use unrounded calculations from the published estimates; year-to-year change factors multiply; percentage changes do not simply add. These averages describe different visitor groups in each year and do not establish what caused the change. Source: Tourism Research Australia.`;
 document.getElementById('change-summary').textContent=`${displayName(country)}, 2024 → 2025: visitor trips ${formatChange(after.visitors/before.visitors-1)}, nights ${formatChange(after.nights/before.nights-1)} and spending ${formatChange(after.spend/before.spend-1)}. The outlined row follows the market selector; all other rows remain visible.`;
// INTERVIEW: LINKING: send the same country to the heatmap signal. runAsync() evaluates the chart update.
// INTERVIEW: The signal controls the outline/text layer; it does not remove the other heatmap rows.
 const heatmap=window.chartViews['09-change-heatmap'];
 if(heatmap&&heatmap.signal('marketFocus')!==country)heatmap.signal('marketFocus',country).runAsync().catch(console.error);
}
// INTERVIEW: Read the scatterplot signals, find the current-year leaders with reduce(), and update the surrounding narrative.
function updateMarketSummary(){
 const view=window.chartViews['08-market-scatter'];if(!view||!marketRows.length)return;
 const year=Number(view.signal('year')),focus=view.signal('focus'),rows=marketRows.filter(r=>r.year===year);
 const spendLeader=rows.reduce((a,b)=>a.spend>b.spend?a:b),tripLeader=rows.reduce((a,b)=>a.visitors>b.visitors?a:b);
 const row=rows.find(r=>r.country===focus);
 document.getElementById('market-heading').textContent=year+' · '+(row?displayName(row.country)+' in focus':displayName(spendLeader.country)+' leads spending among published origins');
 document.getElementById('market-summary').textContent=row?`${displayName(row.country)}: about ${formatTrips(row.visitors)} visitor trips and ${formatMoney(row.spend).replace(' million Australian dollars','m AUD')} spent in Australia in ${year}. Other dots within the chosen scale remain for comparison.`:`Among the 18 published markets in ${year}, ${displayName(spendLeader.country)} generated ${formatMoney(spendLeader.spend).replace(' million Australian dollars','m AUD')} from ${formatTrips(spendLeader.visitors)} trips. ${displayName(tripLeader.country)} had ${formatTrips(tripLeader.visitors)} trips but ${formatMoney(tripLeader.spend).replace(' million Australian dollars','m AUD')} in spending. More trips did not identify the spending leader.`;
 const detail=view.signal('marketScale')==='Smaller markets',inside=r=>r.visitors<=40000&&r.spend<=120000000;
 document.getElementById('market-scale-note').textContent=detail?`Detail: ${rows.filter(inside).length} of ${rows.length} markets; up to 40,000 trips and AUD 120m. Both years use these same bounds. ${row&&!inside(row)?displayName(row.country)+' is outside this detail and is outlined in the compact overview.':'The compact overview keeps all markets in context.'}`:'Overview: all 18 published markets. Choose Smaller markets to spread out the crowded lower-left cluster. Each scale keeps the same bounds across years.';
 syncMarketOverview(year,focus,detail);updateComparison(focus);scheduleProse();
}
// INTERVIEW: CHART LOADING PIPELINE: find container -> fetch specification -> adapt dimensions -> embed -> retain View.
// INTERVIEW: async/await lets the browser keep working while requests and rendering finish.
async function renderChart(name,index){
// INTERVIEW: padStart(2,0) produces the two-digit chart ID, for example index 7 becomes chart08. aria-busy describes loading state.
 const el=document.getElementById('chart'+String(index+1).padStart(2,'0'));
 el.setAttribute('aria-busy','true');
 if(!el.querySelector('svg'))el.innerHTML='<p class="chart-status" role="status">Loading chart…</p>';
 try{
// INTERVIEW: fetch retrieves the specification; json() parses it into an object. Its data.url fields tell Vega which data to load.
  const spec=await (await fetch('specs/'+name+'.json',{cache:'no-cache'})).json();
// INTERVIEW: Measure available container width. The following index-based adjustments adapt labels, legends and chart sizes.
// INTERVIEW: Selected heatmap values remain visible at every width; compact text fits the three cells on phones.
  const width=Math.max(230,el.clientWidth);
  if(index===1)spec.layer[0].encoding.x.title='Spending per trip (AUD)';
  if(index===6&&width<500)spec.layer[1].encoding.strokeWidth.legend.columns=1;
  if(index===8&&width<400)spec.layer[2].mark.fontSize=13;
  if(index===7&&width<360)spec.layer[0].encoding.x.axis.values={expr:"marketScale == 'Smaller markets' ? [0,20000,40000] : [0,100000,200000]"};
  if(index===0){spec.hconcat.forEach(p=>{p.width=Math.floor((width-38)/2);p.height=p.width});delete spec.width;delete spec.height;spec.config.legend.disable=true}
  else if(index===5){spec.width=width;spec.height=width<400?640:580}
  else if(index===6){spec.height=width<500?260:440;if(width<600)spec.layer[4].transform=[{filter:"originFocus == 'All origins' ? (datum.country == 'Malaysia' || datum.country == 'New Zealand') : datum.country == originFocus"},...spec.layer[4].transform.filter(t=>!t.filter)]}
  else if(index===9){for(const panel of spec.vconcat)panel.width=Math.max(110,width-(width<500?144:190));if(width<500){spec.vconcat[1].encoding.y.axis.labelExpr="datum.label == 'New Zealand' ? ['New','Zealand'] : datum.label == 'United States' ? ['United','States'] : datum.label == 'Other published markets' ? ['Other published','markets'] : datum.label == 'Unpublished + rounding' ? ['Unpublished','+ rounding'] : datum.label";spec.vconcat[1].encoding.y.axis.labelLimit=110;spec.vconcat[1].encoding.x.axis.tickCount=3;spec.vconcat[0].encoding.x.title=['Spending in Australia','(AUD billions)'];spec.vconcat[1].encoding.x.title=['Cumulative spending','(AUD billions)'];spec.vconcat[1].title.subtitle=['Enlarged scale: gains and losses.','Labels: change in AUD millions.'];}}
  // Give the explanatory idioms more area than their contextual comparisons.
  if(index===1)spec.height=240;
  if(index===2){spec.width=Math.min(width-12,380);spec.height=spec.width;}
  if(index===3)spec.height=Math.min(400,width*.98);
  if(index===4)spec.height=Math.min(360,width*.9);
  if(index===10)spec.height=380;
  if(index===11)spec.height=240;
// INTERVIEW: Embed the specification into the container. SVG gives scalable vector marks; actions:false hides the default editor menu.
// INTERVIEW: The loader base is the site directory, excluding a chapter hash, so relative data URLs remain valid.
  const result=await vegaEmbed(el,spec,{actions:false,renderer:'svg',tooltip:{theme:'light'},loader:vega.loader({baseURL:chartBaseURL})});
// INTERVIEW: Store the View, restore state selection, and register listeners only for the scatterplot year/focus parameters.
// INTERVIEW: A parameter in Vega-Lite becomes a signal in the running Vega View.
  window.chartViews[name]=result.view;
  if(index===0)await bindWaffleFeedback(result.view);
  if(index===3)await bindSpendingMap(result.view);
  if(index===4)await bindVisitsMap(result.view);
  if(index===4||index===5)await result.view.signal('stateFocus',selectedState).runAsync();
  if(index===7){result.view.addSignalListener('year',updateMarketSummary);result.view.addSignalListener('focus',updateMarketSummary);result.view.addSignalListener('marketScale',updateMarketSummary);updateMarketSummary()}
// INTERVIEW: Catch errors thrown by fetch/embed and show a useful fallback. Some internal Vega data warnings may not throw; visual checks still matter.
 }catch(error){window.chartFailures.push({name,message:error.message});el.innerHTML='<p class="chart-error">This chart could not load. Please use its data table or downloadable data below.</p>';console.error(name,error)}
 finally{el.setAttribute('aria-busy','false')}
}
// Preview a traveller group across both waffles; click retains the comparison.
let waffleSelected='';
async function bindWaffleFeedback(view){
 const rows=await (await fetch('data/waffle.json')).json();
 const buttons=[...document.querySelectorAll('[data-waffle-group]')];
 let shown=null;
 const show=group=>{
  if(group===shown)return;shown=group;
  const traveller=group||'Domestic day';
  const trips=rows.find(r=>r.traveller===traveller&&r.metric==='Visitor trips').share;
  const spend=rows.find(r=>r.traveller===traveller&&r.metric==='Spending in Australia').share;
  view.signal('waffleFocus',group).runAsync().catch(console.error);
  document.getElementById('waffle-group-name').textContent=traveller;
  document.getElementById('waffle-trip-share').textContent=(trips*100).toFixed(1)+'%';
  document.getElementById('waffle-spend-share').textContent=(spend*100).toFixed(1)+'%';
  document.getElementById('waffle-share-gap').textContent='Spending share is '+(spend/trips).toFixed(1)+'\u00d7 its trip share.';
  buttons.forEach(b=>{b.classList.toggle('is-previewed',b.dataset.waffleGroup===group);b.setAttribute('aria-pressed',String(b.dataset.waffleGroup===waffleSelected))});
 };
 const choose=group=>{waffleSelected=waffleSelected===group?'':group;shown=null;show(waffleSelected)};
 const groupOf=item=>item?.datum?.traveller;
 view.addEventListener('mouseover',(_,item)=>{const group=groupOf(item);if(group)show(group)});
 view.addEventListener('mouseout',()=>show(waffleSelected));
 view.addEventListener('click',(_,item)=>{const group=groupOf(item);if(group)choose(group)});
 for(const b of buttons){
  b.onmouseenter=b.onfocus=()=>show(b.dataset.waffleGroup);
  b.onmouseleave=b.onblur=()=>show(waffleSelected);
  b.onclick=()=>choose(b.dataset.waffleGroup);
 }
 document.getElementById('reset-waffle').onclick=()=>{waffleSelected='';shown=null;show('')};
 show(waffleSelected);
}
// Hover outlines preserve the spending colour. The dropdown offers keyboard/touch access.
async function bindSpendingMap(view){
 const rows=await (await fetch('data/states.json')).json();
 const select=document.getElementById('spending-state');
 if(select.options.length===1)for(const row of [...rows].sort((a,b)=>a.state.localeCompare(b.state))){
  const option=document.createElement('option');option.value=row.code;option.textContent=row.state;select.append(option);
 }
 let shown=null;
 const show=code=>{
  if(code===shown)return;shown=code;
  const row=rows.find(r=>r.code===code)||rows.find(r=>r.code==='NT');
  view.signal('mapFocus',code||'').runAsync().catch(console.error);
  document.getElementById('spending-state-name').textContent=row.state;
  document.getElementById('spending-state-rate').textContent='$'+Math.round(row.spend_per_resident).toLocaleString('en-AU');
  document.getElementById('spending-state-detail').textContent='AUD '+(row.spend/1e9).toFixed(2)+'bn spending / '+(row.population/1e6).toFixed(2)+'m residents';
 };
 const codeOf=item=>item?.datum?.properties?.code||item?.datum?.code;
 view.addEventListener('mouseover',(_,item)=>{const code=codeOf(item);if(code)show(code)});
 view.addEventListener('mouseout',()=>show(select.value));
 view.addEventListener('click',(_,item)=>{const code=codeOf(item);if(code){select.value=code;show(code)}});
 select.onchange=()=>show(select.value);
 show(select.value);
}
// The visit card previews hover; clicks retain the existing linked state selection.
let visitMapRows=[];
function updateVisitsCard(code=selectedState){
 const row=visitMapRows.find(r=>r.code===code)||visitMapRows.find(r=>r.code==='NSW');
 if(!row)return;
 document.getElementById('visits-state-value').textContent=row.visitors>=1e6?(row.visitors/1e6).toFixed(1)+'m':(row.visitors/1e3).toFixed(0)+'k';
 document.getElementById('visits-state-name').textContent=row.state;
 document.getElementById('visits-state-detail').textContent=formatTrips(row.visitors)+' visits recorded in 2025.';
}
async function bindVisitsMap(view){
 visitMapRows=await (await fetch('data/states.json')).json();
 const codeOf=item=>item?.datum?.properties?.code||item?.datum?.code;
 view.addEventListener('mouseover',(_,item)=>{
  const code=codeOf(item);if(!code)return;
  updateVisitsCard(code);view.signal('visitHover',code).runAsync().catch(console.error);
 });
 view.addEventListener('mouseout',()=>{
  updateVisitsCard();view.signal('visitHover','').runAsync().catch(console.error);
 });
 view.addEventListener('click',(_,item)=>{const code=codeOf(item);if(code)selectState(code).catch(console.error)});
 updateVisitsCard();
}
// Linked composition extends the visit map: same geography, a new traveller-type dimension.
async function renderStateMix(){
 const basePromise=fetch('specs/state-mix.json',{cache:'no-cache'}).then(response=>response.json());
 await Promise.all([['state-reference','state-reference-chart',referenceState],['state-mix','state-mix-chart',comparisonState]].map(async([key,id,code])=>{
  const el=document.getElementById(id);el.setAttribute('aria-busy','true');
  try{
   const spec=structuredClone(await basePromise);spec.width=Math.max(160,el.clientWidth-105);spec.params[0].value=code;
   const result=await vegaEmbed(el,spec,{actions:false,renderer:'svg',loader:vega.loader({baseURL:chartBaseURL})});window.chartViews[key]=result.view;
  }catch(error){window.chartFailures.push({name:key,message:error.message});el.textContent='The comparison could not load. Use the data table below.';console.error(error)}
  finally{el.setAttribute('aria-busy','false')}
 }));
}
function updateStateMix(){
 const pct=n=>(n*100).toFixed(1)+'%';
 document.getElementById('reference-state').value=referenceState;
 document.getElementById('comparison-state').value=comparisonState;
 for(const [code,id] of [[referenceState,'state-reference-values'],[comparisonState,'state-mix-values']]){
  const host=document.getElementById(id);host.replaceChildren();
  const label=document.createElement('p');label.textContent='Visit share / spending share';host.append(label);
  for(const row of stateMixRows.filter(r=>r.code===code)){
   const line=document.createElement('p');line.textContent=row.traveller+': '+pct(row.visitor_share)+' / '+pct(row.spend_share);host.append(line);
  }
 }
 const rows=[referenceState,comparisonState].map(code=>stateMixRows.find(r=>r.code===code&&r.traveller==='Domestic overnight'));
 if(rows.some(r=>!r))return;
 document.getElementById('state-mix-summary').textContent=referenceState===comparisonState?'Both panels show '+displayName(referenceState)+'. Choose a different comparison state to see the contrast.':`Domestic overnight visitors account for ${pct(rows[0].visitor_share)} of visits and ${pct(rows[0].spend_share)} of spending in ${displayName(referenceState)}, versus ${pct(rows[1].visitor_share)} of visits and ${pct(rows[1].spend_share)} of spending in ${displayName(comparisonState)}.`;
 document.getElementById('state-mix-context').textContent='The reference stays fixed. Selecting a state in either legend changes the comparison state and highlights the visit map and destination treemap.';
}
function buildStateComparison(){
 for(const id of ['reference-state','comparison-state']){
  const select=document.getElementById(id);
  for(const state of colourSemantics.states){const option=document.createElement('option');option.value=state.key;option.textContent=state.label;select.append(option)}
 }
 document.getElementById('reference-state').addEventListener('change',async e=>{referenceState=e.target.value;updateStateMix();await window.chartViews['state-reference']?.signal('stateFocus',referenceState).runAsync()});
 document.getElementById('comparison-state').addEventListener('change',e=>selectState(e.target.value));
 document.getElementById('reset-state-comparison').addEventListener('click',async()=>{referenceState='NSW';comparisonState='VIC';await selectState('All states');await window.chartViews['state-reference']?.signal('stateFocus',referenceState).runAsync()});
 updateStateMix();
}
// Week 10 focus+context: this overview retains all markets while the main view enlarges the cluster.
async function renderMarketOverview(){
 const el=document.getElementById('market-overview-chart');
 try{
  const spec=await (await fetch('specs/08-market-overview.json',{cache:'no-cache'})).json();
  spec.width=Math.max(160,document.getElementById('chart08').clientWidth-100);
  const result=await vegaEmbed(el,spec,{actions:false,renderer:'svg',loader:vega.loader({baseURL:chartBaseURL})});window.chartViews['08-market-overview']=result.view;
 }catch(error){window.chartFailures.push({name:'08-market-overview',message:error.message});el.textContent='The overview could not load. Choose All markets above for context.';console.error(error)}
}
function syncMarketOverview(year,focus,detail){
 document.getElementById('market-overview-panel').hidden=!detail;
 document.getElementById('market-overview-heading').textContent=year+' · all markets in context';
 const view=window.chartViews['08-market-overview'];
 if(view&&(view.signal('year')!==year||view.signal('focus')!==focus))view.signal('year',year).signal('focus',focus).runAsync().catch(console.error);
}

// INTERVIEW: DATA ALTERNATIVE: load the same prepared values into a readable HTML table inside a native dialog.
// INTERVIEW: National data are limited to 2025 here because the domestic survey changed. Region parents are excluded to avoid double counting.
async function showTable(name){
 let rows=await (await fetch('data/'+name+'.json')).json();
 if(name==='national')rows=rows.filter(r=>r.year===2025);
 if(name==='regions')rows=rows.filter(r=>r.value>0).map(r=>({region:r.name,state:r.parent,spend:r.value}));
 const labels={spend:'Spending in Australia (Australian dollars)',total_spend:'Total trip spending (Australian dollars)',spend_per_trip:'Spending per trip (Australian dollars)',population:'Residents (June 2025)',spend_per_resident:'Australian dollars per resident',visitors:['states','state-mix'].includes(name)?'State visits':'Visitor trips',share:'Participation',visitor_share:'Share of state visits',spend_share:'Share of state spending',change:'Change (%)',other:'Other visitors (Australian dollars per night)',business:'Business-event visitors (Australian dollars per night)',value:'Change / total (Australian dollars billions)',start:'Start (Australian dollars billions)',end:'End (Australian dollars billions)',nights:'Visitor nights'};
// INTERVIEW: Hide coordinates and layout-order columns from this reader-facing table; retain them in the underlying download.
 const hidden=new Set(['longitude','latitude','label_lon','label_lat','order']);
 const table=document.createElement('table');const head=document.createElement('thead'),body=document.createElement('tbody');
 const keys=Object.keys(rows[0]||{}).filter(k=>!hidden.has(k));const hr=document.createElement('tr');keys.forEach(key=>{const th=document.createElement('th');th.textContent=labels[key]||key.replaceAll('_',' ');th.scope='col';hr.append(th)});head.append(hr);
 rows.forEach(row=>{const tr=document.createElement('tr');keys.forEach(key=>{const td=document.createElement('td');td.textContent=row[key]===null?'Not available':typeof row[key]==='number'?new Intl.NumberFormat('en-AU',{maximumFractionDigits:['share','change','visitor_share','spend_share'].includes(key)?1:4,...(['share','change','visitor_share','spend_share'].includes(key)?{style:'percent'}:{})}).format(row[key]):displayName(row[key]);tr.append(td)});body.append(tr)});table.append(head,body);
 document.getElementById('data-note').textContent=(name==='national'?'2025 snapshot only. The downloadable source also contains 2024 domestic estimates, which cannot be compared directly because the survey changed. ':name==='state-mix'?'2025 business-event totals by traveller group, not all tourism. Shares use the sum of the three published components within each state; rounding may differ from the separate state total. ':name==='activities'?'Includes all five supplied activities; the chart selects four to keep the comparison readable. ':name==='regions'?'Destination regions only; parent groups are not added again. ':'')+'Use the downloadable data link for the full reusable dataset. All amounts are recorded in Australian dollars, without adjusting for inflation.';
 document.getElementById('table-wrap').replaceChildren(table);document.getElementById('data-title').textContent=name.replaceAll('-',' ')+' · chart data';document.getElementById('data-dialog').showModal();
}
// INTERVIEW: Create a table button, CSV download and specification link for each figure, using its HTML data-table/data-chart attributes.
document.querySelectorAll('.chart-tools').forEach(el=>{
 const host=el.parentElement;host.classList.add('has-chart-actions');
 const details=document.createElement('details');details.className='chart-action-menu';
 const summary=document.createElement('summary');summary.title='Chart actions';
 const label=host.querySelector('.plot-title,h3')?.textContent||'Traveller mix comparison';
 summary.setAttribute('aria-label','Chart actions: '+label);
 const dots=document.createElement('span');dots.setAttribute('aria-hidden','true');dots.textContent='⋯';summary.append(dots);
 const panel=document.createElement('div');panel.className='chart-action-panel';
 const close=()=>{details.open=false;summary.focus()};
 const b=document.createElement('button');b.type='button';b.textContent='Read data table';
 b.addEventListener('click',()=>{close();showTable(el.dataset.table)});
 const csv=document.createElement('a');csv.href='data/'+el.dataset.table+'.csv';csv.textContent='Download data';csv.setAttribute('download','');csv.addEventListener('click',close);
 const spec=document.createElement('a');spec.href='specs/'+el.dataset.chart+'.json';spec.textContent='Chart specification';
 panel.append(b,csv,spec);details.append(summary,panel);el.append(details);
 details.addEventListener('toggle',()=>{
  if(details.open)document.querySelectorAll('.chart-action-menu[open]').forEach(other=>{if(other!==details)other.open=false});
 });
});
// Native disclosure controls retain ordinary Tab/Enter access to links and buttons.
document.addEventListener('pointerdown',event=>{
 document.querySelectorAll('.chart-action-menu[open]').forEach(menu=>{if(!menu.contains(event.target))menu.open=false});
});
document.addEventListener('keydown',event=>{
 if(event.key!=='Escape')return;
 const menu=document.querySelector('.chart-action-menu[open]');
 if(menu){event.preventDefault();menu.open=false;menu.querySelector('summary').focus()}
});
// INTERVIEW: Close the dialog using its button or a click on the backdrop. The native dialog also supports Escape.
document.getElementById('close-dialog').addEventListener('click',()=>document.getElementById('data-dialog').close());
document.getElementById('data-dialog').addEventListener('click',e=>{if(e.target===e.currentTarget)e.currentTarget.close()});
// INTERVIEW: Reset all three scatterplot controls to the initial overview; updateMarketSummary also refreshes the linked table/heatmap.
document.getElementById('reset-market').addEventListener('click',async()=>{
 const view=window.chartViews['08-market-scatter'];if(!view)return;
 await view.signal('year',2025).signal('focus','All markets').signal('marketScale','All markets').runAsync();updateMarketSummary();
});
// INTERVIEW: STARTUP: wait for fonts, load control data, build legends/origin buttons, then render the figures and their supporting views.
// INTERVIEW: Promise.all waits for independent chart renders together; it does not deliberately load them one at a time.
async function start(){
 await document.fonts.ready;
 try{
  marketRows=await (await fetch('data/markets.json')).json();
// INTERVIEW: Load category colours for HTML legends and destination values for the selected-state detail list.
  [colourSemantics,regionRows,stateMixRows]=await Promise.all(['colour-semantics','regions','state-mix'].map(async name=>(await fetch('data/'+name+'.json')).json()));
  buildColourLegends();buildStateComparison();
  const origins=await (await fetch('data/origins.json')).json();
// INTERVIEW: Create origin buttons from actual data. Clicking sets originFocus; conditional opacity fades unrelated routes.
// INTERVIEW: aria-pressed tells assistive technology which button is selected.
  for(const row of [{country:'All origins'},...origins]){
   const button=document.createElement('button');button.type='button';button.dataset.origin=row.country;button.setAttribute('aria-pressed',String(row.country==='All origins'));button.textContent=displayName(row.country)+(row.visitors?' · '+formatTrips(row.visitors):'');
   button.addEventListener('click',async()=>{const view=window.chartViews['07-flow-map'];if(!view)return;await view.signal('originFocus',row.country).runAsync();document.querySelectorAll('#origin-key button').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));});document.getElementById('origin-key').append(button);
  }
 }catch(error){console.error('Could not load comparison controls',error)}
 await Promise.all([...charts.map(renderChart),renderStateMix(),renderMarketOverview()]);updateMarketSummary();updateStateMix();document.documentElement.dataset.chartsReady='true';
}
// INTERVIEW: Build visible legends from colour-semantics.json. Chart specifications contain matching colour scales.
// INTERVIEW: State entries are buttons because they also select data; other legend entries are explanatory labels.
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
// INTERVIEW: Activity legends draw a small SVG line with the same dash pattern as the activity chart, adding a cue beyond colour.
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
// INTERVIEW: COORDINATED STATE SELECTION: send one state to BOTH the symbol map and destination treemap, then show its regions below.
// INTERVIEW: The optional ?. call skips a View that has not loaded yet. Promise.all waits for both available updates.
async function selectState(state){
 selectedState=state;
 updateVisitsCard();
 if(state!=='All states')comparisonState=state;
 updateStateMix();
 await Promise.all(['05-symbol-map','06-treemap','state-mix'].map(name=>window.chartViews[name]?.signal('stateFocus',name==='state-mix'?comparisonState:state).runAsync()));
// INTERVIEW: Synchronise the pressed appearance of both state legends, so their controls agree.
 document.querySelectorAll('[data-state]').forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.state===state)));
 const detail=document.getElementById('state-detail');detail.replaceChildren();
 const destinations=regionRows.filter(r=>r.parent===state&&r.value>0),total=destinations.reduce((sum,r)=>sum+r.value,0);
 const intro=document.createElement('p');intro.textContent=state==='All states'?'Hover a rectangle for its spending and share, or choose a state above for all its values. Small rectangles may not fit a label.':displayName(state)+' · displayed total: '+formatMoney(total);detail.append(intro);
 if(state!=='All states'){
  const list=document.createElement('ul');
// INTERVIEW: Keep only destination leaves belonging to the selected state and sort by spending, largest first.
  for(const row of destinations.sort((a,b)=>b.value-a.value)){
   const item=document.createElement('li');item.textContent=displayName(row.name).replace('Hobart & south','Hobart and the South')+': '+formatMoney(row.value)+' · '+(row.value/total*100).toFixed(1)+'% of displayed state spending';list.append(item);
  }detail.append(list);
 }
 scheduleProse();
}
// Align the top of neighbouring chart views without forcing equal chart heights.
// INTERVIEW: DESKTOP ALIGNMENT: compare the plot tops in neighbouring figure columns and add only the required top margin.
// INTERVIEW: Skip stacked/mobile figures. This aligns chart starts without forcing all charts to have the same height.
function fitProse(){
 for(const row of document.querySelectorAll('.two-col:has(>figure)')){
  const views=[...row.children].filter(e=>e.tagName==='FIGURE').map(f=>f.querySelector(':scope > .chart')).filter(Boolean);
  for(const view of views)view.style.marginTop='';
  if(views.length!==2||Math.abs(views[0].closest('figure').getBoundingClientRect().left-views[1].closest('figure').getBoundingClientRect().left)<1)continue;
  const tops=views.map(v=>v.getBoundingClientRect().top),target=Math.max(...tops);
  views.forEach((v,i)=>v.style.marginTop=(target-tops[i])+'px');
 }
}
// INTERVIEW: Batch alignment work into the next browser animation frame; cancel an older pending request to avoid duplicate work.
let proseFrame;
function scheduleProse(){cancelAnimationFrame(proseFrame);proseFrame=requestAnimationFrame(fitProse)}
document.fonts.ready.then(scheduleProse);addEventListener('resize',scheduleProse);
// Keep anchor headings below the navigation, including its two-row phone layout.
const chapterNav=document.querySelector('.chapter-nav');
const chapterLinks=[...chapterNav.querySelectorAll('.chapter-links a')];
const storyChapters=chapterLinks.map(link=>document.querySelector(link.getAttribute('href')));
let chapterFrame;
function updateChapterNav(){
 const height=Math.ceil(chapterNav.getBoundingClientRect().height);
 document.documentElement.style.setProperty('--chapter-nav-height',height+'px');
 let current=null;
 for(const chapter of storyChapters){if(chapter.getBoundingClientRect().top<=height+80)current=chapter.id}
 chapterLinks.forEach(link=>{
  if(link.getAttribute('href')==='#'+current)link.setAttribute('aria-current','location');
  else link.removeAttribute('aria-current');
 });
}
function scheduleChapterNav(){cancelAnimationFrame(chapterFrame);chapterFrame=requestAnimationFrame(updateChapterNav)}
new ResizeObserver(scheduleChapterNav).observe(chapterNav);
addEventListener('scroll',scheduleChapterNav,{passive:true});
addEventListener('resize',scheduleChapterNav);
document.fonts.ready.then(scheduleChapterNav);
updateChapterNav();
// Charts change section heights during startup. Re-align a direct chapter URL
// once those heights settle, unless the reader has already begun interacting.
const initialStoryHash=location.hash;
let readerInteracted=false;
for(const event of ['pointerdown','wheel','touchstart','keydown']){
 addEventListener(event,()=>{readerInteracted=true},{once:true,passive:true});
}
function settleInitialAnchor(){
 requestAnimationFrame(()=>requestAnimationFrame(()=>{
  if(!readerInteracted&&initialStoryHash&&location.hash===initialStoryHash){
   const target=document.getElementById(initialStoryHash.slice(1));
   target?.scrollIntoView({block:'start',behavior:'instant'});
   scheduleChapterNav();
  }
 }));
}
// INTERVIEW: Run startup once. Keep resize work in a promise queue so two expensive redraws do not run over each other.
start().then(()=>{scheduleProse();scheduleChapterNav();settleInitialAnchor()});let resizeTimer,previousWidth=innerWidth,renderQueue=Promise.resolve();
// INTERVIEW: RESPONSIVE REDRAW: ignore width changes smaller than 20px and wait 200ms after the latest resize event (debouncing).
// INTERVIEW: Save selected year/market/scale/origin, finalise old Views, rebuild at the new size, then restore the selections.
// INTERVIEW: State selection is restored inside renderChart using selectedState; finalise releases old chart resources.
addEventListener('resize',()=>{if(Math.abs(innerWidth-previousWidth)<20)return;clearTimeout(resizeTimer);resizeTimer=setTimeout(()=>{
 renderQueue=renderQueue.then(async()=>{
  previousWidth=innerWidth;const prior=window.chartViews['08-market-scatter'];const year=prior?.signal('year'),focus=prior?.signal('focus'),marketScale=prior?.signal('marketScale'),originFocus=window.chartViews['07-flow-map']?.signal('originFocus');
  Object.values(window.chartViews).forEach(v=>v.finalize());await Promise.all([...charts.map(renderChart),renderStateMix(),renderMarketOverview()]);
  if(year!==undefined&&window.chartViews['08-market-scatter'])await window.chartViews['08-market-scatter'].signal('year',year).signal('focus',focus).signal('marketScale',marketScale).runAsync();
  if(originFocus!==undefined&&window.chartViews['07-flow-map'])await window.chartViews['07-flow-map'].signal('originFocus',originFocus).runAsync();
  updateMarketSummary();scheduleProse();
 }).catch(console.error);
 },200)});
