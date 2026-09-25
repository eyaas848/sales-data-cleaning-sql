import pandas as pd
import sqlite3

df = pd.read_csv('raw_sales_data.csv')
print(f"Raw rows: {len(df)}")
print(f"Duplicates: {df.duplicated().sum()}")
print(f"Missing values per column:\n{df.isnull().sum()}\n")

df = df.drop_duplicates()

df['customer_name'] = df['customer_name'].str.strip().str.title()
df['product'] = df['product'].str.strip().str.title()
df['city'] = df['city'].str.strip().str.title()

df['price'] = df['price'].abs()

df['order_date'] = pd.to_datetime(df['order_date'], format='mixed', errors='coerce')

df_clean = df.dropna(subset=['customer_name', 'product', 'price'])
print(f"Rows after cleaning: {len(df_clean)}")

df_clean.to_csv('cleaned_sales_data.csv', index=False)

conn = sqlite3.connect('sales.db')
df_clean.to_sql('sales', conn, if_exists='replace', index=False)

revenue_by_city = pd.read_sql("""
    SELECT city, ROUND(SUM(price * quantity), 2) AS total_revenue
    FROM sales
    WHERE city IS NOT NULL
    GROUP BY city
    ORDER BY total_revenue DESC;
""", conn)

top_products = pd.read_sql("""
    SELECT product, SUM(quantity) AS total_units_sold
    FROM sales
    WHERE product IS NOT NULL
    GROUP BY product
    ORDER BY total_units_sold DESC;
""", conn)

print("\nRevenue by city:")
print(revenue_by_city)
print("\nBest-selling products:")
print(top_products)

conn.close()
