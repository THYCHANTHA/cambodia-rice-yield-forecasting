# Recorded results

Every number below was **transcribed from the recorded output of the original notebooks**. Nothing was re-run for this repository. Cell numbers refer to the original notebooks (`v4`, `v5`, `v6`); in this repository they are notebooks 04, 05 and 06, each with one extra banner cell at the top.

Read this together with [validity_review.md](validity_review.md): notebook 04 contains target leakage (`storage_ratio`) and notebook 05 is invalid.

## Notebook 04 (`v4`): yield, kg/ha (optimistic, leakage flagged)

Source: cells 8, 14, 16, 19-21, 23, 28.

| Quantity | Value |
|---|---|
| Records after outlier removal, train / test | 9,763 / 1,724 (85/15 split, `random_state=42`, stratified by zone) |
| Target restricted to | 300-6,000 kg/ha (237 records removed) |
| Best model | LightGBM |
| R-squared (test) / CV R-squared | 0.9044 / 0.9092 +/- 0.0022 (5-fold) |
| RMSE / MAE | 385.02 / 153.98 kg/ha |
| MAPE | 8.08% |
| Predictions within 10% | 86.8% (86.83% in cell 28) |
| 95% of absolute errors within | 754.40 kg/ha |
| Residual standard deviation | 384.90 kg/ha |
| Largest single error | 3,470.47 kg/ha |
| R-squared, low-yield parcels (< 1,667 kg/ha) | **-0.757** |
| R-squared, high-yield parcels (> 3,333 kg/ha) | 0.591 |

| Model | R-squared | CV R-squared | RMSE | MAE |
|---|---|---|---|---|
| LightGBM | 0.9044 | 0.9092 +/- 0.0022 | 385.02 | 153.98 |
| XGBoost | 0.9030 | 0.9058 +/- 0.0026 | 387.72 | 156.64 |
| Voting ensemble (LightGBM, XGBoost, Gradient Boosting) | 0.8994 | n/a | 394.80 | 178.14 |
| Gradient Boosting | 0.8550 | 0.8482 +/- 0.0052 | 474.10 | 269.11 |
| Random Forest | 0.7695 | 0.7538 +/- 0.0044 | 597.67 | 381.31 |

## Notebook 05 (`v5`): production, kg (SUPERSEDED, invalid)

Source: cell 0 and cells 4-5. Test n = 1,393 of 9,286 records after outlier removal.

LightGBM R-squared 0.9998 (CV 0.9997 +/- 0.0001), RMSE 28 kg, MAE 10 kg, MAPE 0.58%, 99.8% within 20%. XGBoost 0.9995, Gradient Boosting 0.9948, Random Forest 0.9856. **These values reflect target leakage and are not model performance.**

## Notebook 06 (`v6`): production, kg (leakage-free)

Source: cell 0 output.

| Quantity | Value |
|---|---|
| Records | 11,743 loaded; 9,561 after outlier removal (81.4%) |
| Production restricted to | 30-10,000 kg (1,324 records, 11.27%, removed as IQR outliers) |
| Features | 97 after engineering; 76 after feature selection |
| Train / test | 8,126 / 1,435 (85/15, `random_state=42`, stratified by zone) |
| Best model | XGBoost |
| R-squared (test) / CV R-squared | 0.8382 / 0.8060 +/- 0.0123 (5-fold) |
| RMSE / MAE | 759 kg / 407 kg |
| MAPE | 19.44% |
| Predictions within 20% | 68.9% |

| Model | R-squared | CV R-squared | RMSE (kg) | MAE (kg) |
|---|---|---|---|---|
| XGBoost | 0.8382 | 0.8060 +/- 0.0123 | 758.83 | 406.56 |
| LightGBM | 0.8352 | 0.8058 +/- 0.0122 | 765.91 | 411.16 |
| Gradient Boosting | 0.8301 | 0.8044 +/- 0.0159 | 777.58 | 447.46 |
| Random Forest | 0.8077 | 0.7879 +/- 0.0127 | 827.32 | 471.71 |

The "Top 15 Features" table printed by notebook 06 is malformed (one feature at 0.9, the rest at 0.0) and is **not** reported.

## What is not in this summary

Descriptive survey estimates (for example yields or production by province or zone), correlations of survey variables, and record-level predictions are withheld because they derive from confidential data.
