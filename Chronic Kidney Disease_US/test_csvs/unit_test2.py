# Filename: unit_test2.py

def dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_gender_of_the_person_Code_Female(data_df):
    #"https://www.census.gov/quickfacts/fact/table/US/PST045223"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_gender_of_the_person__Code__Female evaluation function. Result is expected to be 50.5%.'
    try:
        codes = ['45878463']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['gender_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 50.5) / np.sqrt((data_per * (100 - data_per) + 50.5 * (100 - 50.5)) / 2)
        ratio = data_per / 50.5
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 50.5, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_gender_of_the_person__Code__Female percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_gender_of_the_person_Code_Female.explanation = str(output_vals)
        return res

def dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_gender_of_the_person_Code_Male(data_df):
    #"https://www.census.gov/quickfacts/fact/table/US/PST045223"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_gender_of_the_person__Code__Male evaluation function. Result is expected to be 49.5%.'
    try:
        codes = ['45880669']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['gender_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 49.5) / np.sqrt((data_per * (100 - data_per) + 49.5 * (100 - 49.5)) / 2)
        ratio = data_per / 49.5
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 49.5, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_gender_of_the_person__Code__Male percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_gender_of_the_person_Code_Male.explanation = str(output_vals)
        return res

def dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person_Code_White(data_df):
    #"https://www.census.gov/quickfacts/fact/table/US/PST045223"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person__Code__White evaluation function. Result is expected to be 75.8%.'
    try:
        codes = ['8527']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['race_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 75.8) / np.sqrt((data_per * (100 - data_per) + 75.8 * (100 - 75.8)) / 2)
        ratio = data_per / 75.8
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 75.8, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person__Code__White percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person_Code_White.explanation = str(output_vals)
        return res

def dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person_Code_Black_or_African_American(data_df):
    #"https://www.census.gov/quickfacts/fact/table/US/PST045223"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person__Code__Black_or_African_American evaluation function. Result is expected to be 13.6%.'
    try:
        codes = ['8516']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['race_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 13.6) / np.sqrt((data_per * (100 - data_per) + 13.6 * (100 - 13.6)) / 2)
        ratio = data_per / 13.6
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 13.6, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person__Code__Black_or_African_American percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person_Code_Black_or_African_American.explanation = str(output_vals)
        return res

def dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person_Code_Asian(data_df):
    #"https://www.census.gov/quickfacts/fact/table/US/PST045223"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person__Code__Asian evaluation function. Result is expected to be 6.4%.'
    try:
        codes = ['8557']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['race_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 6.4) / np.sqrt((data_per * (100 - data_per) + 6.4 * (100 - 6.4)) / 2)
        ratio = data_per / 6.4
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 6.4, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person__Code__Asian percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person_Code_Asian.explanation = str(output_vals)
        return res

def dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person_Code_Native_Hawaiian_or_Other_Pacific_Islander(data_df):
    #"https://www.census.gov/quickfacts/fact/table/US/PST045223"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person__Code__Native_Hawaiian_or_Other_Pacific_Islander evaluation function. Result is expected to be 0.2%.'
    try:
        codes = ['8657']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['race_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 0.2) / np.sqrt((data_per * (100 - data_per) + 0.2 * (100 - 0.2)) / 2)
        ratio = data_per / 0.2
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 0.2, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person__Code__Native_Hawaiian_or_Other_Pacific_Islander percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person_Code_Native_Hawaiian_or_Other_Pacific_Islander.explanation = str(output_vals)
        return res

def dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person_Code_American_Indian_or_Alaska_Native(data_df):
    #"https://www.census.gov/quickfacts/fact/table/US/PST045223"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person__Code__American_Indian_or_Alaska_Native evaluation function. Result is expected to be 1.3%.'
    try:
        codes = ['8521']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['race_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 1.3) / np.sqrt((data_per * (100 - data_per) + 1.3 * (100 - 1.3)) / 2)
        ratio = data_per / 1.3
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 1.3, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person__Code__American_Indian_or_Alaska_Native percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person_Code_American_Indian_or_Alaska_Native.explanation = str(output_vals)
        return res

def dftest_A_foreign_key_that_refers_to_the_standard_concept_identifier_in_the_Standardized_Vocabularies_for_the_ethnicity_of_the_person_Code_Not_Hispanic_or_Latino(data_df):
    #"https://www.census.gov/quickfacts/fact/table/US/PST045223"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'A_foreign_key_that_refers_to_the_standard_concept_identifier_in_the_Standardized_Vocabularies_for_the_ethnicity_of_the_person__Code__Not_Hispanic_or_Latino evaluation function. Result is expected to be 59.3%.'
    try:
        codes = ['38003564']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['ethnicity_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 59.3) / np.sqrt((data_per * (100 - data_per) + 59.3 * (100 - 59.3)) / 2)
        ratio = data_per / 59.3
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 59.3, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'A_foreign_key_that_refers_to_the_standard_concept_identifier_in_the_Standardized_Vocabularies_for_the_ethnicity_of_the_person__Code__Not_Hispanic_or_Latino percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_that_refers_to_the_standard_concept_identifier_in_the_Standardized_Vocabularies_for_the_ethnicity_of_the_person_Code_Not_Hispanic_or_Latino.explanation = str(output_vals)
        return res

def dftest_A_foreign_key_that_refers_to_the_standard_concept_identifier_in_the_Standardized_Vocabularies_for_the_ethnicity_of_the_person_Code_Hispanic_or_Latino(data_df):
    #"https://www.census.gov/quickfacts/fact/table/US/PST045223"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'A_foreign_key_that_refers_to_the_standard_concept_identifier_in_the_Standardized_Vocabularies_for_the_ethnicity_of_the_person__Code__Hispanic_or_Latino evaluation function. Result is expected to be 19.1%.'
    try:
        codes = ['38003563']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['ethnicity_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 19.1) / np.sqrt((data_per * (100 - data_per) + 19.1 * (100 - 19.1)) / 2)
        ratio = data_per / 19.1
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 19.1, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'A_foreign_key_that_refers_to_the_standard_concept_identifier_in_the_Standardized_Vocabularies_for_the_ethnicity_of_the_person__Code__Hispanic_or_Latino percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_that_refers_to_the_standard_concept_identifier_in_the_Standardized_Vocabularies_for_the_ethnicity_of_the_person_Code_Hispanic_or_Latino.explanation = str(output_vals)
        return res

