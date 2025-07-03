# Filename: unit_test4.py

def dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_gender_of_the_person_Code_Female_diagnosed(data_df):
    #"https://www.cdc.gov/ckd/index.html; https://www.kidney.org/news/newsroom/factsheets/Chronic-Kidney-Disease"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_gender_of_the_person__Code__Female evaluation function. Result is expected to be 15.4%.'
    try:
        diagnosed_ids = data_df[data_df['condition_concept_id'].astype(str).isin(['46271022', '443614', '443601', '443611', '45582391', '443597', '3553408', '44792018', '37017104', '44792017', '443612', '45763854', '45763855', '37017813', '1571486', '45553438', '44830172', '619679', '45582392', '44792255', '3577568', '3577571', '196991', '3553777', '45543858', '44792227', '3553776', '45553437', '44792229', '3577573', '45582394', '3553778', '3577569', '36210709', '35209276', '45768812', '44782429', '45582393', '3553779', '36716947', '198185', '1990140', '35209279', '4322556', '44792231'])]['person_id'].unique()
        diagnosed = data_df[data_df['person_id'].isin(diagnosed_ids)]
        codes = ['45878463']
        ref_for_percentage = data_df[data_df['gender_concept_id'].astype(str).isin(codes)]
        data_per = 100 * diagnosed[diagnosed['gender_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 15.4) / np.sqrt((data_per * (100 - data_per) + 15.4 * (100 - 15.4)) / 2)
        ratio = data_per / 15.4
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 15.4, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_gender_of_the_person__Code__Female percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_gender_of_the_person_Code_Female_diagnosed.explanation = str(output_vals)
        return res

def dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person_Code_White_diagnosed(data_df):
    #"CDC, Chronic Kidney Disease in the United States (https://www.cdc.gov/kidneydisease/publications.html)"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person__Code__White evaluation function. Result is expected to be 12.5%.'
    try:
        diagnosed_ids = data_df[data_df['condition_concept_id'].astype(str).isin(['46271022', '443614', '443601', '443611', '45582391', '443597', '3553408', '44792018', '37017104', '44792017', '443612', '45763854', '45763855', '37017813', '1571486', '45553438', '44830172', '619679', '45582392', '44792255', '3577568', '3577571', '196991', '3553777', '45543858', '44792227', '3553776', '45553437', '44792229', '3577573', '45582394', '3553778', '3577569', '36210709', '35209276', '45768812', '44782429', '45582393', '3553779', '36716947', '198185', '1990140', '35209279', '4322556', '44792231'])]['person_id'].unique()
        diagnosed = data_df[data_df['person_id'].isin(diagnosed_ids)]
        codes = ['8527']
        ref_for_percentage = data_df[data_df['race_concept_id'].astype(str).isin(codes)]
        data_per = 100 * diagnosed[diagnosed['race_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 12.5) / np.sqrt((data_per * (100 - data_per) + 12.5 * (100 - 12.5)) / 2)
        ratio = data_per / 12.5
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 12.5, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person__Code__White percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person_Code_White_diagnosed.explanation = str(output_vals)
        return res

def dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person_Code_Black_or_African_American_diagnosed(data_df):
    #"https://blackdoctor.org/nearly-35-of-people-with-chronic-kidney-disease-are-black/, https://www.cdc.gov/kidneydisease/publications-resources/annual-report.html"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person__Code__Black_or_African_American evaluation function. Result is expected to be 35%.'
    try:
        diagnosed_ids = data_df[data_df['condition_concept_id'].astype(str).isin(['46271022', '443614', '443601', '443611', '45582391', '443597', '3553408', '44792018', '37017104', '44792017', '443612', '45763854', '45763855', '37017813', '1571486', '45553438', '44830172', '619679', '45582392', '44792255', '3577568', '3577571', '196991', '3553777', '45543858', '44792227', '3553776', '45553437', '44792229', '3577573', '45582394', '3553778', '3577569', '36210709', '35209276', '45768812', '44782429', '45582393', '3553779', '36716947', '198185', '1990140', '35209279', '4322556', '44792231'])]['person_id'].unique()
        diagnosed = data_df[data_df['person_id'].isin(diagnosed_ids)]
        codes = ['8516']
        ref_for_percentage = data_df[data_df['race_concept_id'].astype(str).isin(codes)]
        data_per = 100 * diagnosed[diagnosed['race_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 35) / np.sqrt((data_per * (100 - data_per) + 35 * (100 - 35)) / 2)
        ratio = data_per / 35
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 35, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person__Code__Black_or_African_American percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person_Code_Black_or_African_American_diagnosed.explanation = str(output_vals)
        return res

def dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person_Code_Asian_diagnosed(data_df):
    #("https://pubmed.ncbi.nlm.nih.gov/34570204/")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person__Code__Asian evaluation function. Result is expected to be 1.7%.'
    try:
        diagnosed_ids = data_df[data_df['condition_concept_id'].astype(str).isin(['46271022', '443614', '443601', '443611', '45582391', '443597', '3553408', '44792018', '37017104', '44792017', '443612', '45763854', '45763855', '37017813', '1571486', '45553438', '44830172', '619679', '45582392', '44792255', '3577568', '3577571', '196991', '3553777', '45543858', '44792227', '3553776', '45553437', '44792229', '3577573', '45582394', '3553778', '3577569', '36210709', '35209276', '45768812', '44782429', '45582393', '3553779', '36716947', '198185', '1990140', '35209279', '4322556', '44792231'])]['person_id'].unique()
        diagnosed = data_df[data_df['person_id'].isin(diagnosed_ids)]
        codes = ['8557']
        ref_for_percentage = data_df[data_df['race_concept_id'].astype(str).isin(codes)]
        data_per = 100 * diagnosed[diagnosed['race_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 1.7) / np.sqrt((data_per * (100 - data_per) + 1.7 * (100 - 1.7)) / 2)
        ratio = data_per / 1.7
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 1.7, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person__Code__Asian percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person_Code_Asian_diagnosed.explanation = str(output_vals)
        return res

def dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person_Code_Native_Hawaiian_or_Other_Pacific_Islander_diagnosed(data_df):
    #"https://pubmed.ncbi.nlm.nih.gov/32387021/"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person__Code__Native_Hawaiian_or_Other_Pacific_Islander evaluation function. Result is expected to be 3.5%.'
    try:
        diagnosed_ids = data_df[data_df['condition_concept_id'].astype(str).isin(['46271022', '443614', '443601', '443611', '45582391', '443597', '3553408', '44792018', '37017104', '44792017', '443612', '45763854', '45763855', '37017813', '1571486', '45553438', '44830172', '619679', '45582392', '44792255', '3577568', '3577571', '196991', '3553777', '45543858', '44792227', '3553776', '45553437', '44792229', '3577573', '45582394', '3553778', '3577569', '36210709', '35209276', '45768812', '44782429', '45582393', '3553779', '36716947', '198185', '1990140', '35209279', '4322556', '44792231'])]['person_id'].unique()
        diagnosed = data_df[data_df['person_id'].isin(diagnosed_ids)]
        codes = ['8657']
        ref_for_percentage = data_df[data_df['race_concept_id'].astype(str).isin(codes)]
        data_per = 100 * diagnosed[diagnosed['race_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 3.5) / np.sqrt((data_per * (100 - data_per) + 3.5 * (100 - 3.5)) / 2)
        ratio = data_per / 3.5
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 3.5, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person__Code__Native_Hawaiian_or_Other_Pacific_Islander percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person_Code_Native_Hawaiian_or_Other_Pacific_Islander_diagnosed.explanation = str(output_vals)
        return res

def dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person_Code_American_Indian_or_Alaska_Native_diagnosed(data_df):
    #"https://www.cdc.gov/ckd/surveillance/index.html"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person__Code__American_Indian_or_Alaska_Native evaluation function. Result is expected to be 15.9%.'
    try:
        diagnosed_ids = data_df[data_df['condition_concept_id'].astype(str).isin(['46271022', '443614', '443601', '443611', '45582391', '443597', '3553408', '44792018', '37017104', '44792017', '443612', '45763854', '45763855', '37017813', '1571486', '45553438', '44830172', '619679', '45582392', '44792255', '3577568', '3577571', '196991', '3553777', '45543858', '44792227', '3553776', '45553437', '44792229', '3577573', '45582394', '3553778', '3577569', '36210709', '35209276', '45768812', '44782429', '45582393', '3553779', '36716947', '198185', '1990140', '35209279', '4322556', '44792231'])]['person_id'].unique()
        diagnosed = data_df[data_df['person_id'].isin(diagnosed_ids)]
        codes = ['8521']
        ref_for_percentage = data_df[data_df['race_concept_id'].astype(str).isin(codes)]
        data_per = 100 * diagnosed[diagnosed['race_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 15.9) / np.sqrt((data_per * (100 - data_per) + 15.9 * (100 - 15.9)) / 2)
        ratio = data_per / 15.9
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 15.9, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person__Code__American_Indian_or_Alaska_Native percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_that_refers_to_an_identifier_in_the_Standardized_Vocabularies_for_the_race_of_the_person_Code_American_Indian_or_Alaska_Native_diagnosed.explanation = str(output_vals)
        return res

def dftest_A_foreign_key_that_refers_to_the_standard_concept_identifier_in_the_Standardized_Vocabularies_for_the_ethnicity_of_the_person_Code_Not_Hispanic_or_Latino_diagnosed(data_df):
    #("https://www.cdc.gov/kidneydisease/pdf/Chronic-Kidney-Disease-Fact-Sheet-2021.pdf", "https://www.statista.com/statistics/780675/chronic-kidney-disease-prevalence-us-by-ethnicity/")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: A_foreign_key_that_refers_to_the_standard_concept_identifier_in_the_Standardized_Vocabularies_for_the_ethnicity_of_the_person__Code__Not_Hispanic_or_Latino evaluation function. Result is expected to be 13.8%.'
    try:
        diagnosed_ids = data_df[data_df['condition_concept_id'].astype(str).isin(['46271022', '443614', '443601', '443611', '45582391', '443597', '3553408', '44792018', '37017104', '44792017', '443612', '45763854', '45763855', '37017813', '1571486', '45553438', '44830172', '619679', '45582392', '44792255', '3577568', '3577571', '196991', '3553777', '45543858', '44792227', '3553776', '45553437', '44792229', '3577573', '45582394', '3553778', '3577569', '36210709', '35209276', '45768812', '44782429', '45582393', '3553779', '36716947', '198185', '1990140', '35209279', '4322556', '44792231'])]['person_id'].unique()
        diagnosed = data_df[data_df['person_id'].isin(diagnosed_ids)]
        codes = ['38003564']
        ref_for_percentage = data_df[data_df['ethnicity_concept_id'].astype(str).isin(codes)]
        data_per = 100 * diagnosed[diagnosed['ethnicity_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 13.8) / np.sqrt((data_per * (100 - data_per) + 13.8 * (100 - 13.8)) / 2)
        ratio = data_per / 13.8
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 13.8, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: A_foreign_key_that_refers_to_the_standard_concept_identifier_in_the_Standardized_Vocabularies_for_the_ethnicity_of_the_person__Code__Not_Hispanic_or_Latino percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_that_refers_to_the_standard_concept_identifier_in_the_Standardized_Vocabularies_for_the_ethnicity_of_the_person_Code_Not_Hispanic_or_Latino_diagnosed.explanation = str(output_vals)
        return res

def dftest_A_foreign_key_that_refers_to_the_standard_concept_identifier_in_the_Standardized_Vocabularies_for_the_ethnicity_of_the_person_Code_Hispanic_or_Latino_diagnosed(data_df):
    #"https://www.kidney.org/news/newsroom/factsheets/CKD_Awareness; https://pmc.ncbi.nlm.nih.gov/articles/PMC7269703/"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: A_foreign_key_that_refers_to_the_standard_concept_identifier_in_the_Standardized_Vocabularies_for_the_ethnicity_of_the_person__Code__Hispanic_or_Latino evaluation function. Result is expected to be 15.1%.'
    try:
        diagnosed_ids = data_df[data_df['condition_concept_id'].astype(str).isin(['46271022', '443614', '443601', '443611', '45582391', '443597', '3553408', '44792018', '37017104', '44792017', '443612', '45763854', '45763855', '37017813', '1571486', '45553438', '44830172', '619679', '45582392', '44792255', '3577568', '3577571', '196991', '3553777', '45543858', '44792227', '3553776', '45553437', '44792229', '3577573', '45582394', '3553778', '3577569', '36210709', '35209276', '45768812', '44782429', '45582393', '3553779', '36716947', '198185', '1990140', '35209279', '4322556', '44792231'])]['person_id'].unique()
        diagnosed = data_df[data_df['person_id'].isin(diagnosed_ids)]
        codes = ['38003563']
        ref_for_percentage = data_df[data_df['ethnicity_concept_id'].astype(str).isin(codes)]
        data_per = 100 * diagnosed[diagnosed['ethnicity_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / ref_for_percentage['person_id'].nunique()
        val = (data_per - 15.1) / np.sqrt((data_per * (100 - data_per) + 15.1 * (100 - 15.1)) / 2)
        ratio = data_per / 15.1
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 15.1, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: A_foreign_key_that_refers_to_the_standard_concept_identifier_in_the_Standardized_Vocabularies_for_the_ethnicity_of_the_person__Code__Hispanic_or_Latino percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_that_refers_to_the_standard_concept_identifier_in_the_Standardized_Vocabularies_for_the_ethnicity_of_the_person_Code_Hispanic_or_Latino_diagnosed.explanation = str(output_vals)
        return res

