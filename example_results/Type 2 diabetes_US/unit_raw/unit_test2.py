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

