/* Local Vega/Vega-Lite specifications; viewport changes preserve control values. */
const charts=['01-waffle','02-spend-per-trip','03-sankey','04-choropleth','05-symbol-map','06-treemap','07-flow-map','08-market-scatter','09-change-heatmap','10-waterfall','11-activity-slope','12-per-night'];
window.chartViews={};window.chartFailures=[];
async function renderChart(name,index){
 const el=document.getElementById('chart'+String(index+1).padStart(2,'0'));
 try{
  const spec=await (await fetch('specs/'+name+'.json')).json();
  const width=Math.max(230,el.clientWidth);
  if(index===0){spec.hconcat.forEach(p=>{p.width=Math.floor((width-38)/2);p.height=p.width});delete spec.width;delete spec.height;spec.config.legend.disable=true}
  else if(index===5){spec.width=width;spec.height=width<500?460:380}
  else if(index===6){spec.height=width<500?260:440}
  else if(index===9&&width<500){spec.layer[0].mark.size=22;spec.layer[1].mark.fontSize=9;spec.encoding.x.axis.labelAngle=-45;spec.height=280}
  else if(index===10&&width<500){spec.height=310}
  if(index===3||index===4)spec.height=Math.min(380,width*.88);
  const result=await vegaEmbed(el,spec,{actions:false,renderer:'svg',tooltip:{theme:'light'},loader:vega.loader({baseURL:document.baseURI})});
  window.chartViews[name]=result.view;
 }catch(error){window.chartFailures.push({name,message:error.message});el.innerHTML='<p class="chart-error">This chart could not load. Please use its data table or CSV below.</p>';console.error(name,error)}
}
async function showTable(name){
 const rows=await (await fetch('data/'+name+'.json')).json();
 const table=document.createElement('table');const head=document.createElement('thead'),body=document.createElement('tbody');
 const keys=Object.keys(rows[0]||{});const hr=document.createElement('tr');keys.forEach(key=>{const th=document.createElement('th');th.textContent=key.replaceAll('_',' ');th.scope='col';hr.append(th)});head.append(hr);
 rows.forEach(row=>{const tr=document.createElement('tr');keys.forEach(key=>{const td=document.createElement('td');td.textContent=row[key]===null?'Not available':typeof row[key]==='number'?new Intl.NumberFormat('en-AU',{maximumFractionDigits:4}).format(row[key]):row[key];tr.append(td)});body.append(tr)});table.append(head,body);
 document.getElementById('table-wrap').replaceChildren(table);document.getElementById('data-title').textContent=name.replaceAll('-',' ')+' · chart data';document.getElementById('data-dialog').showModal();
}
document.querySelectorAll('.chart-tools').forEach(el=>{const b=document.createElement('button');b.textContent='Read data table';b.addEventListener('click',()=>showTable(el.dataset.table));const csv=document.createElement('a');csv.href='data/'+el.dataset.table+'.csv';csv.textContent='CSV';csv.setAttribute('download','');const spec=document.createElement('a');spec.href='specs/'+el.dataset.chart+'.json';spec.textContent='Chart specification';el.append(b,csv,spec)});
document.getElementById('close-dialog').addEventListener('click',()=>document.getElementById('data-dialog').close());
document.getElementById('data-dialog').addEventListener('click',e=>{if(e.target===e.currentTarget)e.currentTarget.close()});
async function start(){await document.fonts.ready;await Promise.all(charts.map(renderChart));document.documentElement.dataset.chartsReady='true'}
start();let resizeTimer,previousWidth=innerWidth;addEventListener('resize',()=>{if(Math.abs(innerWidth-previousWidth)<20)return;clearTimeout(resizeTimer);resizeTimer=setTimeout(async()=>{previousWidth=innerWidth;const prior=window.chartViews['08-market-scatter'];const year=prior?.signal('year'),focus=prior?.signal('focus');Object.values(window.chartViews).forEach(v=>v.finalize());await Promise.all(charts.map(renderChart));if(year!==undefined)await window.chartViews['08-market-scatter'].signal('year',year).signal('focus',focus).runAsync()},200)});
