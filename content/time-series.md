A random sample breaks time order, so time series use a different path: the **full** data is aggregated per period (one DuckDB `GROUP BY` for files), which stays small at any size.

```python
ts = fe.timeseries("events.parquet", time="created_at", value="amount", agg="sum", freq=None)
ts.show()
ts.trend            # {"direction": "rising", "change_per_year_pct": 18.1, ...}
ts.seasonality      # weekly / daily / yearly strength
ts.anomalies        # unusual periods
```

- `freq` is `"hour"`, `"day"` or `"week"`, chosen from the time span by default.
- `agg="sum"` suits events (sales, orders) and `agg="mean"` suits measurements. Leave out `value` to count rows.
- The report covers empty periods, trend (% per year), seasonality (after removing a moving average, so a random walk isn't mistaken for a pattern), the busiest weekday or hour, and anomalies (robust z-score > 4).

```python
fc = ts.forecast(horizon=14)
fc.show()                                         # backtest leaderboard
fc.forecast                                       # next 14 periods
open("forecast.py", "w").write(fc.script())       # python forecast.py events.parquet
```

`forecast()` compares naive, seasonal naive, moving average, drift and trend + season in a 3-fold rolling backtest (MAE, sMAPE) and keeps the most accurate. These are the baselines any more complex model has to beat. The forecast script reproduces the same numbers from the raw file.
