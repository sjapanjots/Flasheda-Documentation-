| Rows | Default engine | Why |
|---|---|---|
| < 1M | pandas | simplest; fits in memory |
| 1M – 200M | polars (else DuckDB) | lazy, multi-threaded, streams larger-than-memory files |
| > 200M | PySpark, if installed | distributed |

Override with `fe.analyze(..., engine="duckdb")` or `report.codegen("duckdb")`. `fe.available_engines()` shows what's installed.

- **Sampling.** With DuckDB installed, files are sampled with a seeded reservoir sample in one native scan. Without it, a vectorised random-key pass over chunks gives the same uniform sample. Parquet row counts come from metadata.
- **Consistency.** DuckDB reads CSV values as integers, decimals or text only, so `"yes"`/`"no"` aren't turned into booleans. That way every engine sees the same values.
- **Validation.** For each engine, the generated code's output on the sample is compared row by row (order-insensitive, numbers to 6 significant digits) with the pandas reference implementation.
