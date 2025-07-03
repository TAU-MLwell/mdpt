# Filename: unit_test2.py

def dftest_Male_gender_(data_df):
    #("America's Health Rankings: https://www.americashealthrankings.org/explore/annual/measure/Hypertension/state/MA", "U.S. Census Bureau: https://www.census.gov/quickfacts/fact/table/MA")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Male_gender_ evaluation function. Result is expected to be 48.5%.'
    try:
        codes = ['M']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['Gender'].astype(str).isin(codes)]['Patient'].nunique() / ref_for_percentage['Patient'].nunique()
        val = (data_per - 48.5) / np.sqrt((data_per * (100 - data_per) + 48.5 * (100 - 48.5)) / 2)
        ratio = data_per / 48.5
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 48.5, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Male_gender_ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Male_gender_.explanation = str(output_vals)
        return res

def dftest_Female_gender_(data_df):
    #("U.S. Census Bureau (https://www.census.gov/quickfacts/MA)", "America's Health Rankings (https://www.americashealthrankings.org/explore/annual/measure/Hypertension/state/MA)")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Female_gender_ evaluation function. Result is expected to be 51.5%.'
    try:
        codes = ['F']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['Gender'].astype(str).isin(codes)]['Patient'].nunique() / ref_for_percentage['Patient'].nunique()
        val = (data_per - 51.5) / np.sqrt((data_per * (100 - data_per) + 51.5 * (100 - 51.5)) / 2)
        ratio = data_per / 51.5
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 51.5, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Female_gender_ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Female_gender_.explanation = str(output_vals)
        return res

def dftest_White_race_(data_df):
    #("U.S. Census Bureau QuickFacts: https://www.census.gov/quickfacts/fact/table/MA/PST045224")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'White_race_ evaluation function. Result is expected to be 70.7%.'
    try:
        codes = ['white']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['Race'].astype(str).isin(codes)]['Patient'].nunique() / ref_for_percentage['Patient'].nunique()
        val = (data_per - 70.7) / np.sqrt((data_per * (100 - data_per) + 70.7 * (100 - 70.7)) / 2)
        ratio = data_per / 70.7
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 70.7, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'White_race_ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_White_race_.explanation = str(output_vals)
        return res

def dftest_Black_or_African_American_race_(data_df):
    #("U.S. Census Bureau: https://www.census.gov/quickfacts/fact/table/MA/PST045224")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Black_or_African_American_race_ evaluation function. Result is expected to be 9.0%.'
    try:
        codes = ['black']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['Race'].astype(str).isin(codes)]['Patient'].nunique() / ref_for_percentage['Patient'].nunique()
        val = (data_per - 9.0) / np.sqrt((data_per * (100 - data_per) + 9.0 * (100 - 9.0)) / 2)
        ratio = data_per / 9.0
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 9.0, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Black_or_African_American_race_ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Black_or_African_American_race_.explanation = str(output_vals)
        return res

def dftest_Asian_race_(data_df):
    #("U.S. Census Bureau QuickFacts - Massachusetts (https://www.census.gov/quickfacts/fact/table/MA/PST045224)")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Asian_race_ evaluation function. Result is expected to be 7.2%.'
    try:
        codes = ['asian']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['Race'].astype(str).isin(codes)]['Patient'].nunique() / ref_for_percentage['Patient'].nunique()
        val = (data_per - 7.2) / np.sqrt((data_per * (100 - data_per) + 7.2 * (100 - 7.2)) / 2)
        ratio = data_per / 7.2
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 7.2, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Asian_race_ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Asian_race_.explanation = str(output_vals)
        return res

def dftest_American_Indian_or_Alaska_Native_race_(data_df):
    #("U.S. Census Bureau QuickFacts - Massachusetts: https://www.census.gov/quickfacts/fact/table/MA/PST045224")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'American_Indian_or_Alaska_Native_race_ evaluation function. Result is expected to be 0.2%.'
    try:
        codes = ['native']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['Race'].astype(str).isin(codes)]['Patient'].nunique() / ref_for_percentage['Patient'].nunique()
        val = (data_per - 0.2) / np.sqrt((data_per * (100 - data_per) + 0.2 * (100 - 0.2)) / 2)
        ratio = data_per / 0.2
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 0.2, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'American_Indian_or_Alaska_Native_race_ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_American_Indian_or_Alaska_Native_race_.explanation = str(output_vals)
        return res

def dftest_Native_Hawaiian_or_Other_Pacific_Islander_race_(data_df):
    #("U.S. Census Bureau QuickFacts: https://www.census.gov/quickfacts/fact/table/MA/PST045224")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Native_Hawaiian_or_Other_Pacific_Islander_race_ evaluation function. Result is expected to be 0.1%.'
    try:
        codes = ['hawaiian', 'pacific']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['Race'].astype(str).isin(codes)]['Patient'].nunique() / ref_for_percentage['Patient'].nunique()
        val = (data_per - 0.1) / np.sqrt((data_per * (100 - data_per) + 0.1 * (100 - 0.1)) / 2)
        ratio = data_per / 0.1
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 0.1, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Native_Hawaiian_or_Other_Pacific_Islander_race_ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Native_Hawaiian_or_Other_Pacific_Islander_race_.explanation = str(output_vals)
        return res

def dftest_Other_race_(data_df):
    #("U.S. Census Bureau QuickFacts for Massachusetts: https://www.census.gov/quickfacts/fact/table/MA/PST045224")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Other_race_ evaluation function. Result is expected to be 5.4%.'
    try:
        codes = ['other']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['Race'].astype(str).isin(codes)]['Patient'].nunique() / ref_for_percentage['Patient'].nunique()
        val = (data_per - 5.4) / np.sqrt((data_per * (100 - data_per) + 5.4 * (100 - 5.4)) / 2)
        ratio = data_per / 5.4
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 5.4, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Other_race_ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Other_race_.explanation = str(output_vals)
        return res

def dftest_Hispanic_or_Latino_ethnicity_(data_df):
    #("U.S. Census Bureau QuickFacts - Massachusetts (https://www.census.gov/quickfacts/fact/table/MA/PST045224)")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Hispanic_or_Latino_ethnicity_ evaluation function. Result is expected to be 13.1%.'
    try:
        codes = ['Hispanic or Latino']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['Ethnicity'].astype(str).isin(codes)]['Patient'].nunique() / ref_for_percentage['Patient'].nunique()
        val = (data_per - 13.1) / np.sqrt((data_per * (100 - data_per) + 13.1 * (100 - 13.1)) / 2)
        ratio = data_per / 13.1
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 13.1, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Hispanic_or_Latino_ethnicity_ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Hispanic_or_Latino_ethnicity_.explanation = str(output_vals)
        return res

def dftest_Not_Hispanic_or_Latino_ethnicity_(data_df):
    #("U.S. Census Bureau QuickFacts - Massachusetts (https://www.census.gov/quickfacts/fact/table/MA/PST045224)")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Not_Hispanic_or_Latino_ethnicity_ evaluation function. Result is expected to be 79.3%.'
    try:
        codes = ['Not Hispanic or Latino']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['Ethnicity'].astype(str).isin(codes)]['Patient'].nunique() / ref_for_percentage['Patient'].nunique()
        val = (data_per - 79.3) / np.sqrt((data_per * (100 - data_per) + 79.3 * (100 - 79.3)) / 2)
        ratio = data_per / 79.3
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 79.3, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Not_Hispanic_or_Latino_ethnicity_ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Not_Hispanic_or_Latino_ethnicity_.explanation = str(output_vals)
        return res

