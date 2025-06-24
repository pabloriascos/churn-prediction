# Churn Prediction Insights

This project contains exploratory analysis for the Telco customer churn dataset. A new script `churn_insights.py` generates summary statistics that highlight churn behavior for each feature.

## Generating insights

Run the script with Python to produce two CSV files in `data/processed`:

```bash
python3 src/churn_insights.py
```

The output files are:

- `categorical_churn_rates.csv` – churn rate for every category in categorical features.
- `numeric_averages_by_churn.csv` – average numeric values grouped by churn label.

These summaries can be useful to detect which customer segments have higher churn probability and how numeric metrics differ between churned and non-churned clients.
