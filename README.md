# RegressionAnalysisOfExperimentalData


# SQL ChEMBl database - data cleaning for Kinase protein family

## Finding the corresponding experimental value with experimental significance
1. Searched for Target Proteins containing Kinase in their name
2. Selected the corresponding Assays
3. Filtered out Assays below 200 compounds
4. Removed activities with no published values and no conclusive comments
5. Updated the pchembl_value for the rest of published_value is NULL
6. Removed activities based on standard_units = '%' (140,985)
7. Removed activities based on duplicates with EC50s
8. Merged identical duplicates
9. Removed duplicates that had no pchembl_value or standard_relation of NOT '=' and a normal duplicate
10. Geo-mean remaining duplicates
11. Updated pchembl_values for standard_relations '>' and '<' by offsetting the concentration by a logarithmic factor of 1
12. Update pchembl_value for standard_type = 'Potency' AND activity_comment = '(A/a)ctive' and remove the others
13. Delete remaining pchembl_value = NULL
----------------------------------------
14. Construct Assay, Compound and Activities files - remove cmpds with only one listed activity
----------------------------------------
15. Remove Compounds without corresponding SMILES/Structure 
16. Update and Remove Assays with stddev < 0.5 and hits < 200
17. Update files again

