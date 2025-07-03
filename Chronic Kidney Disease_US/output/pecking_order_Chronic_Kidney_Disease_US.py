## Filename: unit_test0.py

import pandas as pd
import numpy as np
import math
from scipy.special import stdtr

def dftest_check_data_types(data_df):
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Datatype checking function for each column in the dataframe.'
    try:
        dtype_df = pd.DataFrame(columns=data_df.columns)
        dtype_df.loc[0] = 0
        # Check if there is a single datatype in each column
        for col in data_df.columns:
            unique_dtypes = data_df[col].apply(type).unique()
            dtype_df.loc[:,col] = len(unique_dtypes)
        
        mixed_cols = dtype_df[dtype_df>1].dropna(axis=1).columns
        res = len(mixed_cols) == 0
        output_vals['mixed_cols'] = list(mixed_cols.values)
        if res == False:
            fail_exp = 'There are multiple data types in the following columns: ' + ', '.join(str(p) for p in dtype_df[mixed_cols])
            explanation += ' ' + fail_exp
            
    except Exception as e:
        res = False
        test_flag = 'error'
        explanation += ' ' + str(e)
        
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_check_data_types.explanation = str(output_vals)
        return res

def dftest_check_incidence(data_df):
    # ref: ['("CDC: https://www.cdc.gov/kidney-disease/php/overview.html", "JAMA Internal Medicine: https://jamanetwork.com/journals/jamainternalmedicine/fullarticle/2767936", "US Census Bureau: https://www.census.gov/")']
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Five year mean incidence comparison function (2016-2021). Theoretical value is expected to be np.nan.'
    try:
        # Diagnosis codes for Chronic Kidney Disease
        diagnosis_codes = ['46271022', '443614', '443601', '443611', '45582391', '443597', '3553408', '44792018', '37017104', '44792017', '443612', '45763854', '45763855', '37017813', '1571486', '45553438', '44830172', '619679', '45582392', '44792255', '3577568', '3577571', '196991', '3553777', '45543858', '44792227', '3553776', '45553437', '44792229', '3577573', '45582394', '3553778', '3577569', '36210709', '35209276', '45768812', '44782429', '45582393', '3553779', '36716947', '198185', '1990140', '35209279', '4322556', '44792231']
        # Initialize an empty list to store incidence rates
        incidence = []
        # Loop through the years 2016 to 2021
        for i in range(0, 6):
            year = 2016 + i
            # Filter the dataframe for the specific year
            df_year = data_df[data_df['condition_start_datetime'].dt.year == year]
            # Calculate the incidence rate for the year
            incidence_rate = 100*df_year[df_year['condition_concept_id'].astype(str).isin(diagnosis_codes)]['person_id'].nunique() / data_df['person_id'].nunique()
            # Append the incidence rate to the list
            incidence.append(incidence_rate)
        # Calculate the mean incidence rate
        mean_incidence = np.mean(incidence)
        expected_incidence = np.nan
        val  = (mean_incidence - expected_incidence) / np.sqrt((mean_incidence*(100 - mean_incidence)+expected_incidence*(100 - expected_incidence))/2)
        ratio = mean_incidence/expected_incidence
        res = (abs(val) < 0.2) & (0.85<=ratio<=1.15)
        output_vals['ratio'] = ratio
        output_vals['smd'] = val
        output_vals['expected_value'] = expected_incidence
        output_vals['data_per'] = mean_incidence 
        if res == False:
            fail_exp = 'mean incidence in the examined data is ' + str(mean_incidence)
            explanation += ' ' + fail_exp
            
    except Exception as e:
        res = False
        test_flag = 'error'
        explanation += ' ' + str(e)
        
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_check_incidence.explanation = str(output_vals)
        return res

def dftest_check_prevalence(data_df):
    # ref: ['("CDC: https://www.cdc.gov/kidney-disease/php/overview.html", "JAMA Internal Medicine: https://jamanetwork.com/journals/jamainternalmedicine/fullarticle/2767936", "US Census Bureau: https://www.census.gov/")']
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Prevalence comparison function. Theoretical value is expected to be 14.'
    try:
        # Diagnosis codes for Chronic Kidney Disease
        diagnosis_codes = ['46271022', '443614', '443601', '443611', '45582391', '443597', '3553408', '44792018', '37017104', '44792017', '443612', '45763854', '45763855', '37017813', '1571486', '45553438', '44830172', '619679', '45582392', '44792255', '3577568', '3577571', '196991', '3553777', '45543858', '44792227', '3553776', '45553437', '44792229', '3577573', '45582394', '3553778', '3577569', '36210709', '35209276', '45768812', '44782429', '45582393', '3553779', '36716947', '198185', '1990140', '35209279', '4322556', '44792231']
        # Calculate the prevalence of Chronic Kidney Disease
        prevalence = 100*data_df[data_df['condition_concept_id'].astype(str).isin(diagnosis_codes)]['person_id'].nunique() / data_df['person_id'].nunique()
        expected_prevalence = 14
        val  = (prevalence - expected_prevalence) / np.sqrt((prevalence*(100 - prevalence)+expected_prevalence*(100 - expected_prevalence))/2)
        ratio = prevalence/expected_prevalence
        res = (abs(val) < 0.2) & (0.85<=ratio<=1.15)
        output_vals["ratio"] = ratio
        output_vals["smd"] = val
        output_vals["expected_value"] = expected_prevalence
        output_vals["data_per"] = prevalence
        if res == False:
            fail_exp = 'prevalence in the examined data is ' + str(prevalence)
            explanation += ' ' + fail_exp
            
    except Exception as e:
        res = False
        test_flag = 'error'
        explanation += ' ' + str(e)
        
    finally:
        output_vals["explanation"] = explanation
        output_vals["test_flag"] = test_flag
        dftest_check_prevalence.explanation = str(output_vals)
        return res

def dftest_calculate_age_distribution(data_df):
    # ref: ['"CDC: https://www.cdc.gov/kidney-disease/basics.html']
    explanation = 'Compares mean diagnosis age of Chronic Kidney Disease patients to the theoretical mean age. Expected value is 60.'
    # calculate age at diagnosis
    try:
        data_df = data_df[data_df['condition_concept_id'].astype(str).isin(['46271022', '443614', '443601', '443611', '45582391', '443597', '3553408', '44792018', '37017104', '44792017', '443612', '45763854', '45763855', '37017813', '1571486', '45553438', '44830172', '619679', '45582392', '44792255', '3577568', '3577571', '196991', '3553777', '45543858', '44792227', '3553776', '45553437', '44792229', '3577573', '45582394', '3553778', '3577569', '36210709', '35209276', '45768812', '44782429', '45582393', '3553779', '36716947', '198185', '1990140', '35209279', '4322556', '44792231'])]
        data_df['condition_start_datetime'] = pd.to_datetime(data_df['condition_start_datetime'])
        data_df['birth_datetime'] = pd.to_datetime(data_df['birth_datetime'])
        data_df['diagnosis_age'] = data_df['condition_start_datetime'].dt.year - data_df['birth_datetime'].dt.year
        data_df = data_df.sort_values(by=['person_id','condition_start_datetime'], ascending=True)
        unique_patients = data_df.dropna(subset=['condition_start_datetime'], axis=0).drop_duplicates(subset=['person_id'], keep='first')
        mean_age = unique_patients['diagnosis_age'].mean()
        theoretical_mean_age = 60
        val  = (mean_age - theoretical_mean_age) / np.sqrt((mean_age*(100 - mean_age)+theoretical_mean_age*(100 - theoretical_mean_age))/2)
        ratio = mean_age/theoretical_mean_age
        res = (abs(val) < 0.2) & (0.85<=ratio<=1.15)
        output_vals = {'data_per': mean_age, 'expected_value': theoretical_mean_age, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Mean diagnosis age in the examined data is ' + str(mean_age)
            explanation += ' ' + fail_exp
        
    except Exception as e:
        res = False
        binary = "Error"
        explanation = str(e)
        
    finally:
        output_vals = {}
        output_vals['pval'] = res
        output_vals['explanation'] = explanation
        output_vals['binary'] = binary
        dftest_calculate_age_distribution.explanation = str(output_vals)
    
    return res



# Filename: unit_test1.py

def dftest_Hypertension_diagnosis_codes_diagnosed(data_df):
    #"https://www.ncbi.nlm.nih.gov/pubmed/31430376, https://www.kidney.org/news/newsroom/factsheets/Hypertension-and-CKD"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Hypertension_diagnosis_codes rate comparison function. Theoretical value is expected to be between 60.0 and 80.0.'
    try:
        diagnosed_ids = data_df[data_df['condition_concept_id'].astype(str).isin(['46271022', '443614', '443601', '443611', '45582391', '443597', '3553408', '44792018', '37017104', '44792017', '443612', '45763854', '45763855', '37017813', '1571486', '45553438', '44830172', '619679', '45582392', '44792255', '3577568', '3577571', '196991', '3553777', '45543858', '44792227', '3553776', '45553437', '44792229', '3577573', '45582394', '3553778', '3577569', '36210709', '35209276', '45768812', '44782429', '45582393', '3553779', '36716947', '198185', '1990140', '35209279', '4322556', '44792231'])]['person_id'].unique()
        diagnosed = data_df[data_df['person_id'].isin(diagnosed_ids)]

        codes = ['316866', '40398391', '40345175', '40323436', '40398396']
        data_per = 100 * diagnosed[diagnosed['condition_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / diagnosed['person_id'].nunique()
        res = (60.0 <= data_per <= 80.0)
        output_vals = {'data_per': data_per, 'range_low': 60.0, 'range_high': 80.0}
        if res == False:
            fail_exp = 'Among diagnosed: Hypertension_diagnosis_codes evaluation in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Hypertension_diagnosis_codes_diagnosed.explanation = str(output_vals)
        return res

def dftest_Heart_failure_diagnosis_codes_diagnosed(data_df):
    #("https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5723148/")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Heart_failure_diagnosis_codes rate comparison function. Theoretical value is expected to be 18.6.'
    try:
        diagnosed_ids = data_df[data_df['condition_concept_id'].astype(str).isin(['46271022', '443614', '443601', '443611', '45582391', '443597', '3553408', '44792018', '37017104', '44792017', '443612', '45763854', '45763855', '37017813', '1571486', '45553438', '44830172', '619679', '45582392', '44792255', '3577568', '3577571', '196991', '3553777', '45543858', '44792227', '3553776', '45553437', '44792229', '3577573', '45582394', '3553778', '3577569', '36210709', '35209276', '45768812', '44782429', '45582393', '3553779', '36716947', '198185', '1990140', '35209279', '4322556', '44792231'])]['person_id'].unique()
        diagnosed = data_df[data_df['person_id'].isin(diagnosed_ids)]
        codes = ['316139', '45766164', '4215689', '3548004', '3540945']
        data_per = 100 * diagnosed[diagnosed['condition_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / diagnosed['person_id'].nunique()
        val = (data_per - 18.6) / np.sqrt((data_per * (100 - data_per) + 18.6 * (100 - 18.6)) / 2)
        ratio = data_per / 18.6
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 18.6, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: Heart_failure_diagnosis_codes percentage in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Heart_failure_diagnosis_codes_diagnosed.explanation = str(output_vals)
        return res

def dftest_Diabetes_Mellitus_without_complication_diagnosis_codes_diagnosed(data_df):
    #("https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5723148/", "https://www.cdc.gov/diabetes/pdfs/data/statistics/national-diabetes-statistics-report.pdf")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Diabetes_Mellitus_without_complication_diagnosis_codes rate comparison function. Theoretical value is expected to be between 32.0 and 40.0.'
    try:
        diagnosed_ids = data_df[data_df['condition_concept_id'].astype(str).isin(['46271022', '443614', '443601', '443611', '45582391', '443597', '3553408', '44792018', '37017104', '44792017', '443612', '45763854', '45763855', '37017813', '1571486', '45553438', '44830172', '619679', '45582392', '44792255', '3577568', '3577571', '196991', '3553777', '45543858', '44792227', '3553776', '45553437', '44792229', '3577573', '45582394', '3553778', '3577569', '36210709', '35209276', '45768812', '44782429', '45582393', '3553779', '36716947', '198185', '1990140', '35209279', '4322556', '44792231'])]['person_id'].unique()
        diagnosed = data_df[data_df['person_id'].isin(diagnosed_ids)]

        codes = ['40389543', '201820', '111552007', '31321000119102']
        data_per = 100 * diagnosed[diagnosed['condition_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / diagnosed['person_id'].nunique()
        res = (32.0 <= data_per <= 40.0)
        output_vals = {'data_per': data_per, 'range_low': 32.0, 'range_high': 40.0}
        if res == False:
            fail_exp = 'Among diagnosed: Diabetes_Mellitus_without_complication_diagnosis_codes evaluation in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Diabetes_Mellitus_without_complication_diagnosis_codes_diagnosed.explanation = str(output_vals)
        return res

def dftest_Diabetes_Mellitus_with_complication_diagnosis_codes_diagnosed(data_df):
    #"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5723148/"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Diabetes_Mellitus_with_complication_diagnosis_codes rate comparison function. Theoretical value is expected to be 39.2.'
    try:
        diagnosed_ids = data_df[data_df['condition_concept_id'].astype(str).isin(['46271022', '443614', '443601', '443611', '45582391', '443597', '3553408', '44792018', '37017104', '44792017', '443612', '45763854', '45763855', '37017813', '1571486', '45553438', '44830172', '619679', '45582392', '44792255', '3577568', '3577571', '196991', '3553777', '45543858', '44792227', '3553776', '45553437', '44792229', '3577573', '45582394', '3553778', '3577569', '36210709', '35209276', '45768812', '44782429', '45582393', '3553779', '36716947', '198185', '1990140', '35209279', '4322556', '44792231'])]['person_id'].unique()
        diagnosed = data_df[data_df['person_id'].isin(diagnosed_ids)]
        codes = ['40386733', '4096038', '3520110', '4099213', '40547638']
        data_per = 100 * diagnosed[diagnosed['condition_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / diagnosed['person_id'].nunique()
        val = (data_per - 39.2) / np.sqrt((data_per * (100 - data_per) + 39.2 * (100 - 39.2)) / 2)
        ratio = data_per / 39.2
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 39.2, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: Diabetes_Mellitus_with_complication_diagnosis_codes percentage in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Diabetes_Mellitus_with_complication_diagnosis_codes_diagnosed.explanation = str(output_vals)
        return res

def dftest_Hyperlipidemia_diagnosis_codes_diagnosed(data_df):
    #("https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5723148/", "https://www.kidney.org/atoz/content/hyperlipidemia")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Hyperlipidemia_diagnosis_codes rate comparison function. Theoretical value is expected to be between 40.0 and 60.0.'
    try:
        diagnosed_ids = data_df[data_df['condition_concept_id'].astype(str).isin(['46271022', '443614', '443601', '443611', '45582391', '443597', '3553408', '44792018', '37017104', '44792017', '443612', '45763854', '45763855', '37017813', '1571486', '45553438', '44830172', '619679', '45582392', '44792255', '3577568', '3577571', '196991', '3553777', '45543858', '44792227', '3553776', '45553437', '44792229', '3577573', '45582394', '3553778', '3577569', '36210709', '35209276', '45768812', '44782429', '45582393', '3553779', '36716947', '198185', '1990140', '35209279', '4322556', '44792231'])]['person_id'].unique()
        diagnosed = data_df[data_df['person_id'].isin(diagnosed_ids)]

        codes = ['432867', '438720', '4292079', '4096215', '40321212']
        data_per = 100 * diagnosed[diagnosed['condition_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / diagnosed['person_id'].nunique()
        res = (40.0 <= data_per <= 60.0)
        output_vals = {'data_per': data_per, 'range_low': 40.0, 'range_high': 60.0}
        if res == False:
            fail_exp = 'Among diagnosed: Hyperlipidemia_diagnosis_codes evaluation in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Hyperlipidemia_diagnosis_codes_diagnosed.explanation = str(output_vals)
        return res

# Filename: unit_test1.py

def dftest_Coronary_Artery_Disease_diagnosis_codes_diagnosed(data_df):
    #("https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5723148/")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Coronary_Artery_Disease_diagnosis_codes rate comparison function. Theoretical value is expected to be 40.0.'
    try:
        diagnosed_ids = data_df[data_df['condition_concept_id'].astype(str).isin(['46271022', '443614', '443601', '443611', '45582391', '443597', '3553408', '44792018', '37017104', '44792017', '443612', '45763854', '45763855', '37017813', '1571486', '45553438', '44830172', '619679', '45582392', '44792255', '3577568', '3577571', '196991', '3553777', '45543858', '44792227', '3553776', '45553437', '44792229', '3577573', '45582394', '3553778', '3577569', '36210709', '35209276', '45768812', '44782429', '45582393', '3553779', '36716947', '198185', '1990140', '35209279', '4322556', '44792231'])]['person_id'].unique()
        diagnosed = data_df[data_df['person_id'].isin(diagnosed_ids)]
        codes = ['317576', '4187067', '316995', '4134723', '4194618', '40321192']
        data_per = 100 * diagnosed[diagnosed['condition_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / diagnosed['person_id'].nunique()
        val = (data_per - 40.0) / np.sqrt((data_per * (100 - data_per) + 40.0 * (100 - 40.0)) / 2)
        ratio = data_per / 40.0
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 40.0, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: Coronary_Artery_Disease_diagnosis_codes percentage in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Coronary_Artery_Disease_diagnosis_codes_diagnosed.explanation = str(output_vals)
        return res

def dftest_Peripheral_Vascular_Disease_diagnosis_codes_diagnosed(data_df):
    #"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5723148/"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Peripheral_Vascular_Disease_diagnosis_codes rate comparison function. Theoretical value is expected to be 27.8.'
    try:
        diagnosed_ids = data_df[data_df['condition_concept_id'].astype(str).isin(['46271022', '443614', '443601', '443611', '45582391', '443597', '3553408', '44792018', '37017104', '44792017', '443612', '45763854', '45763855', '37017813', '1571486', '45553438', '44830172', '619679', '45582392', '44792255', '3577568', '3577571', '196991', '3553777', '45543858', '44792227', '3553776', '45553437', '44792229', '3577573', '45582394', '3553778', '3577569', '36210709', '35209276', '45768812', '44782429', '45582393', '3553779', '36716947', '198185', '1990140', '35209279', '4322556', '44792231'])]['person_id'].unique()
        diagnosed = data_df[data_df['person_id'].isin(diagnosed_ids)]
        codes = ['321052', '40648191', '40315969', '44782775', '317309']
        data_per = 100 * diagnosed[diagnosed['condition_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / diagnosed['person_id'].nunique()
        val = (data_per - 27.8) / np.sqrt((data_per * (100 - data_per) + 27.8 * (100 - 27.8)) / 2)
        ratio = data_per / 27.8
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 27.8, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: Peripheral_Vascular_Disease_diagnosis_codes percentage in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Peripheral_Vascular_Disease_diagnosis_codes_diagnosed.explanation = str(output_vals)
        return res

def dftest_Depression_diagnosis_codes_diagnosed(data_df):
    #("https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5723148/", "https://pubmed.ncbi.nlm.nih.gov/")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Depression_diagnosis_codes rate comparison function. Theoretical value is expected to be between 20.0 and 30.0.'
    try:
        diagnosed_ids = data_df[data_df['condition_concept_id'].astype(str).isin(['46271022', '443614', '443601', '443611', '45582391', '443597', '3553408', '44792018', '37017104', '44792017', '443612', '45763854', '45763855', '37017813', '1571486', '45553438', '44830172', '619679', '45582392', '44792255', '3577568', '3577571', '196991', '3553777', '45543858', '44792227', '3553776', '45553437', '44792229', '3577573', '45582394', '3553778', '3577569', '36210709', '35209276', '45768812', '44782429', '45582393', '3553779', '36716947', '198185', '1990140', '35209279', '4322556', '44792231'])]['person_id'].unique()
        diagnosed = data_df[data_df['person_id'].isin(diagnosed_ids)]

        codes = ['370143000', '83458005', '41006004', '310497006', '394924000', '79842004', '719593009', '49468007', '718636001', '300706003', '366979004', '320751009', '192080009', '413296003', '48589009', '310496002', '450714000', '87512008', '712823008', '160329001', '191616006', '231542000', '62951006', '719592004', '418072004', '191630001', '255339005', '428901000124105', '1084061000000106', '832007', '191659001', '274948002', '440547003', '42594001', '36923009', '87414006', '142001000119106', '63778009', '231499006', '231500002', '1153575004', '281000119103', '860721000000107', '405049007', '66344007', '720455008', 'LA10576-9', '75837004', '247776002', '720452006', '405071002']
        data_per = 100 * diagnosed[diagnosed['condition_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / diagnosed['person_id'].nunique()
        res = (20.0 <= data_per <= 30.0)
        output_vals = {'data_per': data_per, 'range_low': 20.0, 'range_high': 30.0}
        if res == False:
            fail_exp = 'Among diagnosed: Depression_diagnosis_codes evaluation in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Depression_diagnosis_codes_diagnosed.explanation = str(output_vals)
        return res

def dftest_Osteoporosis_diagnosis_codes_diagnosed(data_df):
    #("https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5723148/")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Osteoporosis_diagnosis_codes rate comparison function. Theoretical value is expected to be 31.8.'
    try:
        diagnosed_ids = data_df[data_df['condition_concept_id'].astype(str).isin(['46271022', '443614', '443601', '443611', '45582391', '443597', '3553408', '44792018', '37017104', '44792017', '443612', '45763854', '45763855', '37017813', '1571486', '45553438', '44830172', '619679', '45582392', '44792255', '3577568', '3577571', '196991', '3553777', '45543858', '44792227', '3553776', '45553437', '44792229', '3577573', '45582394', '3553778', '3577569', '36210709', '35209276', '45768812', '44782429', '45582393', '3553779', '36716947', '198185', '1990140', '35209279', '4322556', '44792231'])]['person_id'].unique()
        diagnosed = data_df[data_df['person_id'].isin(diagnosed_ids)]
        codes = ['80502', '40321845', '4173335', '4002134', '44824536']
        data_per = 100 * diagnosed[diagnosed['condition_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / diagnosed['person_id'].nunique()
        val = (data_per - 31.8) / np.sqrt((data_per * (100 - data_per) + 31.8 * (100 - 31.8)) / 2)
        ratio = data_per / 31.8
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 31.8, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: Osteoporosis_diagnosis_codes percentage in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Osteoporosis_diagnosis_codes_diagnosed.explanation = str(output_vals)
        return res

def dftest_Osteopenia_diagnosis_codes_diagnosed(data_df):
    #"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5723148/, https://pubmed.ncbi.nlm.nih.gov/29212092/"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Osteopenia_diagnosis_codes rate comparison function. Theoretical value is expected to be between 25.0 and 30.0.'
    try:
        diagnosed_ids = data_df[data_df['condition_concept_id'].astype(str).isin(['46271022', '443614', '443601', '443611', '45582391', '443597', '3553408', '44792018', '37017104', '44792017', '443612', '45763854', '45763855', '37017813', '1571486', '45553438', '44830172', '619679', '45582392', '44792255', '3577568', '3577571', '196991', '3553777', '45543858', '44792227', '3553776', '45553437', '44792229', '3577573', '45582394', '3553778', '3577569', '36210709', '35209276', '45768812', '44782429', '45582393', '3553779', '36716947', '198185', '1990140', '35209279', '4322556', '44792231'])]['person_id'].unique()
        diagnosed = data_df[data_df['person_id'].isin(diagnosed_ids)]

        codes = ['4195039', '40321904', '45767044', '45757320', '40557720']
        data_per = 100 * diagnosed[diagnosed['condition_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / diagnosed['person_id'].nunique()
        res = (25.0 <= data_per <= 30.0)
        output_vals = {'data_per': data_per, 'range_low': 25.0, 'range_high': 30.0}
        if res == False:
            fail_exp = 'Among diagnosed: Osteopenia_diagnosis_codes evaluation in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Osteopenia_diagnosis_codes_diagnosed.explanation = str(output_vals)
        return res

def dftest_Gout_diagnosis_codes_diagnosed(data_df):
    #"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5723148/"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Gout_diagnosis_codes rate comparison function. Theoretical value is expected to be 16.6.'
    try:
        diagnosed_ids = data_df[data_df['condition_concept_id'].astype(str).isin(['46271022', '443614', '443601', '443611', '45582391', '443597', '3553408', '44792018', '37017104', '44792017', '443612', '45763854', '45763855', '37017813', '1571486', '45553438', '44830172', '619679', '45582392', '44792255', '3577568', '3577571', '196991', '3553777', '45543858', '44792227', '3553776', '45553437', '44792229', '3577573', '45582394', '3553778', '3577569', '36210709', '35209276', '45768812', '44782429', '45582393', '3553779', '36716947', '198185', '1990140', '35209279', '4322556', '44792231'])]['person_id'].unique()
        diagnosed = data_df[data_df['person_id'].isin(diagnosed_ids)]
        codes = ['440674', '40321216', '4096347', '40321215', '40388651']
        data_per = 100 * diagnosed[diagnosed['condition_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / diagnosed['person_id'].nunique()
        val = (data_per - 16.6) / np.sqrt((data_per * (100 - data_per) + 16.6 * (100 - 16.6)) / 2)
        ratio = data_per / 16.6
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 16.6, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: Gout_diagnosis_codes percentage in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Gout_diagnosis_codes_diagnosed.explanation = str(output_vals)
        return res

def dftest_Sleep_Apnea_diagnosis_codes_diagnosed(data_df):
    #"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5723148/"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Sleep_Apnea_diagnosis_codes rate comparison function. Theoretical value is expected to be between 50.0 and 60.0.'
    try:
        diagnosed_ids = data_df[data_df['condition_concept_id'].astype(str).isin(['46271022', '443614', '443601', '443611', '45582391', '443597', '3553408', '44792018', '37017104', '44792017', '443612', '45763854', '45763855', '37017813', '1571486', '45553438', '44830172', '619679', '45582392', '44792255', '3577568', '3577571', '196991', '3553777', '45543858', '44792227', '3553776', '45553437', '44792229', '3577573', '45582394', '3553778', '3577569', '36210709', '35209276', '45768812', '44782429', '45582393', '3553779', '36716947', '198185', '1990140', '35209279', '4322556', '44792231'])]['person_id'].unique()
        diagnosed = data_df[data_df['person_id'].isin(diagnosed_ids)]

        codes = ['313459', '442588', '42872389', '27405005', '442164004']
        data_per = 100 * diagnosed[diagnosed['condition_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / diagnosed['person_id'].nunique()
        res = (50.0 <= data_per <= 60.0)
        output_vals = {'data_per': data_per, 'range_low': 50.0, 'range_high': 60.0}
        if res == False:
            fail_exp = 'Among diagnosed: Sleep_Apnea_diagnosis_codes evaluation in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Sleep_Apnea_diagnosis_codes_diagnosed.explanation = str(output_vals)
        return res

def dftest_Hyperparathyroidism_diagnosis_codes_diagnosed(data_df):
    #("https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5723148/", "https://www.kidney.org/")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Hyperparathyroidism_diagnosis_codes rate comparison function. Theoretical value is expected to be between 40.0 and 60.0.'
    try:
        diagnosed_ids = data_df[data_df['condition_concept_id'].astype(str).isin(['46271022', '443614', '443601', '443611', '45582391', '443597', '3553408', '44792018', '37017104', '44792017', '443612', '45763854', '45763855', '37017813', '1571486', '45553438', '44830172', '619679', '45582392', '44792255', '3577568', '3577571', '196991', '3553777', '45543858', '44792227', '3553776', '45553437', '44792229', '3577573', '45582394', '3553778', '3577569', '36210709', '35209276', '45768812', '44782429', '45582393', '3553779', '36716947', '198185', '1990140', '35209279', '4322556', '44792231'])]['person_id'].unique()
        diagnosed = data_df[data_df['person_id'].isin(diagnosed_ids)]

        codes = ['133729', '4009174', '40321160', '136934', '40387238']
        data_per = 100 * diagnosed[diagnosed['condition_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / diagnosed['person_id'].nunique()
        res = (40.0 <= data_per <= 60.0)
        output_vals = {'data_per': data_per, 'range_low': 40.0, 'range_high': 60.0}
        if res == False:
            fail_exp = 'Among diagnosed: Hyperparathyroidism_diagnosis_codes evaluation in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Hyperparathyroidism_diagnosis_codes_diagnosed.explanation = str(output_vals)
        return res

def dftest_Liver_Disease_diagnosis_codes_diagnosed(data_df):
    #("https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5723148/")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Liver_Disease_diagnosis_codes rate comparison function. Theoretical value is expected to be 28.46.'
    try:
        diagnosed_ids = data_df[data_df['condition_concept_id'].astype(str).isin(['46271022', '443614', '443601', '443611', '45582391', '443597', '3553408', '44792018', '37017104', '44792017', '443612', '45763854', '45763855', '37017813', '1571486', '45553438', '44830172', '619679', '45582392', '44792255', '3577568', '3577571', '196991', '3553777', '45543858', '44792227', '3553776', '45553437', '44792229', '3577573', '45582394', '3553778', '3577569', '36210709', '35209276', '45768812', '44782429', '45582393', '3553779', '36716947', '198185', '1990140', '35209279', '4322556', '44792231'])]['person_id'].unique()
        diagnosed = data_df[data_df['person_id'].isin(diagnosed_ids)]
        codes = ['194984', '4059300', '3539203', '40317578', '4113557', '37162164', '4059292', '4115573', '4212540', '37164288', '4352876', '4341650', '4340951', '4277276', '4341654', '4055224', '4207165', '4277921', '4290259', '1244824', '605193', '4009394', '45771255']
        data_per = 100 * diagnosed[diagnosed['condition_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / diagnosed['person_id'].nunique()
        val = (data_per - 28.46) / np.sqrt((data_per * (100 - data_per) + 28.46 * (100 - 28.46)) / 2)
        ratio = data_per / 28.46
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 28.46, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: Liver_Disease_diagnosis_codes percentage in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Liver_Disease_diagnosis_codes_diagnosed.explanation = str(output_vals)
        return res



# Filename: unit_test2.py

def dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_gender_of_the_person_Code_Female(data_df):
    #"https://www.census.gov/quickfacts/fact/table/US/PST045223"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_gender_of_the_person__Code__Female evaluation function. Result is expected to be 50.5%.'
    try:
        codes = ['45878463']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['gender_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 50.5) / np.sqrt((data_per * (100 - data_per) + 50.5 * (100 - 50.5)) / 2)
        ratio = data_per / 50.5
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 50.5, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_gender_of_the_person__Code__Female percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_gender_of_the_person_Code_Female.explanation = str(output_vals)
        return res

def dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_gender_of_the_person_Code_Male(data_df):
    #"https://www.census.gov/quickfacts/fact/table/US/PST045223"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_gender_of_the_person__Code__Male evaluation function. Result is expected to be 49.5%.'
    try:
        codes = ['45880669']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['gender_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 49.5) / np.sqrt((data_per * (100 - data_per) + 49.5 * (100 - 49.5)) / 2)
        ratio = data_per / 49.5
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 49.5, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_gender_of_the_person__Code__Male percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_gender_of_the_person_Code_Male.explanation = str(output_vals)
        return res

def dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person_Code_White(data_df):
    #"https://www.census.gov/quickfacts/fact/table/US/PST045223"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person__Code__White evaluation function. Result is expected to be 75.8%.'
    try:
        codes = ['8527']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['race_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 75.8) / np.sqrt((data_per * (100 - data_per) + 75.8 * (100 - 75.8)) / 2)
        ratio = data_per / 75.8
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 75.8, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person__Code__White percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person_Code_White.explanation = str(output_vals)
        return res

def dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person_Code_Black_or_African_American(data_df):
    #"https://www.census.gov/quickfacts/fact/table/US/PST045223"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person__Code__Black_or_African_American evaluation function. Result is expected to be 13.6%.'
    try:
        codes = ['8516']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['race_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 13.6) / np.sqrt((data_per * (100 - data_per) + 13.6 * (100 - 13.6)) / 2)
        ratio = data_per / 13.6
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 13.6, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person__Code__Black_or_African_American percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person_Code_Black_or_African_American.explanation = str(output_vals)
        return res

def dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person_Code_Asian(data_df):
    #"https://www.census.gov/quickfacts/fact/table/US/PST045223"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person__Code__Asian evaluation function. Result is expected to be 6.4%.'
    try:
        codes = ['8557']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['race_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 6.4) / np.sqrt((data_per * (100 - data_per) + 6.4 * (100 - 6.4)) / 2)
        ratio = data_per / 6.4
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 6.4, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person__Code__Asian percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person_Code_Asian.explanation = str(output_vals)
        return res

def dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person_Code_Native_Hawaiian_or_Other_Pacific_Islander(data_df):
    #"https://www.census.gov/quickfacts/fact/table/US/PST045223"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person__Code__Native_Hawaiian_or_Other_Pacific_Islander evaluation function. Result is expected to be 0.2%.'
    try:
        codes = ['8657']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['race_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 0.2) / np.sqrt((data_per * (100 - data_per) + 0.2 * (100 - 0.2)) / 2)
        ratio = data_per / 0.2
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 0.2, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person__Code__Native_Hawaiian_or_Other_Pacific_Islander percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person_Code_Native_Hawaiian_or_Other_Pacific_Islander.explanation = str(output_vals)
        return res

def dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person_Code_American_Indian_or_Alaska_Native(data_df):
    #"https://www.census.gov/quickfacts/fact/table/US/PST045223"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person__Code__American_Indian_or_Alaska_Native evaluation function. Result is expected to be 1.3%.'
    try:
        codes = ['8521']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['race_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 1.3) / np.sqrt((data_per * (100 - data_per) + 1.3 * (100 - 1.3)) / 2)
        ratio = data_per / 1.3
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 1.3, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person__Code__American_Indian_or_Alaska_Native percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person_Code_American_Indian_or_Alaska_Native.explanation = str(output_vals)
        return res

def dftest_A_foreign_key_that_refers_to_the_standard_concept_identifier_in_the_Standardized_Vocabularies_for_the_ethnicity_of_the_person_Code_Not_Hispanic_or_Latino(data_df):
    #"https://www.census.gov/quickfacts/fact/table/US/PST045223"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'A_foreign_key_that_refers_to_the_standard_concept_identifier_in_the_Standardized_Vocabularies_for_the_ethnicity_of_the_person__Code__Not_Hispanic_or_Latino evaluation function. Result is expected to be 59.3%.'
    try:
        codes = ['38003564']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['ethnicity_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 59.3) / np.sqrt((data_per * (100 - data_per) + 59.3 * (100 - 59.3)) / 2)
        ratio = data_per / 59.3
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 59.3, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'A_foreign_key_that_refers_to_the_standard_concept_identifier_in_the_Standardized_Vocabularies_for_the_ethnicity_of_the_person__Code__Not_Hispanic_or_Latino percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_that_refers_to_the_standard_concept_identifier_in_the_Standardized_Vocabularies_for_the_ethnicity_of_the_person_Code_Not_Hispanic_or_Latino.explanation = str(output_vals)
        return res

def dftest_A_foreign_key_that_refers_to_the_standard_concept_identifier_in_the_Standardized_Vocabularies_for_the_ethnicity_of_the_person_Code_Hispanic_or_Latino(data_df):
    #"https://www.census.gov/quickfacts/fact/table/US/PST045223"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'A_foreign_key_that_refers_to_the_standard_concept_identifier_in_the_Standardized_Vocabularies_for_the_ethnicity_of_the_person__Code__Hispanic_or_Latino evaluation function. Result is expected to be 19.1%.'
    try:
        codes = ['38003563']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['ethnicity_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 19.1) / np.sqrt((data_per * (100 - data_per) + 19.1 * (100 - 19.1)) / 2)
        ratio = data_per / 19.1
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 19.1, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'A_foreign_key_that_refers_to_the_standard_concept_identifier_in_the_Standardized_Vocabularies_for_the_ethnicity_of_the_person__Code__Hispanic_or_Latino percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_that_refers_to_the_standard_concept_identifier_in_the_Standardized_Vocabularies_for_the_ethnicity_of_the_person_Code_Hispanic_or_Latino.explanation = str(output_vals)
        return res



# Filename: unit_test3.py

def dftest_A_foreign_key_to_a_standard_concept_identifier_for_Lisinopril(data_df):
    #("FDA Drug Label for Lisinopril: https://www.accessdata.fda.gov/drugsatfda_docs/label/2019/019777s078lbl.pdf", "ACE inhibitor-induced cough: A review of the literature, Journal of Clinical Pharmacology, 2010")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'A_foreign_key_to_a_standard_concept_identifier_for_Lisinopril treatment comparison function. Theoretical value is expected to be between 5.0 and 20.0.'
    try:
        codes = ['OMOP5144214', 'OMOP5144239', 'OMOP499160', 'OMOP9930']
        data_per = 100 * data_df[data_df['drug_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / data_df['person_id'].nunique()
        res = (5.0 <= data_per <= 20.0)
        output_vals = {'data_per': data_per, 'range_low': 5.0, 'range_high': 20.0}
        if res == False:
            fail_exp = 'A_foreign_key_to_a_standard_concept_identifier_for_Lisinopril evaluation in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_to_a_standard_concept_identifier_for_Lisinopril.explanation = str(output_vals)
        return res

def dftest_A_foreign_key_to_a_standard_concept_identifier_for_Amlodipine(data_df):
    #"https://jamanetwork.com/journals/jamanetworkopen/fullarticle/2767936"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'A_foreign_key_to_a_standard_concept_identifier_for_Amlodipine treatment comparison function. Theoretical value is expected to be 11.2.'
    try:
        codes = ['OMOP2059251', 'OMOP2183925', 'OMOP687181', 'OMOP2059']
        data_per = 100 * data_df[data_df['drug_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / data_df['person_id'].nunique()
        val  = (data_per - 11.2) / np.sqrt((data_per * (100 - data_per) + 11.2 * (100 - 11.2)) / 2)
        ratio = data_per / 11.2
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 11.2, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'A_foreign_key_to_a_standard_concept_identifier_for_Amlodipine percentage in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_to_a_standard_concept_identifier_for_Amlodipine.explanation = str(output_vals)
        return res

def dftest_A_foreign_key_to_a_standard_concept_identifier_for_Metoprolol(data_df):
    #"American Heart Association (https://www.heart.org), NIH (https://www.nih.gov)"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'A_foreign_key_to_a_standard_concept_identifier_for_Metoprolol treatment comparison function. Theoretical value is expected to be between 5.0 and 10.0.'
    try:
        codes = ['OMOP954341', 'OMOP954342', 'OMOP954136', 'OMOP954059']
        data_per = 100 * data_df[data_df['drug_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / data_df['person_id'].nunique()
        res = (5.0 <= data_per <= 10.0)
        output_vals = {'data_per': data_per, 'range_low': 5.0, 'range_high': 10.0}
        if res == False:
            fail_exp = 'A_foreign_key_to_a_standard_concept_identifier_for_Metoprolol evaluation in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_to_a_standard_concept_identifier_for_Metoprolol.explanation = str(output_vals)
        return res

def dftest_A_foreign_key_to_a_standard_concept_identifier_for_Furosemide(data_df):
    #"NCBI (https://pubmed.ncbi.nlm.nih.gov/), CDC (https://www.cdc.gov/)"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'A_foreign_key_to_a_standard_concept_identifier_for_Furosemide treatment comparison function. Theoretical value is expected to be between 1.0 and 2.0.'
    try:
        codes = ['OMOP402924', 'OMOP2308035', 'OMOP2308031', 'OMOP402939', 'OMOP402916', 'OMOP402669', 'OMOP4797056', 'OMOP2463847', 'OMOP2306003', 'OMOP402888', 'OMOP2402017', 'OMOP808497', 'OMOP402679', 'OMOP402852', 'OMOP402925', 'OMOP402847', 'OMOP402694', 'OMOP4983135', 'OMOP402894', 'OMOP2279946', 'OMOP2024937', 'OMOP402941', 'OMOP402747', 'OMOP2182857', 'OMOP402858', 'OMOP402917', 'OMOP402931', 'OMOP2087500', 'OMOP402960', 'OMOP1100838', 'OMOP808093', 'OMOP402701', 'OMOP2245254', 'OMOP2151692', 'OMOP2370500', 'OMOP402670', 'OMOP2308036', 'OMOP402696', 'OMOP5039239', 'OMOP2186220', 'OMOP402853', 'OMOP402848', 'OMOP2463846', 'OMOP2463850', 'OMOP2151691', 'OMOP2189990', 'OMOP2370502', 'OMOP2494918', 'OMOP2339404', 'OMOP2182856', 'OMOP4817479', 'OMOP402889', 'OMOP2463848', 'OMOP402680', 'OMOP807885', 'OMOP807835', 'OMOP807011', 'OMOP2213974', 'OMOP996360', 'OMOP444250', 'OMOP2151694', 'OMOP2494922', 'OMOP4786952', 'OMOP809135', 'OMOP2182855', 'OMOP402842', 'OMOP2026963', 'OMOP402690', 'OMOP5039240', 'OMOP2058247', 'OMOP444254', 'OMOP402862', 'OMOP2308033', 'OMOP2182854', 'OMOP2433001', 'OMOP402895', 'OMOP808224', 'OMOP2433000', 'OMOP2339407', 'OMOP402742', 'OMOP808442', 'OMOP2308034', 'OMOP2370501', 'OMOP806859', 'OMOP2276639', 'OMOP807260', 'OMOP444295', 'OMOP402748', 'OMOP4812991', 'OMOP402684', 'OMOP402952', 'OMOP402935', 'OMOP808508', 'OMOP4811954', 'OMOP444299', 'OMOP2511712', 'OMOP444228', 'OMOP2106006', 'OMOP2463851', 'OMOP4787167', 'OMOP2106010', 'OMOP2342760', 'OMOP4983134', 'OMOP1103335']
        data_per = 100 * data_df[data_df['drug_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / data_df['person_id'].nunique()
        res = (1.0 <= data_per <= 2.0)
        output_vals = {'data_per': data_per, 'range_low': 1.0, 'range_high': 2.0}
        if res == False:
            fail_exp = 'A_foreign_key_to_a_standard_concept_identifier_for_Furosemide evaluation in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_to_a_standard_concept_identifier_for_Furosemide.explanation = str(output_vals)
        return res

def dftest_A_foreign_key_to_a_standard_concept_identifier_for_Erythropoietin(data_df):
    #"National Kidney Foundation: https://www.kidney.org; PubMed: https://pubmed.ncbi.nlm.nih.gov; CDC Chronic Kidney Disease Statistics: https://www.cdc.gov/ckd"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'A_foreign_key_to_a_standard_concept_identifier_for_Erythropoietin treatment comparison function. Theoretical value is expected to be between 20.0 and 30.0.'
    try:
        codes = ['4306138', '43009086', '40561484', '2066937', '604277', '2066885', '42959946', '42959948', '42959947', '2066900', '2066921', '2066895', '42959938', '42959980', '2066932', '42959961', '2066933', '42959986', '42959969', '42959965', '42959984', '2066880', '2066935', '42959934', '2066881', '42959983', '42959985', '42959964', '42959982', '40527799', '2066917', '42959963', '2066915', '2066936', '42959981', '42959967', '42959962', '42959939', '42959968', '2066934', '2066883', '2066916', '2066884', '4009497', '2066882', '2066919', '2066899', '2066920', '2066931', '42959935', '2066918', '2066894', '41110257', '36878928', '604278', '42959943', '40860464', '42959945']
        data_per = 100 * data_df[data_df['drug_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / data_df['person_id'].nunique()
        res = (20.0 <= data_per <= 30.0)
        output_vals = {'data_per': data_per, 'range_low': 20.0, 'range_high': 30.0}
        if res == False:
            fail_exp = 'A_foreign_key_to_a_standard_concept_identifier_for_Erythropoietin evaluation in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_to_a_standard_concept_identifier_for_Erythropoietin.explanation = str(output_vals)
        return res

def dftest_A_foreign_key_to_a_standard_concept_identifier_for_Calcitriol(data_df):
    #"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'A_foreign_key_to_a_standard_concept_identifier_for_Calcitriol treatment comparison function. Theoretical value is expected to be between 10.0 and 20.0.'
    try:
        codes = ['4123687', '21139618', '44042131', '44168167', '2011210', '43029029', '2044573', '35159369', '2044579', '43838325', '43712167', '43856338', '41016718', '43802104', '43766093', '41204818', '41016716', '41142241', '42958487', '43694342', '43820235', '43784233', '41016717', '40802694', '40551700', '35144076', '40551699', '21159410', '2913496', '40802695', '2044575', '2044577', '43564652', '40549825', '35149488', '43265859', '40802693', '42958489', '43730199', '44097785', '2044568', '2044569', '43029030', '44030093', '43564654', '43622194', '21600819', '42958486', '43271347', '4203232', '35156017', '35197846', '2044574', '36881139', '21080721', '36884938', '2044567', '35129833', '4131903', '2044570', '43564655', '42958488', '43255082', '4195394', '35147954', '41173278', '41110787', '35140880', '35136517', '2044576', '43676545', '2044571', '21100401', '21129715', '43676542', '21110211', '43564653', '2044566', '35136781', '44025874', '35142535', '44164442', '4203224', '35149691', '42958496', '42479056', '35142277', '41266652', '42958493', '35140869', '4235684', '21149477', '2044572', '43260429', '36677581', '21602040', '41048032', '43622189', '36681037', '41019902', '41079403', '35145484', '2011211', '35139643', '42958492', '40554657', '43640350', '35150785', '2044556', '2011208', '43820231', '43564651', '35141809', '35139950', '36963335', '40556095', '40973586', '43694340', '35155654', '4236617', '4210657', '40860984', '2044588', '42958482', '40570380', '43730197', '43838327', '43640348', '43586136', '35130310', '42958485', '43730200', '35156987', '43640349', '36681038', '43640351', '42482038', '35141742', '43029033', '43766092']
        data_per = 100 * data_df[data_df['drug_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / data_df['person_id'].nunique()
        res = (10.0 <= data_per <= 20.0)
        output_vals = {'data_per': data_per, 'range_low': 10.0, 'range_high': 20.0}
        if res == False:
            fail_exp = 'A_foreign_key_to_a_standard_concept_identifier_for_Calcitriol evaluation in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_to_a_standard_concept_identifier_for_Calcitriol.explanation = str(output_vals)
        return res

def dftest_A_foreign_key_to_a_standard_concept_identifier_for_Cinacalcet(data_df):
    #"https://pubmed.ncbi.nlm.nih.gov/PMC6577"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'A_foreign_key_to_a_standard_concept_identifier_for_Cinacalcet treatment comparison function. Theoretical value is expected to be between 20.0 and 30.0.'
    try:
        codes = ['OMOP5164046', 'OMOP5164048', 'OMOP4835486', 'OMOP481']
        data_per = 100 * data_df[data_df['drug_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / data_df['person_id'].nunique()
        res = (20.0 <= data_per <= 30.0)
        output_vals = {'data_per': data_per, 'range_low': 20.0, 'range_high': 30.0}
        if res == False:
            fail_exp = 'A_foreign_key_to_a_standard_concept_identifier_for_Cinacalcet evaluation in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_to_a_standard_concept_identifier_for_Cinacalcet.explanation = str(output_vals)
        return res



# Filename: unit_test4.py

def dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_gender_of_the_person_Code_Female_diagnosed(data_df):
    #"https://www.cdc.gov/ckd/index.html; https://www.kidney.org/news/newsroom/factsheets/Chronic-Kidney-Disease"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_gender_of_the_person__Code__Female evaluation function. Result is expected to be 15.4%.'
    try:
        diagnosed_ids = data_df[data_df['condition_concept_id'].astype(str).isin(['46271022', '443614', '443601', '443611', '45582391', '443597', '3553408', '44792018', '37017104', '44792017', '443612', '45763854', '45763855', '37017813', '1571486', '45553438', '44830172', '619679', '45582392', '44792255', '3577568', '3577571', '196991', '3553777', '45543858', '44792227', '3553776', '45553437', '44792229', '3577573', '45582394', '3553778', '3577569', '36210709', '35209276', '45768812', '44782429', '45582393', '3553779', '36716947', '198185', '1990140', '35209279', '4322556', '44792231'])]['person_id'].unique()
        diagnosed = data_df[data_df['person_id'].isin(diagnosed_ids)]
        codes = ['45878463']
        ref_for_percentage = data_df[data_df['gender_concept_id'].astype(str).isin(codes)]
        data_per = 100 * diagnosed[diagnosed['gender_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 15.4) / np.sqrt((data_per * (100 - data_per) + 15.4 * (100 - 15.4)) / 2)
        ratio = data_per / 15.4
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 15.4, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_gender_of_the_person__Code__Female percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_gender_of_the_person_Code_Female_diagnosed.explanation = str(output_vals)
        return res

def dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person_Code_White_diagnosed(data_df):
    #"CDC, Chronic Kidney Disease in the United States (https://www.cdc.gov/kidneydisease/publications.html)"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person__Code__White evaluation function. Result is expected to be 12.5%.'
    try:
        diagnosed_ids = data_df[data_df['condition_concept_id'].astype(str).isin(['46271022', '443614', '443601', '443611', '45582391', '443597', '3553408', '44792018', '37017104', '44792017', '443612', '45763854', '45763855', '37017813', '1571486', '45553438', '44830172', '619679', '45582392', '44792255', '3577568', '3577571', '196991', '3553777', '45543858', '44792227', '3553776', '45553437', '44792229', '3577573', '45582394', '3553778', '3577569', '36210709', '35209276', '45768812', '44782429', '45582393', '3553779', '36716947', '198185', '1990140', '35209279', '4322556', '44792231'])]['person_id'].unique()
        diagnosed = data_df[data_df['person_id'].isin(diagnosed_ids)]
        codes = ['8527']
        ref_for_percentage = data_df[data_df['race_concept_id'].astype(str).isin(codes)]
        data_per = 100 * diagnosed[diagnosed['race_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 12.5) / np.sqrt((data_per * (100 - data_per) + 12.5 * (100 - 12.5)) / 2)
        ratio = data_per / 12.5
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 12.5, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person__Code__White percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person_Code_White_diagnosed.explanation = str(output_vals)
        return res

def dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person_Code_Black_or_African_American_diagnosed(data_df):
    #"https://blackdoctor.org/nearly-35-of-people-with-chronic-kidney-disease-are-black/, https://www.cdc.gov/kidneydisease/publications-resources/annual-report.html"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person__Code__Black_or_African_American evaluation function. Result is expected to be 35%.'
    try:
        diagnosed_ids = data_df[data_df['condition_concept_id'].astype(str).isin(['46271022', '443614', '443601', '443611', '45582391', '443597', '3553408', '44792018', '37017104', '44792017', '443612', '45763854', '45763855', '37017813', '1571486', '45553438', '44830172', '619679', '45582392', '44792255', '3577568', '3577571', '196991', '3553777', '45543858', '44792227', '3553776', '45553437', '44792229', '3577573', '45582394', '3553778', '3577569', '36210709', '35209276', '45768812', '44782429', '45582393', '3553779', '36716947', '198185', '1990140', '35209279', '4322556', '44792231'])]['person_id'].unique()
        diagnosed = data_df[data_df['person_id'].isin(diagnosed_ids)]
        codes = ['8516']
        ref_for_percentage = data_df[data_df['race_concept_id'].astype(str).isin(codes)]
        data_per = 100 * diagnosed[diagnosed['race_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 35) / np.sqrt((data_per * (100 - data_per) + 35 * (100 - 35)) / 2)
        ratio = data_per / 35
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 35, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person__Code__Black_or_African_American percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person_Code_Black_or_African_American_diagnosed.explanation = str(output_vals)
        return res

def dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person_Code_Asian_diagnosed(data_df):
    #("https://pubmed.ncbi.nlm.nih.gov/34570204/")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person__Code__Asian evaluation function. Result is expected to be 1.7%.'
    try:
        diagnosed_ids = data_df[data_df['condition_concept_id'].astype(str).isin(['46271022', '443614', '443601', '443611', '45582391', '443597', '3553408', '44792018', '37017104', '44792017', '443612', '45763854', '45763855', '37017813', '1571486', '45553438', '44830172', '619679', '45582392', '44792255', '3577568', '3577571', '196991', '3553777', '45543858', '44792227', '3553776', '45553437', '44792229', '3577573', '45582394', '3553778', '3577569', '36210709', '35209276', '45768812', '44782429', '45582393', '3553779', '36716947', '198185', '1990140', '35209279', '4322556', '44792231'])]['person_id'].unique()
        diagnosed = data_df[data_df['person_id'].isin(diagnosed_ids)]
        codes = ['8557']
        ref_for_percentage = data_df[data_df['race_concept_id'].astype(str).isin(codes)]
        data_per = 100 * diagnosed[diagnosed['race_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 1.7) / np.sqrt((data_per * (100 - data_per) + 1.7 * (100 - 1.7)) / 2)
        ratio = data_per / 1.7
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 1.7, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person__Code__Asian percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person_Code_Asian_diagnosed.explanation = str(output_vals)
        return res

def dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person_Code_Native_Hawaiian_or_Other_Pacific_Islander_diagnosed(data_df):
    #"https://pubmed.ncbi.nlm.nih.gov/32387021/"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person__Code__Native_Hawaiian_or_Other_Pacific_Islander evaluation function. Result is expected to be 3.5%.'
    try:
        diagnosed_ids = data_df[data_df['condition_concept_id'].astype(str).isin(['46271022', '443614', '443601', '443611', '45582391', '443597', '3553408', '44792018', '37017104', '44792017', '443612', '45763854', '45763855', '37017813', '1571486', '45553438', '44830172', '619679', '45582392', '44792255', '3577568', '3577571', '196991', '3553777', '45543858', '44792227', '3553776', '45553437', '44792229', '3577573', '45582394', '3553778', '3577569', '36210709', '35209276', '45768812', '44782429', '45582393', '3553779', '36716947', '198185', '1990140', '35209279', '4322556', '44792231'])]['person_id'].unique()
        diagnosed = data_df[data_df['person_id'].isin(diagnosed_ids)]
        codes = ['8657']
        ref_for_percentage = data_df[data_df['race_concept_id'].astype(str).isin(codes)]
        data_per = 100 * diagnosed[diagnosed['race_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 3.5) / np.sqrt((data_per * (100 - data_per) + 3.5 * (100 - 3.5)) / 2)
        ratio = data_per / 3.5
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 3.5, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person__Code__Native_Hawaiian_or_Other_Pacific_Islander percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person_Code_Native_Hawaiian_or_Other_Pacific_Islander_diagnosed.explanation = str(output_vals)
        return res

def dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person_Code_American_Indian_or_Alaska_Native_diagnosed(data_df):
    #"https://www.cdc.gov/ckd/surveillance/index.html"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person__Code__American_Indian_or_Alaska_Native evaluation function. Result is expected to be 15.9%.'
    try:
        diagnosed_ids = data_df[data_df['condition_concept_id'].astype(str).isin(['46271022', '443614', '443601', '443611', '45582391', '443597', '3553408', '44792018', '37017104', '44792017', '443612', '45763854', '45763855', '37017813', '1571486', '45553438', '44830172', '619679', '45582392', '44792255', '3577568', '3577571', '196991', '3553777', '45543858', '44792227', '3553776', '45553437', '44792229', '3577573', '45582394', '3553778', '3577569', '36210709', '35209276', '45768812', '44782429', '45582393', '3553779', '36716947', '198185', '1990140', '35209279', '4322556', '44792231'])]['person_id'].unique()
        diagnosed = data_df[data_df['person_id'].isin(diagnosed_ids)]
        codes = ['8521']
        ref_for_percentage = data_df[data_df['race_concept_id'].astype(str).isin(codes)]
        data_per = 100 * diagnosed[diagnosed['race_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 15.9) / np.sqrt((data_per * (100 - data_per) + 15.9 * (100 - 15.9)) / 2)
        ratio = data_per / 15.9
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 15.9, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person__Code__American_Indian_or_Alaska_Native percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person_Code_American_Indian_or_Alaska_Native_diagnosed.explanation = str(output_vals)
        return res

def dftest_A_foreign_key_that_refers_to_the_standard_concept_identifier_in_the_Standardized_Vocabularies_for_the_ethnicity_of_the_person_Code_Not_Hispanic_or_Latino_diagnosed(data_df):
    #("https://www.cdc.gov/kidneydisease/pdf/Chronic-Kidney-Disease-Fact-Sheet-2021.pdf", "https://www.statista.com/statistics/780675/chronic-kidney-disease-prevalence-us-by-ethnicity/")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: A_foreign_key_that_refers_to_the_standard_concept_identifier_in_the_Standardized_Vocabularies_for_the_ethnicity_of_the_person__Code__Not_Hispanic_or_Latino evaluation function. Result is expected to be 13.8%.'
    try:
        diagnosed_ids = data_df[data_df['condition_concept_id'].astype(str).isin(['46271022', '443614', '443601', '443611', '45582391', '443597', '3553408', '44792018', '37017104', '44792017', '443612', '45763854', '45763855', '37017813', '1571486', '45553438', '44830172', '619679', '45582392', '44792255', '3577568', '3577571', '196991', '3553777', '45543858', '44792227', '3553776', '45553437', '44792229', '3577573', '45582394', '3553778', '3577569', '36210709', '35209276', '45768812', '44782429', '45582393', '3553779', '36716947', '198185', '1990140', '35209279', '4322556', '44792231'])]['person_id'].unique()
        diagnosed = data_df[data_df['person_id'].isin(diagnosed_ids)]
        codes = ['38003564']
        ref_for_percentage = data_df[data_df['ethnicity_concept_id'].astype(str).isin(codes)]
        data_per = 100 * diagnosed[diagnosed['ethnicity_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 13.8) / np.sqrt((data_per * (100 - data_per) + 13.8 * (100 - 13.8)) / 2)
        ratio = data_per / 13.8
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 13.8, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: A_foreign_key_that_refers_to_the_standard_concept_identifier_in_the_Standardized_Vocabularies_for_the_ethnicity_of_the_person__Code__Not_Hispanic_or_Latino percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_that_refers_to_the_standard_concept_identifier_in_the_Standardized_Vocabularies_for_the_ethnicity_of_the_person_Code_Not_Hispanic_or_Latino_diagnosed.explanation = str(output_vals)
        return res

def dftest_A_foreign_key_that_refers_to_the_standard_concept_identifier_in_the_Standardized_Vocabularies_for_the_ethnicity_of_the_person_Code_Hispanic_or_Latino_diagnosed(data_df):
    #"https://www.kidney.org/news/newsroom/factsheets/CKD_Awareness; https://pmc.ncbi.nlm.nih.gov/articles/PMC7269703/"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: A_foreign_key_that_refers_to_the_standard_concept_identifier_in_the_Standardized_Vocabularies_for_the_ethnicity_of_the_person__Code__Hispanic_or_Latino evaluation function. Result is expected to be 15.1%.'
    try:
        diagnosed_ids = data_df[data_df['condition_concept_id'].astype(str).isin(['46271022', '443614', '443601', '443611', '45582391', '443597', '3553408', '44792018', '37017104', '44792017', '443612', '45763854', '45763855', '37017813', '1571486', '45553438', '44830172', '619679', '45582392', '44792255', '3577568', '3577571', '196991', '3553777', '45543858', '44792227', '3553776', '45553437', '44792229', '3577573', '45582394', '3553778', '3577569', '36210709', '35209276', '45768812', '44782429', '45582393', '3553779', '36716947', '198185', '1990140', '35209279', '4322556', '44792231'])]['person_id'].unique()
        diagnosed = data_df[data_df['person_id'].isin(diagnosed_ids)]
        codes = ['38003563']
        ref_for_percentage = data_df[data_df['ethnicity_concept_id'].astype(str).isin(codes)]
        data_per = 100 * diagnosed[diagnosed['ethnicity_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 15.1) / np.sqrt((data_per * (100 - data_per) + 15.1 * (100 - 15.1)) / 2)
        ratio = data_per / 15.1
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 15.1, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: A_foreign_key_that_refers_to_the_standard_concept_identifier_in_the_Standardized_Vocabularies_for_the_ethnicity_of_the_person__Code__Hispanic_or_Latino percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_that_refers_to_the_standard_concept_identifier_in_the_Standardized_Vocabularies_for_the_ethnicity_of_the_person_Code_Hispanic_or_Latino_diagnosed.explanation = str(output_vals)
        return res



# Filename: unit_test5.py

def dftest_Serum_Creatinine_Measurement(data_df):
    #"Mayo Clinic: https://www.mayoclinic.org/tests-procedures/creatinine-test/about/pac-20384646; National Kidney Foundation: https://www.kidney.org/atoz/content/serumcreatinine"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Creatinine_Measurement evaluation function. 95% of the population is expected to be between 0.6 and 1.3.'
    try:
        codes = ['40307212']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['40307212'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 0.6) & (data_df['value_as_number'] <= 1.3)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['40307212'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 0.6, 'range_high': 1.3}
        if res == False:
            fail_exp = 'Serum_Creatinine_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Creatinine_Measurement.explanation = str(output_vals)
        return res

def dftest_Blood_Urea_Nitrogen_Measurement(data_df):
    #"WebMD: https://www.webmd.com/a-to-z-guides/blood-urea-nitrogen; Mayo Clinic: https://www.mayoclinic.org/tests-procedures/blood-urea-nitrogen/about/pac-20384821; MedlinePlus: https://medlineplus.gov/lab-tests/blood-urea-nitrogen-bun-test/"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Blood_Urea_Nitrogen_Measurement evaluation function. 95% of the population is expected to be between 7.0 and 20.0.'
    try:
        codes = ['3028280']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['3028280'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 7.0) & (data_df['value_as_number'] <= 20.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['3028280'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 7.0, 'range_high': 20.0}
        if res == False:
            fail_exp = 'Blood_Urea_Nitrogen_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Blood_Urea_Nitrogen_Measurement.explanation = str(output_vals)
        return res

def dftest_Serum_Potassium_Measurement(data_df):
    #"Cleveland Clinic: https://my.clevelandclinic.org/health/diagnostics/16888-blood-tests; Mayo Clinic: https://www.mayoclinic.org/tests-procedures/potassium-test/about/pac-20384923"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Potassium_Measurement evaluation function. 95% of the population is expected to be between 3.5 and 5.0.'
    try:
        codes = ['4154489']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['4154489'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 3.5) & (data_df['value_as_number'] <= 5.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['4154489'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 3.5, 'range_high': 5.0}
        if res == False:
            fail_exp = 'Serum_Potassium_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Potassium_Measurement.explanation = str(output_vals)
        return res

def dftest_Serum_Sodium_Measurement(data_df):
    #"Cleveland Clinic: https://my.clevelandclinic.org/health/diagnostics/16888-blood-tests"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Sodium_Measurement evaluation function. 95% of the population is expected to be between 135.0 and 145.0.'
    try:
        codes = ['4021154']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['4021154'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 135.0) & (data_df['value_as_number'] <= 145.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['4021154'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 135.0, 'range_high': 145.0}
        if res == False:
            fail_exp = 'Serum_Sodium_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Sodium_Measurement.explanation = str(output_vals)
        return res

def dftest_Serum_Calcium_Measurement(data_df):
    #"Cleveland Clinic: https://my.clevelandclinic.org/health/diagnostics/16888-blood-tests; MedlinePlus: https://medlineplus.gov/lab-tests/calcium-blood-test/"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Calcium_Measurement evaluation function. 95% of the population is expected to be between 8.5 and 10.2.'
    try:
        codes = ['4154490']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['4154490'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 8.5) & (data_df['value_as_number'] <= 10.2)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['4154490'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 8.5, 'range_high': 10.2}
        if res == False:
            fail_exp = 'Serum_Calcium_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Calcium_Measurement.explanation = str(output_vals)
        return res

def dftest_Serum_Phosphorus_Measurement(data_df):
    #"Cleveland Clinic: https://my.clevelandclinic.org/health/diagnostics/16888-blood-tests; Mayo Clinic: https://www.mayoclinic.org/tests-procedures/phosphorus-test/about/pac-20384904"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Phosphorus_Measurement evaluation function. 95% of the population is expected to be between 2.5 and 4.5.'
    try:
        codes = ['41139003']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['41139003'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 2.5) & (data_df['value_as_number'] <= 4.5)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['41139003'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 2.5, 'range_high': 4.5}
        if res == False:
            fail_exp = 'Serum_Phosphorus_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Phosphorus_Measurement.explanation = str(output_vals)
        return res

def dftest_Serum_Albumin_Measurement(data_df):
    #"Cleveland Clinic: https://my.clevelandclinic.org/health/diagnostics/16888-blood-tests; Mayo Clinic: https://www.mayoclinic.org/tests-procedures/albumin-test/about/pac-20384922"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Albumin_Measurement evaluation function. 95% of the population is expected to be between 3.5 and 5.0.'
    try:
        codes = ['40307274']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['40307274'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 3.5) & (data_df['value_as_number'] <= 5.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['40307274'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 3.5, 'range_high': 5.0}
        if res == False:
            fail_exp = 'Serum_Albumin_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Albumin_Measurement.explanation = str(output_vals)
        return res

def dftest_Hemoglobin_Measurement(data_df):
    #"Cleveland Clinic: https://my.clevelandclinic.org/health/diagnostics/16888-blood-tests"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Hemoglobin_Measurement evaluation function. 95% of the population is expected to be between 12.1 and 17.2.'
    try:
        codes = ['4154636']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['4154636'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 12.1) & (data_df['value_as_number'] <= 17.2)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['4154636'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 12.1, 'range_high': 17.2}
        if res == False:
            fail_exp = 'Hemoglobin_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Hemoglobin_Measurement.explanation = str(output_vals)
        return res

def dftest_Hematocrit_Measurement(data_df):
    #"Cleveland Clinic: https://my.clevelandclinic.org/health/diagnostics/16888-blood-tests, Mayo Clinic: https://www.mayoclinic.org/tests-procedures/hematocrit/about/pac-20384728"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Hematocrit_Measurement evaluation function. 95% of the population is expected to be between 36.0 and 50.0.'
    try:
        codes = ['3009542']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['3009542'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 36.0) & (data_df['value_as_number'] <= 50.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['3009542'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 36.0, 'range_high': 50.0}
        if res == False:
            fail_exp = 'Hematocrit_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Hematocrit_Measurement.explanation = str(output_vals)
        return res

def dftest_Glomerular_Filtration_Rate_Measurement(data_df):
    #"National Kidney Foundation: https://www.kidney.org/kidney-topics/estimate-glomerular-filtration-rate"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Glomerular_Filtration_Rate_Measurement evaluation function. 95% of the population is expected to be between 90.0 and 120.0.'
    try:
        codes = ['40771922']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['40771922'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 90.0) & (data_df['value_as_number'] <= 120.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['40771922'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 90.0, 'range_high': 120.0}
        if res == False:
            fail_exp = 'Glomerular_Filtration_Rate_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Glomerular_Filtration_Rate_Measurement.explanation = str(output_vals)
        return res

def dftest_Urine_Protein_Measurement(data_df):
    #("National Kidney Foundation: https://www.kidney.org", "American Association for Clinical Chemistry: https://www.aacc.org")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Urine_Protein_Measurement evaluation function. 95% of the population is expected to be between 0.0 and 30.0.'
    try:
        codes = ['4211845']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['4211845'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 0.0) & (data_df['value_as_number'] <= 30.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['4211845'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 0.0, 'range_high': 30.0}
        if res == False:
            fail_exp = 'Urine_Protein_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Urine_Protein_Measurement.explanation = str(output_vals)
        return res

def dftest_Urine_Albumin_Measurement(data_df):
    #("National Kidney Foundation: https://www.kidney.org/atoz/content/albuminuria", "Mayo Clinic: https://www.mayoclinic.org/tests-procedures/urine-test/about/pac-20384907")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Urine_Albumin_Measurement evaluation function. 95% of the population is expected to be between 0.0 and 30.0.'
    try:
        codes = ['4152996']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['4152996'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 0.0) & (data_df['value_as_number'] <= 30.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['4152996'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 0.0, 'range_high': 30.0}
        if res == False:
            fail_exp = 'Urine_Albumin_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Urine_Albumin_Measurement.explanation = str(output_vals)
        return res

def dftest_Urine_Creatinine_Measurement(data_df):
    #"Healthline: https://www.healthline.com/health/protein-levels-in-urine; Mayo Clinic: https://www.mayoclinic.org/tests-procedures/creatinine-test/about/pac-20384604; Lab Tests Online: https://labtestsonline.org/tests/creatinine-urine"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Urine_Creatinine_Measurement evaluation function. 95% of the population is expected to be between 20.0 and 320.0.'
    try:
        codes = ['40309992']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['40309992'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 20.0) & (data_df['value_as_number'] <= 320.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['40309992'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 20.0, 'range_high': 320.0}
        if res == False:
            fail_exp = 'Urine_Creatinine_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Urine_Creatinine_Measurement.explanation = str(output_vals)
        return res

def dftest_Parathyroid_Hormone_Measurement(data_df):
    #"Cleveland Clinic: https://my.clevelandclinic.org/health/diagnostics/16888-blood-tests; Mayo Clinic Laboratories: https://www.mayocliniclabs.com/test-catalog/Overview/8365"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Parathyroid_Hormone_Measurement evaluation function. 95% of the population is expected to be between 10.0 and 65.0.'
    try:
        codes = ['4141751']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['4141751'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 10.0) & (data_df['value_as_number'] <= 65.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['4141751'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 10.0, 'range_high': 65.0}
        if res == False:
            fail_exp = 'Parathyroid_Hormone_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Parathyroid_Hormone_Measurement.explanation = str(output_vals)
        return res

# Filename: unit_test5.py

def dftest_Serum_Bicarbonate_Measurement(data_df):
    #"Cleveland Clinic: https://my.clevelandclinic.org/health/diagnostics/16888-blood-tests"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Bicarbonate_Measurement evaluation function. 95% of the population is expected to be between 22.0 and 29.0.'
    try:
        codes = ['4150494']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['4150494'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 22.0) & (data_df['value_as_number'] <= 29.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['4150494'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 22.0, 'range_high': 29.0}
        if res == False:
            fail_exp = 'Serum_Bicarbonate_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Bicarbonate_Measurement.explanation = str(output_vals)
        return res

def dftest_Serum_Chloride_Measurement(data_df):
    #"Cleveland Clinic: https://my.clevelandclinic.org/health/diagnostics/16888-blood-tests; Mayo Clinic: https://www.mayoclinic.org/tests-procedures/chloride-test/about/pac-20384900"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Chloride_Measurement evaluation function. 95% of the population is expected to be between 96.0 and 106.0.'
    try:
        codes = ['4153270']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['4153270'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 96.0) & (data_df['value_as_number'] <= 106.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['4153270'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 96.0, 'range_high': 106.0}
        if res == False:
            fail_exp = 'Serum_Chloride_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Chloride_Measurement.explanation = str(output_vals)
        return res

def dftest_Serum_Magnesium_Measurement(data_df):
    #"Cleveland Clinic: https://my.clevelandclinic.org/health/diagnostics/16888-blood-tests"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Magnesium_Measurement evaluation function. 95% of the population is expected to be between 1.7 and 2.2.'
    try:
        codes = ['4270766']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['4270766'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 1.7) & (data_df['value_as_number'] <= 2.2)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['4270766'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 1.7, 'range_high': 2.2}
        if res == False:
            fail_exp = 'Serum_Magnesium_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Magnesium_Measurement.explanation = str(output_vals)
        return res

def dftest_Serum_Uric_Acid_Measurement(data_df):
    #"Cleveland Clinic: https://my.clevelandclinic.org/health/diagnostics/16888-blood-tests; Mayo Clinic: https://www.mayoclinic.org/tests-procedures/uric-acid-test/about/pac-20384914"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Uric_Acid_Measurement evaluation function. 95% of the population is expected to be between 2.4 and 7.0.'
    try:
        codes = ['4076924']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['4076924'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 2.4) & (data_df['value_as_number'] <= 7.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['4076924'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 2.4, 'range_high': 7.0}
        if res == False:
            fail_exp = 'Serum_Uric_Acid_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Uric_Acid_Measurement.explanation = str(output_vals)
        return res

def dftest_Serum_Total_Protein_Measurement(data_df):
    #"Cleveland Clinic: https://my.clevelandclinic.org/health/diagnostics/16888-blood-tests; Mayo Clinic: https://www.mayoclinic.org/tests-procedures/total-protein-test/about/pac-20384985"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Total_Protein_Measurement evaluation function. 95% of the population is expected to be between 6.0 and 8.3.'
    try:
        codes = ['4152983']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['4152983'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 6.0) & (data_df['value_as_number'] <= 8.3)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['4152983'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 6.0, 'range_high': 8.3}
        if res == False:
            fail_exp = 'Serum_Total_Protein_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Total_Protein_Measurement.explanation = str(output_vals)
        return res

def dftest_Serum_Alkaline_Phosphatase_Measurement(data_df):
    #"Cleveland Clinic: https://my.clevelandclinic.org/health/diagnostics/16888-blood-tests; Mayo Clinic: https://www.mayoclinic.org/tests-procedures/alkaline-phosphatase/about/pac-20384923"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Alkaline_Phosphatase_Measurement evaluation function. 95% of the population is expected to be between 44.0 and 121.0.'
    try:
        codes = ['4156813']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['4156813'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 44.0) & (data_df['value_as_number'] <= 121.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['4156813'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 44.0, 'range_high': 121.0}
        if res == False:
            fail_exp = 'Serum_Alkaline_Phosphatase_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Alkaline_Phosphatase_Measurement.explanation = str(output_vals)
        return res

def dftest_Serum_Aspartate_Aminotransferase_Measurement(data_df):
    #"Cleveland Clinic: https://my.clevelandclinic.org/health/diagnostics/16888-blood-tests; Mayo Clinic: https://www.mayoclinic.org/tests-procedures/liver-function-tests/about/pac-20394595"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Aspartate_Aminotransferase_Measurement evaluation function. 95% of the population is expected to be between 8.0 and 33.0.'
    try:
        codes = ['37392189']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['37392189'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 8.0) & (data_df['value_as_number'] <= 33.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['37392189'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 8.0, 'range_high': 33.0}
        if res == False:
            fail_exp = 'Serum_Aspartate_Aminotransferase_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Aspartate_Aminotransferase_Measurement.explanation = str(output_vals)
        return res

def dftest_Serum_Alanine_Aminotransferase_Measurement(data_df):
    #"Cleveland Clinic: https://my.clevelandclinic.org/health/diagnostics/16888-blood-tests"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Alanine_Aminotransferase_Measurement evaluation function. 95% of the population is expected to be between 7.0 and 56.0.'
    try:
        codes = ['3006923']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['3006923'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 7.0) & (data_df['value_as_number'] <= 56.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['3006923'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 7.0, 'range_high': 56.0}
        if res == False:
            fail_exp = 'Serum_Alanine_Aminotransferase_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Alanine_Aminotransferase_Measurement.explanation = str(output_vals)
        return res

def dftest_Serum_Bilirubin_Measurement(data_df):
    #"Cleveland Clinic: https://my.clevelandclinic.org/health/diagnostics/16888-blood-tests; Mayo Clinic: https://www.mayoclinic.org/tests-procedures/bilirubin-test/about/pac-20384812"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Bilirubin_Measurement evaluation function. 95% of the population is expected to be between 0.1 and 1.2.'
    try:
        codes = ['4197972']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['4197972'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 0.1) & (data_df['value_as_number'] <= 1.2)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['4197972'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 0.1, 'range_high': 1.2}
        if res == False:
            fail_exp = 'Serum_Bilirubin_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Bilirubin_Measurement.explanation = str(output_vals)
        return res

def dftest_Serum_Ferritin_Measurement(data_df):
    #"Mayo Clinic: https://www.mayoclinic.org/tests-procedures/ferritin-test/about/pac-20384928, LabCorp: https://www.labcorp.com/tests/004598/ferritin"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Ferritin_Measurement evaluation function. 95% of the population is expected to be between 24.0 and 336.0.'
    try:
        codes = ['4148588']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['4148588'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 24.0) & (data_df['value_as_number'] <= 336.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['4148588'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 24.0, 'range_high': 336.0}
        if res == False:
            fail_exp = 'Serum_Ferritin_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Ferritin_Measurement.explanation = str(output_vals)
        return res

def dftest_Serum_Transferrin_Measurement(data_df):
    #"MedicineNet: https://www.medicinenet.com/ferritin_blood_test/article.htm; Mayo Clinic: https://www.mayoclinic.org/tests-procedures/transferrin-test/about/pac-20384922; LabCorp: https://www.labcorp.com/tests/001321/transferrin"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Transferrin_Measurement evaluation function. 95% of the population is expected to be between 200.0 and 400.0.'
    try:
        codes = ['40315296']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['40315296'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 200.0) & (data_df['value_as_number'] <= 400.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['40315296'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 200.0, 'range_high': 400.0}
        if res == False:
            fail_exp = 'Serum_Transferrin_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Transferrin_Measurement.explanation = str(output_vals)
        return res

def dftest_Serum_Creatinine_Measurement_1(data_df):
    #"Mayo Clinic: https://www.mayoclinic.org/tests-procedures/creatinine-test/about/pac-20384646; NIH: https://medlineplus.gov/lab-tests/creatinine-test/"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Creatinine_Measurement evaluation function. 95% of the population is expected to be between 0.6 and 1.2.'
    try:
        codes = ['40307212']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['40307212'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 0.6) & (data_df['value_as_number'] <= 1.2)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['40307212'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 0.6, 'range_high': 1.2}
        if res == False:
            fail_exp = 'Serum_Creatinine_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Creatinine_Measurement_1.explanation = str(output_vals)
        return res

def dftest_Blood_Urea_Nitrogen_Measurement_1(data_df):
    #"WebMD: https://www.webmd.com/a-to-z-guides/blood-urea-nitrogen; Mayo Clinic: https://www.mayoclinic.org/tests-procedures/blood-urea-nitrogen/about/pac-20384821; MedlinePlus: https://medlineplus.gov/lab-tests/blood-urea-nitrogen-bun-test/"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Blood_Urea_Nitrogen_Measurement evaluation function. 95% of the population is expected to be between 7.0 and 20.0.'
    try:
        codes = ['3028280']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['3028280'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 7.0) & (data_df['value_as_number'] <= 20.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['3028280'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 7.0, 'range_high': 20.0}
        if res == False:
            fail_exp = 'Blood_Urea_Nitrogen_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Blood_Urea_Nitrogen_Measurement_1.explanation = str(output_vals)
        return res

def dftest_Serum_Albumin_Measurement_1(data_df):
    #"Cleveland Clinic: https://my.clevelandclinic.org/health/diagnostics/16888-blood-tests; MedlinePlus: https://medlineplus.gov/lab-tests/albumin-blood-test"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Albumin_Measurement evaluation function. 95% of the population is expected to be between 3.5 and 5.0.'
    try:
        codes = ['40307274']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['40307274'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 3.5) & (data_df['value_as_number'] <= 5.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['40307274'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 3.5, 'range_high': 5.0}
        if res == False:
            fail_exp = 'Serum_Albumin_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Albumin_Measurement_1.explanation = str(output_vals)
        return res

def dftest_Hemoglobin_Measurement_1(data_df):
    #"Cleveland Clinic: https://my.clevelandclinic.org/health/diagnostics/16888-blood-tests; Mayo Clinic: https://www.mayoclinic.org/tests-procedures/hemoglobin-test/about/pac-20385075"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Hemoglobin_Measurement evaluation function. 95% of the population is expected to be between 12.0 and 18.0.'
    try:
        codes = ['4154636']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['4154636'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 12.0) & (data_df['value_as_number'] <= 18.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['4154636'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 12.0, 'range_high': 18.0}
        if res == False:
            fail_exp = 'Hemoglobin_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Hemoglobin_Measurement_1.explanation = str(output_vals)
        return res

def dftest_Serum_Chloride_Measurement_1(data_df):
    #"Cleveland Clinic: https://my.clevelandclinic.org/health/diagnostics/16888-blood-tests; Mayo Clinic: https://www.mayoclinic.org/tests-procedures/chloride-test/about/pac-20384900"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Chloride_Measurement evaluation function. 95% of the population is expected to be between 96.0 and 106.0.'
    try:
        codes = ['4153270']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['4153270'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 96.0) & (data_df['value_as_number'] <= 106.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['4153270'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 96.0, 'range_high': 106.0}
        if res == False:
            fail_exp = 'Serum_Chloride_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Chloride_Measurement_1.explanation = str(output_vals)
        return res

def dftest_Serum_Uric_Acid_Measurement_1(data_df):
    #"Cleveland Clinic: https://my.clevelandclinic.org/health/diagnostics/16888-blood-tests; Mayo Clinic: https://www.mayoclinic.org/tests-procedures/uric-acid-test/about/pac-20384914"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Uric_Acid_Measurement evaluation function. 95% of the population is expected to be between 2.6 and 7.2.'
    try:
        codes = ['4076924']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['4076924'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 2.6) & (data_df['value_as_number'] <= 7.2)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['4076924'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 2.6, 'range_high': 7.2}
        if res == False:
            fail_exp = 'Serum_Uric_Acid_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Uric_Acid_Measurement_1.explanation = str(output_vals)
        return res

def dftest_Serum_Bilirubin_Measurement_1(data_df):
    #"Cleveland Clinic: https://my.clevelandclinic.org/health/diagnostics/16888-blood-tests; Mayo Clinic: https://www.mayoclinic.org/tests-procedures/bilirubin-test/about/pac-20384812"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Bilirubin_Measurement evaluation function. 95% of the population is expected to be between 0.1 and 1.2.'
    try:
        codes = ['4197972']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['4197972'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 0.1) & (data_df['value_as_number'] <= 1.2)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['4197972'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 0.1, 'range_high': 1.2}
        if res == False:
            fail_exp = 'Serum_Bilirubin_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Bilirubin_Measurement_1.explanation = str(output_vals)
        return res



