# RegressionAnalysisOfExperimentalData

Preparing an up-to-date dataset of experimental data is tricky. Please find details in ```ProgressReport.pdf``` on how to download, clean and structure the data. All SQL commands are provided in ```SQLcommands``` as text files and can be run in sequence according to the pdf and the instructions below.

Sample processed data is provided in the ```data``` folder and contains Chemical Activity (target variable) and the relevant context information, incl. molecules used for later embedding (predictor variables).

This experiment was conducted and implemented in collaboration with Novartis scientists, initial trials on simple feed-forward neural network were conducted, but subsequent progress is proprietary. For more information please refer to:

Martin EJ, Polyakov VR, Tian L, Perez RC. Profile-QSAR 2.0: Kinase Virtual Screening Accuracy Comparable to Four-Concentration IC50s for Realistically Novel Compounds. J Chem Inf Model. 2017 Aug 28;57(8):2077-2088. doi: 10.1021/acs.jcim.7b00166. Epub 2017 Jul 26. PMID: 28651433.

# SQL ChEMBL database - data cleaning for Kinase protein family

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

### More details:
1. Find the kinase protein target IDs from the target_dictionary by searching for kinases in the pref_name (-> kinases_dictionary_data.csv)

`SELECT * FROM public.target_dictionary
WHERE pref_name LIKE '%kinase%'`

2. Save the results as .csv and use the taget IDs (tid) to search for relevant assays (-> all_kinase_assays.csv): 

`SELECT * FROM public.assays
WHERE tid IN (8, 188, 213, ... , 117289)`

3. Save the result as .csv and look for the corresponding activities for each assay (searching from assay_id):
(-> saves as SQL table kinase_activities)

`SELECT * INTO TABLE kinase_activities FROM public.activities
WHERE assay_id IN (371, 372, ... 1642574, 1642575)`

4. Count the activities for all assays and sort them. Save indexes as .csv (-> assay_id_and_counts.csv) but also
(-> SQL relevant_assayids AND relevant_assayidover200)

`SELECT assay_id, COUNT(*) AS CountOf FROM public.kinase_activities
GROUP BY assay_id HAVING COUNT(*)>1 
ORDER BY Countof DESC, assay_id ASC`

5. Save the kinase_activities for the relevant assays and save in SQL table:

`SELECT * INTO TABLE relevant_kinase_activities FROM public.kinase_activities
WHERE assay_id IN (1301717, 688293, ..., 1527619, 1642538)`

6. Save the temp_notnullpic50 for the relevant assays:

`SELECT * INTO public.temp_notnullpic50 FROM public.relevant_kinase_activities
WHERE pchembl_value IS NOT NULL`

7. Check the assay_ids with 200+ entries

`SELECT assay_id, COUNT(*) AS CountOf FROM public.temp_notnullpic50
GROUP BY assay_id HAVING COUNT(*)>=200
ORDER BY Countof DESC, assay_id ASC`

8. Select Assays with entries over 200
9. Select Assays with targets corresponding to proteins (H, D)
10. Remove Activities that only describe a compound once
11. Remove ACtivities that have '%' units
12. Remove Activities that have standard_types other than IC50, EC50, IC50, Ki, Potency
13. Remove Activities that have published_value of null and no further conclusive comment or their Ki counterparts
14. (U87168)
`update public.all_activities
set pchembl_value = 4 where published_value is null`
