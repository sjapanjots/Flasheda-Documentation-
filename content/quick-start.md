```python
import flasheda as fe

# Analyse any size in seconds
report = fe.analyze("orders.csv", target="churn")
report.show()                         # console report
report.save_html("report.html")       # or report.save_pdf("report.pdf")

# Cleaning code for the full data, already validated on the sample
fe.clean("orders.csv", target="churn", engine="polars").save("clean_orders.py")

# Compare models and get preparation + training scripts
result = fe.train("orders.csv", target="churn")
result.show()
result.save("prep.py", "train.py")    # python prep.py && python train.py

# Guard new data
contract = report.contract()
fe.check("orders_next_month.csv", contract).show()

# Everything above as one runnable notebook
report.to_notebook("orders.ipynb", train=True)
```
