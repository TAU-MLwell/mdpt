Filename: unit_test0.py

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
    # ref: ['("American Heart Association, 2023: https://www.heart.org", "U.S. Census Bureau, 2023: https://www.census.gov")']
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Five year mean incidence comparison function (2016-2021). Theoretical value is expected to be 10 per 1,000 person-years.'
    try:
        # Diagnosis codes for Congestive Heart Failure
        diagnosis_codes = ['428.0', '428.2', '428.9', '398.91', '428.2', '428.0']
        # Initialize an empty list to store incidence rates
        incidence = []
        # Loop through the years 2016 to 2021
        for i in range(0, 6):
            year = 2016 + i
            # Filter the dataframe for the specific year
            df_year = data_df[data_df['admittime'].dt.year == year]
            # Calculate the incidence rate for the year
            incidence_rate = 100*df_year[df_year['icd9_code'].astype(str).isin(diagnosis_codes)]['subject_id'].nunique() / data_df['subject_id'].nunique()
            # Append the incidence rate to the list
            incidence.append(incidence_rate)
        # Calculate the mean incidence rate
        mean_incidence = np.mean(incidence)
        expected_incidence = 10
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
    # ref: ['("American Heart Association, 2023: https://www.heart.org", "U.S. Census Bureau, 2023: https://www.census.gov")']
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Prevalence comparison function. Theoretical value is expected to be 2.2.'
    try:
        # Diagnosis codes for Congestive Heart Failure
        diagnosis_codes = ['428.0', '428.2', '428.9', '398.91', '428.2', '428.0']
        # Calculate the prevalence of Congestive Heart Failure
        prevalence = 100*data_df[data_df['icd9_code'].astype(str).isin(diagnosis_codes)]['subject_id'].nunique() / data_df['subject_id'].nunique()
        expected_prevalence = 2.2
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
    # ref: ['("PubMed, National Trends in Heart Failure Hospitalizations", "https://pubmed.ncbi.nlm.nih.gov", "CDC Heart Failure Statistics", "https://www.cdc.gov/heartdisease/heart_failure.htm", "American Heart Association Heart Failure Data", "https://www.heart.org/en/health-topics/heart-failure")']
    '''Calculates and compares age distribution of Congestive Heart Failure patients'''
    limit = 0.05
    #calculate age distribution of patients
    try:
        
        data_df = data_df[data_df['icd9_code'].astype(str).isin(['428.0', '428.2', '428.9', '398.91', '428.2', '428.0'])]
        data_df['admittime'] = pd.to_datetime(data_df['admittime'])
        data_df['dob'] = pd.to_datetime(data_df['dob'])
        data_df['diagnosis_age'] = data_df['admittime'].dt.year - data_df['dob'].dt.year
        data_df = data_df.sort_values(by=['subject_id','admittime'], ascending=True)
        unique_patients = data_df.dropna(subset=['admittime'], axis=0).drop_duplicates(subset=['subject_id'], keep='first')
        data_dist = unique_patients['diagnosis_age'].value_counts()
        data_stats = unique_patients['diagnosis_age'].describe()
        var_data = data_stats['std'].item()**2
        var_th = 104.03999999999999
        df = ((var_data/data_stats['count'].item()) + (var_th/(157000)))**2/(var_data**2/((data_stats['count'].item()**2) * (data_stats['count'].item() -1)) + var_th**2/(24649000000 * (157000 - 1)))
        Sx_data = data_stats['std'].item()/math.sqrt(data_stats['count'].item())
        Sx_th = 10.2/math.sqrt(157000)
        tt = (data_stats['mean'].item() - 72.1)/math.sqrt(Sx_data+Sx_th)
        pval = 2*stdtr(df, -np.abs(tt))
        res = pval
        
        if pval > limit:
            binary = "Pass"
            explanation = 'Age distribution matches the theoretical distribution - 72.1 +- 10.2'
        else:
            binary = "Fail"
            explanation = 'Age distribution is expected to be ' + str(72.1) + ' +- ' + str(10.2) + '; in the data it is ' + str(data_stats['mean'].item()) + ' +- ' + str(data_stats['std'].item())
    
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
    #"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2763498/, https://www.ahajournals.org/journal/circ"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Hypertension_diagnosis_codes rate comparison function. Theoretical value is expected to be between 60.0 and 80.0.'
    try:
        diagnosed_ids = data_df[data_df['icd9_code'].astype(str).isin(['428.0', '428.2', '428.9', '398.91', '428.2', '428.0'])]['subject_id'].unique()
        diagnosed = data_df[data_df['subject_id'].isin(diagnosed_ids)]
        codes = ['401', '401.9', '402', '402.9', '403.9', '404.9', '405', '362.11']
        data_per = 100 * diagnosed[diagnosed['icd9_code'].astype(str).isin(codes)]['subject_id'].nunique() / diagnosed['subject_id'].nunique()
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

def dftest_Diabetes_Mellitus_diagnosis_codes_diagnosed(data_df):
    #("https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2763498/")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Diabetes_Mellitus_diagnosis_codes rate comparison function. Theoretical value is expected to be 40.0.'
    try:
        diagnosed_ids = data_df[data_df['icd9_code'].astype(str).isin(['428.0', '428.2', '428.9', '398.91', '428.2', '428.0'])]['subject_id'].unique()
        diagnosed = data_df[data_df['subject_id'].isin(diagnosed_ids)]
        codes = ['250', '250.0', '250.02', '250.5', '250.7', '249']
        data_per = 100 * diagnosed[diagnosed['icd9_code'].astype(str).isin(codes)]['subject_id'].nunique() / diagnosed['subject_id'].nunique()
        val = (data_per - 40.0) / np.sqrt((data_per * (100 - data_per) + 40.0 * (100 - 40.0)) / 2)
        ratio = data_per / 40.0
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 40.0, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: Diabetes_Mellitus_diagnosis_codes percentage in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Diabetes_Mellitus_diagnosis_codes_diagnosed.explanation = str(output_vals)
        return res

def dftest_Chronic_Obstructive_Pulmonary_Disease_diagnosis_codes_diagnosed(data_df):
    #("https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2763498/", "https://pubmed.ncbi.nlm.nih.gov/19875773/")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Chronic_Obstructive_Pulmonary_Disease_diagnosis_codes rate comparison function. Theoretical value is expected to be between 20.0 and 30.0.'
    try:
        diagnosed_ids = data_df[data_df['icd9_code'].astype(str).isin(['428.0', '428.2', '428.9', '398.91', '428.2', '428.0'])]['subject_id'].unique()
        diagnosed = data_df[data_df['subject_id'].isin(diagnosed_ids)]
        codes = ['491', '491.2', '493.2', '491.20', '493.20', '416', '416.9']
        data_per = 100 * diagnosed[diagnosed['icd9_code'].astype(str).isin(codes)]['subject_id'].nunique() / diagnosed['subject_id'].nunique()
        res = (20.0 <= data_per <= 30.0)
        output_vals = {'data_per': data_per, 'range_low': 20.0, 'range_high': 30.0}
        if res == False:
            fail_exp = 'Among diagnosed: Chronic_Obstructive_Pulmonary_Disease_diagnosis_codes evaluation in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Chronic_Obstructive_Pulmonary_Disease_diagnosis_codes_diagnosed.explanation = str(output_vals)
        return res

def dftest_Atrial_Fibrillation_diagnosis_codes_diagnosed(data_df):
    #("https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2763498/")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Atrial_Fibrillation_diagnosis_codes rate comparison function. Theoretical value is expected to be between 20.0 and 40.0.'
    try:
        diagnosed_ids = data_df[data_df['icd9_code'].astype(str).isin(['428.0', '428.2', '428.9', '398.91', '428.2', '428.0'])]['subject_id'].unique()
        diagnosed = data_df[data_df['subject_id'].isin(diagnosed_ids)]
        codes = ['427.31', '427.3', '427.32', '427.4', '427.41', '426.10']
        data_per = 100 * diagnosed[diagnosed['icd9_code'].astype(str).isin(codes)]['subject_id'].nunique() / diagnosed['subject_id'].nunique()
        res = (20.0 <= data_per <= 40.0)
        output_vals = {'data_per': data_per, 'range_low': 20.0, 'range_high': 40.0}
        if res == False:
            fail_exp = 'Among diagnosed: Atrial_Fibrillation_diagnosis_codes evaluation in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Atrial_Fibrillation_diagnosis_codes_diagnosed.explanation = str(output_vals)
        return res

def dftest_Coronary_Artery_Disease_diagnosis_codes_diagnosed(data_df):
    #("https://www.jacc.org/doi/full/10.1016/j.jacc.2015.06.1033")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Coronary_Artery_Disease_diagnosis_codes rate comparison function. Theoretical value is expected to be between 40.0 and 60.0.'
    try:
        diagnosed_ids = data_df[data_df['icd9_code'].astype(str).isin(['428.0', '428.2', '428.9', '398.91', '428.2', '428.0'])]['subject_id'].unique()
        diagnosed = data_df[data_df['subject_id'].isin(diagnosed_ids)]
        codes = ['414.0', '414.01', '414.06', '414.04', '414.11', '414.4', '429.2', '429.9', '746.85']
        data_per = 100 * diagnosed[diagnosed['icd9_code'].astype(str).isin(codes)]['subject_id'].nunique() / diagnosed['subject_id'].nunique()
        res = (40.0 <= data_per <= 60.0)
        output_vals = {'data_per': data_per, 'range_low': 40.0, 'range_high': 60.0}
        if res == False:
            fail_exp = 'Among diagnosed: Coronary_Artery_Disease_diagnosis_codes evaluation in the examined data is ' + str(data_per)
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

def dftest_Anemia_diagnosis_codes_diagnosed(data_df):
    #("https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2763498/", "https://pubmed.ncbi.nlm.nih.gov/18474750/")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Anemia_diagnosis_codes rate comparison function. Theoretical value is expected to be between 30.0 and 50.0.'
    try:
        diagnosed_ids = data_df[data_df['icd9_code'].astype(str).isin(['428.0', '428.2', '428.9', '398.91', '428.2', '428.0'])]['subject_id'].unique()
        diagnosed = data_df[data_df['subject_id'].isin(diagnosed_ids)]
        codes = ['285.9', '285.22', '285.2', '281.8', '285.29', '280.9', '280', '285.0', '281']
        data_per = 100 * diagnosed[diagnosed['icd9_code'].astype(str).isin(codes)]['subject_id'].nunique() / diagnosed['subject_id'].nunique()
        res = (30.0 <= data_per <= 50.0)
        output_vals = {'data_per': data_per, 'range_low': 30.0, 'range_high': 50.0}
        if res == False:
            fail_exp = 'Among diagnosed: Anemia_diagnosis_codes evaluation in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Anemia_diagnosis_codes_diagnosed.explanation = str(output_vals)
        return res

def dftest_Renal_Failure_diagnosis_codes_diagnosed(data_df):
    #"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2763498/, https://www.jacc.org/"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Renal_Failure_diagnosis_codes rate comparison function. Theoretical value is expected to be between 20.0 and 30.0.'
    try:
        diagnosed_ids = data_df[data_df['icd9_code'].astype(str).isin(['428.0', '428.2', '428.9', '398.91', '428.2', '428.0'])]['subject_id'].unique()
        diagnosed = data_df[data_df['subject_id'].isin(diagnosed_ids)]
        codes = ['584', '584.6', '584.7', '584.9', '587', '588', '753.15']
        data_per = 100 * diagnosed[diagnosed['icd9_code'].astype(str).isin(codes)]['subject_id'].nunique() / diagnosed['subject_id'].nunique()
        res = (20.0 <= data_per <= 30.0)
        output_vals = {'data_per': data_per, 'range_low': 20.0, 'range_high': 30.0}
        if res == False:
            fail_exp = 'Among diagnosed: Renal_Failure_diagnosis_codes evaluation in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Renal_Failure_diagnosis_codes_diagnosed.explanation = str(output_vals)
        return res

def dftest_Obesity_diagnosis_codes_diagnosed(data_df):
    #"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2763498/"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Obesity_diagnosis_codes rate comparison function. Theoretical value is expected to be 35.0.'
    try:
        diagnosed_ids = data_df[data_df['icd9_code'].astype(str).isin(['428.0', '428.2', '428.9', '398.91', '428.2', '428.0'])]['subject_id'].unique()
        diagnosed = data_df[data_df['subject_id'].isin(diagnosed_ids)]
        codes = ['278.00', '278.01', '278.03', '278.0', '278']
        data_per = 100 * diagnosed[diagnosed['icd9_code'].astype(str).isin(codes)]['subject_id'].nunique() / diagnosed['subject_id'].nunique()
        val = (data_per - 35.0) / np.sqrt((data_per * (100 - data_per) + 35.0 * (100 - 35.0)) / 2)
        ratio = data_per / 35.0
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 35.0, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: Obesity_diagnosis_codes percentage in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Obesity_diagnosis_codes_diagnosed.explanation = str(output_vals)
        return res

def dftest_Hyperlipidemia_diagnosis_codes_diagnosed(data_df):
    #"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2763498/"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Hyperlipidemia_diagnosis_codes rate comparison function. Theoretical value is expected to be between 40.0 and 60.0.'
    try:
        diagnosed_ids = data_df[data_df['icd9_code'].astype(str).isin(['428.0', '428.2', '428.9', '398.91', '428.2', '428.0'])]['subject_id'].unique()
        diagnosed = data_df[data_df['subject_id'].isin(diagnosed_ids)]
        codes = ['272.2', '272.4', '272.0']
        data_per = 100 * diagnosed[diagnosed['icd9_code'].astype(str).isin(codes)]['subject_id'].nunique() / diagnosed['subject_id'].nunique()
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

def dftest_Depression_diagnosis_codes_diagnosed(data_df):
    #"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2763498/"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Depression_diagnosis_codes rate comparison function. Theoretical value is expected to be between 20.0 and 40.0.'
    try:
        diagnosed_ids = data_df[data_df['icd9_code'].astype(str).isin(['428.0', '428.2', '428.9', '398.91', '428.2', '428.0'])]['subject_id'].unique()
        diagnosed = data_df[data_df['subject_id'].isin(diagnosed_ids)]
        codes = ['311', '296.2', '296.20', '296.21', '296.22', '296.30', '296.31', '296.32', '296.34', '298.0', '296.3', '296.82']
        data_per = 100 * diagnosed[diagnosed['icd9_code'].astype(str).isin(codes)]['subject_id'].nunique() / diagnosed['subject_id'].nunique()
        res = (20.0 <= data_per <= 40.0)
        output_vals = {'data_per': data_per, 'range_low': 20.0, 'range_high': 40.0}
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

def dftest_Peripheral_Vascular_Disease_diagnosis_codes_diagnosed(data_df):
    #"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2763498/"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Peripheral_Vascular_Disease_diagnosis_codes rate comparison function. Theoretical value is expected to be 15.0.'
    try:
        diagnosed_ids = data_df[data_df['icd9_code'].astype(str).isin(['428.0', '428.2', '428.9', '398.91', '428.2', '428.0'])]['subject_id'].unique()
        diagnosed = data_df[data_df['subject_id'].isin(diagnosed_ids)]
        codes = ['443.9', '443.8', '443', '997.2', '443.81', '250.7', '747.60', '747.6']
        data_per = 100 * diagnosed[diagnosed['icd9_code'].astype(str).isin(codes)]['subject_id'].nunique() / diagnosed['subject_id'].nunique()
        val = (data_per - 15.0) / np.sqrt((data_per * (100 - data_per) + 15.0 * (100 - 15.0)) / 2)
        ratio = data_per / 15.0
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 15.0, 'ratio': ratio, 'smd': val}
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

def dftest_Sleep_Apnea_diagnosis_codes_diagnosed(data_df):
    #("https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2763498/", "https://www.ahajournals.org/doi/10.1161/CIRCHEARTFAILURE.109.873265")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Sleep_Apnea_diagnosis_codes rate comparison function. Theoretical value is expected to be between 30.0 and 50.0.'
    try:
        diagnosed_ids = data_df[data_df['icd9_code'].astype(str).isin(['428.0', '428.2', '428.9', '398.91', '428.2', '428.0'])]['subject_id'].unique()
        diagnosed = data_df[data_df['subject_id'].isin(diagnosed_ids)]
        codes = ['327.2', '327.20', '327.21', '327.23', '327.26', '327.27', '327.29', '780.51', '780.53', '780.57', '307.46', '786.03']
        data_per = 100 * diagnosed[diagnosed['icd9_code'].astype(str).isin(codes)]['subject_id'].nunique() / diagnosed['subject_id'].nunique()
        res = (30.0 <= data_per <= 50.0)
        output_vals = {'data_per': data_per, 'range_low': 30.0, 'range_high': 50.0}
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

def dftest_Hypothyroidism_diagnosis_codes_diagnosed(data_df):
    #"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2763498/"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Hypothyroidism_diagnosis_codes rate comparison function. Theoretical value is expected to be 15.0.'
    try:
        diagnosed_ids = data_df[data_df['icd9_code'].astype(str).isin(['428.0', '428.2', '428.9', '398.91', '428.2', '428.0'])]['subject_id'].unique()
        diagnosed = data_df[data_df['subject_id'].isin(diagnosed_ids)]
        codes = ['244', '244.9', '244.1', '244.2', '243', '245']
        data_per = 100 * diagnosed[diagnosed['icd9_code'].astype(str).isin(codes)]['subject_id'].nunique() / diagnosed['subject_id'].nunique()
        val = (data_per - 15.0) / np.sqrt((data_per * (100 - data_per) + 15.0 * (100 - 15.0)) / 2)
        ratio = data_per / 15.0
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 15.0, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: Hypothyroidism_diagnosis_codes percentage in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Hypothyroidism_diagnosis_codes_diagnosed.explanation = str(output_vals)
        return res

def dftest_Stroke_diagnosis_codes_diagnosed(data_df):
    #("https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2763498/")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Stroke_diagnosis_codes rate comparison function. Theoretical value is expected to be 10.0.'
    try:
        diagnosed_ids = data_df[data_df['icd9_code'].astype(str).isin(['428.0', '428.2', '428.9', '398.91', '428.2', '428.0'])]['subject_id'].unique()
        diagnosed = data_df[data_df['subject_id'].isin(diagnosed_ids)]
        codes = ['434.91', '434.01', '434.11', '436']
        data_per = 100 * diagnosed[diagnosed['icd9_code'].astype(str).isin(codes)]['subject_id'].nunique() / diagnosed['subject_id'].nunique()
        val = (data_per - 10.0) / np.sqrt((data_per * (100 - data_per) + 10.0 * (100 - 10.0)) / 2)
        ratio = data_per / 10.0
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 10.0, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: Stroke_diagnosis_codes percentage in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Stroke_diagnosis_codes_diagnosed.explanation = str(output_vals)
        return res

def dftest_Liver_Disease_diagnosis_codes_diagnosed(data_df):
    #"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2763498/"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Liver_Disease_diagnosis_codes rate comparison function. Theoretical value is expected to be 10.0.'
    try:
        diagnosed_ids = data_df[data_df['icd9_code'].astype(str).isin(['428.0', '428.2', '428.9', '398.91', '428.2', '428.0'])]['subject_id'].unique()
        diagnosed = data_df[data_df['subject_id'].isin(diagnosed_ids)]
        codes = ['571', '573', '572']
        data_per = 100 * diagnosed[diagnosed['icd9_code'].astype(str).isin(codes)]['subject_id'].nunique() / diagnosed['subject_id'].nunique()
        val = (data_per - 10.0) / np.sqrt((data_per * (100 - data_per) + 10.0 * (100 - 10.0)) / 2)
        ratio = data_per / 10.0
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 10.0, 'ratio': ratio, 'smd': val}
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

def dftest_Gender_of_the_patient_Male_(data_df):
    #"https://www.mass.gov/info-details/basic-facts, https://www.census.gov/quickfacts/MA"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Gender_of_the_patient__Male_ evaluation function. Result is expected to be 48.5%.'
    try:
        codes = ['M']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['gender'].astype(str).isin(codes)]['subject_id'].nunique() / ref_for_percentage['subject_id'].nunique()
        val = (data_per - 48.5) / np.sqrt((data_per * (100 - data_per) + 48.5 * (100 - 48.5)) / 2)
        ratio = data_per / 48.5
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 48.5, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Gender_of_the_patient__Male_ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Gender_of_the_patient_Male_.explanation = str(output_vals)
        return res

def dftest_Gender_of_the_patient_Female_(data_df):
    #("https://www.mass.gov/info-details/basic-facts", "https://www.census.gov/quickfacts/MA")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Gender_of_the_patient__Female_ evaluation function. Result is expected to be 51.5%.'
    try:
        codes = ['F']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['gender'].astype(str).isin(codes)]['subject_id'].nunique() / ref_for_percentage['subject_id'].nunique()
        val = (data_per - 51.5) / np.sqrt((data_per * (100 - data_per) + 51.5 * (100 - 51.5)) / 2)
        ratio = data_per / 51.5
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 51.5, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Gender_of_the_patient__Female_ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Gender_of_the_patient_Female_.explanation = str(output_vals)
        return res

def dftest_Ethnicity_of_the_patient_White_(data_df):
    #"https://www.census.gov/quickfacts/MA"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Ethnicity_of_the_patient__White_ evaluation function. Result is expected to be 67.6%.'
    try:
        codes = ['WHITE']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['ethnicity'].astype(str).isin(codes)]['subject_id'].nunique() / ref_for_percentage['subject_id'].nunique()
        val = (data_per - 67.6) / np.sqrt((data_per * (100 - data_per) + 67.6 * (100 - 67.6)) / 2)
        ratio = data_per / 67.6
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 67.6, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Ethnicity_of_the_patient__White_ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Ethnicity_of_the_patient_White_.explanation = str(output_vals)
        return res

def dftest_Ethnicity_of_the_patient_Black_African_American_(data_df):
    #"https://www.census.gov/quickfacts/MA"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Ethnicity_of_the_patient__Black_African_American_ evaluation function. Result is expected to be 9%.'
    try:
        codes = ['BLACK/AFRICAN AMERICAN']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['ethnicity'].astype(str).isin(codes)]['subject_id'].nunique() / ref_for_percentage['subject_id'].nunique()
        val = (data_per - 9) / np.sqrt((data_per * (100 - data_per) + 9 * (100 - 9)) / 2)
        ratio = data_per / 9
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 9, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Ethnicity_of_the_patient__Black_African_American_ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Ethnicity_of_the_patient_Black_African_American_.explanation = str(output_vals)
        return res

def dftest_Ethnicity_of_the_patient_Asian_(data_df):
    #("https://www.census.gov/quickfacts/MA")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Ethnicity_of_the_patient__Asian_ evaluation function. Result is expected to be 7.2%.'
    try:
        codes = ['ASIAN']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['ethnicity'].astype(str).isin(codes)]['subject_id'].nunique() / ref_for_percentage['subject_id'].nunique()
        val = (data_per - 7.2) / np.sqrt((data_per * (100 - data_per) + 7.2 * (100 - 7.2)) / 2)
        ratio = data_per / 7.2
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 7.2, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Ethnicity_of_the_patient__Asian_ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Ethnicity_of_the_patient_Asian_.explanation = str(output_vals)
        return res

def dftest_Ethnicity_of_the_patient_Hispanic_Latino_(data_df):
    #("https://www.census.gov/quickfacts/MA")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Ethnicity_of_the_patient__Hispanic_Latino_ evaluation function. Result is expected to be 12.8%.'
    try:
        codes = ['HISPANIC/LATINO']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['ethnicity'].astype(str).isin(codes)]['subject_id'].nunique() / ref_for_percentage['subject_id'].nunique()
        val = (data_per - 12.8) / np.sqrt((data_per * (100 - data_per) + 12.8 * (100 - 12.8)) / 2)
        ratio = data_per / 12.8
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 12.8, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Ethnicity_of_the_patient__Hispanic_Latino_ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Ethnicity_of_the_patient_Hispanic_Latino_.explanation = str(output_vals)
        return res

def dftest_Ethnicity_of_the_patient_Other_(data_df):
    #"https://www.census.gov/quickfacts/fact/table/US/PST045222"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Ethnicity_of_the_patient__Other_ evaluation function. Result is expected to be 2.6%.'
    try:
        codes = ['OTHER']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['ethnicity'].astype(str).isin(codes)]['subject_id'].nunique() / ref_for_percentage['subject_id'].nunique()
        val = (data_per - 2.6) / np.sqrt((data_per * (100 - data_per) + 2.6 * (100 - 2.6)) / 2)
        ratio = data_per / 2.6
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 2.6, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Ethnicity_of_the_patient__Other_ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Ethnicity_of_the_patient_Other_.explanation = str(output_vals)
        return res



# Filename: unit_test3.py

def dftest_Lisinopril(data_df):
    #("American Heart Association (AHA): https://www.ahajournals.org/", "National Center for Biotechnology Information (NCBI): https://pubmed.ncbi.nlm.nih.gov/")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Lisinopril treatment comparison function. Theoretical value is expected to be between 25.0 and 30.0.'
    try:
        codes = ['OMOP5144214', 'OMOP5144239', 'OMOP5144188', 'OMOP682007', 'OMOP682008']
        data_per = 100 * data_df[data_df['formulary_drug_cd'].astype(str).isin(codes)]['subject_id'].nunique() / data_df['subject_id'].nunique()
        res = (25.0 <= data_per <= 30.0)
        output_vals = {'data_per': data_per, 'range_low': 25.0, 'range_high': 30.0}
        if res == False:
            fail_exp = 'Lisinopril evaluation in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Lisinopril.explanation = str(output_vals)
        return res

def dftest_Carvedilol(data_df):
    #("https://pubmed.ncbi.nlm.nih.gov/39969604/", "https://www.ahajournals.org")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Carvedilol treatment comparison function. Theoretical value is expected to be between 10.0 and 15.0.'
    try:
        codes = ['OMOP4963242', 'OMOP673567', 'OMOP1036662', 'OMOP4963243']
        data_per = 100 * data_df[data_df['formulary_drug_cd'].astype(str).isin(codes)]['subject_id'].nunique() / data_df['subject_id'].nunique()
        res = (10.0 <= data_per <= 15.0)
        output_vals = {'data_per': data_per, 'range_low': 10.0, 'range_high': 15.0}
        if res == False:
            fail_exp = 'Carvedilol evaluation in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Carvedilol.explanation = str(output_vals)
        return res

def dftest_Furosemide(data_df):
    #"https://pubmed.ncbi.nlm.nih.gov/, https://www.heart.org/"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Furosemide treatment comparison function. Theoretical value is expected to be between 80.0 and 90.0.'
    try:
        codes = ['OMOP402924', 'OMOP402916', 'OMOP402669', 'OMOP402939']
        data_per = 100 * data_df[data_df['formulary_drug_cd'].astype(str).isin(codes)]['subject_id'].nunique() / data_df['subject_id'].nunique()
        res = (80.0 <= data_per <= 90.0)
        output_vals = {'data_per': data_per, 'range_low': 80.0, 'range_high': 90.0}
        if res == False:
            fail_exp = 'Furosemide evaluation in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Furosemide.explanation = str(output_vals)
        return res

def dftest_Spironolactone(data_df):
    #"https://pubmed.ncbi.nlm.nih.gov/31951680/"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Spironolactone treatment comparison function. Theoretical value is expected to be between 30.0 and 35.0.'
    try:
        codes = ['OMOP2306915', 'OMOP2431903', 'OMOP2306917', 'OMOP310885']
        data_per = 100 * data_df[data_df['formulary_drug_cd'].astype(str).isin(codes)]['subject_id'].nunique() / data_df['subject_id'].nunique()
        res = (30.0 <= data_per <= 35.0)
        output_vals = {'data_per': data_per, 'range_low': 30.0, 'range_high': 35.0}
        if res == False:
            fail_exp = 'Spironolactone evaluation in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Spironolactone.explanation = str(output_vals)
        return res

def dftest_Digoxin(data_df):
    #"https://www.jacc.org, https://pmc.ncbi.nlm.nih.gov/articles/PMC9716..."
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Digoxin treatment comparison function. Theoretical value is expected to be between 1.0 and 2.0.'
    try:
        codes = ['OMOP4810774', 'OMOP4808566', 'OMOP4797715', 'OMOP426290']
        data_per = 100 * data_df[data_df['formulary_drug_cd'].astype(str).isin(codes)]['subject_id'].nunique() / data_df['subject_id'].nunique()
        res = (1.0 <= data_per <= 2.0)
        output_vals = {'data_per': data_per, 'range_low': 1.0, 'range_high': 2.0}
        if res == False:
            fail_exp = 'Digoxin evaluation in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Digoxin.explanation = str(output_vals)
        return res

def dftest_Valsartan(data_df):
    #"https://jamanetwork.com/journals/jama/article-abstract/2767933"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Valsartan treatment comparison function. Theoretical value is expected to be between 5.0 and 10.0.'
    try:
        codes = ['OMOP4660125', 'OMOP4660077', 'OMOP4660015', 'OMOP4660016']
        data_per = 100 * data_df[data_df['formulary_drug_cd'].astype(str).isin(codes)]['subject_id'].nunique() / data_df['subject_id'].nunique()
        res = (5.0 <= data_per <= 10.0)
        output_vals = {'data_per': data_per, 'range_low': 5.0, 'range_high': 10.0}
        if res == False:
            fail_exp = 'Valsartan evaluation in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Valsartan.explanation = str(output_vals)
        return res

def dftest_Sacubitril_Valsartan(data_df):
    #"American Heart Association (https://www.ahajournals.org/doi/10.1161/CIRCH.2021), CDC (https://www.cdc.gov/heartfailure/facts.htm)"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Sacubitril_Valsartan treatment comparison function. Theoretical value is expected to be between 13.0 and 15.0.'
    try:
        codes = ['OMOP514883', 'OMOP514772', 'OMOP514742', 'OMOP344647']
        data_per = 100 * data_df[data_df['formulary_drug_cd'].astype(str).isin(codes)]['subject_id'].nunique() / data_df['subject_id'].nunique()
        res = (13.0 <= data_per <= 15.0)
        output_vals = {'data_per': data_per, 'range_low': 13.0, 'range_high': 15.0}
        if res == False:
            fail_exp = 'Sacubitril_Valsartan evaluation in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Sacubitril_Valsartan.explanation = str(output_vals)
        return res

def dftest_Bisoprolol(data_df):
    #("American Heart Association (AHA)", "PubMed articles on Bisoprolol prescription prevalence in CHF patients globally")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Bisoprolol treatment comparison function. Theoretical value is expected to be between 20.0 and 25.0.'
    try:
        codes = ['OMOP677039', 'OMOP677156', 'OMOP1114451', 'OMOP482159']
        data_per = 100 * data_df[data_df['formulary_drug_cd'].astype(str).isin(codes)]['subject_id'].nunique() / data_df['subject_id'].nunique()
        res = (20.0 <= data_per <= 25.0)
        output_vals = {'data_per': data_per, 'range_low': 20.0, 'range_high': 25.0}
        if res == False:
            fail_exp = 'Bisoprolol evaluation in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Bisoprolol.explanation = str(output_vals)
        return res

def dftest_Ivabradine(data_df):
    #("JACC: https://www.jacc.org/doi/full/10.1016/j.jacc.2020.01.045", "PubMed: https://pubmed.ncbi.nlm.nih.gov/")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Ivabradine treatment comparison function. Theoretical value is expected to be between 1.0 and 2.0.'
    try:
        codes = ['OMOP4782017', 'OMOP4711986', 'OMOP4782005', 'OMOP4782006']
        data_per = 100 * data_df[data_df['formulary_drug_cd'].astype(str).isin(codes)]['subject_id'].nunique() / data_df['subject_id'].nunique()
        res = (1.0 <= data_per <= 2.0)
        output_vals = {'data_per': data_per, 'range_low': 1.0, 'range_high': 2.0}
        if res == False:
            fail_exp = 'Ivabradine evaluation in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Ivabradine.explanation = str(output_vals)
        return res

def dftest_Eplerenone(data_df):
    #"https://www.jacc.org/doi/full/10.1016/j.jacc.2020.03.012"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Eplerenone treatment comparison function. Theoretical value is expected to be between 10.0 and 15.0.'
    try:
        codes = ['OMOP702692', 'OMOP702693', 'OMOP702657', 'OMOP702656']
        data_per = 100 * data_df[data_df['formulary_drug_cd'].astype(str).isin(codes)]['subject_id'].nunique() / data_df['subject_id'].nunique()
        res = (10.0 <= data_per <= 15.0)
        output_vals = {'data_per': data_per, 'range_low': 10.0, 'range_high': 15.0}
        if res == False:
            fail_exp = 'Eplerenone evaluation in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Eplerenone.explanation = str(output_vals)
        return res

def dftest_Torsemide(data_df):
    #("National Center for Biotechnology Information, NCBI - https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8887...")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Torsemide treatment comparison function. Theoretical value is expected to be between 1.0 and 2.0.'
    try:
        codes = ['OMOP2119248', 'OMOP2056968', 'OMOP4685321', 'OMOP2338862']
        data_per = 100 * data_df[data_df['formulary_drug_cd'].astype(str).isin(codes)]['subject_id'].nunique() / data_df['subject_id'].nunique()
        res = (1.0 <= data_per <= 2.0)
        output_vals = {'data_per': data_per, 'range_low': 1.0, 'range_high': 2.0}
        if res == False:
            fail_exp = 'Torsemide evaluation in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Torsemide.explanation = str(output_vals)
        return res



# Filename: unit_test4.py

def dftest_Gender_of_the_patient_Male__diagnosed(data_df):
    #"American Heart Association, 2023 Heart Disease and Stroke Statistics Update (https://www.heart.org/en/news/2023)"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Gender_of_the_patient__Male_ evaluation function. Result is expected to be 56%.'
    try:
        diagnosed_ids = data_df[data_df['icd9_code'].astype(str).isin(['428.0', '428.2', '428.9', '398.91', '428.2', '428.0'])]['subject_id'].unique()
        diagnosed = data_df[data_df['subject_id'].isin(diagnosed_ids)]
        codes = ['M']
        ref_for_percentage = data_df[data_df['gender'].astype(str).isin(codes)]
        
        data_per = 100 * diagnosed[diagnosed['gender'].astype(str).isin(codes)]['subject_id'].nunique() / ref_for_percentage['subject_id'].nunique()
        val = (data_per - 56) / np.sqrt((data_per * (100 - data_per) + 56 * (100 - 56)) / 2)
        ratio = data_per / 56
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 56, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: Gender_of_the_patient__Male_ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
            
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
        
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Gender_of_the_patient_Male__diagnosed.explanation = str(output_vals)
        return res

def dftest_Ethnicity_of_the_patient_Black_African_American__diagnosed(data_df):
    #"https://pubmed.ncbi.nlm.nih.gov/33741769/"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Ethnicity_of_the_patient__Black_African_American_ evaluation function. Result is expected to be 25%.'
    try:
        diagnosed_ids = data_df[data_df['icd9_code'].astype(str).isin(['428.0', '428.2', '428.9', '398.91', '428.2', '428.0'])]['subject_id'].unique()
        diagnosed = data_df[data_df['subject_id'].isin(diagnosed_ids)]
        codes = ['BLACK/AFRICAN AMERICAN']
        ref_for_percentage = data_df[data_df['ethnicity'].astype(str).isin(codes)]
        
        data_per = 100 * diagnosed[diagnosed['ethnicity'].astype(str).isin(codes)]['subject_id'].nunique() / ref_for_percentage['subject_id'].nunique()
        val = (data_per - 25) / np.sqrt((data_per * (100 - data_per) + 25 * (100 - 25)) / 2)
        ratio = data_per / 25
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 25, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: Ethnicity_of_the_patient__Black_African_American_ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
            
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
        
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Ethnicity_of_the_patient_Black_African_American__diagnosed.explanation = str(output_vals)
        return res

def dftest_Ethnicity_of_the_patient_Asian__diagnosed(data_df):
    #("https://jamanetwork.com/journals/jamanetworkopen/fullarticle/2770645")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Ethnicity_of_the_patient__Asian_ evaluation function. Result is expected to be 2.9%.'
    try:
        diagnosed_ids = data_df[data_df['icd9_code'].astype(str).isin(['428.0', '428.2', '428.9', '398.91', '428.2', '428.0'])]['subject_id'].unique()
        diagnosed = data_df[data_df['subject_id'].isin(diagnosed_ids)]
        codes = ['ASIAN']
        ref_for_percentage = data_df[data_df['ethnicity'].astype(str).isin(codes)]
        
        data_per = 100 * diagnosed[diagnosed['ethnicity'].astype(str).isin(codes)]['subject_id'].nunique() / ref_for_percentage['subject_id'].nunique()
        val = (data_per - 2.9) / np.sqrt((data_per * (100 - data_per) + 2.9 * (100 - 2.9)) / 2)
        ratio = data_per / 2.9
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 2.9, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: Ethnicity_of_the_patient__Asian_ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
            
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
        
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Ethnicity_of_the_patient_Asian__diagnosed.explanation = str(output_vals)
        return res

def dftest_Ethnicity_of_the_patient_Hispanic_Latino__diagnosed(data_df):
    #("American Heart Association, 2021", "https://resources.healthgrades.com/right-care")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Ethnicity_of_the_patient__Hispanic_Latino_ evaluation function. Result is expected to be 7.5%.'
    try:
        diagnosed_ids = data_df[data_df['icd9_code'].astype(str).isin(['428.0', '428.2', '428.9', '398.91', '428.2', '428.0'])]['subject_id'].unique()
        diagnosed = data_df[data_df['subject_id'].isin(diagnosed_ids)]
        codes = ['HISPANIC/LATINO']
        ref_for_percentage = data_df[data_df['ethnicity'].astype(str).isin(codes)]
        
        data_per = 100 * diagnosed[diagnosed['ethnicity'].astype(str).isin(codes)]['subject_id'].nunique() / ref_for_percentage['subject_id'].nunique()
        val = (data_per - 7.5) / np.sqrt((data_per * (100 - data_per) + 7.5 * (100 - 7.5)) / 2)
        ratio = data_per / 7.5
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 7.5, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: Ethnicity_of_the_patient__Hispanic_Latino_ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
            
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
        
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Ethnicity_of_the_patient_Hispanic_Latino__diagnosed.explanation = str(output_vals)
        return res

def dftest_Ethnicity_of_the_patient_Other__diagnosed(data_df):
    #("American Heart Association, 2023")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Ethnicity_of_the_patient__Other_ evaluation function. Result is expected to be 6.5%.'
    try:
        diagnosed_ids = data_df[data_df['icd9_code'].astype(str).isin(['428.0', '428.2', '428.9', '398.91', '428.2', '428.0'])]['subject_id'].unique()
        diagnosed = data_df[data_df['subject_id'].isin(diagnosed_ids)]
        codes = ['OTHER']
        ref_for_percentage = data_df[data_df['ethnicity'].astype(str).isin(codes)]
        
        data_per = 100 * diagnosed[diagnosed['ethnicity'].astype(str).isin(codes)]['subject_id'].nunique() / ref_for_percentage['subject_id'].nunique()
        val = (data_per - 6.5) / np.sqrt((data_per * (100 - data_per) + 6.5 * (100 - 6.5)) / 2)
        ratio = data_per / 6.5
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 6.5, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: Ethnicity_of_the_patient__Other_ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
            
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
        
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Ethnicity_of_the_patient_Other__diagnosed.explanation = str(output_vals)
        return res



# Filename: unit_test5.py

def dftest_Radiologic_examination_chest_single_view(data_df):
    #"https://www.radiologyinfo.org"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Radiologic_examination__chest__single_view evaluation function. 95% of the population is expected to be between 40.0 and 50.0.'
    try:
        codes = ['71045', '71046', '71047', '71030', '71020', '71023', '71022', '71021']
        if data_df[data_df['icd9_code'].astype(str).isin(codes)]['subject_id'].nunique() > 0:
            data_in_range = data_df[(data_df['icd9_code'].astype(str).isin(codes)) & (data_df['valuenum'] >= 40.0) & (data_df['valuenum'] <= 50.0)]['subject_id'].nunique() / data_df[data_df['icd9_code'].astype(str).isin(codes)]['subject_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 40.0, 'range_high': 50.0}
        if res == False:
            fail_exp = 'Radiologic_examination__chest__single_view evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Radiologic_examination_chest_single_view.explanation = str(output_vals)
        return res

def dftest_Transferase_aspartate_amino_AST_SGOT_(data_df):
    #("https://www.verywellhealth.com/ast-sgot-8411027", "https://www.mayoclinic.org/tests-procedures/liver-function-tests/about/pac-20385003", "https://labtestsonline.org/tests/aspartate-aminotransferase-ast")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Transferase__aspartate_amino__AST___SGOT_ evaluation function. 95% of the population is expected to be between 8.0 and 33.0.'
    try:
        codes = ['84450']
        if data_df[data_df['icd9_code'].astype(str).isin(codes)]['subject_id'].nunique() > 0:
            data_in_range = data_df[(data_df['icd9_code'].astype(str).isin(codes)) & (data_df['valuenum'] >= 8.0) & (data_df['valuenum'] <= 33.0)]['subject_id'].nunique() / data_df[data_df['icd9_code'].astype(str).isin(codes)]['subject_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 8.0, 'range_high': 33.0}
        if res == False:
            fail_exp = 'Transferase__aspartate_amino__AST___SGOT_ evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Transferase_aspartate_amino_AST_SGOT_.explanation = str(output_vals)
        return res

def dftest_Alanine_aminotransferase_ALT_measurement(data_df):
    #"https://www.webmd.com/fatty-liver-disease/alanine-aminotransferase-alt, https://www.mayoclinic.org/tests-procedures/liver-function-tests/about/pac-20394595"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Alanine_aminotransferase__ALT__measurement evaluation function. 95% of the population is expected to be between 7.0 and 56.0.'
    try:
        codes = ['84460']
        if data_df[data_df['icd9_code'].astype(str).isin(codes)]['subject_id'].nunique() > 0:
            data_in_range = data_df[(data_df['icd9_code'].astype(str).isin(codes)) & (data_df['valuenum'] >= 7.0) & (data_df['valuenum'] <= 56.0)]['subject_id'].nunique() / data_df[data_df['icd9_code'].astype(str).isin(codes)]['subject_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 7.0, 'range_high': 56.0}
        if res == False:
            fail_exp = 'Alanine_aminotransferase__ALT__measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Alanine_aminotransferase_ALT_measurement.explanation = str(output_vals)
        return res

def dftest_B_type_Natriuretic_Peptide_BNP_measurement(data_df):
    #("https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2828020/", "https://www.heart.org")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'B_type_Natriuretic_Peptide__BNP__measurement evaluation function. 95% of the population is expected to be between 0.0 and 100.0.'
    try:
        codes = ['2339-0', '2345-7', '2340-8']
        if data_df[data_df['itemid'].astype(str).isin(codes)]['subject_id'].nunique() > 0:
            data_in_range = data_df[(data_df['itemid'].astype(str).isin(codes)) & (data_df['valuenum'] >= 0.0) & (data_df['valuenum'] <= 100.0)]['subject_id'].nunique() / data_df[data_df['itemid'].astype(str).isin(codes)]['subject_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 0.0, 'range_high': 100.0}
        if res == False:
            fail_exp = 'B_type_Natriuretic_Peptide__BNP__measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_B_type_Natriuretic_Peptide_BNP_measurement.explanation = str(output_vals)
        return res

def dftest_Troponin_I_measurement(data_df):
    #"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2828020/, https://www.heart.org"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Troponin_I_measurement evaluation function. The value is expected to be less than 0.04.'
    try:
        codes = ['3094-0', '3097-3']
        if data_df[data_df['itemid'].astype(str).isin(codes)]['subject_id'].nunique() > 0:
            data_in_range = data_df[(data_df['itemid'].astype(str).isin(codes)) & (data_df['valuenum'] < 0.04)]['subject_id'].nunique() / data_df[data_df['itemid'].astype(str).isin(codes)]['subject_id'].nunique()
            res = data_in_range > 0.95
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'expected_value': 0.04}
        if res == False:
            fail_exp = 'Troponin_I_measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Troponin_I_measurement.explanation = str(output_vals)
        return res

def dftest_Troponin_T_measurement(data_df):
    #("https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2828020/", "https://www.heart.org")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Troponin_T_measurement evaluation function. The value is expected to be less than 0.01.'
    try:
        codes = ['10839-9', '10840-7']
        if data_df[data_df['itemid'].astype(str).isin(codes)]['subject_id'].nunique() > 0:
            data_in_range = data_df[(data_df['itemid'].astype(str).isin(codes)) & (data_df['valuenum'] < 0.01)]['subject_id'].nunique() / data_df[data_df['itemid'].astype(str).isin(codes)]['subject_id'].nunique()
            res = data_in_range > 0.95
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'expected_value': 0.01}
        if res == False:
            fail_exp = 'Troponin_T_measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Troponin_T_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_Creatinine_measurement(data_df):
    #"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2828020/"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Creatinine_measurement evaluation function. 95% of the population is expected to be between 0.6 and 1.3.'
    try:
        codes = ['2951-2', '2955-3', '2956-1']
        if data_df[data_df['itemid'].astype(str).isin(codes)]['subject_id'].nunique() > 0:
            data_in_range = data_df[(data_df['itemid'].astype(str).isin(codes)) & (data_df['valuenum'] >= 0.6) & (data_df['valuenum'] <= 1.3)]['subject_id'].nunique() / data_df[data_df['itemid'].astype(str).isin(codes)]['subject_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 0.6, 'range_high': 1.3}
        if res == False:
            fail_exp = 'Serum_Creatinine_measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Creatinine_measurement.explanation = str(output_vals)
        return res

def dftest_Blood_Urea_Nitrogen_BUN_measurement(data_df):
    #"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2828020/, https://www.mayoclinic.org/tests-procedures/blood-tests/about/pac-20384989, https://medlineplus.gov/lab-tests/blood-urea-nitrogen-bun-test/"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Blood_Urea_Nitrogen__BUN__measurement evaluation function. 95% of the population is expected to be between 7.0 and 20.0.'
    try:
        codes = ['3094-0', '3097-3']
        if data_df[data_df['itemid'].astype(str).isin(codes)]['subject_id'].nunique() > 0:
            data_in_range = data_df[(data_df['itemid'].astype(str).isin(codes)) & (data_df['valuenum'] >= 7.0) & (data_df['valuenum'] <= 20.0)]['subject_id'].nunique() / data_df[data_df['itemid'].astype(str).isin(codes)]['subject_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 7.0, 'range_high': 20.0}
        if res == False:
            fail_exp = 'Blood_Urea_Nitrogen__BUN__measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Blood_Urea_Nitrogen_BUN_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_Electrolytes_measurement(data_df):
    #"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2828020/, https://www.mayoclinic.org"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Electrolytes_measurement evaluation function. 95% of the population is expected to be between 135.0 and 145.0.'
    try:
        codes = ['2345-7', '2340-8']
        if data_df[data_df['itemid'].astype(str).isin(codes)]['subject_id'].nunique() > 0:
            data_in_range = data_df[(data_df['itemid'].astype(str).isin(codes)) & (data_df['valuenum'] >= 135.0) & (data_df['valuenum'] <= 145.0)]['subject_id'].nunique() / data_df[data_df['itemid'].astype(str).isin(codes)]['subject_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 135.0, 'range_high': 145.0}
        if res == False:
            fail_exp = 'Serum_Electrolytes_measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Electrolytes_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_Magnesium_measurement(data_df):
    #"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2828020/, https://ods.od.nih.gov/factsheets/Magnesium-HealthProfessional/"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Magnesium_measurement evaluation function. 95% of the population is expected to be between 1.7 and 2.2.'
    try:
        codes = ['1751-7', '1759-0']
        if data_df[data_df['itemid'].astype(str).isin(codes)]['subject_id'].nunique() > 0:
            data_in_range = data_df[(data_df['itemid'].astype(str).isin(codes)) & (data_df['valuenum'] >= 1.7) & (data_df['valuenum'] <= 2.2)]['subject_id'].nunique() / data_df[data_df['itemid'].astype(str).isin(codes)]['subject_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 1.7, 'range_high': 2.2}
        if res == False:
            fail_exp = 'Serum_Magnesium_measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Magnesium_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_Calcium_measurement(data_df):
    #"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2828020/, https://medlineplus.gov/lab-tests/calcium-in-blood/"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Calcium_measurement evaluation function. 95% of the population is expected to be between 8.5 and 10.2.'
    try:
        codes = ['17861-6', '17862-4']
        if data_df[data_df['itemid'].astype(str).isin(codes)]['subject_id'].nunique() > 0:
            data_in_range = data_df[(data_df['itemid'].astype(str).isin(codes)) & (data_df['valuenum'] >= 8.5) & (data_df['valuenum'] <= 10.2)]['subject_id'].nunique() / data_df[data_df['itemid'].astype(str).isin(codes)]['subject_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 8.5, 'range_high': 10.2}
        if res == False:
            fail_exp = 'Serum_Calcium_measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Calcium_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_Phosphate_measurement(data_df):
    #"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2828020/"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Phosphate_measurement evaluation function. 95% of the population is expected to be between 2.5 and 4.5.'
    try:
        codes = ['17861-6', '17862-4']
        if data_df[data_df['itemid'].astype(str).isin(codes)]['subject_id'].nunique() > 0:
            data_in_range = data_df[(data_df['itemid'].astype(str).isin(codes)) & (data_df['valuenum'] >= 2.5) & (data_df['valuenum'] <= 4.5)]['subject_id'].nunique() / data_df[data_df['itemid'].astype(str).isin(codes)]['subject_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 2.5, 'range_high': 4.5}
        if res == False:
            fail_exp = 'Serum_Phosphate_measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Phosphate_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_Glucose_measurement(data_df):
    #("https://diabetes.org/diabetes/a1c/diagnosis", "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2828020/")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Glucose_measurement evaluation function. 95% of the population is expected to be between 70.0 and 99.0.'
    try:
        codes = ['2345-7', '2340-8']
        if data_df[data_df['itemid'].astype(str).isin(codes)]['subject_id'].nunique() > 0:
            data_in_range = data_df[(data_df['itemid'].astype(str).isin(codes)) & (data_df['valuenum'] >= 70.0) & (data_df['valuenum'] <= 99.0)]['subject_id'].nunique() / data_df[data_df['itemid'].astype(str).isin(codes)]['subject_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 70.0, 'range_high': 99.0}
        if res == False:
            fail_exp = 'Serum_Glucose_measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Glucose_measurement.explanation = str(output_vals)
        return res



