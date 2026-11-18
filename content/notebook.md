```python
report = fe.analyze("orders.csv", target="churn")
report.to_notebook("orders.ipynb", train=True, time="created_at", engine="duckdb")
```

One runnable Jupyter notebook with:
- summary and warnings
- the analysis
- the cleaning (and feature) plan and its code
- *optional:* the model comparison and training code (`train=True`)
- *optional:* a time-series profile and forecast (`time=`)
- a contract check (`contract=False` to skip)

Every code cell is a generated script that was validated on the sample, so the notebook runs top to bottom.
