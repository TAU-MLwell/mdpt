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

