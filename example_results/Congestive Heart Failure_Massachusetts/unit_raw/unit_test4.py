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

