# Limitations

1. **Target leakage.** Notebook 05 (production, first version) and notebook 04 (yield, via `storage_ratio`) contain leakage. Their recorded accuracy is not a valid estimate of predictive performance. Only notebook 06 is leakage-free by construction. See `reports/validity_review.md`.
2. **Random parcel-level splits.** Parcels from the same holding can be in train and test, and no spatial or zone holdout was used. The results do not show how the models would perform for new holdings, new provinces or a new season.
3. **Not a time-series forecast.** One survey year is used. "Forecasting" in the project name means prediction on held-out records.
4. **Truncated targets.** Yield is limited to 300-6,000 kg/ha and production to 30-10,000 kg after outlier removal. The models are not evaluated on, and should not be applied to, values outside those ranges.
5. **Weak performance at low yields.** Yield R-squared is negative (-0.757) for parcels below 1,667 kg/ha.
6. **Preprocessing fitted on all data** (outlier bounds, GPS clustering) before the split, a mild form of leakage.
7. **No automated hyperparameter tuning**, despite code comments describing the models as "optimised".
8. **No saved models.** No model artefacts were found, so none are published and no inference demo exists.
9. **Confidential data.** The survey data cannot be shared, so the notebooks cannot be run from this repository, and outputs, maps and record-level predictions are withheld.
10. **Incomplete preparation chain.** The step that builds `final_dataset.csv` was not among the packaged files, so end-to-end reproduction from raw survey data is not currently possible.
11. **Library versions unknown.** The versions used at NIS were not recorded.
12. **Permission not confirmed.** NIS permission to publish has not been confirmed. Only code, aggregate performance metrics and model-performance charts are published.
13. **No causal claims.** Associations in a single observational survey do not establish that any practice causes higher yield.
