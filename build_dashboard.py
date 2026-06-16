import json

with open("/home/claude/project/data/aggregated.json") as f:
    agg = json.load(f)

data_json = json.dumps(agg)

html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Sales Performance Console — FY2024-25</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>
<style>
  :root{
    --navy:#10243E;
    --navy-soft:#1B3A5C;
    --paper:#F4F6F8;
    --card:#FFFFFF;
    --line:#E2E8F0;
    --ink:#1A2433;
    --muted:#6B7A8F;
    --blue:#2E75B6;
    --blue-soft:#CFE3F4;
    --amber:#F4A300;
    --green:#1F9D7C;
    --red:#D64545;
  }
  *{box-sizing:border-box;}
  body{
    margin:0;
    font-family:'Inter',sans-serif;
    background:var(--paper);
    color:var(--ink);
  }
  .topbar{
    background:linear-gradient(135deg,var(--navy) 0%, var(--navy-soft) 100%);
    color:#fff;
    padding:36px 40px 90px;
    position:relative;
    overflow:hidden;
  }
  .topbar::after{
    content:"";
    position:absolute; right:-80px; top:-80px;
    width:300px; height:300px; border-radius:50%;
    background:radial-gradient(circle, rgba(244,163,0,0.18), transparent 70%);
  }
  .eyebrow{
    font-family:'IBM Plex Mono',monospace;
    font-size:12px; letter-spacing:.18em; text-transform:uppercase;
    color:var(--amber); margin:0 0 10px;
  }
  h1{
    font-family:'Space Grotesk',sans-serif;
    font-size:34px; margin:0 0 6px; font-weight:700;
  }
  .subtitle{ color:#C7D2E0; font-size:15px; max-width:640px; line-height:1.5;}

  .wrap{ max-width:1240px; margin:0 auto; padding:0 40px 60px;}

  .kpi-row{
    display:grid; grid-template-columns:repeat(5,1fr); gap:18px;
    margin-top:-58px; position:relative; z-index:2;
  }
  .kpi{
    background:var(--card); border-radius:14px; padding:20px 22px;
    box-shadow:0 10px 30px -18px rgba(16,36,62,0.35);
    border:1px solid var(--line);
  }
  .kpi .label{ font-size:12px; text-transform:uppercase; letter-spacing:.08em; color:var(--muted); font-weight:600;}
  .kpi .value{ font-family:'Space Grotesk',sans-serif; font-size:26px; font-weight:700; margin-top:6px; color:var(--navy);}
  .kpi .sub{ font-size:12px; color:var(--muted); margin-top:4px;}

  .section{ margin-top:46px; }
  .section-head{ display:flex; align-items:baseline; justify-content:space-between; margin-bottom:14px; flex-wrap:wrap; gap:8px;}
  .section-head h2{ font-family:'Space Grotesk',sans-serif; font-size:20px; margin:0; }
  .section-head p{ margin:0; color:var(--muted); font-size:13px; max-width:520px; }

  .grid-2{ display:grid; grid-template-columns:1.3fr 1fr; gap:20px; }
  .grid-3{ display:grid; grid-template-columns:repeat(3,1fr); gap:20px; }

  .card{
    background:var(--card); border:1px solid var(--line); border-radius:14px;
    padding:20px; box-shadow:0 6px 20px -16px rgba(16,36,62,0.25);
  }
  .card h3{ font-family:'Space Grotesk',sans-serif; font-size:15px; margin:0 0 4px; }
  .card .desc{ font-size:12px; color:var(--muted); margin:0 0 14px;}
  .chart-box{ position:relative; height:300px; }
  .chart-box.tall{ height:380px; }

  .insights{
    background:var(--navy); color:#fff; border-radius:14px; padding:28px 30px;
    margin-top:46px;
  }
  .insights h2{ font-family:'Space Grotesk',sans-serif; margin:0 0 16px; font-size:20px;}
  .insight-grid{ display:grid; grid-template-columns:repeat(2,1fr); gap:18px;}
  .insight-card{ background:rgba(255,255,255,0.06); border-radius:10px; padding:16px 18px; border:1px solid rgba(255,255,255,0.1);}
  .insight-card .tag{ font-family:'IBM Plex Mono',monospace; font-size:11px; letter-spacing:.12em; text-transform:uppercase; color:var(--amber); margin-bottom:8px; display:block;}
  .insight-card p{ margin:0; font-size:13.5px; line-height:1.55; color:#E4EBF3;}
  .insight-card.rec{ border-left:3px solid var(--green); }
  .insight-card.warn{ border-left:3px solid var(--red); }

  .filters{ display:flex; gap:10px; margin-bottom:14px; flex-wrap:wrap; }
  .filters button{
    font-family:'Inter',sans-serif; font-size:12.5px; font-weight:600;
    padding:7px 14px; border-radius:20px; border:1px solid var(--line);
    background:#fff; color:var(--muted); cursor:pointer; transition:.15s;
  }
  .filters button.active{ background:var(--blue); color:#fff; border-color:var(--blue); }
  .filters button:hover{ border-color:var(--blue); }

  table{ width:100%; border-collapse:collapse; font-size:13px; }
  th,td{ text-align:left; padding:9px 10px; border-bottom:1px solid var(--line); }
  th{ font-size:11px; text-transform:uppercase; letter-spacing:.06em; color:var(--muted); font-weight:600;}
  td.num, th.num{ text-align:right; font-family:'IBM Plex Mono',monospace; font-size:12.5px;}
  tr:hover td{ background:#F7FAFD; }
  .pos{ color:var(--green); font-weight:600;}
  .neg{ color:var(--red); font-weight:600;}

  .footer{ text-align:center; color:var(--muted); font-size:12px; padding:30px 0 10px;}

  @media (max-width:980px){
    .kpi-row{ grid-template-columns:repeat(2,1fr); margin-top:20px;}
    .grid-2,.grid-3,.insight-grid{ grid-template-columns:1fr; }
    .topbar{ padding-bottom:40px; }
  }
</style>
</head>
<body>

<div class="topbar">
  <div class="wrap" style="padding:0;">
    <p class="eyebrow">Business Sales Performance Console · FY2024–2025</p>
    <h1>Sales &amp; Profitability Analytics</h1>
    <p class="subtitle">Two years of order-level retail data (furniture, office supplies &amp; technology) cleaned and analyzed to surface revenue trends, top performers, and where the business is leaking margin.</p>
  </div>
</div>

<div class="wrap">

  <div class="kpi-row" id="kpiRow"></div>

  <div class="section">
    <div class="section-head">
      <div>
        <h2>Revenue &amp; Profit Trend</h2>
        <p>Monthly revenue with profit overlay — note the strong Nov/Dec seasonal peaks both years and a soft start to Q1.</p>
      </div>
    </div>
    <div class="card">
      <div class="chart-box tall"><canvas id="trendChart"></canvas></div>
    </div>
  </div>

  <div class="section">
    <div class="section-head">
      <div>
        <h2>Category &amp; Sub-Category Performance</h2>
        <p>Technology drives revenue and profit. Furniture is the largest single category by revenue but loses money overall.</p>
      </div>
    </div>
    <div class="grid-2">
      <div class="card">
        <h3>Revenue Share by Category</h3>
        <p class="desc">Share of total revenue, FY2024–25</p>
        <div class="chart-box"><canvas id="catRevChart"></canvas></div>
      </div>
      <div class="card">
        <h3>Profit by Category</h3>
        <p class="desc">Furniture is the only category operating at a net loss</p>
        <div class="chart-box"><canvas id="catProfitChart"></canvas></div>
      </div>
    </div>
    <div class="card" style="margin-top:20px;">
      <h3>Profit Margin % by Sub-Category</h3>
      <p class="desc">All four furniture sub-categories sit below zero margin — every Chairs, Sofas, Tables &amp; Bookcases sale currently loses money on average</p>
      <div class="chart-box tall"><canvas id="subcatChart"></canvas></div>
    </div>
  </div>

  <div class="section">
    <div class="section-head">
      <div>
        <h2>Top Products</h2>
        <p>Highest revenue-generating products. Hover bars for profit and units sold.</p>
      </div>
    </div>
    <div class="card">
      <div class="chart-box tall"><canvas id="topProductsChart"></canvas></div>
    </div>
  </div>

  <div class="section">
    <div class="section-head">
      <div>
        <h2>Regional &amp; Customer Segment View</h2>
        <p>West and East regions lead on revenue; East converts best to profit. Consumer segment is the largest by both revenue and order count.</p>
      </div>
    </div>
    <div class="grid-2">
      <div class="card">
        <h3>Revenue &amp; Margin by Region</h3>
        <div class="chart-box"><canvas id="regionChart"></canvas></div>
      </div>
      <div class="card">
        <h3>Revenue by Customer Segment</h3>
        <div class="chart-box"><canvas id="segmentChart"></canvas></div>
      </div>
    </div>
  </div>

  <div class="section">
    <div class="section-head">
      <div>
        <h2>Discounting Impact on Margin</h2>
        <p>Profitability turns negative once discounts exceed ~20% — a clear ceiling for promotional pricing.</p>
      </div>
    </div>
    <div class="card">
      <div class="chart-box"><canvas id="discountChart"></canvas></div>
    </div>
  </div>

  <div class="section">
    <div class="section-head">
      <div>
        <h2>Product Detail Table</h2>
        <p>All products ranked by revenue. Red profit values flag negative-margin items.</p>
      </div>
    </div>
    <div class="card">
      <div style="max-height:420px; overflow:auto;">
        <table id="productTable">
          <thead>
            <tr><th>Product</th><th class="num">Revenue</th><th class="num">Profit</th><th class="num">Units Sold</th><th class="num">Margin %</th></tr>
          </thead>
          <tbody></tbody>
        </table>
      </div>
    </div>
  </div>

  <div class="insights">
    <h2>Key Insights &amp; Recommendations</h2>
    <div class="insight-grid">
      <div class="insight-card">
        <span class="tag">Revenue Trend</span>
        <p>Revenue grew from <b>$133.7K</b> in Jan 2024 to a <b>$275.2K</b> peak in Nov 2025 — a clear upward trajectory with strong Nov/Dec seasonality (holiday buying) in both years, and a consistent Jan/Feb dip.</p>
      </div>
      <div class="insight-card warn">
        <span class="tag">Margin Risk · Furniture</span>
        <p>Furniture generates <b>38% of revenue ($1.51M)</b> but posts an overall <b>loss of -$60.5K (-4.0% margin)</b>. Chairs (-5.3%), Sofas (-4.2%), Bookcases (-3.6%) and Tables (-3.3%) are all unprofitable on average.</p>
      </div>
      <div class="insight-card rec">
        <span class="tag">Top Performer · Technology</span>
        <p>Technology is the profit engine: <b>56% of revenue</b> and <b>$247.9K profit (11.2% margin)</b>. Laptops alone contribute <b>$121.8K</b> profit. Ultrabook Pro 14 and Business Laptop 15 are the two highest-revenue products in the catalog.</p>
      </div>
      <div class="insight-card warn">
        <span class="tag">Discounting</span>
        <p>Average margin is healthy at 0–20% discount (5.9%–14.0%) but turns <b>negative beyond 20%</b> (-1.1% at 21–30%, -3.3% above 30%). Discounts above 20% are effectively subsidized sales.</p>
      </div>
      <div class="insight-card rec">
        <span class="tag">Regional Opportunity</span>
        <p><b>East region</b> has the best margin (6.6%) despite not having the highest revenue. <b>Central</b> is both the lowest-revenue ($507.9K) and lowest-margin (4.0%) region — a priority for sales investment or cost review.</p>
      </div>
      <div class="insight-card">
        <span class="tag">Customer Segments</span>
        <p>Consumer is the largest segment (<b>$1.96M revenue, $117.8K profit</b>) with the highest AOV ($947.55). Corporate and Home Office trail but show similar margin profiles — cross-sell potential via Technology accessories.</p>
      </div>
    </div>
  </div>

  <div class="footer">
    Generated for internal analysis · Data: simulated retail sales, Jan 2024 – Dec 2025 · Cleaned dataset: 4,200 orders
  </div>

</div>

<script>
const DATA = __DATA_JSON__;

const fmtMoney = (v, compact=true) => {
  if (compact && Math.abs(v) >= 1000) {
    return '$' + (v/1000).toFixed(1) + 'K';
  }
  return '$' + v.toLocaleString(undefined, {maximumFractionDigits:0});
};
const fmtFull = (v) => '$' + v.toLocaleString(undefined, {maximumFractionDigits:0});

// ---------- KPI cards ----------
const kpi = DATA.kpi;
const kpiRow = document.getElementById('kpiRow');
const kpiDefs = [
  {label:'Total Revenue', value: fmtFull(kpi.total_revenue), sub:'Jan 2024 – Dec 2025'},
  {label:'Total Profit', value: fmtFull(kpi.total_profit), sub: kpi.overall_margin_pct.toFixed(1)+'% overall margin'},
  {label:'Total Orders', value: kpi.total_orders.toLocaleString(), sub: kpi.total_units.toLocaleString()+' units sold'},
  {label:'Avg Order Value', value: '$'+kpi.avg_order_value.toFixed(0), sub:'per order'},
  {label:'Loss-Making Category', value:'Furniture', sub:'-4.0% margin · $1.51M revenue'},
];
kpiDefs.forEach(k=>{
  kpiRow.innerHTML += `<div class="kpi"><div class="label">${k.label}</div><div class="value">${k.value}</div><div class="sub">${k.sub}</div></div>`;
});

const PALETTE = {
  blue:'#2E75B6', blueSoft:'#9FC5E8', amber:'#F4A300', amberSoft:'#FBD79A',
  green:'#1F9D7C', red:'#D64545', navy:'#10243E', grid:'#E2E8F0'
};
Chart.defaults.font.family = "Inter, sans-serif";
Chart.defaults.color = '#5C6B80';
Chart.defaults.plugins.legend.labels.boxWidth = 14;
Chart.defaults.plugins.legend.labels.usePointStyle = true;

// ---------- Trend chart ----------
const monthly = DATA.monthly;
new Chart(document.getElementById('trendChart'), {
  type:'line',
  data:{
    labels: monthly.map(m=>m['Order Month']),
    datasets:[
      {label:'Revenue', data: monthly.map(m=>m.Revenue), borderColor:PALETTE.blue, backgroundColor:'rgba(46,117,182,0.08)', fill:true, tension:.35, yAxisID:'y', borderWidth:2.5, pointRadius:3},
      {label:'Profit', data: monthly.map(m=>m.Profit), borderColor:PALETTE.amber, backgroundColor:'rgba(244,163,0,0.06)', fill:true, tension:.35, yAxisID:'y1', borderWidth:2.5, pointRadius:3},
    ]
  },
  options:{
    responsive:true, maintainAspectRatio:false,
    interaction:{mode:'index', intersect:false},
    scales:{
      x:{grid:{display:false}},
      y:{position:'left', grid:{color:PALETTE.grid}, ticks:{callback:v=>fmtMoney(v)}, title:{display:true,text:'Revenue'}},
      y1:{position:'right', grid:{display:false}, ticks:{callback:v=>fmtMoney(v)}, title:{display:true,text:'Profit'}},
    },
    plugins:{ tooltip:{callbacks:{label:(ctx)=> ctx.dataset.label+': '+fmtFull(ctx.raw)}}}
  }
});

// ---------- Category charts ----------
const cat = DATA.category;
new Chart(document.getElementById('catRevChart'), {
  type:'doughnut',
  data:{ labels: cat.map(c=>c.Category), datasets:[{ data: cat.map(c=>c.Revenue), backgroundColor:[PALETTE.blue, PALETTE.amber, PALETTE.blueSoft], borderColor:'#fff', borderWidth:2 }]},
  options:{ responsive:true, maintainAspectRatio:false, plugins:{ tooltip:{callbacks:{label:(ctx)=> ctx.label+': '+fmtFull(ctx.raw)}}, legend:{position:'bottom'}}}
});

new Chart(document.getElementById('catProfitChart'), {
  type:'bar',
  data:{ labels: cat.map(c=>c.Category), datasets:[{ label:'Profit', data: cat.map(c=>c.Profit), backgroundColor: cat.map(c=>c.Profit>=0?PALETTE.blue:PALETTE.red), borderRadius:6 }]},
  options:{ responsive:true, maintainAspectRatio:false, plugins:{legend:{display:false}, tooltip:{callbacks:{label:(ctx)=>fmtFull(ctx.raw)}}}, scales:{ y:{ grid:{color:PALETTE.grid}, ticks:{callback:v=>fmtMoney(v)}}, x:{grid:{display:false}} }}
});

// ---------- Sub-category margin ----------
const subcat = DATA.subcategory.slice().sort((a,b)=> a['Margin %'] - b['Margin %']);
new Chart(document.getElementById('subcatChart'), {
  type:'bar',
  data:{ labels: subcat.map(s=>s['Sub-Category']+' ('+s.Category+')'), datasets:[{ label:'Margin %', data: subcat.map(s=>s['Margin %']), backgroundColor: subcat.map(s=>s['Margin %']<0?PALETTE.red:PALETTE.blue), borderRadius:5 }]},
  options:{ indexAxis:'y', responsive:true, maintainAspectRatio:false, plugins:{legend:{display:false}, tooltip:{callbacks:{label:(ctx)=> ctx.raw.toFixed(2)+'%'}}}, scales:{ x:{ grid:{color:PALETTE.grid}, ticks:{callback:v=>v+'%'}}, y:{grid:{display:false}} }}
});

// ---------- Top products ----------
const topN = DATA.top_products.slice(0,10).slice().reverse();
new Chart(document.getElementById('topProductsChart'), {
  type:'bar',
  data:{ labels: topN.map(p=>p['Product Name']), datasets:[{ label:'Revenue', data: topN.map(p=>p.Revenue), backgroundColor:PALETTE.blue, borderRadius:5 }]},
  options:{ indexAxis:'y', responsive:true, maintainAspectRatio:false,
    plugins:{legend:{display:false}, tooltip:{callbacks:{label:(ctx)=>{ const p=topN[ctx.dataIndex]; return [ 'Revenue: '+fmtFull(p.Revenue), 'Profit: '+fmtFull(p.Profit), 'Units: '+p.Units ];}}}},
    scales:{ x:{ grid:{color:PALETTE.grid}, ticks:{callback:v=>fmtMoney(v)}}, y:{grid:{display:false}} }}
});

// ---------- Region chart ----------
const region = DATA.region;
new Chart(document.getElementById('regionChart'), {
  data:{
    labels: region.map(r=>r.Region),
    datasets:[
      {type:'bar', label:'Revenue', data: region.map(r=>r.Revenue), backgroundColor:PALETTE.blue, yAxisID:'y', borderRadius:5, order:2},
      {type:'line', label:'Margin %', data: region.map(r=>r['Margin %']), borderColor:PALETTE.amber, backgroundColor:PALETTE.amber, yAxisID:'y1', tension:.3, borderWidth:2.5, pointRadius:4, order:1}
    ]
  },
  options:{ responsive:true, maintainAspectRatio:false,
    plugins:{ tooltip:{callbacks:{label:(ctx)=> ctx.dataset.label==='Margin %' ? 'Margin: '+ctx.raw.toFixed(2)+'%' : 'Revenue: '+fmtFull(ctx.raw) }}},
    scales:{ x:{grid:{display:false}}, y:{position:'left', grid:{color:PALETTE.grid}, ticks:{callback:v=>fmtMoney(v)}}, y1:{position:'right', grid:{display:false}, ticks:{callback:v=>v+'%'}} } }
});

// ---------- Segment chart ----------
const segment = DATA.segment;
new Chart(document.getElementById('segmentChart'), {
  type:'bar',
  data:{ labels: segment.map(s=>s['Customer Segment']), datasets:[
      {label:'Revenue', data: segment.map(s=>s.Revenue), backgroundColor:PALETTE.blue, borderRadius:5},
      {label:'Profit', data: segment.map(s=>s.Profit), backgroundColor:PALETTE.amber, borderRadius:5},
  ]},
  options:{ responsive:true, maintainAspectRatio:false, plugins:{tooltip:{callbacks:{label:(ctx)=> ctx.dataset.label+': '+fmtFull(ctx.raw)}}}, scales:{ y:{grid:{color:PALETTE.grid}, ticks:{callback:v=>fmtMoney(v)}}, x:{grid:{display:false}} }}
});

// ---------- Discount chart ----------
const disc = DATA.discount;
new Chart(document.getElementById('discountChart'), {
  type:'bar',
  data:{ labels: disc.map(d=>d['Discount Band']), datasets:[{ label:'Avg Margin %', data: disc.map(d=>d.AvgMargin), backgroundColor: disc.map(d=>d.AvgMargin<0?PALETTE.red:PALETTE.blue), borderRadius:6 }]},
  options:{ responsive:true, maintainAspectRatio:false, plugins:{legend:{display:false}, tooltip:{callbacks:{label:(ctx)=> ctx.raw.toFixed(2)+'%'}}}, scales:{ y:{grid:{color:PALETTE.grid}, ticks:{callback:v=>v+'%'}}, x:{grid:{display:false}} }}
});

// ---------- Product table ----------
const tbody = document.querySelector('#productTable tbody');
DATA.top_products.forEach(p=>{
  const margin = (p.Profit / p.Revenue * 100);
  const cls = p.Profit < 0 ? 'neg' : 'pos';
  tbody.innerHTML += `<tr><td>${p['Product Name']}</td><td class="num">${fmtFull(p.Revenue)}</td><td class="num ${cls}">${fmtFull(p.Profit)}</td><td class="num">${p.Units}</td><td class="num ${cls}">${margin.toFixed(1)}%</td></tr>`;
});
</script>
</body>
</html>
"""

html = html.replace("__DATA_JSON__", data_json)

with open("/home/claude/project/outputs/sales_dashboard.html", "w") as f:
    f.write(html)

print("Dashboard written, size:", len(html))
