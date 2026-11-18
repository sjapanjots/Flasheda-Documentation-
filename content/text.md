`fe.analyze` profiles text columns automatically:

- **Personal data.** Emails, phone numbers, URLs, IP addresses and card numbers (Luhn-checked), as the share of each column's non-empty values, with a warning. Dates, times, amounts and order numbers are excluded.
- **Free text** (≥ 3 words or ≥ 30 characters on average). Length, words, % empty, % duplicates, % all caps, and the most common words.

```python
report.text["personal_data_columns"]   # ["email", "contact_note"]
report.text["columns"]["review"]["free_text"]["top_words"]
```
