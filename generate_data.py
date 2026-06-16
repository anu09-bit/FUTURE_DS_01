import pandas as pd
import numpy as np

np.random.seed(42)

# --- Reference data -------------------------------------------------------
regions = ["North", "South", "East", "West", "Central"]

categories = {
    "Furniture": ["Chairs", "Tables", "Bookcases", "Sofas"],
    "Office Supplies": ["Binders", "Paper", "Storage", "Art Supplies", "Pens"],
    "Technology": ["Phones", "Laptops", "Accessories", "Printers"],
}

products = {
    "Chairs": ["Ergo Office Chair", "Mesh Task Chair", "Executive Leather Chair"],
    "Tables": ["Conference Table", "Standing Desk", "Round Meeting Table"],
    "Bookcases": ["5-Shelf Bookcase", "Corner Bookcase"],
    "Sofas": ["2-Seater Sofa", "Reception Sofa"],
    "Binders": ["Heavy Duty Binder", "View Binder 2-inch", "Round Ring Binder"],
    "Paper": ["Copy Paper A4 (Ream)", "Sticky Notes Pack", "Notebook Pack"],
    "Storage": ["File Cabinet", "Storage Box (Pack of 5)", "Plastic Drawer Unit"],
    "Art Supplies": ["Marker Set", "Sketch Pad", "Color Pencil Set"],
    "Pens": ["Gel Pen Pack", "Permanent Marker Pack", "Highlighter Set"],
    "Phones": ["Smartphone X12", "Smartphone Lite", "Office Cordless Phone"],
    "Laptops": ["UltraBook Pro 14", "Business Laptop 15", "ChromeBook Edu"],
    "Accessories": ["Wireless Mouse", "Bluetooth Keyboard", "USB-C Hub", "Laptop Sleeve"],
    "Printers": ["LaserJet Printer", "All-in-One InkJet Printer", "Label Printer"],
}

# Base unit price ranges per sub-category (min, max)
price_ranges = {
    "Chairs": (90, 450), "Tables": (150, 900), "Bookcases": (120, 500), "Sofas": (300, 1200),
    "Binders": (3, 25), "Paper": (4, 30), "Storage": (15, 150), "Art Supplies": (5, 60), "Pens": (3, 20),
    "Phones": (60, 900), "Laptops": (400, 1800), "Accessories": (10, 120), "Printers": (80, 600),
}

# Category-level cost margin ranges (gives realistic profit/loss incl. some loss-makers)
margin_ranges = {
    "Furniture": (-0.20, 0.20),
    "Office Supplies": (0.05, 0.35),
    "Technology": (0.00, 0.30),
}

segments = ["Consumer", "Corporate", "Home Office"]
ship_modes = ["Standard Class", "Second Class", "First Class", "Same Day"]

n_orders = 4200
start_date = pd.Timestamp("2024-01-01")
end_date = pd.Timestamp("2025-12-31")
date_range_days = (end_date - start_date).days

rows = []
order_id_counter = 1000

# Seasonal multiplier by month (slightly higher Nov/Dec, lower Feb)
seasonal = {1: 0.9, 2: 0.8, 3: 0.95, 4: 1.0, 5: 1.0, 6: 1.05,
            7: 1.0, 8: 0.95, 9: 1.05, 10: 1.1, 11: 1.25, 12: 1.35}

for i in range(n_orders):
    # Random date weighted slightly toward recent months (growth trend) and seasonality
    while True:
        offset = np.random.randint(0, date_range_days + 1)
        order_date = start_date + pd.Timedelta(days=offset)
        month_weight = seasonal[order_date.month]
        # mild growth trend across the 2 years
        growth_weight = 0.8 + 0.4 * (offset / date_range_days)
        if np.random.rand() < (month_weight * growth_weight) / 1.6:
            break

    category = np.random.choice(list(categories.keys()), p=[0.22, 0.45, 0.33])
    sub_category = np.random.choice(categories[category])
    product = np.random.choice(products[sub_category])
    region = np.random.choice(regions, p=[0.18, 0.22, 0.22, 0.24, 0.14])
    segment = np.random.choice(segments, p=[0.5, 0.3, 0.2])
    ship_mode = np.random.choice(ship_modes, p=[0.55, 0.2, 0.15, 0.1])

    low, high = price_ranges[sub_category]
    unit_price = round(np.random.uniform(low, high), 2)
    quantity = np.random.randint(1, 8)
    discount = np.random.choice([0, 0.1, 0.15, 0.2, 0.3, 0.4], p=[0.45, 0.2, 0.15, 0.1, 0.07, 0.03])

    sales = round(unit_price * quantity * (1 - discount), 2)

    m_low, m_high = margin_ranges[category]
    margin = np.random.uniform(m_low, m_high)
    # Higher discounts erode margin further
    margin -= discount * 0.5
    profit = round(sales * margin, 2)

    order_id_counter += 1
    rows.append({
        "Order ID": f"ORD-{order_id_counter}",
        "Order Date": order_date.strftime("%Y-%m-%d"),
        "Customer Segment": segment,
        "Region": region,
        "Category": category,
        "Sub-Category": sub_category,
        "Product Name": product,
        "Quantity": quantity,
        "Unit Price": unit_price,
        "Discount": discount,
        "Sales": sales,
        "Profit": profit,
        "Ship Mode": ship_mode,
    })

df = pd.DataFrame(rows)

# Introduce a few realistic "messy data" issues for the cleaning step
messy_idx = np.random.choice(df.index, size=40, replace=False)
df.loc[messy_idx[:15], "Discount"] = np.nan          # missing discounts
df.loc[messy_idx[15:25], "Region"] = df.loc[messy_idx[15:25], "Region"].str.lower()  # inconsistent casing
df.loc[messy_idx[25:30], "Sales"] = -df.loc[messy_idx[25:30], "Sales"]  # negative sales (returns/errors)
dup_rows = df.loc[messy_idx[30:35]]
df = pd.concat([df, dup_rows], ignore_index=True)    # duplicate rows

df = df.sort_values("Order Date").reset_index(drop=True)
df.to_csv("/home/claude/project/data/sales_data_raw.csv", index=False)
print("Saved raw dataset:", df.shape)
print(df.head())
