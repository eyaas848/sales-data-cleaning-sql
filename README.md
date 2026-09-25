# Data Cleaning & SQL Analysis — Online Sales

## Context
Raw online sales dataset containing realistic real-world problems: duplicates, missing values, inconsistent date formats, badly formatted text (casing, spacing), and data entry errors (negative prices).

## Issues identified
- 10 exact duplicate rows
- ~52 missing values per column (names, products, prices, quantities, dates, cities)
- Inconsistent casing/spacing in names, products, cities ("sara EL amrani", "phone ", "RABAT")
- Negative prices (likely data entry error)
- Dates in 3 different formats (2024-01-15, 15/01/2024, 2024/01/18)

## Cleaning steps (Python / Pandas)
1. **Removed exact duplicates** — drop_duplicates()
2. **Standardized text formatting** — .str.strip().str.title() on names, products, cities
3. **Fixed negative prices** — .abs() (assumption: data entry error, not a refund)
4. **Standardized dates** — pd.to_datetime(format='mixed') to handle all 3 formats
5. **Handled missing values** — dropped rows missing critical fields (name/product/price); kept rows with missing quantity/city (less critical)

**Result**: 310 raw rows -> 150 clean, reliable rows

## SQL Queries

```sql
-- Total revenue by city
SELECT city, ROUND(SUM(price * quantity), 2) AS total_revenue
FROM sales
WHERE city IS NOT NULL
GROUP BY city
ORDER BY total_revenue DESC;

-- Best-selling product (by units)
SELECT product, SUM(quantity) AS total_units_sold
FROM sales
WHERE product IS NOT NULL
GROUP BY product
ORDER BY total_units_sold DESC;
```

## Key findings
- Rabat generates the highest revenue (82,500) ahead of Casablanca (60,000)
- Phone is the best-selling product by volume (100 units)

## Tech stack
Python (Pandas), SQLite, SQL, Git/GitHub

## Files
- raw_sales_data.csv — original raw dataset
- cleaned_sales_data.csv — cleaned dataset
- cleaning_and_analysis.py — full script
- sales.db — SQLite database
