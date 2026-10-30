# Data dictionary (modelling table `final_dataset.csv`)

The table has **85 columns** (64 integer, 15 float, 6 text). Only column **names and types** are listed; no values. Descriptions are **inferred from the column names and the notebook code**, not from an official NIS codebook, which was not available. Treat them as indicative.

| Group | Columns | Meaning (inferred) |
|---|---|---|
| Identifiers (dropped before modelling) | `int_key`, `int_id`, `parcel_id`, `crop_field` | Interview, parcel and field identifiers |
| Crop | `crop_code`, `crop_name` | Rice type (codes 101, 102, 103 mapped to non-aromatic, aromatic and sticky paddy in notebook 04) |
| Fertiliser (18) | `fert_applied`, `fert_type_org`, `fert_type_inorg`, `fert_org_solid`, `fert_org_liquid`, `fert_org_comp`, `fert_org_sludge`, `fert_org_biostim`, `fert_org_other`, `fert_inorg_urea`, `fert_inorg_other_nitro`, `fert_inorg_phosphate`, `fert_inorg_other_potassic`, `fert_inorg_potassium`, `fert_inorg_other_potassic.1`, `fert_inorg_npk`, `fert_inorg_dap`, `fert_inorg_other_unspec` | Whether and which organic and inorganic fertilisers were applied |
| Pesticide (8) | `pest_applied`, `pest_insect`, `pest_herb`, `pest_fungi`, `pest_rodent`, `pest_mollusc`, `pest_other`, `pest_unspec` | Whether and which pesticide types were applied |
| Practice | `irrigated`, `harvest_count`, `cultivation_type`, `planted_not_harvested` | Irrigation, number of harvests, cultivation type, whether planted area was not harvested |
| Area (5) | `area_planted_ha`, `area_harvested_ha`, `area_not_hv`, `area_not_hv_unit`, `area_not_hv_ha` | Planted, harvested and unharvested area (hectares and original units) |
| **Targets** | `production_total(kg)`, `yield_total(kg/ha)` | Total production (kg) and yield (kg per hectare) |
| Losses (20) | `reason_drought`, `reason_flood`, `reason_nat_event`, `reason_pest`, `reason_theft`, `reason_sickness`, `reason_no_labor`, `reason_other`, `reason_not_hv_*` (12 columns) | Reported reasons for crop loss and for area not harvested |
| Storage (4) | `stored`, `stored_qty`, `stored_qty_unit`, `stored_qty_total(kg)` | Whether and how much of the harvest was stored |
| Use of harvest (7) | `use_cons`, `use_sale`, `use_seed`, `use_feed`, `use_inkind`, `use_other`, `use_count` | Whether the harvest was consumed, sold, used as seed or feed, paid in kind |
| Shares (5) | `share_cons(%)`, `share_sale(%)`, `share_seed(%)`, `share_inkind(%)`, `share_feed(%)` | Share of the harvest by use |
| Price | `sale_price(KHR)` | Sale price in Cambodian riel |
| Location | `prov`, `zone`, `GPS_NEW__Latitude`, `GPS_NEW__Longitude` | Province, agro-ecological zone, parcel coordinates (**sensitive: never published**) |
| Survey design | `weight` | Survey weight (used as a feature in notebook 04) |

## Leakage-relevant columns

`production_total(kg)` and `yield_total(kg/ha)` are mathematically linked through area harvested. Any feature built from one of them leaks the other. See `reports/validity_review.md`.
