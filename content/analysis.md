```python
report = fe.analyze(source, n=None, target=None, engine=None, random_state=42)
```

`source` can be a pandas or polars DataFrame, a CSV/TSV or Parquet path, or a database source from [`fe.sql`](databases).

The report covers:

| Section | Contents |
|---|---|
| Overview | true row count, columns, types, memory (sample and estimated full size), duplicate rows |
| Missing values | null count and % per column, columns above 20% (warn) and 50% (critical), rows with any null |
| Numeric columns | mean, std, min, quartiles, max, IQR outliers, skewness, kurtosis, constant columns |
| Categorical columns | distinct values, cardinality, mode, top values, high-cardinality and likely-ID flags |
| Correlations | Pearson (numbers), Cramér's V (categories), point-biserial (number vs. true/false) |
| Text | personal data and free-text statistics (see [Text](text)) |
| Target | task, balance, predictive power, leakage, recommended metric and split (see [Target](target)) |

Short warnings summarise what needs attention, e.g. *"Possible target leakage: refund_issued"*.

```python
report.show()                  # rich console output
report.save_html("r.html")     # standalone HTML page
report.save_pdf("r.pdf")       # PDF
report.to_dict(); report.to_json()
report.warnings                # list of strings
```

Nothing is written to disk unless you ask; `fe.analyze(..., save_pdf=True)` also writes `flasheda_report.pdf`.

The sample size is 5,000 rows by default; change it per call with `n=`, for a block of code with `with fe.sample_size(20_000): ...` (safe in threads and async code), or globally with `fe.set_sample_size(20_000)`.

DataFrames and files are sampled differently: a DataFrame uses pandas `DataFrame.sample(random_state=...)`, a file a seeded DuckDB reservoir sample (or chunked random keys without DuckDB). The same seed gives a reproducible sample for each, but the same data as a DataFrame and as a file gives different sampled rows.

If one section of the analysis fails (say, correlations on an odd column), the report still comes back. The section is empty, the error is in `report.errors`, and a warning names it. Pass `strict=True` to raise instead. A failure in the target analysis always raises.
