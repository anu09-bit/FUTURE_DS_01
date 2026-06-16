const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun,
  Header, Footer, AlignmentType, LevelFormat, HeadingLevel, BorderStyle,
  WidthType, ShadingType, VerticalAlign, PageNumber, PageBreak, TableOfContents,
  PositionalTab, PositionalTabAlignment, PositionalTabRelativeTo, PositionalTabLeader,
} = require("docx");

const agg = JSON.parse(fs.readFileSync("/home/claude/project/data/aggregated.json", "utf8"));
const CHARTS = "/home/claude/project/charts/";

const NAVY = "10243E";
const BLUE = "2E75B6";
const AMBER = "F4A300";
const RED = "C0392B";
const GREEN = "1F9D7C";
const MUTED = "6B7A8F";
const LINE = "E2E8F0";
const LIGHT_BLUE = "EAF2FA";

const money = (v, decimals=0) => {
  const n = Number(v);
  const abs = Math.abs(n).toLocaleString("en-US", {minimumFractionDigits: decimals, maximumFractionDigits: decimals});
  return (n < 0 ? "-$" : "$") + abs;
};
const pct = (v) => Number(v).toFixed(2) + "%";

// ---------- helpers ----------
function img(file, width, height, desc) {
  return new Paragraph({
    spacing: { before: 120, after: 60 },
    alignment: AlignmentType.CENTER,
    children: [new ImageRun({
      type: "png",
      data: fs.readFileSync(CHARTS + file),
      transformation: { width, height },
      altText: { title: desc, description: desc, name: desc },
    })],
  });
}
function caption(text) {
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 200 },
    children: [new TextRun({ text, italics: true, size: 18, color: MUTED })],
  });
}
function h1(text) {
  return new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun(text)] });
}
function h2(text) {
  return new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun(text)] });
}
function body(text, opts={}) {
  return new Paragraph({ spacing: { after: 160 }, children: [new TextRun({ text, ...opts })] });
}
function bullet(children) {
  return new Paragraph({ numbering: { reference: "bullets", level: 0 }, spacing: { after: 80 }, children });
}
function statRun(text, color) {
  return new TextRun({ text, bold: true, color });
}

const cellBorders = { top: {style:BorderStyle.SINGLE,size:1,color:LINE}, bottom:{style:BorderStyle.SINGLE,size:1,color:LINE}, left:{style:BorderStyle.SINGLE,size:1,color:LINE}, right:{style:BorderStyle.SINGLE,size:1,color:LINE} };
function tcell(text, opts={}) {
  return new TableCell({
    borders: cellBorders,
    width: { size: opts.width || 1560, type: WidthType.DXA },
    shading: opts.header ? { fill: NAVY, type: ShadingType.CLEAR } : (opts.fill ? { fill: opts.fill, type: ShadingType.CLEAR } : undefined),
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    verticalAlign: VerticalAlign.CENTER,
    children: [new Paragraph({
      alignment: opts.align || AlignmentType.LEFT,
      children: [new TextRun({ text: String(text), bold: !!opts.header, color: opts.header ? "FFFFFF" : (opts.color || "1A2433"), size: opts.size || 20 })]
    })]
  });
}

// ============================================================================
// COVER PAGE
// ============================================================================
const cover = [
  new Paragraph({ spacing: { before: 2400 }, children: [] }),
  new Paragraph({
    children: [new TextRun({ text: "BUSINESS SALES PERFORMANCE ANALYTICS", color: AMBER, bold: true, size: 22, characterSpacing: 30 })],
  }),
  new Paragraph({
    spacing: { before: 120, after: 120 },
    children: [new TextRun({ text: "Sales & Profitability Analysis Report", bold: true, size: 56, color: NAVY })],
  }),
  new Paragraph({
    spacing: { after: 600 },
    children: [new TextRun({ text: "FY2024–2025 · Furniture, Office Supplies & Technology Retail Dataset", size: 24, color: MUTED })],
  }),
  new Paragraph({
    border: { top: { style: BorderStyle.SINGLE, size: 6, color: BLUE, space: 8 } },
    spacing: { before: 800, after: 200 },
    children: [],
  }),
  new Paragraph({ spacing: { after: 40 }, children: [new TextRun({ text: "Prepared for: ", bold: true, size: 22 }), new TextRun({ text: "Business Owner / Leadership Team", size: 22 })] }),
  new Paragraph({ spacing: { after: 40 }, children: [new TextRun({ text: "Prepared by: ", bold: true, size: 22 }), new TextRun({ text: "Data Analytics Internship — Task 1", size: 22 })] }),
  new Paragraph({ spacing: { after: 40 }, children: [new TextRun({ text: "Reporting Period: ", bold: true, size: 22 }), new TextRun({ text: `${agg.report.date_min} to ${agg.report.date_max}`, size: 22 })] }),
  new Paragraph({ spacing: { after: 40 }, children: [new TextRun({ text: "Records Analyzed: ", bold: true, size: 22 }), new TextRun({ text: `${agg.report.clean_rows.toLocaleString()} cleaned order line items`, size: 22 })] }),
  new Paragraph({ children: [new PageBreak()] }),
];

// ============================================================================
// TABLE OF CONTENTS
// ============================================================================
const toc = [
  h1("Table of Contents"),
  new TableOfContents("Table of Contents", { hyperlink: true, headingStyleRange: "1-2" }),
  new Paragraph({ children: [new PageBreak()] }),
];

// ============================================================================
// EXECUTIVE SUMMARY
// ============================================================================
const execSummary = [
  h1("1. Executive Summary"),
  body(`Across the two-year period (${agg.report.date_min} to ${agg.report.date_max}), the business generated total revenue of ${money(agg.kpi.total_revenue)} from ${agg.kpi.total_orders.toLocaleString()} orders and ${agg.kpi.total_units.toLocaleString()} units sold, at an average order value of ${money(agg.kpi.avg_order_value,2)}. Overall profit reached ${money(agg.kpi.total_profit)}, an overall margin of ${pct(agg.kpi.overall_margin_pct)}.`),
  body("Revenue shows a clear upward trajectory with strong seasonal peaks in November and December of both years, driven primarily by the Technology category. However, the analysis surfaces one urgent issue: Furniture, the second-largest category by revenue, is operating at a net loss across every sub-category. This report breaks down where the money is being made, where it is being lost, and what actions would have the highest impact on profitability."),
  h2("Top-Line Numbers"),
];

// KPI table
const kpiTableRows = [
  new TableRow({ children: [tcell("Metric", {header:true, width: 4680}), tcell("Value", {header:true, width: 4680})] }),
  new TableRow({ children: [tcell("Total Revenue"), tcell(money(agg.kpi.total_revenue), {align: AlignmentType.RIGHT})] }),
  new TableRow({ children: [tcell("Total Profit"), tcell(money(agg.kpi.total_profit), {align: AlignmentType.RIGHT, color: "1F9D7C"})] }),
  new TableRow({ children: [tcell("Overall Profit Margin"), tcell(pct(agg.kpi.overall_margin_pct), {align: AlignmentType.RIGHT})] }),
  new TableRow({ children: [tcell("Total Orders"), tcell(agg.kpi.total_orders.toLocaleString(), {align: AlignmentType.RIGHT})] }),
  new TableRow({ children: [tcell("Total Units Sold"), tcell(agg.kpi.total_units.toLocaleString(), {align: AlignmentType.RIGHT})] }),
  new TableRow({ children: [tcell("Average Order Value"), tcell(money(agg.kpi.avg_order_value, 2), {align: AlignmentType.RIGHT})] }),
];
execSummary.push(new Table({ width: {size: 9360, type: WidthType.DXA}, columnWidths: [4680, 4680], rows: kpiTableRows }));
execSummary.push(new Paragraph({ children: [new PageBreak()] }));

// ============================================================================
// SECTION 2: DATA CLEANING
// ============================================================================
const r = agg.report;
const cleaning = [
  h1("2. Data Preparation & Cleaning"),
  body("Before analysis, the raw transactional dataset was reviewed and cleaned to ensure accurate, trustworthy results. Common real-world data quality issues were identified and resolved:"),
  bullet([new TextRun(`Removed `), statRun(`${r.duplicates_removed} duplicate order records`, NAVY), new TextRun(" that had been entered more than once.")]),
  bullet([new TextRun(`Corrected `), statRun(`${r.negative_sales_fixed} negative sales values`, NAVY), new TextRun(" caused by data-entry errors (converted to absolute values).")]),
  bullet([new TextRun(`Filled `), statRun(`${r.missing_discounts_filled} missing discount values`, NAVY), new TextRun(" using the median discount for the relevant product category.")]),
  bullet([new TextRun("Standardized text fields (region names, categories, product names) to consistent capitalization — e.g. fixed inconsistent casing such as \u201Cnorth\u201D vs \u201CNorth\u201D.")]),
  bullet([new TextRun("Parsed order dates into a proper date format and derived "), statRun("Order Month", NAVY), new TextRun(" and "), statRun("Profit Margin %", NAVY), new TextRun(" fields for trend and profitability analysis.")]),
  body(`The dataset started with ${r.raw_rows.toLocaleString()} rows and ${r.raw_cols} columns. After cleaning, the analysis-ready dataset contains ${r.clean_rows.toLocaleString()} rows and ${r.clean_cols} columns, covering the period ${r.date_min} to ${r.date_max}.`, {italics:true}),
  new Paragraph({ children: [new PageBreak()] }),
];

// ============================================================================
// SECTION 3: REVENUE TRENDS
// ============================================================================
const monthly = agg.monthly;
const firstMonth = monthly[0], lastMonth = monthly[monthly.length-1];
const peakMonth = monthly.reduce((a,b)=> b.Revenue > a.Revenue ? b : a);
const lowMonth = monthly.reduce((a,b)=> b.Revenue < a.Revenue ? b : a);

const trends = [
  h1("3. Revenue Trends Over Time"),
  body(`Monthly revenue rose from ${money(firstMonth.Revenue)} in ${firstMonth["Order Month"]} to ${money(lastMonth.Revenue)} in ${lastMonth["Order Month"]}. The strongest month was ${peakMonth["Order Month"]} at ${money(peakMonth.Revenue)}, while the weakest was ${lowMonth["Order Month"]} at ${money(lowMonth.Revenue)}.`),
  img("01_monthly_revenue_trend.png", 624, 307, "Monthly revenue trend chart"),
  caption("Figure 1: Monthly revenue trend, Jan 2024 – Dec 2025"),
  body("A consistent seasonal pattern is visible in both years: revenue dips in January–February, builds steadily through the middle of the year, and peaks sharply in November–December — the typical holiday buying season for office and technology equipment."),
  img("02_yoy_revenue_comparison.png", 624, 307, "Year over year monthly revenue comparison"),
  caption("Figure 2: Year-over-year monthly revenue comparison"),
  body("Comparing 2024 to 2025 month-by-month, most months in 2025 outperform their 2024 equivalent, particularly from September onward — indicating the business is on a growth trajectory heading into the next holiday season."),
];

// ============================================================================
// SECTION 4: TOP PRODUCTS
// ============================================================================
const top10 = agg.top_products.slice(0,10);
const topProductRows = [
  new TableRow({ children: [
    tcell("Rank", {header:true, width: 700, align: AlignmentType.CENTER}),
    tcell("Product", {header:true, width: 3460}),
    tcell("Revenue", {header:true, width: 1800, align: AlignmentType.RIGHT}),
    tcell("Profit", {header:true, width: 1800, align: AlignmentType.RIGHT}),
    tcell("Units Sold", {header:true, width: 1600, align: AlignmentType.RIGHT}),
  ]}),
];
top10.forEach((p, i) => {
  const profitColor = p.Profit < 0 ? RED : "1A2433";
  topProductRows.push(new TableRow({ children: [
    tcell(i+1, {align: AlignmentType.CENTER, fill: i%2===0?LIGHT_BLUE:undefined}),
    tcell(p["Product Name"], {fill: i%2===0?LIGHT_BLUE:undefined}),
    tcell(money(p.Revenue), {align: AlignmentType.RIGHT, fill: i%2===0?LIGHT_BLUE:undefined}),
    tcell(money(p.Profit), {align: AlignmentType.RIGHT, color: profitColor, fill: i%2===0?LIGHT_BLUE:undefined}),
    tcell(p.Units, {align: AlignmentType.RIGHT, fill: i%2===0?LIGHT_BLUE:undefined}),
  ]}));
});

const topProducts = [
  h1("4. Top-Selling Products"),
  body(`The top 10 products by revenue account for a substantial share of total sales. Notably, two of the top five products by revenue — the 2-Seater Sofa and Reception Sofa — are loss-making, generating combined revenue of ${money(top10[0].Revenue + top10.find(p=>p["Product Name"]==="Reception Sofa").Revenue)} but a combined loss of ${money(top10[0].Profit + top10.find(p=>p["Product Name"]==="Reception Sofa").Profit)}.`),
  img("03_top10_products_revenue.png", 624, 342, "Top 10 products by revenue chart"),
  caption("Figure 3: Top 10 products ranked by total revenue"),
  new Table({ width: {size: 9360, type: WidthType.DXA}, columnWidths: [700, 3460, 1800, 1800, 1600], rows: topProductRows }),
  caption("Table 1: Top 10 products — revenue, profit, and units sold (red = loss-making)"),
  new Paragraph({ children: [new PageBreak()] }),
];

// ============================================================================
// SECTION 5: CATEGORY & SUB-CATEGORY
// ============================================================================
const cat = agg.category;
const subcat = agg.subcategory.slice().sort((a,b)=>a["Margin %"]-b["Margin %"]);
const catRows = [
  new TableRow({ children: [
    tcell("Category", {header:true, width: 2800}),
    tcell("Revenue", {header:true, width: 2200, align: AlignmentType.RIGHT}),
    tcell("Profit", {header:true, width: 2200, align: AlignmentType.RIGHT}),
    tcell("Margin %", {header:true, width: 2160, align: AlignmentType.RIGHT}),
  ]}),
];
cat.forEach((c,i)=>{
  const color = c.Profit < 0 ? RED : "1A2433";
  catRows.push(new TableRow({ children: [
    tcell(c.Category, {fill: i%2===0?LIGHT_BLUE:undefined}),
    tcell(money(c.Revenue), {align: AlignmentType.RIGHT, fill: i%2===0?LIGHT_BLUE:undefined}),
    tcell(money(c.Profit), {align: AlignmentType.RIGHT, color, fill: i%2===0?LIGHT_BLUE:undefined}),
    tcell(pct(c["Margin %"]), {align: AlignmentType.RIGHT, color, fill: i%2===0?LIGHT_BLUE:undefined}),
  ]}));
});

const categorySection = [
  h1("5. Category & Sub-Category Profitability"),
  body("Technology dominates both revenue and profit, contributing 56% of total revenue and over 100% of total profit (offsetting losses elsewhere). Office Supplies is the smallest category by revenue but has the healthiest profit margin. Furniture, despite being the second-largest category by revenue, is the only category losing money overall."),
  img("04_category_performance.png", 624, 260, "Category revenue share and profit chart"),
  caption("Figure 4: Revenue share and profit by category"),
  new Table({ width: {size: 9360, type: WidthType.DXA}, columnWidths: [2800,2200,2200,2160], rows: catRows }),
  caption("Table 2: Category-level revenue, profit, and margin"),
  h2("Sub-Category Margin Breakdown"),
  body(`Drilling into sub-categories reveals the source of the Furniture loss: all four Furniture sub-categories — Chairs (${pct(subcat[0]["Margin %"])}), Sofas (${pct(subcat[1]["Margin %"])}), Bookcases (${pct(subcat[2]["Margin %"])}), and Tables (${pct(subcat[3]["Margin %"])}) — operate at negative margins. By contrast, every Technology and Office Supplies sub-category is profitable, with Storage (${pct(subcat[subcat.length-1]["Margin %"]) }) the strongest performer.`),
  img("05_subcategory_margin.png", 624, 342, "Sub-category profit margin chart"),
  caption("Figure 5: Profit margin % by sub-category (red = loss-making)"),
];

// ============================================================================
// SECTION 6: REGIONAL PERFORMANCE
// ============================================================================
const region = agg.region;
const regionRows = [
  new TableRow({ children: [
    tcell("Region", {header:true, width: 2340}),
    tcell("Revenue", {header:true, width: 2340, align: AlignmentType.RIGHT}),
    tcell("Profit", {header:true, width: 2340, align: AlignmentType.RIGHT}),
    tcell("Margin %", {header:true, width: 2340, align: AlignmentType.RIGHT}),
  ]}),
];
region.forEach((rg,i)=>{
  regionRows.push(new TableRow({ children: [
    tcell(rg.Region, {fill: i%2===0?LIGHT_BLUE:undefined}),
    tcell(money(rg.Revenue), {align: AlignmentType.RIGHT, fill: i%2===0?LIGHT_BLUE:undefined}),
    tcell(money(rg.Profit), {align: AlignmentType.RIGHT, fill: i%2===0?LIGHT_BLUE:undefined}),
    tcell(pct(rg["Margin %"]), {align: AlignmentType.RIGHT, fill: i%2===0?LIGHT_BLUE:undefined}),
  ]}));
});

const topRegion = region[0];
const bestMarginRegion = region.slice().sort((a,b)=>b["Margin %"]-a["Margin %"])[0];
const worstRegion = region[region.length-1];

const regionalSection = [
  new Paragraph({ children: [new PageBreak()] }),
  h1("6. Regional Performance"),
  body(`${topRegion.Region} is the highest-revenue region at ${money(topRegion.Revenue)}, closely followed by East and South. ${bestMarginRegion.Region} has the best profit margin at ${pct(bestMarginRegion["Margin %"])}, while ${worstRegion.Region} trails both in revenue (${money(worstRegion.Revenue)}) and margin (${pct(worstRegion["Margin %"])}).`),
  img("06_regional_performance.png", 624, 251, "Regional revenue and margin chart"),
  caption("Figure 6: Revenue and profit margin by region"),
  new Table({ width: {size: 9360, type: WidthType.DXA}, columnWidths: [2340,2340,2340,2340], rows: regionRows }),
  caption("Table 3: Regional revenue, profit, and margin"),
  new Paragraph({ children: [new PageBreak()] }),
];

// ============================================================================
// SECTION 7: CUSTOMER SEGMENTS
// ============================================================================
const segment = agg.segment;
const segmentSection = [
  h1("7. Customer Segment Analysis"),
  body(`The Consumer segment is the largest, generating ${money(segment[0].Revenue)} in revenue and ${money(segment[0].Profit)} in profit from ${segment[0].Orders.toLocaleString()} orders (AOV ${money(segment[0].AOV,2)}). Corporate and Home Office follow with broadly similar margin profiles, suggesting an opportunity for targeted bundles (e.g., Technology accessories) to lift order value in these segments.`),
  img("07_segment_performance.png", 624, 347, "Customer segment revenue chart"),
  caption("Figure 7: Revenue by customer segment (with average order value)"),
  new Paragraph({ children: [new PageBreak()] }),
];

// ============================================================================
// SECTION 8: DISCOUNTING
// ============================================================================
const disc = agg.discount;
const discountSection = [
  h1("8. Discounting Strategy & Margin Impact"),
  body("Discounting has a direct and measurable effect on profitability. Orders with no discount or modest discounts (up to 20%) remain profitable on average, but margins turn negative once discounts exceed 20% — meaning every sale at that discount level currently costs the business money after accounting for cost of goods."),
  img("08_discount_vs_margin.png", 624, 347, "Discount band vs average profit margin chart"),
  caption("Figure 8: Average profit margin % by discount band"),
  body(`Specifically: 0% discount orders average ${pct(disc[0].AvgMargin)} margin, while orders discounted above 30% average ${pct(disc[disc.length-1].AvgMargin)} margin. This establishes a practical ceiling of roughly 20% for promotional discounting without eroding profitability.`),
  new Paragraph({ children: [new PageBreak()] }),
];

// ============================================================================
// SECTION 9: INSIGHTS & RECOMMENDATIONS
// ============================================================================
const insights = [
  h1("9. Key Insights & Recommendations"),
  h2("Insight 1 — Furniture is a structural loss-maker"),
  body("Every Furniture sub-category (Chairs, Sofas, Bookcases, Tables) operates at a negative margin, costing the business roughly $60,500 over two years despite contributing 38% of revenue."),
  bullet([new TextRun("Recommendation: "), statRun("Review supplier costs and pricing for Furniture.", NAVY), new TextRun(" Even a modest price increase (3-5%) or renegotiated supplier costs could move this category to breakeven or profitability.")]),
  bullet([new TextRun("Recommendation: "), statRun("Audit Furniture discounting policy", NAVY), new TextRun(" — combined with Insight 3 below, Furniture items may be over-discounted relative to their margin structure.")]),

  h2("Insight 2 — Technology is the business's profit engine"),
  body("Technology contributes 56% of revenue and effectively all of the company's net profit (Furniture losses are offset by Technology and Office Supplies gains). Laptops alone generated over $121,000 in profit."),
  bullet([new TextRun("Recommendation: "), statRun("Increase marketing spend and inventory investment in Technology", NAVY), new TextRun(", particularly Laptops and Phones, which show both high revenue and strong margins.")]),
  bullet([new TextRun("Recommendation: "), statRun("Bundle Technology accessories with Laptop/Phone purchases", NAVY), new TextRun(" to lift average order value across all customer segments.")]),

  h2("Insight 3 — Discounts above 20% are unprofitable"),
  body("Average profit margin turns negative once discounts exceed 20%, and worsens further beyond 30%."),
  bullet([new TextRun("Recommendation: "), statRun("Cap standard promotional discounts at 20%", NAVY), new TextRun(", and require manager approval for any discount above this threshold.")]),
  bullet([new TextRun("Recommendation: "), statRun("Replace deep discounts with value-adds", NAVY), new TextRun(" (e.g., free shipping, bundled accessories) that drive sales without directly eroding the price.")]),

  h2("Insight 4 — Revenue is growing but seasonal"),
  body("Revenue grew year-over-year for most months, with sharp peaks in November-December and consistent dips in January-February."),
  bullet([new TextRun("Recommendation: "), statRun("Plan inventory and staffing around the Nov-Dec peak", NAVY), new TextRun(" to avoid stockouts during the highest-revenue period.")]),
  bullet([new TextRun("Recommendation: "), statRun("Run targeted Q1 promotions", NAVY), new TextRun(" (within the 20% discount cap) to smooth the January-February revenue dip.")]),

  h2("Insight 5 — Central region underperforms"),
  body("Central has both the lowest revenue ($507,900) and the lowest profit margin (4.0%) of all five regions, while East achieves the best margin (6.6%) without leading on revenue."),
  bullet([new TextRun("Recommendation: "), statRun("Investigate Central region operations", NAVY), new TextRun(" — review pricing, shipping costs, and sales coverage to understand the margin gap versus East.")]),
  bullet([new TextRun("Recommendation: "), statRun("Apply East region's pricing/discount discipline", NAVY), new TextRun(" as a benchmark for other regions.")]),
];

// ============================================================================
// SECTION 10: METHODOLOGY
// ============================================================================
const methodology = [
  h1("10. Methodology & Notes"),
  h2("Data Source"),
  body("This analysis uses a simulated retail sales dataset (2024-2025) modeled on the structure of common public sales datasets (e.g., Superstore-style: Order Date, Region, Category, Sub-Category, Product, Sales, Profit, Discount, Customer Segment). The dataset was generated to reflect realistic seasonal patterns, category mixes, and profitability dynamics for demonstration purposes. The same cleaning and analysis workflow applies directly to real business data — simply replace the source file with actual sales records."),
  h2("Tools Used"),
  bullet([new TextRun("Python (pandas) for data cleaning, aggregation, and KPI calculation")]),
  bullet([new TextRun("Matplotlib for static chart generation")]),
  bullet([new TextRun("HTML/JavaScript (Chart.js) for the interactive dashboard")]),
  bullet([new TextRun("docx for this report")]),
  h2("Key Definitions"),
  bullet([new TextRun("Revenue / Sales: Total sale amount after discount, before cost of goods")]),
  bullet([new TextRun("Profit: Revenue minus cost of goods (can be negative)")]),
  bullet([new TextRun("Profit Margin %: Profit ÷ Revenue × 100")]),
  bullet([new TextRun("AOV (Average Order Value): Total revenue ÷ number of unique orders")]),
];

// ============================================================================
// DOCUMENT ASSEMBLY
// ============================================================================
const doc = new Document({
  creator: "Data Analytics Internship",
  title: "Business Sales Performance Analytics Report",
  styles: {
    default: { document: { run: { font: "Arial", size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 30, bold: true, font: "Arial", color: "10243E" },
        paragraph: { spacing: { before: 280, after: 160 }, outlineLevel: 0,
          border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "2E75B6", space: 4 } } } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 24, bold: true, font: "Arial", color: "2E75B6" },
        paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 1 } },
    ],
  },
  numbering: {
    config: [
      { reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    ],
  },
  sections: [{
    properties: {
      page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } },
    },
    headers: {
      default: new Header({ children: [
        new Paragraph({
          tabStops: [{ type: "right", position: 9360 }],
          children: [
            new TextRun({ text: "Sales Performance Analytics", size: 16, color: MUTED }),
            new TextRun({ text: "\tFY2024–2025", size: 16, color: MUTED }),
          ],
        }),
      ]}),
    },
    footers: {
      default: new Footer({ children: [
        new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({ text: "Page ", size: 16, color: MUTED }),
            new TextRun({ children: [PageNumber.CURRENT], size: 16, color: MUTED }),
            new TextRun({ text: " of ", size: 16, color: MUTED }),
            new TextRun({ children: [PageNumber.TOTAL_PAGES], size: 16, color: MUTED }),
          ],
        }),
      ]}),
    },
    children: [
      ...cover,
      ...toc,
      ...execSummary,
      ...cleaning,
      ...trends,
      ...topProducts,
      ...categorySection,
      ...regionalSection,
      ...segmentSection,
      ...discountSection,
      ...insights,
      ...methodology,
    ],
  }],
});

Packer.toBuffer(doc).then((buffer) => {
  fs.writeFileSync("/home/claude/project/outputs/Sales_Performance_Analytics_Report.docx", buffer);
  console.log("Report written.");
});
