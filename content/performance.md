Measured on synthetic data with typical problems (missing values, junk text, duplicates, skew):

| Task | Time |
|---|---|
| Analyse a 5.1M-row Parquet file | 0.56 s |
| Analyse, plan, generate and validate cleaning code, 1M-row CSV with a target | 2.5 s |
| Run the generated polars cleaning script on 1M rows | 0.9 s |
| `fe.train()` on a 1M-row CSV (features, 4 models, validation) | 6.7 s |
| Generated `prep.py` + `train.py` on 1M rows | 1.3 s + 20 s |
| Learn a contract from 1M rows / run the check script on 1M rows | 0.8 s / 0.6–0.9 s |
| Compare two 1M-row files | 0.6 s |
| Analyse a 1M-row SQLite table (5,000 rows transferred) | 0.3 s |
| Time-series profile of a 5.3M-row Parquet file | 0.7 s |
| Generated forecast script on 5.3M rows | 0.6 s |
| Notebook with cleaning, features, training, forecast and contract | 5 s |
