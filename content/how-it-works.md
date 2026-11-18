```
source ──► fixed-size sample ──► analysers ──► report (console / HTML / PDF / JSON)
 (file,      (DuckDB reservoir,     │
  DataFrame,  sampling in the       ▼
  database)   database for SQL)   plan of engine-neutral steps ──► writer ──► script
                                    │                              (pandas, polars,
                                    ▼                               DuckDB, PySpark)
                                  validate: run the script on the sample and
                                  compare with the reference implementation
```

1. **Sample.** The true row count comes from file metadata or `count(*)`; then a uniform random sample (5,000 rows by default) is drawn without loading the full data.
2. **Analyse.** Overview, missing values, numeric and categorical profiles, correlations, text and personal data, and (with a target) task type, class balance, predictive power and leakage.
3. **Plan.** Findings become a list of engine-neutral steps (drop, fill, convert, encode, …), each with its reason and with parameters learned from the sample.
4. **Write.** A writer turns the plan into a standalone script for the chosen engine.
5. **Validate.** The script runs on the sample, and its output is compared with a pandas reference implementation of the same plan.
