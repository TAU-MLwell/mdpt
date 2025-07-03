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
    # ref: ['("CDC National Diabetes Statistics Report 2022: https://www.cdc.gov/diabetes/data/statistics-report/index.html", "American Diabetes Association: https://diabetes.org", "Worldometer US Population Data 2023: https://www.worldometers.info/world-population/us-population/")']
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Five year mean incidence comparison function (2016-2021). Theoretical value is expected to be 1.4 million new cases per year.'
    try:
        # Diagnosis codes for Type 2 diabetes
        diagnosis_codes = ['201826', '4099651', '4230254', '45757508', '4193704', '40482801', '4151282', '4200875', '3569411', '443732', '4304377', '40485020', '45757474', '4130162']
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
        expected_incidence = 1.4  # million new cases per year
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
    # ref: ['("CDC National Diabetes Statistics Report 2022: https://www.cdc.gov/diabetes/data/statistics-report/index.html", "American Diabetes Association: https://diabetes.org", "Worldometer US Population Data 2023: https://www.worldometers.info/world-population/us-population/")']
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Prevalence comparison function. Theoretical value is expected to be 11.3%.'
    try:
        # Diagnosis codes for Type 2 diabetes
        diagnosis_codes = ['201826', '4099651', '4230254', '45757508', '4193704', '40482801', '4151282', '4200875', '3569411', '443732', '4304377', '40485020', '45757474', '4130162']
        # Calculate the prevalence of Type 2 diabetes
        prevalence = 100*data_df[data_df['condition_concept_id'].astype(str).isin(diagnosis_codes)]['person_id'].nunique() / data_df['person_id'].nunique()
        expected_prevalence = 11.3  # percentage
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
    # ref: ['"CDC (https://www.cdc.gov/diabetes/data/statistics-report/index.html), PubMed']
    '''Calculates and compares age distribution of Type 2 diabetes patients'''
    limit = 0.05
    #calculate age distribution of patients
    try:
        
        data_df = data_df[data_df['condition_concept_id'].astype(str).isin(['201826', '4099651', '4230254', '45757508', '4193704', '40482801', '4151282', '4200875', '3569411', '443732', '4304377', '40485020', '45757474', '4130162'])]
        data_df['condition_start_datetime'] = pd.to_datetime(data_df['condition_start_datetime'])
        data_df['birth_datetime'] = pd.to_datetime(data_df['birth_datetime'])
        data_df['diagnosis_age'] = data_df['condition_start_datetime'].dt.year - data_df['birth_datetime'].dt.year
        data_df = data_df.sort_values(by=['person_id','condition_start_datetime'], ascending=True)
        unique_patients = data_df.dropna(subset=['condition_start_datetime'], axis=0).drop_duplicates(subset=['person_id'], keep='first')
        data_dist = unique_patients['diagnosis_age'].value_counts()
        data_stats = unique_patients['diagnosis_age'].describe()
        var_data = data_stats['std'].item()**2
        var_th = 100
        df = ((var_data/data_stats['count'].item()) + (var_th/(33000000)))**2/(var_data**2/((data_stats['count'].item()**2) * (data_stats['count'].item() -1)) + var_th**2/(1089000000000000 * (33000000 - 1)))
        Sx_data = data_stats['std'].item()/math.sqrt(data_stats['count'].item())
        Sx_th = 10/math.sqrt(33000000)
        tt = (data_stats['mean'].item() - 54)/math.sqrt(Sx_data+Sx_th)
        pval = 2*stdtr(df, -np.abs(tt))
        res = pval
        
        if pval > limit:
            binary = "Pass"
            explanation = 'Age distribution matches the theoretical distribution - 54 +- 10'
        else:
            binary = "Fail"
            explanation = 'Age distribution is expected to be ' + str(54) + ' +- ' + str(10) + '; in the data it is ' + str(data_stats['mean'].item()) + ' +- ' + str(data_stats['std'].item())
    
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

def dftest_Hypertension_diagnosis_diagnosed(data_df):
    #"https://diabetesjournals.org/care/article/46/Supplement_1/S1/148923/Standards-of-Medical-Care-in-Diabetes-2023"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Hypertension_diagnosis rate comparison function. Theoretical value is expected to be 70.0.'
    try:
        diagnosed_ids = data_df[data_df['condition_concept_id'].astype(str).isin(['201826', '4099651', '4230254', '45757508', '4193704', '40482801', '4151282', '4200875', '3569411', '443732', '4304377', '40485020', '45757474', '4130162'])]['person_id'].unique()
        diagnosed = data_df[data_df['person_id'].isin(diagnosed_ids)]
        codes = ['316866', '40398391', '40345175', '40323436', '4039839']
        data_per = 100 * diagnosed[diagnosed['condition_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / diagnosed['person_id'].nunique()
        val = (data_per - 70.0) / np.sqrt((data_per * (100 - data_per) + 70.0 * (100 - 70.0)) / 2)
        ratio = data_per / 70.0
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 70.0, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: Hypertension_diagnosis percentage in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Hypertension_diagnosis_diagnosed.explanation = str(output_vals)
        return res

def dftest_Hyperlipidemia_diagnosis_diagnosed(data_df):
    #"https://diabetesjournals.org/care/article/46/Supplement_1/S1/148923/Standards-of-Medical-Care-in-Diabetes-2023"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Hyperlipidemia_diagnosis rate comparison function. Theoretical value is expected to be 70.0.'
    try:
        diagnosed_ids = data_df[data_df['condition_concept_id'].astype(str).isin(['201826', '4099651', '4230254', '45757508', '4193704', '40482801', '4151282', '4200875', '3569411', '443732', '4304377', '40485020', '45757474', '4130162'])]['person_id'].unique()
        diagnosed = data_df[data_df['person_id'].isin(diagnosed_ids)]
        codes = ['432867', '438720', '4292079', '4096215', '4030586']
        data_per = 100 * diagnosed[diagnosed['condition_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / diagnosed['person_id'].nunique()
        val = (data_per - 70.0) / np.sqrt((data_per * (100 - data_per) + 70.0 * (100 - 70.0)) / 2)
        ratio = data_per / 70.0
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 70.0, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: Hyperlipidemia_diagnosis percentage in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Hyperlipidemia_diagnosis_diagnosed.explanation = str(output_vals)
        return res

def dftest_Coronary_artery_disease_diagnosis_diagnosed(data_df):
    #"https://diabetesjournals.org/care/article/46/Supplement_1/S1/148923/Standards-of-Medical-Care-in-Diabetes-2023"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Coronary_artery_disease_diagnosis rate comparison function. Theoretical value is expected to be between 2.0 and 4.0.'
    try:
        diagnosed_ids = data_df[data_df['condition_concept_id'].astype(str).isin(['201826', '4099651', '4230254', '45757508', '4193704', '40482801', '4151282', '4200875', '3569411', '443732', '4304377', '40485020', '45757474', '4130162'])]['person_id'].unique()
        diagnosed = data_df[data_df['person_id'].isin(diagnosed_ids)]
        codes = ['40641917', '317576', '40597938', '40323876', '4034511']
        data_per = 100 * diagnosed[diagnosed['condition_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / diagnosed['person_id'].nunique()
        res = (2.0 <= data_per <= 4.0)
        output_vals = {'data_per': data_per, 'range_low': 2.0, 'range_high': 4.0}
        if res == False:
            fail_exp = 'Among diagnosed: Coronary_artery_disease_diagnosis evaluation in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Coronary_artery_disease_diagnosis_diagnosed.explanation = str(output_vals)
        return res

def dftest_Chronic_kidney_disease_diagnosis_diagnosed(data_df):
    #"https://diabetesjournals.org/care/article/46/Supplement_1/S1/148923/Standards-of-Medical-Care-in-Diabetes-2023"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Chronic_kidney_disease_diagnosis rate comparison function. Theoretical value is expected to be between 30.0 and 40.0.'
    try:
        diagnosed_ids = data_df[data_df['condition_concept_id'].astype(str).isin(['201826', '4099651', '4230254', '45757508', '4193704', '40482801', '4151282', '4200875', '3569411', '443732', '4304377', '40485020', '45757474', '4130162'])]['person_id'].unique()
        diagnosed = data_df[data_df['person_id'].isin(diagnosed_ids)]
        codes = ['46271022', '45582391', '1571486', '44830172', '1990140']
        data_per = 100 * diagnosed[diagnosed['condition_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / diagnosed['person_id'].nunique()
        res = (30.0 <= data_per <= 40.0)
        output_vals = {'data_per': data_per, 'range_low': 30.0, 'range_high': 40.0}
        if res == False:
            fail_exp = 'Among diagnosed: Chronic_kidney_disease_diagnosis evaluation in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Chronic_kidney_disease_diagnosis_diagnosed.explanation = str(output_vals)
        return res

def dftest_Peripheral_vascular_disease_diagnosis_diagnosed(data_df):
    #"https://diabetesjournals.org/care/article/46/Supplement_1/S1/148923/Standards-of-Medical-Care-in-Diabetes-2023"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Peripheral_vascular_disease_diagnosis rate comparison function. Theoretical value is expected to be between 15.0 and 20.0.'
    try:
        diagnosed_ids = data_df[data_df['condition_concept_id'].astype(str).isin(['201826', '4099651', '4230254', '45757508', '4193704', '40482801', '4151282', '4200875', '3569411', '443732', '4304377', '40485020', '45757474', '4130162'])]['person_id'].unique()
        diagnosed = data_df[data_df['person_id'].isin(diagnosed_ids)]
        codes = ['321052', '40648191', '40315969', '44782775', '313928']
        data_per = 100 * diagnosed[diagnosed['condition_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / diagnosed['person_id'].nunique()
        res = (15.0 <= data_per <= 20.0)
        output_vals = {'data_per': data_per, 'range_low': 15.0, 'range_high': 20.0}
        if res == False:
            fail_exp = 'Among diagnosed: Peripheral_vascular_disease_diagnosis evaluation in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Peripheral_vascular_disease_diagnosis_diagnosed.explanation = str(output_vals)
        return res

def dftest_Retinopathy_diagnosis_diagnosed(data_df):
    #"https://diabetesjournals.org/care/article/46/Supplement_1/S1/148923/Standards-of-Medical-Care-in-Diabetes-2023"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Retinopathy_diagnosis rate comparison function. Theoretical value is expected to be 28.5.'
    try:
        diagnosed_ids = data_df[data_df['condition_concept_id'].astype(str).isin(['201826', '4099651', '4230254', '45757508', '4193704', '40482801', '4151282', '4200875', '3569411', '443732', '4304377', '40485020', '45757474', '4130162'])]['person_id'].unique()
        diagnosed = data_df[data_df['person_id'].isin(diagnosed_ids)]
        codes = ['376103', '4255281', '4174977', '4102647', '37108931']
        data_per = 100 * diagnosed[diagnosed['condition_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / diagnosed['person_id'].nunique()
        val = (data_per - 28.5) / np.sqrt((data_per * (100 - data_per) + 28.5 * (100 - 28.5)) / 2)
        ratio = data_per / 28.5
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 28.5, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: Retinopathy_diagnosis percentage in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Retinopathy_diagnosis_diagnosed.explanation = str(output_vals)
        return res

def dftest_Stroke_diagnosis_diagnosed(data_df):
    #"https://diabetesjournals.org/care/article/46/Supplement_1/S1/148923/Standards-of-Medical-Care-in-Diabetes-2023"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Stroke_diagnosis rate comparison function. Theoretical value is expected to be 20.0.'
    try:
        diagnosed_ids = data_df[data_df['condition_concept_id'].astype(str).isin(['201826', '4099651', '4230254', '45757508', '4193704', '40482801', '4151282', '4200875', '3569411', '443732', '4304377', '40485020', '45757474', '4130162'])]['person_id'].unique()
        diagnosed = data_df[data_df['person_id'].isin(diagnosed_ids)]
        codes = ['4189462', '3541196', '4148904', '3573599', '4310996']
        data_per = 100 * diagnosed[diagnosed['condition_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / diagnosed['person_id'].nunique()
        val = (data_per - 20.0) / np.sqrt((data_per * (100 - data_per) + 20.0 * (100 - 20.0)) / 2)
        ratio = data_per / 20.0
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 20.0, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: Stroke_diagnosis percentage in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Stroke_diagnosis_diagnosed.explanation = str(output_vals)
        return res

def dftest_Depression_diagnosis_diagnosed(data_df):
    #("https://diabetesjournals.org/care/article/46/Supplement_1/S1/148923/Standards-of-Medical-Care-in-Diabetes-2023")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Depression_diagnosis rate comparison function. Theoretical value is expected to be 19.0.'
    try:
        diagnosed_ids = data_df[data_df['condition_concept_id'].astype(str).isin(['201826', '4099651', '4230254', '45757508', '4193704', '40482801', '4151282', '4200875', '3569411', '443732', '4304377', '40485020', '45757474', '4130162'])]['person_id'].unique()
        diagnosed = data_df[data_df['person_id'].isin(diagnosed_ids)]
        codes = ['35489007', '310495003', '370143000', '83458005', '410']
        data_per = 100 * diagnosed[diagnosed['condition_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / diagnosed['person_id'].nunique()
        val = (data_per - 19.0) / np.sqrt((data_per * (100 - data_per) + 19.0 * (100 - 19.0)) / 2)
        ratio = data_per / 19.0
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 19.0, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: Depression_diagnosis percentage in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Depression_diagnosis_diagnosed.explanation = str(output_vals)
        return res

def dftest_Osteoarthritis_diagnosis_diagnosed(data_df):
    #"https://diabetesjournals.org/care/article/46/Supplement_1/S1/148923/Standards-of-Medical-Care-in-Diabetes-2023"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Osteoarthritis_diagnosis rate comparison function. Theoretical value is expected to be 29.5.'
    try:
        diagnosed_ids = data_df[data_df['condition_concept_id'].astype(str).isin(['201826', '4099651', '4230254', '45757508', '4193704', '40482801', '4151282', '4200875', '3569411', '443732', '4304377', '40485020', '45757474', '4130162'])]['person_id'].unique()
        diagnosed = data_df[data_df['person_id'].isin(diagnosed_ids)]
        codes = ['80180', '40352991', '40320318', '40320319', '4110738']
        data_per = 100 * diagnosed[diagnosed['condition_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / diagnosed['person_id'].nunique()
        val = (data_per - 29.5) / np.sqrt((data_per * (100 - data_per) + 29.5 * (100 - 29.5)) / 2)
        ratio = data_per / 29.5
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 29.5, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: Osteoarthritis_diagnosis percentage in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Osteoarthritis_diagnosis_diagnosed.explanation = str(output_vals)
        return res

def dftest_Sleep_apnea_diagnosis_diagnosed(data_df):
    #("https://diabetesjournals.org/care/article/46/Supplement_1/S1/148923/Standards-of-Medical-Care-in-Diabetes-2023")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Sleep_apnea_diagnosis rate comparison function. Theoretical value is expected to be 18.0.'
    try:
        diagnosed_ids = data_df[data_df['condition_concept_id'].astype(str).isin(['201826', '4099651', '4230254', '45757508', '4193704', '40482801', '4151282', '4200875', '3569411', '443732', '4304377', '40485020', '45757474', '4130162'])]['person_id'].unique()
        diagnosed = data_df[data_df['person_id'].isin(diagnosed_ids)]
        codes = ['313459', '442588', '42872389', '439794', '40482247']
        data_per = 100 * diagnosed[diagnosed['condition_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / diagnosed['person_id'].nunique()
        val = (data_per - 18.0) / np.sqrt((data_per * (100 - data_per) + 18.0 * (100 - 18.0)) / 2)
        ratio = data_per / 18.0
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 18.0, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: Sleep_apnea_diagnosis percentage in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Sleep_apnea_diagnosis_diagnosed.explanation = str(output_vals)
        return res

def dftest_Fatty_liver_disease_diagnosis_diagnosed(data_df):
    #"American Diabetes Association (ADA) Standards of Medical Care in Diabetes—2023 (https://diabetesjournals.org/care/article/46/Supplement_1/S1/148923/Standards-of-Medical-Care-in-Diabetes-2023); Younossi et al., 'Epidemiology of NAFLD and NASH: Implications for Liver Transplantation,' Hepatology, 2019 (https://aasldpubs.onlinelibrary.wiley.com/doi/full/10.1002/hep.30257)"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Fatty_liver_disease_diagnosis rate comparison function. Theoretical value is expected to be between 55.0 and 70.0.'
    try:
        diagnosed_ids = data_df[data_df['condition_concept_id'].astype(str).isin(['201826', '4099651', '4230254', '45757508', '4193704', '40482801', '4151282', '4200875', '3569411', '443732', '4304377', '40485020', '45757474', '4130162'])]['person_id'].unique()
        diagnosed = data_df[data_df['person_id'].isin(diagnosed_ids)]
        codes = ['4159872', '40565506', '37164766', '4058680', '193256']
        data_per = 100 * diagnosed[diagnosed['condition_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / diagnosed['person_id'].nunique()
        res = (55.0 <= data_per <= 70.0)
        output_vals = {'data_per': data_per, 'range_low': 55.0, 'range_high': 70.0}
        if res == False:
            fail_exp = 'Among diagnosed: Fatty_liver_disease_diagnosis evaluation in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Fatty_liver_disease_diagnosis_diagnosed.explanation = str(output_vals)
        return res

def dftest_Anemia_diagnosis_diagnosed(data_df):
    #("https://diabetesjournals.org/care/article/46/Supplement_1/S1/148923/Standards-of-Medical-Care-in-Diabetes-2023")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Anemia_diagnosis rate comparison function. Theoretical value is expected to be 17.8.'
    try:
        diagnosed_ids = data_df[data_df['condition_concept_id'].astype(str).isin(['201826', '4099651', '4230254', '45757508', '4193704', '40482801', '4151282', '4200875', '3569411', '443732', '4304377', '40485020', '45757474', '4130162'])]['person_id'].unique()
        diagnosed = data_df[data_df['person_id'].isin(diagnosed_ids)]
        codes = ['40624900', '40321260', '4135931', '4150154', '444238']
        data_per = 100 * diagnosed[diagnosed['condition_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / diagnosed['person_id'].nunique()
        val = (data_per - 17.8) / np.sqrt((data_per * (100 - data_per) + 17.8 * (100 - 17.8)) / 2)
        ratio = data_per / 17.8
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 17.8, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: Anemia_diagnosis percentage in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Anemia_diagnosis_diagnosed.explanation = str(output_vals)
        return res



# Filename: unit_test2.py

def dftest_Female(data_df):
    #("https://www.census.gov/topics/population/gender.html")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Female evaluation function. Result is expected to be 50.8.'
    try:
        codes = ['45878463']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['gender_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 50.8) / np.sqrt((data_per * (100 - data_per) + 50.8 * (100 - 50.8)) / 2)
        ratio = data_per / 50.8
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 50.8, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Female percentage in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Female.explanation = str(output_vals)
        return res

def dftest_Male(data_df):
    #"https://www.census.gov/topics/population/gender.html"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Male evaluation function. Result is expected to be 49.5.'
    try:
        codes = ['45880669']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['gender_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 49.5) / np.sqrt((data_per * (100 - data_per) + 49.5 * (100 - 49.5)) / 2)
        ratio = data_per / 49.5
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 49.5, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Male percentage in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Male.explanation = str(output_vals)
        return res

def dftest_White(data_df):
    #"https://www.census.gov/topics/population/race.html"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'White evaluation function. Result is expected to be 75.8.'
    try:
        codes = ['8527']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['race_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 75.8) / np.sqrt((data_per * (100 - data_per) + 75.8 * (100 - 75.8)) / 2)
        ratio = data_per / 75.8
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 75.8, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'White percentage in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_White.explanation = str(output_vals)
        return res

def dftest_Black_or_African_American(data_df):
    #"https://www.census.gov/topics/population/race.html"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Black_or_African_American evaluation function. Result is expected to be 13.6.'
    try:
        codes = ['8516']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['race_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 13.6) / np.sqrt((data_per * (100 - data_per) + 13.6 * (100 - 13.6)) / 2)
        ratio = data_per / 13.6
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 13.6, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Black_or_African_American percentage in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Black_or_African_American.explanation = str(output_vals)
        return res

def dftest_Asian(data_df):
    #"https://www.census.gov/topics/population/race.html"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Asian evaluation function. Result is expected to be 6.2.'
    try:
        codes = ['8657']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['race_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 6.2) / np.sqrt((data_per * (100 - data_per) + 6.2 * (100 - 6.2)) / 2)
        ratio = data_per / 6.2
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 6.2, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Asian percentage in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Asian.explanation = str(output_vals)
        return res

def dftest_Native_Hawaiian_or_Other_Pacific_Islander(data_df):
    #("https://www.census.gov/topics/population/race.html")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Native_Hawaiian_or_Other_Pacific_Islander evaluation function. Result is expected to be 0.2.'
    try:
        codes = ['44814659']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['race_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 0.2) / np.sqrt((data_per * (100 - data_per) + 0.2 * (100 - 0.2)) / 2)
        ratio = data_per / 0.2
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 0.2, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Native_Hawaiian_or_Other_Pacific_Islander percentage in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Native_Hawaiian_or_Other_Pacific_Islander.explanation = str(output_vals)
        return res

def dftest_American_Indian_or_Alaska_Native(data_df):
    #"https://www.census.gov/topics/population/race.html"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'American_Indian_or_Alaska_Native evaluation function. Result is expected to be 1.1.'
    try:
        codes = ['44814653']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['race_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 1.1) / np.sqrt((data_per * (100 - data_per) + 1.1 * (100 - 1.1)) / 2)
        ratio = data_per / 1.1
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 1.1, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'American_Indian_or_Alaska_Native percentage in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_American_Indian_or_Alaska_Native.explanation = str(output_vals)
        return res

def dftest_Other(data_df):
    #"https://www.census.gov/topics/population/race.html"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Other evaluation function. Result is expected to be 6.2.'
    try:
        codes = ['44814649']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['race_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 6.2) / np.sqrt((data_per * (100 - data_per) + 6.2 * (100 - 6.2)) / 2)
        ratio = data_per / 6.2
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 6.2, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Other percentage in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Other.explanation = str(output_vals)
        return res

def dftest_Not_Hispanic_or_Latino(data_df):
    #"https://www.census.gov/topics/population/ethnicity.html"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Not_Hispanic_or_Latino evaluation function. Result is expected to be 81.3.'
    try:
        codes = ['38003564']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['ethnicity_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 81.3) / np.sqrt((data_per * (100 - data_per) + 81.3 * (100 - 81.3)) / 2)
        ratio = data_per / 81.3
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 81.3, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Not_Hispanic_or_Latino percentage in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Not_Hispanic_or_Latino.explanation = str(output_vals)
        return res

def dftest_Hispanic_or_Latino(data_df):
    #"https://www.census.gov/topics/population/ethnicity.html"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Hispanic_or_Latino evaluation function. Result is expected to be 18.9.'
    try:
        codes = ['38003563']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['ethnicity_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 18.9) / np.sqrt((data_per * (100 - data_per) + 18.9 * (100 - 18.9)) / 2)
        ratio = data_per / 18.9
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 18.9, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Hispanic_or_Latino percentage in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Hispanic_or_Latino.explanation = str(output_vals)
        return res



# Filename: unit_test3.py

def dftest_A_foreign_key_to_a_standard_concept_identifier_for_the_drug_concept_1(data_df):
    #("CDC, National Center for Health Statistics, Prescription Drug Use Data (2019-2020)", "https://www.cdc.gov/nchs/fastats/drug-use.htm")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'A_foreign_key_to_a_standard_concept_identifier_for_the_drug_concept_ treatment comparison function. Theoretical value is expected to be 48.6.'
    try:
        codes = ['372567009', '351440', '1077295', '4958904', '937185', '2061072', '351435', '4958891', '937377', '2279494', '473514', '2401510', '4669741', '2120032', '2213513', '937199', '2342329', '4958905', '1061969', '5159401', '4958902', '2338892', '2029857', '2310714', '351402', '937390', '351021', '937493', '2151178', '4958888', '2463317', '5137843', '2149304', '2033200', '937381', '937503', '538016', '992512', '4669792', '2307558', '2463316', '4669825', '2432506', '2404841', '2185769', '2401504', '2026456', '538120', '351024', '937246', '473511', '1077294', '937257', '4958919', '937180', '937207', '937410', '2244734', '5138014', '2057719', '4681012', '4669791', '538128', '4958895', '4669730', '2088991', '937417', '2120031', '2338891', '2432508']
        
        data_per = 100 * data_df[data_df['drug_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / data_df['person_id'].nunique()
        val = (data_per - 48.6) / np.sqrt((data_per * (100 - data_per) + 48.6 * (100 - 48.6)) / 2)
        ratio = data_per / 48.6
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 48.6, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'A_foreign_key_to_a_standard_concept_identifier_for_the_drug_concept_ percentage in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
            
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
        
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_to_a_standard_concept_identifier_for_the_drug_concept_1.explanation = str(output_vals)
        return res

def dftest_A_foreign_key_to_a_standard_concept_identifier_for_the_drug_concept_2(data_df):
    #"CDC Diabetes Statistics (https://www.cdc.gov/diabetes/data/statistics-report/index.html); American Diabetes Association (https://diabetes.org)"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'A_foreign_key_to_a_standard_concept_identifier_for_the_drug_concept_ treatment comparison function. Theoretical value is expected to be between 3.0 and 5.0.'
    try:
        codes = ['OMOP4816916', 'OMOP4816020', 'OMOP4799699', 'OMOP4798813', 'OMOP4737144', 'OMOP4737145', 'OMOP4813663', 'OMOP4797243', 'OMOP4813717', 'OMOP4812901', 'OMOP4798762', 'OMOP2273865', 'OMOP5197605', 'OMOP5197609', 'OMOP5197606', 'OMOP4737140', 'OMOP5197610', 'OMOP4794795', 'OMOP5197575', 'OMOP5197476', 'OMOP4818682', 'OMOP5019550', 'OMOP5197523', 'OMOP5197576', 'OMOP5034089', 'OMOP5197524', 'OMOP5197607', 'OMOP5197477', 'OMOP448230', 'OMOP5034096', 'OMOP2281773', 'OMOP2437995', 'OMOP4737146', 'OMOP5197592', 'OMOP262366', 'OMOP262398', 'OMOP448229', 'OMOP5197573', 'OMOP5197577', 'OMOP4805512', 'OMOP5034097', 'OMOP5197525', 'OMOP448242', 'OMOP5019549', 'OMOP2150571', 'OMOP5197478', 'OMOP5197611', 'OMOP4737141', 'OMOP4988921', 'OMOP5034088', 'OMOP5197474', 'OMOP4988941', 'OMOP5197521', 'OMOP4988931', 'OMOP4988940', 'OMOP5034095', 'OMOP4988930', 'OMOP262365', 'OMOP4737142', 'OMOP4988920', 'OMOP262388', 'OMOP5197533', 'OMOP262371', 'OMOP5197574', 'OMOP262397', 'OMOP5197585', 'OMOP5197486', 'OMOP262373', 'OMOP5197547', 'OMOP5197475', 'OMOP2312991', 'OMOP4988919', 'OMOP2064342', 'OMOP2185240', 'OMOP5034087', 'OMOP2063300', 'OMOP5197496', 'OMOP5197594', 'OMOP5197597', 'OMOP1030786', 'OMOP4988929', 'OMOP4988939', 'OMOP262372', 'OMOP5197534', 'OMOP5197487', 'OMOP1030785', 'OMOP4988938', 'OMOP4988928', 'OMOP448232', 'OMOP5197522', 'OMOP2162785', 'OMOP1069661', 'OMOP5197548', 'OMOP4770239', 'OMOP988910']
        data_per = 100 * data_df[data_df['drug_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / data_df['person_id'].nunique()
        res = (3.0 <= data_per <= 5.0)
        output_vals = {'data_per': data_per, 'range_low': 3.0, 'range_high': 5.0}
        if res == False:
            fail_exp = 'A_foreign_key_to_a_standard_concept_identifier_for_the_drug_concept_ evaluation in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
            
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
        
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_to_a_standard_concept_identifier_for_the_drug_concept_2.explanation = str(output_vals)
        return res

def dftest_A_foreign_key_to_a_standard_concept_identifier_for_the_drug_concept_3(data_df):
    #"CDC National Center for Health Statistics (NCHS): Prescription Drug Use (https://www.cdc.gov/nchs/fastats/drug-use-therapeutic.htm)"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'A_foreign_key_to_a_standard_concept_identifier_for_the_drug_concept_ treatment comparison function. Theoretical value is expected to be less than nan.'
    try:
        codes = ['41015022', '41013449', '40902685', '41209149', '40479734', '37204645', '40482823', '37204646', '42539424', '21600786', '2036050', '21164301', '40749314', '2036051', '36682850', '35625834', '35745885', '43158075', '21105328', '35849793', '21174081', '41302043', '40479756', '43212818', '40834305', '40990121', '41121372', '40996389', '21144561', '21066043', '40933872', '40871653', '21085706', '43158073', '1588688', '43158074', '21105327', '41021095', '35753965', '21115147', '36680081', '41226695', '41038882', '21154487', '21134672', '40749313', '21066044', '40851956', '43168956', '40933873', '43212819', '40479733', '40865407', '41021096', '21105325', '35742520', '21105326', '43168955', '44170664', '41038881', '21164302', '40965071', '40883230', '35758094', '40883228', '41210094', '43135949', '42482588', '35754276', '40491983', '40491982', '40491949', '21130192', '44109980', '40251676', '1243715', '42482589', '41164309', '21159926', '21100924', '37205011', '41203539', '1243768', '37205012', '1242241', '21085707', '41241078', '1243767', '40491948', '21100923', '21075986', '36264758', '35759225', '21169720', '41015546', '44092977', '43272772', '21140127', '43272770', '36259600', '43272771', '43267272', '41271886', '1243766', '36891677', '41271885', '36886571', '35750879', '44163148', '37205009', '21140126', '21120433', '41022059', '3654289', '1245397', '40843546', '1245396', '43267270', '37205010', '43146866', '40835234', '43294440', '2926939', '3654290', '40883229', '43146865', '40749312', '35775102', '40874760', '35763002', '36789352', '36260222', '36789355', '40874761', '21110742', '43146477', '40936968', '36272986', '2057410', '37312784']
        
        data_per = 100 * data_df[data_df['drug_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / data_df['person_id'].nunique()
        res = data_per <= 48.6
        output_vals = {'data_per': data_per, 'expected_value': 48.6}
        if res == False:
            fail_exp = 'A_foreign_key_to_a_standard_concept_identifier_for_the_drug_concept_ evaluation in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
            
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
        
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_to_a_standard_concept_identifier_for_the_drug_concept_3.explanation = str(output_vals)
        return res



# Filename: unit_test4.py

def dftest_Male_diagnosed(data_df):
    #"https://www.cdc.gov/diabetes/data/statistics-report/index.html"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Male evaluation function. Result is expected to be 51.0.'
    try:
        diagnosed_ids = data_df[data_df['condition_concept_id'].astype(str).isin(['201826', '4099651', '4230254', '45757508', '4193704', '40482801', '4151282', '4200875', '3569411', '443732', '4304377', '40485020', '45757474', '4130162'])]['person_id'].unique()
        diagnosed = data_df[data_df['person_id'].isin(diagnosed_ids)]
        codes = ['45880669']
        ref_for_percentage = data_df[data_df['gender_concept_id'].astype(str).isin(codes)]
        
        data_per = 100 * diagnosed[diagnosed['gender_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 51.0) / np.sqrt((data_per * (100 - data_per) + 51.0 * (100 - 51.0)) / 2)
        ratio = data_per / 51.0
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 51.0, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: Male percentage in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Male_diagnosed.explanation = str(output_vals)
        return res

def dftest_White_diagnosed(data_df):
    #"https://www.cdc.gov/diabetes/data/statistics-report/index.html"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: White evaluation function. Result is expected to be 58.0.'
    try:
        diagnosed_ids = data_df[data_df['condition_concept_id'].astype(str).isin(['201826', '4099651', '4230254', '45757508', '4193704', '40482801', '4151282', '4200875', '3569411', '443732', '4304377', '40485020', '45757474', '4130162'])]['person_id'].unique()
        diagnosed = data_df[data_df['person_id'].isin(diagnosed_ids)]
        codes = ['8527']
        ref_for_percentage = data_df[data_df['race_concept_id'].astype(str).isin(codes)]
        
        data_per = 100 * diagnosed[diagnosed['race_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 58.0) / np.sqrt((data_per * (100 - data_per) + 58.0 * (100 - 58.0)) / 2)
        ratio = data_per / 58.0
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 58.0, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: White percentage in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_White_diagnosed.explanation = str(output_vals)
        return res

def dftest_Black_or_African_American_diagnosed(data_df):
    #("https://www.cdc.gov/diabetes/data/statistics-report/index.html", "https://www.cdc.gov/diabetes/php/data-research")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Black_or_African_American evaluation function. Result is expected to be 18.0.'
    try:
        diagnosed_ids = data_df[data_df['condition_concept_id'].astype(str).isin(['201826', '4099651', '4230254', '45757508', '4193704', '40482801', '4151282', '4200875', '3569411', '443732', '4304377', '40485020', '45757474', '4130162'])]['person_id'].unique()
        diagnosed = data_df[data_df['person_id'].isin(diagnosed_ids)]
        codes = ['8516']
        ref_for_percentage = data_df[data_df['race_concept_id'].astype(str).isin(codes)]
        
        data_per = 100 * diagnosed[diagnosed['race_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 18.0) / np.sqrt((data_per * (100 - data_per) + 18.0 * (100 - 18.0)) / 2)
        ratio = data_per / 18.0
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 18.0, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: Black_or_African_American percentage in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Black_or_African_American_diagnosed.explanation = str(output_vals)
        return res

def dftest_Asian_diagnosed(data_df):
    #"https://www.cdc.gov/diabetes/data/statistics-report.html"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Asian evaluation function. Result is expected to be 9.0.'
    try:
        diagnosed_ids = data_df[data_df['condition_concept_id'].astype(str).isin(['201826', '4099651', '4230254', '45757508', '4193704', '40482801', '4151282', '4200875', '3569411', '443732', '4304377', '40485020', '45757474', '4130162'])]['person_id'].unique()
        diagnosed = data_df[data_df['person_id'].isin(diagnosed_ids)]
        codes = ['8657']
        ref_for_percentage = data_df[data_df['race_concept_id'].astype(str).isin(codes)]
        
        data_per = 100 * diagnosed[diagnosed['race_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 9.0) / np.sqrt((data_per * (100 - data_per) + 9.0 * (100 - 9.0)) / 2)
        ratio = data_per / 9.0
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 9.0, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: Asian percentage in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Asian_diagnosed.explanation = str(output_vals)
        return res

def dftest_Native_Hawaiian_or_Other_Pacific_Islander_diagnosed(data_df):
    #("https://www.cdc.gov/diabetes/data/statistics-report/index.html")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Native_Hawaiian_or_Other_Pacific_Islander evaluation function. Result is expected to be 14.5.'
    try:
        diagnosed_ids = data_df[data_df['condition_concept_id'].astype(str).isin(['201826', '4099651', '4230254', '45757508', '4193704', '40482801', '4151282', '4200875', '3569411', '443732', '4304377', '40485020', '45757474', '4130162'])]['person_id'].unique()
        diagnosed = data_df[data_df['person_id'].isin(diagnosed_ids)]
        codes = ['44814659']
        ref_for_percentage = data_df[data_df['race_concept_id'].astype(str).isin(codes)]
        
        data_per = 100 * diagnosed[diagnosed['race_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 14.5) / np.sqrt((data_per * (100 - data_per) + 14.5 * (100 - 14.5)) / 2)
        ratio = data_per / 14.5
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 14.5, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: Native_Hawaiian_or_Other_Pacific_Islander percentage in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Native_Hawaiian_or_Other_Pacific_Islander_diagnosed.explanation = str(output_vals)
        return res

def dftest_Not_Hispanic_or_Latino_diagnosed(data_df):
    #"https://www.cdc.gov/diabetes/library/reports.html"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Not_Hispanic_or_Latino evaluation function. Result is expected to be 66.0.'
    try:
        diagnosed_ids = data_df[data_df['condition_concept_id'].astype(str).isin(['201826', '4099651', '4230254', '45757508', '4193704', '40482801', '4151282', '4200875', '3569411', '443732', '4304377', '40485020', '45757474', '4130162'])]['person_id'].unique()
        diagnosed = data_df[data_df['person_id'].isin(diagnosed_ids)]
        codes = ['38003564']
        ref_for_percentage = data_df[data_df['ethnicity_concept_id'].astype(str).isin(codes)]
        
        data_per = 100 * diagnosed[diagnosed['ethnicity_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 66.0) / np.sqrt((data_per * (100 - data_per) + 66.0 * (100 - 66.0)) / 2)
        ratio = data_per / 66.0
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 66.0, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: Not_Hispanic_or_Latino percentage in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Not_Hispanic_or_Latino_diagnosed.explanation = str(output_vals)
        return res

def dftest_Hispanic_or_Latino_diagnosed(data_df):
    #"https://www.cdc.gov/diabetes/data/statistics-report/index.html"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Hispanic_or_Latino evaluation function. Result is expected to be 17.0.'
    try:
        diagnosed_ids = data_df[data_df['condition_concept_id'].astype(str).isin(['201826', '4099651', '4230254', '45757508', '4193704', '40482801', '4151282', '4200875', '3569411', '443732', '4304377', '40485020', '45757474', '4130162'])]['person_id'].unique()
        diagnosed = data_df[data_df['person_id'].isin(diagnosed_ids)]
        codes = ['38003563']
        ref_for_percentage = data_df[data_df['ethnicity_concept_id'].astype(str).isin(codes)]
        
        data_per = 100 * diagnosed[diagnosed['ethnicity_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 17.0) / np.sqrt((data_per * (100 - data_per) + 17.0 * (100 - 17.0)) / 2)
        ratio = data_per / 17.0
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 17.0, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: Hispanic_or_Latino percentage in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Hispanic_or_Latino_diagnosed.explanation = str(output_vals)
        return res



# Filename: unit_test5.py

def dftest_Hemoglobin_A1c_measurement(data_df):
    #("American Diabetes Association (ADA) guidelines, 2023: https://diabetes.org/diabetes/a1c-test")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Hemoglobin_A1c_measurement evaluation function. 95% of the population is expected to be between 4.0 and 5.6.'
    try:
        codes = ['4184637', '3034639', '40329569', '40307813', '3004410', '3007263', '44793001', '37174831', '4276582', '4152671', '37067387', '36304734']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 4.0) & (data_df['value_as_number'] <= 5.6)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 4.0, 'range_high': 5.6}
        if res == False:
            fail_exp = 'Hemoglobin_A1c_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Hemoglobin_A1c_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_glucose_measurement(data_df):
    #("https://diabetes.org/diabetes/testing-and-diagnosis", "https://www.mayoclinic.org/tests-procedures/blood-sugar-test/about/pac-20384898")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_glucose_measurement evaluation function. 95% of the population is expected to be between 70.0 and 99.0.'
    try:
        codes = ['4331286', '40308384', '37392940', '1002230', '3002666', '3004501', '3032230', '3013826', '3007821', '3032986', '3032779', '3029014', '3026728', '3031928', '3032780', '3050134', '46236948', '3025866', '3010044', '4198878', '42868682', '3013256', '3020058', '3048585', '44816672', '3028944', '3020193', '3030416', '40308385', '3020096', '3053004', '3032719', '3005550', '3012792', '37208638', '3031929', '3026536', '3030583', '40762875', '3012635', '3003435', '3003541', '3052381', '4042759', '3039997', '3036283', '3043536', '3023379', '3040820', '4218282', '3042469', '3045067', '3020317', '40762873', '3050095', '3010030', '3000931', '3019765', '3009006', '3014163', '3048856', '3045700', '3036807', '3049496', '40762876', '3049466', '3004067', '4041723', '3035352', '3013802', '4144235', '4042760', '40308386', '4198732', '4193855', '40308387', '4151548', '4198743', '3018582', '40308392', '4018317', '4195213', '40484576', '3029462', '3048522']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 70.0) & (data_df['value_as_number'] <= 99.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 70.0, 'range_high': 99.0}
        if res == False:
            fail_exp = 'Serum_glucose_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_glucose_measurement.explanation = str(output_vals)
        return res

def dftest_Urine_microalbumin_measurement(data_df):
    #("https://www.kidney.org/atoz/content/albuminuria", "https://www.ohdsi.org/data-standardization/the-common-data-model/")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Urine_microalbumin_measurement evaluation function. The value is expected to be less than 30.0.'
    try:
        codes = ['40310556', '4135536', '4152996', '40340434', '37392915', '4065521', '4021120', '4020542', '37398007', '4150342', '40310557', '3000034', '4065543', '40310558', '40310511', '40310014', '3039436', '40339924', '3039775', '1176069', '3005031', '40340390', '3040290', '40760483', '2212189', '3046828', '37392374', '4164903', '1175782', '4107077', '46236963', '2212188', '4154347', '37171232', '3571868', '37398777', '40761549', '3552318', '1761744', '3018104', '3022826', '40656532', '4017498', '40310510', '40656529', '40759673', '3005577', '3001802', '4263307', '37393926', '3025987', '40340388', '40766204', '3043179', '3043771', '40656531', '36660607', '3049506', '40559459', '4354260', '4193419', '3048516', '46235434', '40762252', '1175719', '3012516', '40761532', '40564399', '3002827', '40656530', '313502007', '57378007', '144680007', '167455002', '1021401000000107', '34535-5', '144809008']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] < 30.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = data_in_range > 0.95
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'expected_value': 30.0}
        if res == False:
            fail_exp = 'Urine_microalbumin_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Urine_microalbumin_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_creatinine_measurement(data_df):
    #"https://medlineplus.gov/lab-tests/creatinine-test/, https://www.mayoclinic.org/tests-procedures/creatinine-test/about/pac-20384646"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_creatinine_measurement evaluation function. 95% of the population is expected to be between 0.6 and 1.2.'
    try:
        codes = ['40307212', '40328452', '4276437', '37392176', '4013964']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 0.6) & (data_df['value_as_number'] <= 1.2)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 0.6, 'range_high': 1.2}
        if res == False:
            fail_exp = 'Serum_creatinine_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_creatinine_measurement.explanation = str(output_vals)
        return res

def dftest_Lipid_panel(data_df):
    #"https://www.heart.org/en/health-topics/cholesterol/about-cholesterol/what-your-cholesterol-levels-mean, https://www.mayoclinic.org/tests-procedures/cholesterol-test/about/pac-20384601"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Lipid_panel evaluation function. 95% of the population is expected to be between 0.0 and 200.0.'
    try:
        codes = ['4037130', '2212095', '37061711', '3010946', '1761868']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 0.0) & (data_df['value_as_number'] <= 200.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 0.0, 'range_high': 200.0}
        if res == False:
            fail_exp = 'Lipid_panel evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Lipid_panel.explanation = str(output_vals)
        return res

def dftest_Blood_urea_nitrogen_measurement(data_df):
    #"https://www.mayoclinic.org/tests-procedures/blood-tests/about/pac-20384989, https://www.labcorp.com"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Blood_urea_nitrogen_measurement evaluation function. 95% of the population is expected to be between 7.0 and 20.0.'
    try:
        codes = ['3028280', '3004295', '3010335', '3027219', '3050151']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 7.0) & (data_df['value_as_number'] <= 20.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 7.0, 'range_high': 20.0}
        if res == False:
            fail_exp = 'Blood_urea_nitrogen_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Blood_urea_nitrogen_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_potassium_measurement(data_df):
    #"https://www.ohdsi.org/data-standardization/the-common-data-model/, https://www.mayoclinic.org/tests-procedures/potassium-test/about/pac-20384923"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_potassium_measurement evaluation function. 95% of the population is expected to be between 3.5 and 5.5.'
    try:
        codes = ['4154489', '40315397', '37392171', '40328422', '4042571']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 3.5) & (data_df['value_as_number'] <= 5.5)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 3.5, 'range_high': 5.5}
        if res == False:
            fail_exp = 'Serum_potassium_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_potassium_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_sodium_measurement(data_df):
    #"https://www.mayoclinic.org/tests-procedures/sodium-test/about/pac-20384914, https://medlineplus.gov/lab-tests/sodium-blood-test/"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_sodium_measurement evaluation function. 95% of the population is expected to be between 135.0 and 145.0.'
    try:
        codes = ['4021154', '40307198', '40328427', '37392172', '4043089']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 135.0) & (data_df['value_as_number'] <= 145.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 135.0, 'range_high': 145.0}
        if res == False:
            fail_exp = 'Serum_sodium_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_sodium_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_chloride_measurement(data_df):
    #("https://www.mayoclinic.org", "https://www.labcorp.com", "https://www.ohdsi.org/data-standardization/the-common-data-model/")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_chloride_measurement evaluation function. 95% of the population is expected to be between 96.0 and 106.0.'
    try:
        codes = ['4153270', '40307199', '40328430', '37392173', '37175143', '4043091', '37175142', '4042572', '3014576', '46235783', '37208548', '40757500', '4019545', '4018188', '40652796', '37027122', '44810905', '4188066', '40757501', '3018572', '3013194', '4309125', '40559449', '40563951', '37038125', '4150330', '4269043', '40484030', '3035285', '3009024', '4055551', '36303415', '37399315', '1761323', '4275204', '40330229', '40308408', '3573197', '3043156', '4021154', '4033092', '37173053', '4249884', '44806562', '37208547', '40307320', '44789167', '40654549', '46235784', '4267665', '4260765', '3019550', '3039964', '37398321', '40654548', '4197838', '2212263', '3025034', '3005396', '40329047', '3033733', '36305577', '40757625', '1002263', '4260767', '4055552', '3550746', '3002111', '3020748', '37392561', '40311134', '40328418', '40311128', '40328427', '4260822', '4153006', '40354600', '4043264', '4165618', '40307198', '40328927', '40307214', '4154490', '44812081', '4276441', '4307448', '40310008']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 96.0) & (data_df['value_as_number'] <= 106.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 96.0, 'range_high': 106.0}
        if res == False:
            fail_exp = 'Serum_chloride_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_chloride_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_bicarbonate_measurement(data_df):
    #("https://labtestsonline.org/tests/bicarbonate", "https://www.mayoclinic.org/tests-procedures/blood-tests/about/pac-20384989", "https://www.ohdsi.org/data-standardization/the-common-data-model/")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_bicarbonate_measurement evaluation function. 95% of the population is expected to be between 22.0 and 29.0.'
    try:
        codes = ['4150494', '40307200', '40328433', '607489', '607488']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 22.0) & (data_df['value_as_number'] <= 29.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 22.0, 'range_high': 29.0}
        if res == False:
            fail_exp = 'Serum_bicarbonate_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_bicarbonate_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_calcium_measurement(data_df):
    #"https://www.mayoclinic.org, https://www.labcorp.com"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_calcium_measurement evaluation function. 95% of the population is expected to be between 8.5 and 10.2.'
    try:
        codes = ['4154490', '4307178', '37392174', '40328436', '40307201']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 8.5) & (data_df['value_as_number'] <= 10.2)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 8.5, 'range_high': 10.2}
        if res == False:
            fail_exp = 'Serum_calcium_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_calcium_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_magnesium_measurement(data_df):
    #("https://www.mayoclinic.org", "https://www.labcorp.com")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_magnesium_measurement evaluation function. 95% of the population is expected to be between 1.7 and 2.2.'
    try:
        codes = ['40307253', '4135561', '40328972', '4270766', '37392207']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 1.7) & (data_df['value_as_number'] <= 2.2)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 1.7, 'range_high': 2.2}
        if res == False:
            fail_exp = 'Serum_magnesium_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_magnesium_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_albumin_measurement(data_df):
    #"https://www.mayoclinic.org/tests-procedures/albumin-test/about/pac-20384922"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_albumin_measurement evaluation function. 95% of the population is expected to be between 3.5 and 5.0.'
    try:
        codes = ['40307274', '37392183', '4017497', '40328997', '607481']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 3.5) & (data_df['value_as_number'] <= 5.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 3.5, 'range_high': 5.0}
        if res == False:
            fail_exp = 'Serum_albumin_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_albumin_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_bilirubin_measurement(data_df):
    #"https://medlineplus.gov/lab-tests/bilirubin-test/, https://www.mayoclinic.org/tests-procedures/bilirubin-test/about/pac-20384812"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_bilirubin_measurement evaluation function. 95% of the population is expected to be between 0.1 and 1.2.'
    try:
        codes = ['4197972', '4198887', '4041529', '40315326', '40315341']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 0.1) & (data_df['value_as_number'] <= 1.2)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 0.1, 'range_high': 1.2}
        if res == False:
            fail_exp = 'Serum_bilirubin_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_bilirubin_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_alkaline_phosphatase_measurement(data_df):
    #("https://www.mayocliniclabs.com", "https://www.labcorp.com", "https://www.ohdsi.org/data-standardization/the-common-data-model/")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_alkaline_phosphatase_measurement evaluation function. 95% of the population is expected to be between 44.0 and 121.0.'
    try:
        codes = ['4156813', '4210713', '4195340', '4275207', '607482', '40328358', '4197973', '4308514', '4043079', '3002069', '40315343', '37398460', '3028089', '3001467', '4230636', '40563829', '4220699', '3037712', '46235077', '3035995', '4042561', '40315356', '40328370', '40328372', '40315355', '3018910', '40315357', '3028993', '40558868', '40328371', '3007970', '3021434', '3042479', '3026942', '37398241', '3036955', '3042545', '37173318', '3035400', '4154344', '4154639', '3021222', '37392184', '4193687', '3036185', '4190903', '40563830', '4190902', '3035062', '3011887', '42870304', '37392185', '3037908', '1761414', '3003860', '3037466', '3020990', '3034550', '4156812', '37398586', '3045684', '37208510', '3000235', '3047120', '40563437', '44789031', '40558869', '44816887']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 44.0) & (data_df['value_as_number'] <= 121.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 44.0, 'range_high': 121.0}
        if res == False:
            fail_exp = 'Serum_alkaline_phosphatase_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_alkaline_phosphatase_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_aspartate_aminotransferase_measurement(data_df):
    #("https://www.mayoclinic.org/tests-procedures/liver-function-tests/about/pac-20385003", "https://www.labcorp.com/tests/001123/aspartate-aminotransferase-ast")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_aspartate_aminotransferase_measurement evaluation function. 95% of the population is expected to be between 8.0 and 33.0.'
    try:
        codes = ['37392189', '40757631', '3013721', '3010587', '3022893']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 8.0) & (data_df['value_as_number'] <= 33.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 8.0, 'range_high': 33.0}
        if res == False:
            fail_exp = 'Serum_aspartate_aminotransferase_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_aspartate_aminotransferase_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_alanine_aminotransferase_measurement(data_df):
    #"https://www.mayoclinic.org, https://www.labcorp.com"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_alanine_aminotransferase_measurement evaluation function. 95% of the population is expected to be between 7.0 and 56.0.'
    try:
        codes = ['44788835', '4198730', '37393531', '3006923', '46236949']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 7.0) & (data_df['value_as_number'] <= 56.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 7.0, 'range_high': 56.0}
        if res == False:
            fail_exp = 'Serum_alanine_aminotransferase_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_alanine_aminotransferase_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_lactate_dehydrogenase_measurement(data_df):
    #"https://www.mayocliniclabs.com, https://www.labcorp.com"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_lactate_dehydrogenase_measurement evaluation function. 95% of the population is expected to be between 140.0 and 280.0.'
    try:
        codes = ['4210717', '40328413', '40315388', '4158890', '37392192']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 140.0) & (data_df['value_as_number'] <= 280.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 140.0, 'range_high': 280.0}
        if res == False:
            fail_exp = 'Serum_lactate_dehydrogenase_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_lactate_dehydrogenase_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_uric_acid_measurement(data_df):
    #"https://www.mayocliniclabs.com/test-info/"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_uric_acid_measurement evaluation function. 95% of the population is expected to be between 2.4 and 7.0.'
    try:
        codes = ['4076924', '4165617', '40307235', '40328946', '37392201']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 2.4) & (data_df['value_as_number'] <= 7.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 2.4, 'range_high': 7.0}
        if res == False:
            fail_exp = 'Serum_uric_acid_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_uric_acid_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_triglycerides_measurement(data_df):
    #"https://www.heart.org/en/health-topics/cholesterol/about-cholesterol/triglycerides, https://www.mayoclinic.org/tests-procedures/cholesterol-test/about/pac-20384601"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_triglycerides_measurement evaluation function. 95% of the population is expected to be between 0.0 and 150.0.'
    try:
        codes = ['4156816', '40329067', '40307753', '4055666', '4276570']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 0.0) & (data_df['value_as_number'] <= 150.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 0.0, 'range_high': 150.0}
        if res == False:
            fail_exp = 'Serum_triglycerides_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_triglycerides_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_high_density_lipoprotein_measurement(data_df):
    #("https://www.heart.org", "https://www.mayoclinic.org")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_high_density_lipoprotein_measurement evaluation function. 95% of the population is expected to be between 40.0 and 60.0.'
    try:
        codes = ['37392562', '46284089', '37393305', '37393338', '4195497', '4156659', '4076704', '37398699', '4042059', '40307325', '4055665', '40329056', '37394092', '44789188', '40308860', '4041557', '40330710']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 40.0) & (data_df['value_as_number'] <= 60.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 40.0, 'range_high': 60.0}
        if res == False:
            fail_exp = 'Serum_high_density_lipoprotein_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_high_density_lipoprotein_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_low_density_lipoprotein_measurement(data_df):
    #"https://www.heart.org, https://www.nhlbi.nih.gov"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_low_density_lipoprotein_measurement evaluation function. 95% of the population is expected to be between 0.0 and 100.0.'
    try:
        codes = ['37399325', '4331302', '37394094', '4012479', '37208747', '40307326', '4041556', '1247080', '37394113']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 0.0) & (data_df['value_as_number'] <= 100.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 0.0, 'range_high': 100.0}
        if res == False:
            fail_exp = 'Serum_low_density_lipoprotein_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_low_density_lipoprotein_measurement.explanation = str(output_vals)
        return res

def dftest_Urine_microalbumin_measurement_1(data_df):
    #("https://www.kidney.org/atoz/content/albuminuria", "https://www.mayoclinic.org/tests-procedures/microalbumin-test/about/pac-20384904")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Urine_microalbumin_measurement evaluation function. 95% of the population is expected to be between 0.0 and 30.0.'
    try:
        codes = ['40310556', '4135536', '4152996', '40340434', '37392915', '4065521', '4021120', '4020542', '37398007', '4150342', '40310557', '3000034', '4065543', '40310558', '40310511', '40310014', '3039436', '40339924', '3039775', '1176069', '3005031', '40340390', '3040290', '40760483', '2212189', '3046828', '37392374', '4164903', '1175782', '4107077', '46236963', '2212188', '4154347', '37171232', '3571868', '37398777', '40761549', '3552318', '1761744', '3018104', '3022826', '40656532', '4017498', '40310510', '40656529', '40759673', '3005577', '3001802', '4263307', '37393926', '3025987', '40340388', '40766204', '3043179', '3043771', '40656531', '36660607', '3049506', '40559459', '4354260', '4193419', '3048516', '46235434', '40762252', '1175719', '3012516', '40761532', '40564399', '3002827', '40656530', '313502007', '57378007', '144680007', '167455002', '1021401000000107', '34535-5', '144809008']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 0.0) & (data_df['value_as_number'] <= 30.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 0.0, 'range_high': 30.0}
        if res == False:
            fail_exp = 'Urine_microalbumin_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Urine_microalbumin_measurement_1.explanation = str(output_vals)
        return res

def dftest_Serum_creatinine_measurement_1(data_df):
    #"https://www.ohdsi.org/data-standardization/the-common-data-model/, https://www.mayocliniclabs.com/test-catalog/Clinical+and+Interpretive/8368"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_creatinine_measurement evaluation function. 95% of the population is expected to be between 0.7 and 1.3.'
    try:
        codes = ['40307212', '40328452', '4276437', '37392176', '4013964']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 0.7) & (data_df['value_as_number'] <= 1.3)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 0.7, 'range_high': 1.3}
        if res == False:
            fail_exp = 'Serum_creatinine_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_creatinine_measurement_1.explanation = str(output_vals)
        return res

def dftest_Serum_potassium_measurement_1(data_df):
    #("https://www.mayoclinic.org/tests-procedures/potassium-test/about/pac-20384923", "https://labtestsonline.org/tests/potassium")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_potassium_measurement evaluation function. 95% of the population is expected to be between 3.5 and 5.0.'
    try:
        codes = ['4154489', '40315397', '37392171', '40328422', '4042571']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 3.5) & (data_df['value_as_number'] <= 5.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 3.5, 'range_high': 5.0}
        if res == False:
            fail_exp = 'Serum_potassium_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_potassium_measurement_1.explanation = str(output_vals)
        return res

def dftest_Serum_phosphate_measurement(data_df):
    #("https://www.mayoclinic.org", "https://www.labcorp.com", "https://www.ohdsi.org/data-standardization/the-common-data-model/")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_phosphate_measurement evaluation function. 95% of the population is expected to be between 2.5 and 4.5.'
    try:
        codes = ['4153271', '4041899', '40328441', '40307202', '37392175']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 2.5) & (data_df['value_as_number'] <= 4.5)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 2.5, 'range_high': 4.5}
        if res == False:
            fail_exp = 'Serum_phosphate_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_phosphate_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_aspartate_aminotransferase_measurement_1(data_df):
    #"https://www.mayocliniclabs.com/test-catalog/Clinical+and+Interpretive/8368"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_aspartate_aminotransferase_measurement evaluation function. 95% of the population is expected to be between 8.0 and 40.0.'
    try:
        codes = ['37392189', '40757631', '3013721', '3010587', '3022893']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 8.0) & (data_df['value_as_number'] <= 40.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 8.0, 'range_high': 40.0}
        if res == False:
            fail_exp = 'Serum_aspartate_aminotransferase_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_aspartate_aminotransferase_measurement_1.explanation = str(output_vals)
        return res

def dftest_Serum_uric_acid_measurement_1(data_df):
    #"https://www.mayoclinic.org/, https://www.labcorp.com/, https://www.ohdsi.org/data-standardization/the-common-data-model/"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_uric_acid_measurement evaluation function. 95% of the population is expected to be between 2.6 and 7.2.'
    try:
        codes = ['4076924', '4165617', '40307235', '40328946', '37392201']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 2.6) & (data_df['value_as_number'] <= 7.2)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 2.6, 'range_high': 7.2}
        if res == False:
            fail_exp = 'Serum_uric_acid_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_uric_acid_measurement_1.explanation = str(output_vals)
        return res

def dftest_Serum_cholesterol_measurement(data_df):
    #("https://www.cdc.gov/cholesterol/index.htm", "https://www.heart.org/en/health-topics/cholesterol/about-cholesterol")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_cholesterol_measurement evaluation function. 95% of the population is expected to be between 200.0 and 200.0.'
    try:
        codes = ['4150330', '40307320', '40329047', '4269849', '37392561', '4195491', '4198117', '40307321', '4042057', '4260765', '4195490', '40307323', '40308864', '4055664', '3027114', '40330714', '4041554', '3019900', '37208551', '40307330', '40308862', '37394091', '3557282', '45763616', '40330712', '4042060', '3049873', '40307751', '3015344', '37397989', '40308860', '3028195', '40757504', '40330710', '4041556', '40307324', '44812280', '2212267', '37393333', '37393335', '4156659', '4042059', '4042588', '4055665', '40307327', '4216465', '40482649', '4042586', '40654583', '44787076', '40307326', '3037598', '42868678', '3044491', '42868675', '40759256', '3026453', '3008254', '37027885', '3031776', '40307325', '44787078', '40759255', '37399257', '40483110', '40566162', '40758961', '3028437', '3035899', '40563013', '44791053', '4042062', '4156815', '4042061', '46284971', '40307333', '4299360', '40307335', '4005374', '4195497', '4196842']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 200.0) & (data_df['value_as_number'] <= 200.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 200.0, 'range_high': 200.0}
        if res == False:
            fail_exp = 'Serum_cholesterol_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_cholesterol_measurement.explanation = str(output_vals)
        return res



