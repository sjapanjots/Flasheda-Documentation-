| Function | Returns | Purpose |
|---|---|---|
| `fe.analyze(source, n=None, *, target=None, engine=None, random_state=42, show=False, save_pdf=False, pdf_path=..., strict=False)` | `EDAReport` | profile a source |
| `fe.clean(source, target=None, engine=None, *, output="cleaned.parquet", features=False, validate=True, **plan_options)` | `GeneratedCode` | cleaning (and feature) script |
| `fe.train(source, target, engine=None, *, output="features.parquet", model_path="model.joblib", models=None, n_splits=5, holdout=0.2, rare_classes="error", random_state=42, config=None)` | `ModelResult` | model comparison, prep and training scripts |
| `fe.CleanConfig(...)` | `CleanConfig` | every cleaning choice in one object (`.save()`, `.load()`, `.replace()`) |
| `fe.check(source, contract)` | `CheckResult` | check full data against a contract (object or JSON path) |
| `fe.compare(reference, current, *, n=None)` | `DriftReport` | schema changes and drift |
| `fe.timeseries(source, time, value=None, *, agg="sum", freq=None)` | `TimeSeriesReport` | time-series profile |
| `fe.sql(url, table=None, query=None)` | `SqlSource` | database table or query as a source |
| `fe.sample_size(n)` | context manager | sample size inside a `with` block (thread- and async-safe) |
| `fe.set_sample_size(n)` / `fe.get_sample_size()` | | process-wide default sample size (≥ 100) |
| `fe.available_engines()` | `dict` | installed engines |

| `EDAReport` method | Purpose |
|---|---|
| `show()`, `to_html()`, `save_html(path)`, `save_pdf(path)`, `to_dict()`, `to_json()` | output |
| `plan(features=False, *, config=None, **options)` | engine-neutral cleaning plan: `.describe()`, `.review()`, `.impact(source)`, `.skipped`, `.suggestions` |
| `codegen(engine=None, *, output=..., features=False, validate=True, **options)` | `GeneratedCode` with `.code`, `.save()`, `.validate()`, `.run(df)` |
| `train(engine=None, **options)` | `ModelResult` |
| `contract(allow_extra_columns=True)` | `Contract` with `.check()`, `.save()`, `.script()`, `.to_pandera()` |
| `to_notebook(path, *, train=False, time=None, value=None, features=False, contract=True, engine=None, source=None)` | notebook path |

`TimeSeriesReport.forecast(horizon=None, methods=None)` returns a `ForecastResult` with `.leaderboard`, `.forecast`, `.show()` and `.script(source=None, output="forecast.csv")`.
