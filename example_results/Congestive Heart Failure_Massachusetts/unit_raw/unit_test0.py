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

