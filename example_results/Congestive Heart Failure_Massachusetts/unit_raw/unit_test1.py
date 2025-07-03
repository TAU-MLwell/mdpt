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

