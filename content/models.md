```python
result = fe.train("orders.csv", target="churn", engine="polars",
                  output="features.parquet", model_path="model.joblib")
result.show()                         # leaderboard
result.best                           # e.g. "hist_gradient_boosting"
result.save("prep.py", "train.py")
```

- Compares a baseline, a linear model (logistic regression or ridge), a random forest and histogram gradient boosting on the sample, using the recommended metric and split.
- `prep.py` cleans the full data and adds features in the chosen engine, then writes `features.parquet`.
- `train.py` cross-validates the best model on that file with the same metric and split, fits on all rows (a random 2,000,000 when there are more) and saves `model.joblib`. It's validated by running it on the sample.
- Restrict the candidates with `models=["logistic_regression", "random_forest"]`, or add your own:
  ```python
  from flasheda.modeling import ModelSpec
  knn = ModelSpec("knn", "sklearn.neighbors", "KNeighborsClassifier", {"n_neighbors": 25}, scale=True)
  fe.train("orders.csv", target="churn", models=[knn, "random_forest"])
  ```
- The baseline is always compared. If no model beats it by more than one standard error, `result.beats_baseline` is `False` and `result.warnings` says the features may carry little signal.
- **Time-based data:** the latest 20% of rows are an untouched holdout. Models are picked by cross-validation on the earlier rows and then scored once on the holdout (the `holdout` column; `holdout=0` turns it off). `train.py` does the same on the full data.
- **Rare classes:** a class with fewer than 2 sampled rows stops with an explanation; for multiclass targets `rare_classes="drop"` or `"merge"` handles it. Folds are reduced, with a warning, when a class is too small for 5.
- `random_state=` seeds the sample, the folds and the models, and is written into `train.py`.
