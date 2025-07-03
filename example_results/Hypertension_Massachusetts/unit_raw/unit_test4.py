# Filename: unit_test4.py

def dftest_Male_gender_diagnosed_with_hypertension__diagnosed(data_df):
    #("CDC - Hypertension Statistics (https://www.cdc.gov/nchs/fastats/hypertension.htm)")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Male_gender_diagnosed_with_hypertension_ evaluation function. Result is expected to be 33.2%.'
    try:
        diagnosed_ids = data_df[data_df['Code'].astype(str).isin(['38341003', '266287006', '56218007', '194756002', '155295004', '64715009', '827069000', '449759005', '194760004', '429457004', '155297007', '827068008', '194759009', '194794002', '471521000000108', '155302005', '195537001', '473392002', '367390009', '599341000000105', '32966004', '194757006', '702817009', '194769003', '155299005', '46113002', '48146000', '137753003', '194776008', '86234004', '194788005', '194772005', '762463000', '845891000000103', '38481006', '60899001', '194791005', '194782006', '132721000119104', '10725009'])]['Patient'].unique()
        diagnosed = data_df[data_df['Patient'].isin(diagnosed_ids)]
        codes = ['M']
        ref_for_percentage = data_df[data_df['Gender'].astype(str).isin(codes)]
        data_per = 100 * diagnosed[diagnosed['Gender'].astype(str).isin(codes)]['Patient'].nunique() / ref_for_percentage['Patient'].nunique()
        val = (data_per - 33.2) / np.sqrt((data_per * (100 - data_per) + 33.2 * (100 - 33.2)) / 2)
        ratio = data_per / 33.2
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 33.2, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: Male_gender_diagnosed_with_hypertension_ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Male_gender_diagnosed_with_hypertension__diagnosed.explanation = str(output_vals)
        return res

def dftest_Female_gender_diagnosed_with_hypertension__diagnosed(data_df):
    #("America's Health Rankings: https://www.americashealthrankings.org/explore/measures/Hypertension/MA")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Female_gender_diagnosed_with_hypertension_ evaluation function. Result is expected to be 18.0%.'
    try:
        diagnosed_ids = data_df[data_df['Code'].astype(str).isin(['38341003', '266287006', '56218007', '194756002', '155295004', '64715009', '827069000', '449759005', '194760004', '429457004', '155297007', '827068008', '194759009', '194794002', '471521000000108', '155302005', '195537001', '473392002', '367390009', '599341000000105', '32966004', '194757006', '702817009', '194769003', '155299005', '46113002', '48146000', '137753003', '194776008', '86234004', '194788005', '194772005', '762463000', '845891000000103', '38481006', '60899001', '194791005', '194782006', '132721000119104', '10725009'])]['Patient'].unique()
        diagnosed = data_df[data_df['Patient'].isin(diagnosed_ids)]
        codes = ['F']
        ref_for_percentage = data_df[data_df['Gender'].astype(str).isin(codes)]
        data_per = 100 * diagnosed[diagnosed['Gender'].astype(str).isin(codes)]['Patient'].nunique() / ref_for_percentage['Patient'].nunique()
        val = (data_per - 18.0) / np.sqrt((data_per * (100 - data_per) + 18.0 * (100 - 18.0)) / 2)
        ratio = data_per / 18.0
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 18.0, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: Female_gender_diagnosed_with_hypertension_ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Female_gender_diagnosed_with_hypertension__diagnosed.explanation = str(output_vals)
        return res

def dftest_White_race_diagnosed_with_hypertension__diagnosed(data_df):
    #("CDC - High Blood Pressure Statistics: https://www.cdc.gov/high-blood-pressure/data.htm")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: White_race_diagnosed_with_hypertension_ evaluation function. Result is expected to be 45%.'
    try:
        diagnosed_ids = data_df[data_df['Code'].astype(str).isin(['38341003', '266287006', '56218007', '194756002', '155295004', '64715009', '827069000', '449759005', '194760004', '429457004', '155297007', '827068008', '194759009', '194794002', '471521000000108', '155302005', '195537001', '473392002', '367390009', '599341000000105', '32966004', '194757006', '702817009', '194769003', '155299005', '46113002', '48146000', '137753003', '194776008', '86234004', '194788005', '194772005', '762463000', '845891000000103', '38481006', '60899001', '194791005', '194782006', '132721000119104', '10725009'])]['Patient'].unique()
        diagnosed = data_df[data_df['Patient'].isin(diagnosed_ids)]
        codes = ['white']
        ref_for_percentage = data_df[data_df['Race'].astype(str).isin(codes)]
        data_per = 100 * diagnosed[diagnosed['Race'].astype(str).isin(codes)]['Patient'].nunique() / ref_for_percentage['Patient'].nunique()
        val = (data_per - 45) / np.sqrt((data_per * (100 - data_per) + 45 * (100 - 45)) / 2)
        ratio = data_per / 45
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 45, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: White_race_diagnosed_with_hypertension_ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_White_race_diagnosed_with_hypertension__diagnosed.explanation = str(output_vals)
        return res

def dftest_Black_or_African_American_race_diagnosed_with_hypertension__diagnosed(data_df):
    #("https://www.heart.org/en/health-topics/high-blood-pressure/why-high-blood-pressure-is-a-silent-killer")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Black_or_African_American_race_diagnosed_with_hypertension_ evaluation function. Result is expected to be 56%.'
    try:
        diagnosed_ids = data_df[data_df['Code'].astype(str).isin(['38341003', '266287006', '56218007', '194756002', '155295004', '64715009', '827069000', '449759005', '194760004', '429457004', '155297007', '827068008', '194759009', '194794002', '471521000000108', '155302005', '195537001', '473392002', '367390009', '599341000000105', '32966004', '194757006', '702817009', '194769003', '155299005', '46113002', '48146000', '137753003', '194776008', '86234004', '194788005', '194772005', '762463000', '845891000000103', '38481006', '60899001', '194791005', '194782006', '132721000119104', '10725009'])]['Patient'].unique()
        diagnosed = data_df[data_df['Patient'].isin(diagnosed_ids)]
        codes = ['black']
        ref_for_percentage = data_df[data_df['Race'].astype(str).isin(codes)]
        data_per = 100 * diagnosed[diagnosed['Race'].astype(str).isin(codes)]['Patient'].nunique() / ref_for_percentage['Patient'].nunique()
        val = (data_per - 56) / np.sqrt((data_per * (100 - data_per) + 56 * (100 - 56)) / 2)
        ratio = data_per / 56
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 56, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: Black_or_African_American_race_diagnosed_with_hypertension_ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Black_or_African_American_race_diagnosed_with_hypertension__diagnosed.explanation = str(output_vals)
        return res

def dftest_Asian_race_diagnosed_with_hypertension__diagnosed(data_df):
    #("AHA Journals", "https://www.ahajournals.org/doi/10.1161/HYPERTENSIONAHA.122.00001")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Asian_race_diagnosed_with_hypertension_ evaluation function. Result is expected to be 24.9%.'
    try:
        diagnosed_ids = data_df[data_df['Code'].astype(str).isin(['38341003', '266287006', '56218007', '194756002', '155295004', '64715009', '827069000', '449759005', '194760004', '429457004', '155297007', '827068008', '194759009', '194794002', '471521000000108', '155302005', '195537001', '473392002', '367390009', '599341000000105', '32966004', '194757006', '702817009', '194769003', '155299005', '46113002', '48146000', '137753003', '194776008', '86234004', '194788005', '194772005', '762463000', '845891000000103', '38481006', '60899001', '194791005', '194782006', '132721000119104', '10725009'])]['Patient'].unique()
        diagnosed = data_df[data_df['Patient'].isin(diagnosed_ids)]
        codes = ['asian']
        ref_for_percentage = data_df[data_df['Race'].astype(str).isin(codes)]
        data_per = 100 * diagnosed[diagnosed['Race'].astype(str).isin(codes)]['Patient'].nunique() / ref_for_percentage['Patient'].nunique()
        val = (data_per - 24.9) / np.sqrt((data_per * (100 - data_per) + 24.9 * (100 - 24.9)) / 2)
        ratio = data_per / 24.9
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 24.9, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: Asian_race_diagnosed_with_hypertension_ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Asian_race_diagnosed_with_hypertension__diagnosed.explanation = str(output_vals)
        return res

def dftest_American_Indian_or_Alaska_Native_race_diagnosed_with_hypertension_national_average_due_to_lack_of_Massachusetts_specific_data__diagnosed(data_df):
    #("CDC Data Brief 378: https://www.cdc.gov/nchs/data/databriefs/db378.pdf")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: American_Indian_or_Alaska_Native_race_diagnosed_with_hypertension__national_average_due_to_lack_of_Massachusetts_specific_data__ evaluation function. Result is expected to be 31.8%.'
    try:
        diagnosed_ids = data_df[data_df['Code'].astype(str).isin(['38341003', '266287006', '56218007', '194756002', '155295004', '64715009', '827069000', '449759005', '194760004', '429457004', '155297007', '827068008', '194759009', '194794002', '471521000000108', '155302005', '195537001', '473392002', '367390009', '599341000000105', '32966004', '194757006', '702817009', '194769003', '155299005', '46113002', '48146000', '137753003', '194776008', '86234004', '194788005', '194772005', '762463000', '845891000000103', '38481006', '60899001', '194791005', '194782006', '132721000119104', '10725009'])]['Patient'].unique()
        diagnosed = data_df[data_df['Patient'].isin(diagnosed_ids)]
        codes = ['native']
        ref_for_percentage = data_df[data_df['Race'].astype(str).isin(codes)]
        data_per = 100 * diagnosed[diagnosed['Race'].astype(str).isin(codes)]['Patient'].nunique() / ref_for_percentage['Patient'].nunique()
        val = (data_per - 31.8) / np.sqrt((data_per * (100 - data_per) + 31.8 * (100 - 31.8)) / 2)
        ratio = data_per / 31.8
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 31.8, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: American_Indian_or_Alaska_Native_race_diagnosed_with_hypertension__national_average_due_to_lack_of_Massachusetts_specific_data__ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_American_Indian_or_Alaska_Native_race_diagnosed_with_hypertension_national_average_due_to_lack_of_Massachusetts_specific_data__diagnosed.explanation = str(output_vals)
        return res

def dftest_Native_Hawaiian_or_Other_Pacific_Islander_race_diagnosed_with_hypertension__diagnosed(data_df):
    #("Heart.org https://www.heart.org/en/news/2023/11/08/native-hawaiian-and-pacific-islander-health", "CDC - Hypertension Statistics https://www.cdc.gov/bloodpressure/facts.htm")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Native_Hawaiian_or_Other_Pacific_Islander_race_diagnosed_with_hypertension_ evaluation function. Result is expected to be 30%.'
    try:
        diagnosed_ids = data_df[data_df['Code'].astype(str).isin(['38341003', '266287006', '56218007', '194756002', '155295004', '64715009', '827069000', '449759005', '194760004', '429457004', '155297007', '827068008', '194759009', '194794002', '471521000000108', '155302005', '195537001', '473392002', '367390009', '599341000000105', '32966004', '194757006', '702817009', '194769003', '155299005', '46113002', '48146000', '137753003', '194776008', '86234004', '194788005', '194772005', '762463000', '845891000000103', '38481006', '60899001', '194791005', '194782006', '132721000119104', '10725009'])]['Patient'].unique()
        diagnosed = data_df[data_df['Patient'].isin(diagnosed_ids)]
        codes = ['hawaiian', 'pacific']
        ref_for_percentage = data_df[data_df['Race'].astype(str).isin(codes)]
        data_per = 100 * diagnosed[diagnosed['Race'].astype(str).isin(codes)]['Patient'].nunique() / ref_for_percentage['Patient'].nunique()
        val = (data_per - 30) / np.sqrt((data_per * (100 - data_per) + 30 * (100 - 30)) / 2)
        ratio = data_per / 30
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 30, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: Native_Hawaiian_or_Other_Pacific_Islander_race_diagnosed_with_hypertension_ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Native_Hawaiian_or_Other_Pacific_Islander_race_diagnosed_with_hypertension__diagnosed.explanation = str(output_vals)
        return res

def dftest_Hispanic_or_Latino_ethnicity_diagnosed_with_hypertension__diagnosed(data_df):
    #("CDC - Hypertension Statistics: https://www.cdc.gov/bloodpressure/facts.htm")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Hispanic_or_Latino_ethnicity_diagnosed_with_hypertension_ evaluation function. Result is expected to be 24.5%.'
    try:
        diagnosed_ids = data_df[data_df['Code'].astype(str).isin(['38341003', '266287006', '56218007', '194756002', '155295004', '64715009', '827069000', '449759005', '194760004', '429457004', '155297007', '827068008', '194759009', '194794002', '471521000000108', '155302005', '195537001', '473392002', '367390009', '599341000000105', '32966004', '194757006', '702817009', '194769003', '155299005', '46113002', '48146000', '137753003', '194776008', '86234004', '194788005', '194772005', '762463000', '845891000000103', '38481006', '60899001', '194791005', '194782006', '132721000119104', '10725009'])]['Patient'].unique()
        diagnosed = data_df[data_df['Patient'].isin(diagnosed_ids)]
        codes = ['Hispanic or Latino']
        ref_for_percentage = data_df[data_df['Ethnicity'].astype(str).isin(codes)]
        data_per = 100 * diagnosed[diagnosed['Ethnicity'].astype(str).isin(codes)]['Patient'].nunique() / ref_for_percentage['Patient'].nunique()
        val = (data_per - 24.5) / np.sqrt((data_per * (100 - data_per) + 24.5 * (100 - 24.5)) / 2)
        ratio = data_per / 24.5
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 24.5, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: Hispanic_or_Latino_ethnicity_diagnosed_with_hypertension_ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Hispanic_or_Latino_ethnicity_diagnosed_with_hypertension__diagnosed.explanation = str(output_vals)
        return res

def dftest_Not_Hispanic_or_Latino_ethnicity_diagnosed_with_hypertension__diagnosed(data_df):
    #("CDC Hypertension Statistics: https://www.cdc.gov/bloodpressure/facts.htm")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Not_Hispanic_or_Latino_ethnicity_diagnosed_with_hypertension_ evaluation function. Result is expected to be 29.0%.'
    try:
        diagnosed_ids = data_df[data_df['Code'].astype(str).isin(['38341003', '266287006', '56218007', '194756002', '155295004', '64715009', '827069000', '449759005', '194760004', '429457004', '155297007', '827068008', '194759009', '194794002', '471521000000108', '155302005', '195537001', '473392002', '367390009', '599341000000105', '32966004', '194757006', '702817009', '194769003', '155299005', '46113002', '48146000', '137753003', '194776008', '86234004', '194788005', '194772005', '762463000', '845891000000103', '38481006', '60899001', '194791005', '194782006', '132721000119104', '10725009'])]['Patient'].unique()
        diagnosed = data_df[data_df['Patient'].isin(diagnosed_ids)]
        codes = ['Not Hispanic or Latino']
        ref_for_percentage = data_df[data_df['Ethnicity'].astype(str).isin(codes)]
        data_per = 100 * diagnosed[diagnosed['Ethnicity'].astype(str).isin(codes)]['Patient'].nunique() / ref_for_percentage['Patient'].nunique()
        val = (data_per - 29.0) / np.sqrt((data_per * (100 - data_per) + 29.0 * (100 - 29.0)) / 2)
        ratio = data_per / 29.0
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 29.0, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: Not_Hispanic_or_Latino_ethnicity_diagnosed_with_hypertension_ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Not_Hispanic_or_Latino_ethnicity_diagnosed_with_hypertension__diagnosed.explanation = str(output_vals)
        return res

