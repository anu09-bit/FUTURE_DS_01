# FUTURE_DS_01
# 📊 Business Sales Performance Analytics

**Data Science & Analytics Internship — Task 1 (2026)**

End-to-end sales analytics project: data cleaning, exploratory analysis, an interactive dashboard, and a client-ready report — built on a 2-year simulated retail sales dataset (Superstore-style: Furniture, Office Supplies, Technology).

> 📥 **Quick links:** [Interactive Dashboard](dashboard/sales_dashboard.html) · [Full Report (Word)](report/Sales_Performance_Analytics_Report.docx) · [Clean Dataset](data/sales_data_clean.csv)

---

## 📁 Repository Structure

```
.
├── data/
│   ├── sales_data_raw.csv         # Raw data with intentional quality issues
│   └── sales_data_clean.csv       # Cleaned, analysis-ready dataset
├── scripts/
│   ├── generate_data.py           # Generates the simulated raw dataset
│   ├── analyze.py                 # Cleans data, computes KPIs, builds charts
│   ├── build_dashboard.py         # Builds the interactive HTML dashboard
│   └── build_report.js            # Builds the Word report
├── charts/                         # Static chart images (PNG) used in the report
├── dashboard/
│   └── sales_dashboard.html       # ⭐ Interactive dashboard — open in any browser
├── report/
│   └── Sales_Performance_Analytics_Report.docx   # Client-ready written report
└── README.md
```

---

## 📊 Dataset Overview

- **Period:** Jan 2024 – Dec 2025 (2 full years)
- **Records:** 4,200 cleaned order line items
- **Fields:** Order ID, Order Date, Customer Segment, Region, Category, Sub-Category, Product Name, Quantity, Unit Price, Discount, Sales, Profit, Ship Mode
- **Categories:** Furniture, Office Supplies, Technology
- **Regions:** North, South, East, West, Central
- **Customer Segments:** Consumer, Corporate, Home Office

The dataset is modeled on the structure of common public retail datasets (e.g., the Superstore dataset) so the same workflow applies directly to real business data — just swap in your own CSV with similar columns.

---

## 🧹 Data Cleaning Steps

1. Removed duplicate order records
2. Converted negative sales values (data-entry errors) to absolute values
3. Filled missing discount values with the category median
4. Standardized text fields (region, category, product names) to consistent capitalization
5. Parsed order dates and derived `Order Month`, `Profit Margin %`, and `Discount Band` fields

---

## 📈 Sample Visuals

| Monthly Revenue Trend | Category Profitability |
|---|---|
| ![Monthly Revenue Trend](charts/01_monthly_revenue_trend.png) | ![Category Performance](charts/04_category_performance.png) |

| Sub-Category Margins | Discount vs Margin |
|---|---|
| ![Sub-Category Margin](charts/05_subcategory_margin.png) | ![Discount vs Margin](charts/08_discount_vs_margin.png) |

See the [interactive dashboard](dashboard/sales_dashboard.html) for the full set of charts, KPIs, and a sortable product table.

---

## 🔑 Key Insights

- **Revenue is growing**, from $133.7K (Jan 2024) to a peak of $275.2K (Nov 2025), with strong Nov/Dec seasonal spikes both years and a consistent Jan/Feb dip.
- **Technology drives profit**: 56% of revenue and ~112% of net profit (offsetting losses elsewhere). Laptops alone contribute over $121K in profit.
- **Furniture is a structural loss-maker**: 38% of revenue but an overall loss of -$60.5K (-4.0% margin). Every Furniture sub-category (Chairs, Sofas, Bookcases, Tables) is unprofitable.
- **Discounts above 20% erode margin** — average margin turns negative beyond that threshold.
- **Regional gap**: East has the best margin (6.6%) without the highest revenue; Central is weakest on both revenue ($507.9K) and margin (4.0%).

---

## 💡 Top Recommendations

1. **Review Furniture pricing/supplier costs** — a 3–5% price adjustment could move the category to breakeven.
2. **Invest further in Technology** (especially Laptops & Phones) and bundle accessories to lift order value.
3. **Cap promotional discounts at 20%** and use value-adds (free shipping, bundles) instead of deeper discounts.
4. **Plan inventory/staffing around the Nov–Dec peak** and run Q1 promotions to smooth the seasonal dip.
5. **Investigate Central region operations** and use East's pricing discipline as a benchmark.

---

## 🚀 How to Use

### View the dashboard
Open `dashboard/sales_dashboard.html` in any web browser — or enable GitHub Pages on this repo and link directly to it. All data is embedded; charts use Chart.js via CDN, so an internet connection is needed only to load that library.

### Read the report
Open `report/Sales_Performance_Analytics_Report.docx` in Word, Google Docs, or LibreOffice. If prompted, click "Update Table" to populate the Table of Contents.

### Reproduce or extend the analysis
```bash
pip install pandas numpy matplotlib

# 1. Generate the sample dataset (skip if using your own data)
python3 scripts/generate_data.py

# 2. Clean the data and produce charts + aggregated tables
python3 scripts/analyze.py

# 3. Rebuild the interactive dashboard
python3 scripts/build_dashboard.py

# 4. Rebuild the Word report (requires Node.js + docx package)
npm install docx
node scripts/build_report.js
```

To analyze your own data, replace `data/sales_data_raw.csv` with your dataset (matching the column structure above) and re-run steps 2–4.

---

## 🛠️ Tools Used

- **Python (pandas, matplotlib)** — data cleaning, KPI calculation, chart generation
- **HTML/JavaScript (Chart.js)** — interactive dashboard
- **docx (Node.js)** — Word report generation

---

## 📌 Skills Demonstrated

- Data cleaning & preparation
- Business-focused KPI analysis (revenue, profit, margin, AOV)
- Trend and seasonality analysis
- Category, regional, and customer segment performance analysis
- Discount/promotion impact analysis
- Insight generation and business storytelling
- Dashboard and report design for non-technical stakeholders

