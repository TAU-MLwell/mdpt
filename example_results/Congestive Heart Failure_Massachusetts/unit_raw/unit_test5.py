# Filename: unit_test5.py

def dftest_Radiologic_examination_chest_single_view(data_df):
    #"https://www.radiologyinfo.org"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Radiologic_examination__chest__single_view evaluation function. 95% of the population is expected to be between 40.0 and 50.0.'
    try:
        codes = ['71045', '71046', '71047', '71030', '71020', '71023', '71022', '71021']
        if data_df[data_df['icd9_code'].astype(str).isin(codes)]['subject_id'].nunique() > 0:
            data_in_range = data_df[(data_df['icd9_code'].astype(str).isin(codes)) & (data_df['valuenum'] >= 40.0) & (data_df['valuenum'] <= 50.0)]['subject_id'].nunique() / data_df[data_df['icd9_code'].astype(str).isin(codes)]['subject_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 40.0, 'range_high': 50.0}
        if res == False:
            fail_exp = 'Radiologic_examination__chest__single_view evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Radiologic_examination_chest_single_view.explanation = str(output_vals)
        return res

def dftest_Transferase_aspartate_amino_AST_SGOT_(data_df):
    #("https://www.verywellhealth.com/ast-sgot-8411027", "https://www.mayoclinic.org/tests-procedures/liver-function-tests/about/pac-20385003", "https://labtestsonline.org/tests/aspartate-aminotransferase-ast")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Transferase__aspartate_amino__AST___SGOT_ evaluation function. 95% of the population is expected to be between 8.0 and 33.0.'
    try:
        codes = ['84450']
        if data_df[data_df['icd9_code'].astype(str).isin(codes)]['subject_id'].nunique() > 0:
            data_in_range = data_df[(data_df['icd9_code'].astype(str).isin(codes)) & (data_df['valuenum'] >= 8.0) & (data_df['valuenum'] <= 33.0)]['subject_id'].nunique() / data_df[data_df['icd9_code'].astype(str).isin(codes)]['subject_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 8.0, 'range_high': 33.0}
        if res == False:
            fail_exp = 'Transferase__aspartate_amino__AST___SGOT_ evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Transferase_aspartate_amino_AST_SGOT_.explanation = str(output_vals)
        return res

def dftest_Alanine_aminotransferase_ALT_measurement(data_df):
    #"https://www.webmd.com/fatty-liver-disease/alanine-aminotransferase-alt, https://www.mayoclinic.org/tests-procedures/liver-function-tests/about/pac-20394595"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Alanine_aminotransferase__ALT__measurement evaluation function. 95% of the population is expected to be between 7.0 and 56.0.'
    try:
        codes = ['84460']
        if data_df[data_df['icd9_code'].astype(str).isin(codes)]['subject_id'].nunique() > 0:
            data_in_range = data_df[(data_df['icd9_code'].astype(str).isin(codes)) & (data_df['valuenum'] >= 7.0) & (data_df['valuenum'] <= 56.0)]['subject_id'].nunique() / data_df[data_df['icd9_code'].astype(str).isin(codes)]['subject_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 7.0, 'range_high': 56.0}
        if res == False:
            fail_exp = 'Alanine_aminotransferase__ALT__measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Alanine_aminotransferase_ALT_measurement.explanation = str(output_vals)
        return res

def dftest_B_type_Natriuretic_Peptide_BNP_measurement(data_df):
    #("https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2828020/", "https://www.heart.org")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'B_type_Natriuretic_Peptide__BNP__measurement evaluation function. 95% of the population is expected to be between 0.0 and 100.0.'
    try:
        codes = ['2339-0', '2345-7', '2340-8']
        if data_df[data_df['itemid'].astype(str).isin(codes)]['subject_id'].nunique() > 0:
            data_in_range = data_df[(data_df['itemid'].astype(str).isin(codes)) & (data_df['valuenum'] >= 0.0) & (data_df['valuenum'] <= 100.0)]['subject_id'].nunique() / data_df[data_df['itemid'].astype(str).isin(codes)]['subject_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 0.0, 'range_high': 100.0}
        if res == False:
            fail_exp = 'B_type_Natriuretic_Peptide__BNP__measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_B_type_Natriuretic_Peptide_BNP_measurement.explanation = str(output_vals)
        return res

def dftest_Troponin_I_measurement(data_df):
    #"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2828020/, https://www.heart.org"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Troponin_I_measurement evaluation function. The value is expected to be less than 0.04.'
    try:
        codes = ['3094-0', '3097-3']
        if data_df[data_df['itemid'].astype(str).isin(codes)]['subject_id'].nunique() > 0:
            data_in_range = data_df[(data_df['itemid'].astype(str).isin(codes)) & (data_df['valuenum'] < 0.04)]['subject_id'].nunique() / data_df[data_df['itemid'].astype(str).isin(codes)]['subject_id'].nunique()
            res = data_in_range > 0.95
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'expected_value': 0.04}
        if res == False:
            fail_exp = 'Troponin_I_measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Troponin_I_measurement.explanation = str(output_vals)
        return res

def dftest_Troponin_T_measurement(data_df):
    #("https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2828020/", "https://www.heart.org")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Troponin_T_measurement evaluation function. The value is expected to be less than 0.01.'
    try:
        codes = ['10839-9', '10840-7']
        if data_df[data_df['itemid'].astype(str).isin(codes)]['subject_id'].nunique() > 0:
            data_in_range = data_df[(data_df['itemid'].astype(str).isin(codes)) & (data_df['valuenum'] < 0.01)]['subject_id'].nunique() / data_df[data_df['itemid'].astype(str).isin(codes)]['subject_id'].nunique()
            res = data_in_range > 0.95
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'expected_value': 0.01}
        if res == False:
            fail_exp = 'Troponin_T_measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Troponin_T_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_Creatinine_measurement(data_df):
    #"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2828020/"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Creatinine_measurement evaluation function. 95% of the population is expected to be between 0.6 and 1.3.'
    try:
        codes = ['2951-2', '2955-3', '2956-1']
        if data_df[data_df['itemid'].astype(str).isin(codes)]['subject_id'].nunique() > 0:
            data_in_range = data_df[(data_df['itemid'].astype(str).isin(codes)) & (data_df['valuenum'] >= 0.6) & (data_df['valuenum'] <= 1.3)]['subject_id'].nunique() / data_df[data_df['itemid'].astype(str).isin(codes)]['subject_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 0.6, 'range_high': 1.3}
        if res == False:
            fail_exp = 'Serum_Creatinine_measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Creatinine_measurement.explanation = str(output_vals)
        return res

def dftest_Blood_Urea_Nitrogen_BUN_measurement(data_df):
    #"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2828020/, https://www.mayoclinic.org/tests-procedures/blood-tests/about/pac-20384989, https://medlineplus.gov/lab-tests/blood-urea-nitrogen-bun-test/"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Blood_Urea_Nitrogen__BUN__measurement evaluation function. 95% of the population is expected to be between 7.0 and 20.0.'
    try:
        codes = ['3094-0', '3097-3']
        if data_df[data_df['itemid'].astype(str).isin(codes)]['subject_id'].nunique() > 0:
            data_in_range = data_df[(data_df['itemid'].astype(str).isin(codes)) & (data_df['valuenum'] >= 7.0) & (data_df['valuenum'] <= 20.0)]['subject_id'].nunique() / data_df[data_df['itemid'].astype(str).isin(codes)]['subject_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 7.0, 'range_high': 20.0}
        if res == False:
            fail_exp = 'Blood_Urea_Nitrogen__BUN__measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Blood_Urea_Nitrogen_BUN_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_Electrolytes_measurement(data_df):
    #"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2828020/, https://www.mayoclinic.org"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Electrolytes_measurement evaluation function. 95% of the population is expected to be between 135.0 and 145.0.'
    try:
        codes = ['2345-7', '2340-8']
        if data_df[data_df['itemid'].astype(str).isin(codes)]['subject_id'].nunique() > 0:
            data_in_range = data_df[(data_df['itemid'].astype(str).isin(codes)) & (data_df['valuenum'] >= 135.0) & (data_df['valuenum'] <= 145.0)]['subject_id'].nunique() / data_df[data_df['itemid'].astype(str).isin(codes)]['subject_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 135.0, 'range_high': 145.0}
        if res == False:
            fail_exp = 'Serum_Electrolytes_measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Electrolytes_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_Magnesium_measurement(data_df):
    #"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2828020/, https://ods.od.nih.gov/factsheets/Magnesium-HealthProfessional/"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Magnesium_measurement evaluation function. 95% of the population is expected to be between 1.7 and 2.2.'
    try:
        codes = ['1751-7', '1759-0']
        if data_df[data_df['itemid'].astype(str).isin(codes)]['subject_id'].nunique() > 0:
            data_in_range = data_df[(data_df['itemid'].astype(str).isin(codes)) & (data_df['valuenum'] >= 1.7) & (data_df['valuenum'] <= 2.2)]['subject_id'].nunique() / data_df[data_df['itemid'].astype(str).isin(codes)]['subject_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 1.7, 'range_high': 2.2}
        if res == False:
            fail_exp = 'Serum_Magnesium_measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Magnesium_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_Calcium_measurement(data_df):
    #"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2828020/, https://medlineplus.gov/lab-tests/calcium-in-blood/"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Calcium_measurement evaluation function. 95% of the population is expected to be between 8.5 and 10.2.'
    try:
        codes = ['17861-6', '17862-4']
        if data_df[data_df['itemid'].astype(str).isin(codes)]['subject_id'].nunique() > 0:
            data_in_range = data_df[(data_df['itemid'].astype(str).isin(codes)) & (data_df['valuenum'] >= 8.5) & (data_df['valuenum'] <= 10.2)]['subject_id'].nunique() / data_df[data_df['itemid'].astype(str).isin(codes)]['subject_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 8.5, 'range_high': 10.2}
        if res == False:
            fail_exp = 'Serum_Calcium_measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Calcium_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_Phosphate_measurement(data_df):
    #"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2828020/"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Phosphate_measurement evaluation function. 95% of the population is expected to be between 2.5 and 4.5.'
    try:
        codes = ['17861-6', '17862-4']
        if data_df[data_df['itemid'].astype(str).isin(codes)]['subject_id'].nunique() > 0:
            data_in_range = data_df[(data_df['itemid'].astype(str).isin(codes)) & (data_df['valuenum'] >= 2.5) & (data_df['valuenum'] <= 4.5)]['subject_id'].nunique() / data_df[data_df['itemid'].astype(str).isin(codes)]['subject_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 2.5, 'range_high': 4.5}
        if res == False:
            fail_exp = 'Serum_Phosphate_measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Phosphate_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_Glucose_measurement(data_df):
    #("https://diabetes.org/diabetes/a1c/diagnosis", "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2828020/")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Glucose_measurement evaluation function. 95% of the population is expected to be between 70.0 and 99.0.'
    try:
        codes = ['2345-7', '2340-8']
        if data_df[data_df['itemid'].astype(str).isin(codes)]['subject_id'].nunique() > 0:
            data_in_range = data_df[(data_df['itemid'].astype(str).isin(codes)) & (data_df['valuenum'] >= 70.0) & (data_df['valuenum'] <= 99.0)]['subject_id'].nunique() / data_df[data_df['itemid'].astype(str).isin(codes)]['subject_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 70.0, 'range_high': 99.0}
        if res == False:
            fail_exp = 'Serum_Glucose_measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Glucose_measurement.explanation = str(output_vals)
        return res

