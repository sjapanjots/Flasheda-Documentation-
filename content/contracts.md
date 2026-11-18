A contract describes what good data looks like. It's learned from a sample, with tolerances, so normal variation passes and real breakage fails.

```python
contract = fe.analyze("orders_jan.parquet").contract()
contract.save("orders.contract.json")

result = fe.check("orders_feb.parquet", "orders.contract.json")   # checks every row
result.ok                                                        # False if any rule fails
result.show()                                                    # the failing rules
```

| Rule | Learned as |
|---|---|
| Type | number, integer, bool, datetime or text, with an allowance for unparseable values |
| Missing | observed % plus a margin that covers the sample's own uncertainty |
| Range | 1st and 99th percentiles stay within bounds (catches unit changes such as ×100) |
| No negatives | for columns never negative in the sample |
| Allowed values | text columns with ≤ 20 values; up to 1% other values |
| Unique | ID columns |

`fe.check` reads files in one DuckDB pass, so it handles files larger than memory. For pipelines and CI:

```python
open("check_orders.py", "w").write(contract.script())
```

```bash
python check_orders.py data/orders_2026_03.parquet   # prints each check, exits 1 on failure
```

The script needs only DuckDB. `contract.to_pandera()` exports the same rules as a [pandera](https://pandera.readthedocs.io) schema.
