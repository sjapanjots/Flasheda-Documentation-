```python
code = fe.clean("orders.csv", target="churn", features=True)
# or: report.codegen(engine, features=True); report.plan(features={"ratios": False})
```

| Feature | Rule |
|---|---|
| Date parts | datetime columns, ISO text, or text in a detected format (`25/12/2026`, `7-Nov-2026`, `25.12.2026 18:30`) → year, month, day, day of week (ISO, Monday = 1), hour (when times vary) |
| One-hot | text columns with ≤ 15 values |
| Frequency encoding | text columns with ≤ 500 values (each value → its share of the sample) |
| Text length / words | free-text columns → `<col>_length`, `<col>_words` |
| Ratios | `a / b` for the most predictive numeric pairs, kept only if the ratio beats both inputs |
| Dropped | free text after its stats, columns with personal data, text with > 500 values |

Day/month order is never guessed. If `07/11/2026` could be 7 November or July 11 (no day above 12 in the sample), the column is listed in `plan.suggestions`. Set the format with `report.plan(features=True, date_formats={"ordered": "%m/%d/%Y"})`.
