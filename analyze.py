import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import json

plt.rcParams.update({
    "figure.dpi": 150,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "font.size": 11,
})

COLOR_PRIMARY = "#2E75B6"
COLOR_ACCENT = "#F4A300"
COLOR_NEG = "#D64545"
PALETTE = ["#2E75B6", "#5BA3D0", "#88C0E8", "#F4A300", "#F2C879", "#8AA0B5"]

# ---------------------------------------------------------------------------
# 1. LOAD + CLEAN
# ---------------------------------------------------------------------------
df = pd.read_csv("/home/claude/project/data/sales_data_raw.csv")
report = {}
report["raw_rows"] = len(df)
report["raw_cols"] = df.shape[1]

# Remove exact duplicate rows
dupes = df.duplicated().sum()
df = df.drop_duplicates().reset_index(drop=True)
report["duplicates_removed"] = int(dupes)

# Standardize text fields (casing/whitespace)
for col in ["Region", "Category", "Sub-Category", "Product Name", "Customer Segment", "Ship Mode"]:
    df[col] = df[col].astype(str).str.strip().str.title()

# Parse dates
df["Order Date"] = pd.to_datetime(df["Order Date"])

# Fix negative sales (data entry errors) -> take absolute value
neg_sales = (df["Sales"] < 0).sum()
df["Sales"] = df["Sales"].abs()
report["negative_sales_fixed"] = int(neg_sales)

# Handle missing discounts -> fill with category median discount
missing_disc = df["Discount"].isna().sum()
df["Discount"] = df["Discount"].fillna(df.groupby("Category")["Discount"].transform("median"))
report["missing_discounts_filled"] = int(missing_disc)

# Derived columns
df["Order Year"] = df["Order Date"].dt.year
df["Order Month"] = df["Order Date"].dt.to_period("M").astype(str)
df["Profit Margin %"] = (df["Profit"] / df["Sales"] * 100).round(2)

report["clean_rows"] = len(df)
report["clean_cols"] = df.shape[1]
report["date_min"] = df["Order Date"].min().strftime("%Y-%m-%d")
report["date_max"] = df["Order Date"].max().strftime("%Y-%m-%d")

df.to_csv("/home/claude/project/data/sales_data_clean.csv", index=False)

# ---------------------------------------------------------------------------
# 2. KPI SUMMARY
# ---------------------------------------------------------------------------
kpi = {
    "total_revenue": float(df["Sales"].sum()),
    "total_profit": float(df["Profit"].sum()),
    "total_orders": int(df["Order ID"].nunique()),
    "total_units": int(df["Quantity"].sum()),
    "avg_order_value": float(df["Sales"].sum() / df["Order ID"].nunique()),
    "overall_margin_pct": float(df["Profit"].sum() / df["Sales"].sum() * 100),
}

# ---------------------------------------------------------------------------
# 3. REVENUE TRENDS OVER TIME (monthly)
# ---------------------------------------------------------------------------
monthly = df.groupby("Order Month").agg(Revenue=("Sales", "sum"), Profit=("Profit", "sum"),
                                         Orders=("Order ID", "nunique")).reset_index()
monthly["Order Month"] = monthly["Order Month"].astype(str)

fig, ax1 = plt.subplots(figsize=(9, 4.5))
ax1.plot(monthly["Order Month"], monthly["Revenue"], marker="o", color=COLOR_PRIMARY, label="Revenue", linewidth=2)
ax1.fill_between(monthly["Order Month"], monthly["Revenue"], alpha=0.08, color=COLOR_PRIMARY)
ax1.set_ylabel("Revenue ($)")
ax1.set_title("Monthly Revenue Trend (2024-2025)", fontsize=13, fontweight="bold")
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax1.set_xticks(range(0, len(monthly), 2))
ax1.set_xticklabels(monthly["Order Month"][::2], rotation=45, ha="right")
plt.tight_layout()
plt.savefig("/home/claude/project/charts/01_monthly_revenue_trend.png", bbox_inches="tight")
plt.close()

# YoY comparison
monthly["Year"] = monthly["Order Month"].str[:4]
monthly["MonthNum"] = monthly["Order Month"].str[5:7]
yoy = monthly.pivot(index="MonthNum", columns="Year", values="Revenue")

fig, ax = plt.subplots(figsize=(9, 4.5))
month_names = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
x = np.arange(len(yoy.index))
width = 0.38
for i, year in enumerate(yoy.columns):
    ax.bar(x + (i - 0.5) * width, yoy[year], width=width, label=year,
           color=PALETTE[i % len(PALETTE)])
ax.set_xticks(x)
ax.set_xticklabels([month_names[int(m)-1] for m in yoy.index])
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.set_title("Year-over-Year Monthly Revenue Comparison", fontsize=13, fontweight="bold")
ax.legend(title="Year")
plt.tight_layout()
plt.savefig("/home/claude/project/charts/02_yoy_revenue_comparison.png", bbox_inches="tight")
plt.close()

# ---------------------------------------------------------------------------
# 4. TOP-SELLING PRODUCTS
# ---------------------------------------------------------------------------
top_products = df.groupby("Product Name").agg(Revenue=("Sales", "sum"), Profit=("Profit", "sum"),
                                               Units=("Quantity", "sum")).sort_values("Revenue", ascending=False)
top10 = top_products.head(10).reset_index()

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.barh(top10["Product Name"][::-1], top10["Revenue"][::-1], color=COLOR_PRIMARY)
ax.set_title("Top 10 Products by Revenue", fontsize=13, fontweight="bold")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
for bar, val in zip(bars, top10["Revenue"][::-1]):
    ax.text(val, bar.get_y() + bar.get_height()/2, f" ${val:,.0f}", va="center", fontsize=9)
plt.tight_layout()
plt.savefig("/home/claude/project/charts/03_top10_products_revenue.png", bbox_inches="tight")
plt.close()

# ---------------------------------------------------------------------------
# 5. CATEGORY PERFORMANCE
# ---------------------------------------------------------------------------
cat_perf = df.groupby("Category").agg(Revenue=("Sales", "sum"), Profit=("Profit", "sum"),
                                       Orders=("Order ID", "nunique")).reset_index()
cat_perf["Margin %"] = (cat_perf["Profit"] / cat_perf["Revenue"] * 100).round(2)
cat_perf = cat_perf.sort_values("Revenue", ascending=False)

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
axes[0].pie(cat_perf["Revenue"], labels=cat_perf["Category"], autopct="%1.0f%%",
            colors=PALETTE[:len(cat_perf)], startangle=120,
            wedgeprops={"edgecolor": "white", "linewidth": 1.5})
axes[0].set_title("Revenue Share by Category", fontsize=12, fontweight="bold")

colors_profit = [COLOR_PRIMARY if v >= 0 else COLOR_NEG for v in cat_perf["Profit"]]
bars = axes[1].bar(cat_perf["Category"], cat_perf["Profit"], color=colors_profit)
axes[1].axhline(0, color="black", linewidth=0.8)
axes[1].set_title("Profit by Category", fontsize=12, fontweight="bold")
axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
for bar, val in zip(bars, cat_perf["Profit"]):
    axes[1].text(bar.get_x() + bar.get_width()/2, val, f"${val:,.0f}",
                  ha="center", va="bottom" if val >= 0 else "top", fontsize=9)
plt.tight_layout()
plt.savefig("/home/claude/project/charts/04_category_performance.png", bbox_inches="tight")
plt.close()

# Sub-category profitability (to spot loss-makers)
subcat_perf = df.groupby(["Category", "Sub-Category"]).agg(
    Revenue=("Sales", "sum"), Profit=("Profit", "sum")).reset_index()
subcat_perf["Margin %"] = (subcat_perf["Profit"] / subcat_perf["Revenue"] * 100).round(2)
subcat_perf = subcat_perf.sort_values("Margin %")

fig, ax = plt.subplots(figsize=(9, 5))
colors_sub = [COLOR_NEG if v < 0 else COLOR_PRIMARY for v in subcat_perf["Margin %"]]
ax.barh(subcat_perf["Sub-Category"], subcat_perf["Margin %"], color=colors_sub)
ax.axvline(0, color="black", linewidth=0.8)
ax.set_title("Profit Margin % by Sub-Category", fontsize=13, fontweight="bold")
ax.set_xlabel("Profit Margin (%)")
plt.tight_layout()
plt.savefig("/home/claude/project/charts/05_subcategory_margin.png", bbox_inches="tight")
plt.close()

# ---------------------------------------------------------------------------
# 6. REGIONAL PERFORMANCE
# ---------------------------------------------------------------------------
region_perf = df.groupby("Region").agg(Revenue=("Sales", "sum"), Profit=("Profit", "sum"),
                                        Orders=("Order ID", "nunique")).reset_index()
region_perf["Margin %"] = (region_perf["Profit"] / region_perf["Revenue"] * 100).round(2)
region_perf = region_perf.sort_values("Revenue", ascending=False)

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
axes[0].bar(region_perf["Region"], region_perf["Revenue"], color=COLOR_PRIMARY)
axes[0].set_title("Revenue by Region", fontsize=12, fontweight="bold")
axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

axes[1].bar(region_perf["Region"], region_perf["Margin %"], color=COLOR_ACCENT)
axes[1].set_title("Profit Margin % by Region", fontsize=12, fontweight="bold")
axes[1].set_ylabel("Margin %")
plt.tight_layout()
plt.savefig("/home/claude/project/charts/06_regional_performance.png", bbox_inches="tight")
plt.close()

# ---------------------------------------------------------------------------
# 7. CUSTOMER SEGMENT ANALYSIS
# ---------------------------------------------------------------------------
seg_perf = df.groupby("Customer Segment").agg(Revenue=("Sales", "sum"), Profit=("Profit", "sum"),
                                               Orders=("Order ID", "nunique")).reset_index()
seg_perf["AOV"] = (seg_perf["Revenue"] / seg_perf["Orders"]).round(2)
seg_perf = seg_perf.sort_values("Revenue", ascending=False)

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.bar(seg_perf["Customer Segment"], seg_perf["Revenue"], color=PALETTE[:len(seg_perf)])
ax.set_title("Revenue by Customer Segment", fontsize=13, fontweight="bold")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
for i, (rev, aov) in enumerate(zip(seg_perf["Revenue"], seg_perf["AOV"])):
    ax.text(i, rev, f"${rev:,.0f}\nAOV ${aov:,.0f}", ha="center", va="bottom", fontsize=9)
plt.tight_layout()
plt.savefig("/home/claude/project/charts/07_segment_performance.png", bbox_inches="tight")
plt.close()

# ---------------------------------------------------------------------------
# 8. DISCOUNT vs PROFIT MARGIN
# ---------------------------------------------------------------------------
disc_bins = [-0.01, 0.001, 0.1, 0.2, 0.3, 1.0]
disc_labels = ["0%", "1-10%", "11-20%", "21-30%", ">30%"]
df["Discount Band"] = pd.cut(df["Discount"], bins=disc_bins, labels=disc_labels)
disc_perf = df.groupby("Discount Band").agg(AvgMargin=("Profit Margin %", "mean"),
                                             Revenue=("Sales", "sum")).reset_index()

fig, ax = plt.subplots(figsize=(8, 4.5))
colors_d = [COLOR_NEG if v < 0 else COLOR_PRIMARY for v in disc_perf["AvgMargin"]]
ax.bar(disc_perf["Discount Band"].astype(str), disc_perf["AvgMargin"], color=colors_d)
ax.axhline(0, color="black", linewidth=0.8)
ax.set_title("Average Profit Margin % by Discount Band", fontsize=13, fontweight="bold")
ax.set_ylabel("Avg Profit Margin %")
plt.tight_layout()
plt.savefig("/home/claude/project/charts/08_discount_vs_margin.png", bbox_inches="tight")
plt.close()

# ---------------------------------------------------------------------------
# SAVE AGGREGATED TABLES FOR DASHBOARD + REPORT
# ---------------------------------------------------------------------------
agg = {
    "kpi": kpi,
    "report": report,
    "monthly": monthly[["Order Month", "Revenue", "Profit", "Orders"]].to_dict(orient="records"),
    "top_products": top_products.reset_index().to_dict(orient="records"),
    "category": cat_perf.to_dict(orient="records"),
    "subcategory": subcat_perf.to_dict(orient="records"),
    "region": region_perf.to_dict(orient="records"),
    "segment": seg_perf.to_dict(orient="records"),
    "discount": disc_perf.assign(**{"Discount Band": disc_perf["Discount Band"].astype(str)}).to_dict(orient="records"),
}

with open("/home/claude/project/data/aggregated.json", "w") as f:
    json.dump(agg, f, indent=2, default=str)

print("KPI:", kpi)
print("\nData quality report:", report)
print("\nCategory performance:\n", cat_perf)
print("\nSub-category margins:\n", subcat_perf)
print("\nRegion performance:\n", region_perf)
print("\nSegment performance:\n", seg_perf)
print("\nTop 5 products:\n", top10.head())
print("\nMonthly (first/last 3):\n", monthly.head(3), "\n", monthly.tail(3))
