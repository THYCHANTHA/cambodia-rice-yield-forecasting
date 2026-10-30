# Published charts

Seven of 105 charts embedded in the original notebooks are published. All were produced by the original notebooks (extracted from their recorded outputs, not re-drawn). They show **model performance and leakage evidence only**.

| File | Notebook (original cell) | Shows |
|---|---|---|
| `yield_model_comparison_r2.png` | 04 (`v4`, cell 27) | R-squared by model, yield |
| `yield_model_comparison_rmse.png` | 04 (cell 27) | RMSE by model, yield |
| `yield_model_comparison_mae.png` | 04 (cell 27) | MAE by model, yield |
| `yield_model_comparison_mae_labelled.png` | 04 (cell 31) | MAE by model with values, yield |
| `yield_prediction_error_distribution.png` | 04 (cell 36) | Histogram of yield prediction errors |
| `yield_feature_importance_LEAKAGE_FLAGGED.png` | 04 (cell 26) | Feature importance. **`storage_ratio` ranks first and contains the target** |
| `production_v5_correlations_LEAKAGE_EVIDENCE.png` | 05 (`v5`, cell 3) | Correlation with yield. **`area_productivity` = 1.0 shows leakage** |

The yield charts inherit notebook 04's leakage problem: **treat the R-squared bars as optimistic**. See `reports/validity_review.md`.

## Withheld (98 charts) and why

| Withheld | Reason |
|---|---|
| Descriptive charts by province or zone (average yield, total production, pesticide applications, fertiliser use) and maps | Descriptive estimates from confidential survey data, unpublished |
| Actual-versus-predicted scatter plots, residual-versus-predicted plots, pair plots and box plots of record values | Plot individual records from confidential data |
| Distributions of raw survey variables, GPS altitude, interview status and month | Raw survey distributions and fieldwork metadata |
| Correlation heatmaps of survey variables | Descriptive statistics of confidential data (the one published correlation chart is kept solely as leakage evidence) |
| A model-summary chart that includes an `ElasticNet` bar | No ElasticNet model was trained in the notebook; the bar is not backed by a result |

If NIS grants permission, additional charts could be released after review.
