**Sample-based decisions.** Fill values, clip bounds, kept categories and contract rules come from the sample. Rare values (much less than 1 in 5,000 rows) may not be seen. Use `n=` for a larger sample.
- **CSV row counts** need one full scan (fast in DuckDB, but not constant time); Parquet counts come from metadata.
- **PySpark output** runs in a separate CI job (Java 21, PySpark 4); the main test matrix only syntax-checks it.
- **Two-digit years** (`%y`) follow each engine's rule: 00–68 → 2000s in pandas, polars and DuckDB, but 2000–2099 in Spark.
- **Training** uses scikit-learn in memory; above 2,000,000 rows the training script uses a random subset.
- **Database sampling** with random ordering (SQLite, MySQL, SQL Server, Oracle) scans the table inside the database and isn't seeded. Dialect SQL is tested as text and with sqlglot; only SQLite and DuckDB run in CI.
- **Engine code paths.** Each engine has its own writer for every step; there is no shared execution layer. The hand-written acceptance tests and the per-engine validation keep them in line.
- **Personal-data detection** is pattern-based. It finds common formats, not every possible one, and isn't a compliance tool.
- **Time series** support hourly, daily and weekly periods.
