# Data access statement

**No data is included in this repository, and none may be added to it.**

## Source

The analysis uses **Cambodia Agriculture Survey (CAS) 2024** holding-level data held by the **National Institute of Statistics (NIS), Cambodia**, which the author accessed during a research internship there. The data include household and holding records with personal fields (such as names and contact details), village identifiers, GPS coordinates of parcels, and crop-level records.

## Why it is not published

- The data are survey microdata with identifiable and location information.
- NIS permission to redistribute the data, derived record-level tables, record-level predictions, or descriptive survey estimates **has not been confirmed**.
- Therefore the repository excludes: the original data and every derived table, record-level predictions, descriptive results by province or zone, maps, and the outputs stored inside the original notebooks.

## How to obtain access

Request the CAS 2024 data from NIS directly, under their data-access terms. This repository's author cannot grant access.

## Reproducing

1. Obtain the data from NIS and place the files in this `data/` folder (they are git-ignored).
2. Notebooks reference `data/<file name>`. Run notebooks 01 to 06 in order.
3. **Known gap:** the notebook that builds `final_dataset.csv` (the input to notebooks 04 to 06) was not among the packaged files. Reproduction from raw data is incomplete until it is located or rewritten.

No synthetic data is provided. Synthetic data was not needed to present the completed work, and inventing a stand-in for the survey could be mistaken for the real data.
