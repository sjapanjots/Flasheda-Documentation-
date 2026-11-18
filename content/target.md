Pass the column you want to predict:

```python
report = fe.analyze("customers.parquet", target="churn")
report.target["task"]                 # "binary" | "multiclass" | "regression"
report.target["feature_power"]        # [{"column": ..., "score": 0..1}, ...] best first
report.target["leakage_columns"]      # columns that predict the target almost perfectly
report.target["recommended_metric"]   # e.g. "PR-AUC / average precision (minority class is 12%...)"
report.target["recommended_split"]    # e.g. "time-based split on signup_date: ..."
```

- **Predictive power** is measured per feature on a held-out part of the sample: a Brier skill score for classification and R² (binned or linear) for regression. ID-like columns score about 0 instead of looking perfect.
- **Leakage**: a feature with power ≥ 0.8 on its own is flagged. It's usually recorded after the outcome (a refund flag for churn, for example).
- **Metric**: PR-AUC for imbalanced binary targets, ROC-AUC for balanced ones, macro-F1 for imbalanced multiclass, MAE for skewed regression targets, otherwise RMSE.
- **Split**: time-based when a date column exists, otherwise stratified (classification) or plain K-fold. Date columns are found by their values, so a column called `moment` holding timestamps counts. Without a name hint like `date` or `_at`, values need a 4-digit year or a clock time, so codes like `1-2` aren't mistaken for dates.
