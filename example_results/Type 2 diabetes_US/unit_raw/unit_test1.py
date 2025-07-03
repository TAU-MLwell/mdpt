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

