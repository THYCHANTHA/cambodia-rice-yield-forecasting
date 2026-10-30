# Validity review

Written at packaging time (2026) by reading the original notebooks and their recorded outputs. **Nothing was re-run, re-tuned or corrected**; this review only documents what the existing work shows. Cell numbers refer to the **original** notebooks (`v4`, `v5`, `v6`), which are published here as notebooks 04, 05 and 06 with one extra banner cell at the top.

## Summary

| Notebook | Task | Leakage | Reliability of the recorded result |
|---|---|---|---|
| 04 (`v4`) | Yield (kg/ha) | **Yes: `storage_ratio` contains the target** | Optimistic upper bound. Do not cite as a generalisation estimate |
| 05 (`v5`) | Production (kg) | **Yes: target-derived feature plus `yield_total`** | **Invalid.** Superseded by notebook 06 |
| 06 (`v6`) | Production (kg) | Leakage features removed | Usable as a random-split, parcel-level estimate, with the caveats below |

## 1. Notebook 05: target leakage (confirmed)

- The target is `production_total(kg)` (cell 0, `target = "production_total(kg)"`).
- The notebook creates `expected_production = area_harvested_ha * yield_total(kg/ha)`. Production is, by definition, area harvested times yield per hectare, so this feature **equals the target**.
- The comment in the code reads "Drop identifiers only (keep production_total(kg) as target)", and `yield_total(kg/ha)` stays in the feature matrix (`X = df_clean.drop(columns=[target])`).
- Recorded result: LightGBM R-squared 0.9998, RMSE 28 kg, MAE 10 kg, MAPE 0.58%, 99.8% within 20%.
- The notebook's own correlation chart ranks `area_productivity` at correlation 1.0 with yield and `expected_production` among the top features (see `visualizations/production_v5_correlations_LEAKAGE_EVIDENCE.png`).
- Notebook 06 is titled "FIXED VERSION (NO LEAKAGE)", drops `yield_total(kg/ha)`, and records R-squared 0.8382 (XGBoost). The difference between 0.9998 and 0.838 is the leakage.

## 2. Notebook 04: target leakage in `storage_ratio` (found at packaging time)

- Cell 11 builds `storage_ratio = stored_qty_total(kg) / (area_harvested_ha * yield_total(kg/ha) + 1e-6)`. The denominator is area times the **target** (cell 14: `target = "yield_total(kg/ha)"`).
- The target column is removed from the features **after** this engineering (`X = df_clean.drop(columns=[target])`), so `storage_ratio` carries the target into the model. Given `stored_qty_total` and `area_harvested_ha`, the ratio determines yield.
- It is the **only** engineered feature that uses the target (checked: `storage_per_ha` and `storage_management_interaction` are built from storage, area and the management score, not from yield). The correlation filter (above 0.90) did **not** remove `storage_ratio` (it is absent from the recorded drop list).
- Independent evidence from the notebook itself: in its feature-importance chart `storage_ratio` is the **top feature** (see `visualizations/yield_feature_importance_LEAKAGE_FLAGGED.png`).
- Consequence: the recorded yield R-squared of 0.904 is most likely inflated. **The size of the effect was not measured**, because no experiment was re-run. It is not known what R-squared the model would reach without `storage_ratio`.

## 3. Other methodological issues (all notebooks)

| Issue | Where | Effect |
|---|---|---|
| **Random parcel-level split.** Parcels from the same holding can appear in both train and test. The holding identifier (`int_key`) is dropped before splitting, so no grouping was used | 04, 05, 06 | Optimistic estimates: the model can recognise holding-specific patterns |
| **Preprocessing fitted before the split.** Outlier bounds on the whole dataset; KMeans clustering of GPS coordinates fitted on all rows (with forward-filled missing coordinates) | 04, 06 | Mild information leakage from test to train |
| **Truncated targets.** Yield limited to 300-6,000 kg/ha; production limited to 30-10,000 kg | 04, 06 | Results do not apply outside those ranges. Removing large producers changes what is being predicted |
| **Heterogeneous performance hidden by one R-squared.** Yield R-squared is -0.757 for parcels below 1,667 kg/ha and 0.591 above 3,333 kg/ha | 04 | The model is poor where yields are lowest |
| **Survey weight used as a feature** (`weight` appears among the top-importance features in the yield chart) | 04 | A sampling artefact, not an agronomic predictor |
| **No automated hyperparameter search.** `optuna` and `RandomizedSearchCV` are imported but never used; the "optimised" models use fixed settings | 04 | The label "hyper-optimised" in the code comments is not supported |
| **A plotted model with no training.** A summary chart (cell 26) lists `ElasticNet` and `Ensemble` bars from hard-coded values; no ElasticNet model is trained in the notebook | 04 | That chart is **not** published |
| **Malformed feature-importance output.** Notebook 06's "Top 15 Features" prints a single feature at 0.9 and the rest at 0.0, with index numbers mismatched to names | 06 | **Not reported as a finding** |
| **Single survey year, cross-sectional.** No temporal validation | all | No claim about forecasting future seasons |

## 4. What was and was not done about it

- **Done:** the problems are documented here and flagged in each notebook's banner and in the README. Recorded numbers are reproduced exactly.
- **Not done:** no re-run, no correction, no new metrics. The instruction for this packaging was to reuse the existing work, not to repeat experiments.
- **Recommended before relying on any figure** (not performed): remove `storage_ratio` and any other feature derived from the target; split by holding (and ideally by province or zone) so that test parcels come from unseen holdings; fit imputation, outlier bounds and clustering on training data only; report intervals; evaluate by yield band.
