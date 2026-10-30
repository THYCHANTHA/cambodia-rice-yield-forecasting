# Methodology (as implemented in the notebooks)

This document describes what the notebooks actually do. It adds no methods. Where something is unknown, it says so.

## 1. Data source and unit of analysis

- Source: Cambodia Agriculture Survey (CAS) 2024, holding-level survey data from the National Institute of Statistics (NIS), Cambodia. The data are confidential and not included.
- The raw survey is a holding-level file plus a crop module (`S4_CROP`) with one row per crop on each parcel. The modelling table has **one row per rice parcel record** (crop codes 101, 102, 103, mapped in the code to non-aromatic, aromatic and sticky paddy).
- Sampling weights (`weight`) are present in the table. Whether the survey design was used in modelling beyond including `weight` as a column is not documented.

## 2. Pipeline

| Step | Notebook | What it does |
|---|---|---|
| 1 | 01 `Extract` | Reads the Stata files, selects sections (household members, holding characteristics, land tenure, economy, machinery, climate shocks, crop module), renames coded columns to descriptive names, writes section CSVs |
| 2 | 02 `merge4` | Merges crop and holding tables for visualisation, maps provinces to four agro-ecological zones, fixes text encoding in names |
| 3 | 03 `visualiztion` | Descriptive charts and maps (crop, fertiliser, pesticide, zone, province). Outputs withheld |
| 4 | *(not packaged)* | Builds `final_dataset.csv`. **The notebook that does this was not among the inspected files** |
| 5 | 04 `v4` | Yield modelling |
| 6 | 05 `v5` | Production modelling, first version (invalid) |
| 7 | 06 `v6` | Production modelling, corrected |

## 3. Targets

- **Yield:** `yield_total(kg/ha)`.
- **Production:** `production_total(kg)`.
- Production equals area harvested times yield, which is why any feature derived from one target leaks the other (see `reports/validity_review.md`).

## 4. Cleaning and feature engineering

- Identifier columns (`int_key`, `int_id`, `parcel_id`, `crop_field`) are dropped before modelling.
- **Outliers.** Yield (notebook 04): restricted to 300-6,000 kg/ha, removing 237 records, then extreme values of planted area, harvested area and stored quantity are trimmed. Production (notebook 06): IQR rule on production, removing 1,324 records (11.27%) and restricting production to 30-10,000 kg, then trimming harvested area and stored quantity.
- **Engineered features** (examples): harvest ratio and loss ratio (harvested versus planted area), stress counts from loss reasons, fertiliser and pesticide interactions with irrigation, a weighted "management score", crop-group indicators, storage per hectare, polynomial and log terms, and eight KMeans clusters of GPS coordinates.
- **Selection.** Constant features are dropped; for each pair of numeric features with absolute correlation above 0.90 one is dropped.
- **Preprocessing pipeline.** Numeric: median imputation and standard scaling. Categorical: constant imputation and one-hot encoding.

## 5. Models and validation

| Item | Setting |
|---|---|
| Learners | `LGBMRegressor`, `XGBRegressor`, `RandomForestRegressor`, `GradientBoostingRegressor`; voting ensemble of the top three (notebook 04) |
| Hyperparameters | Fixed in code: 300-500 trees, learning rate 0.05, depth 6-20, 63 leaves for LightGBM, `random_state=42`. **No automated search was run** |
| Split | `train_test_split`, 15% test, `random_state=42`, stratified by agro-ecological zone. Parcel-level, not grouped by holding |
| Cross-validation | 5-fold `cross_val_score` on the training set, scoring R-squared |
| Metrics | R-squared, RMSE, MAE, MAPE, share within a tolerance (10% yield, 20% production), residual summaries |

Mathematical definitions used (standard):

- RMSE = sqrt( mean( (y - yhat)^2 ) )
- MAE = mean( |y - yhat| )
- MAPE = mean( |y - yhat| / |y| ) x 100
- Within p%: share of records with |y - yhat| / |y| x 100 <= p

## 6. What is not documented

- The library versions used at NIS.
- The step that created `final_dataset.csv`.
- Any NIS data-use agreement or permission terms.
- The meaning of every survey variable beyond what its name and the notebook code indicate. No official codebook was available to the author of this repository.
