```python
src = fe.sql("postgresql://user:pass@host/shop", table="orders")
# or fe.sql(url, query="SELECT * FROM orders WHERE country = 'IN'")

fe.analyze(src, target="churn")
fe.compare(src, "last_month.parquet")
fe.check(src, contract)
src.to_parquet("orders.parquet")      # streams the table in chunks
```

- Works with any SQLAlchemy URL.
- Sampling runs inside the database, so only the sample is transferred: `TABLESAMPLE` on PostgreSQL, `USING SAMPLE` on DuckDB, `ORDER BY random() LIMIT n` elsewhere.
- Passwords are masked in reports (`user:***@host`). Generated scripts read the URL from `$DATABASE_URL`.
- Cleaning code for databases is pandas. For other engines, export with `to_parquet()` first.
