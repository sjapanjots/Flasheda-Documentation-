```bash
pip install flasheda
```

Optional extras add engines and features:

| Extra | Adds | Needed for |
|---|---|---|
| `flasheda[fast]` | polars, DuckDB, pyarrow | fast sampling of big files; polars and DuckDB code |
| `flasheda[ml]` | scikit-learn, pyarrow | `flasheda.train` |
| `flasheda[sql]` | SQLAlchemy, pyarrow | database tables and queries |
| `flasheda[spark]` | PySpark | running generated PySpark code |
| `flasheda[all]` | everything above except PySpark | |

```bash
pip install "flasheda[all]"
```

Requires Python 3.9 or newer and pandas 2.0 or newer.
