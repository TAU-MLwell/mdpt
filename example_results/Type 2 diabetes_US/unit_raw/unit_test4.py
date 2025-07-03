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

