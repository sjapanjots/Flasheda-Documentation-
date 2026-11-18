```python
drift = fe.compare("orders_jan.parquet", "orders_feb.parquet")
drift.show()
drift.ok                 # False on schema changes or major drift
drift["amount"]          # per-column details
```

- Columns added and removed, and type changes.
- Per column: **PSI** (< 0.1 stable, 0.1–0.25 moderate, ≥ 0.25 major); for numbers also a KS test and the median shift; for text, new categories with examples. A jump in nulls also counts as drift.
- Dates and IDs are reported as range shifts, since they always move forward.
