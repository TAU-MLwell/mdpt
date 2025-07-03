# Filename: unit_test5.py

def dftest_Hemoglobin_A1c_measurement(data_df):
    #("American Diabetes Association (ADA) guidelines, 2023: https://diabetes.org/diabetes/a1c-test")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Hemoglobin_A1c_measurement evaluation function. 95% of the population is expected to be between 4.0 and 5.6.'
    try:
        codes = ['4184637', '3034639', '40329569', '40307813', '3004410', '3007263', '44793001', '37174831', '4276582', '4152671', '37067387', '36304734']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 4.0) & (data_df['value_as_number'] <= 5.6)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 4.0, 'range_high': 5.6}
        if res == False:
            fail_exp = 'Hemoglobin_A1c_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Hemoglobin_A1c_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_glucose_measurement(data_df):
    #("https://diabetes.org/diabetes/testing-and-diagnosis", "https://www.mayoclinic.org/tests-procedures/blood-sugar-test/about/pac-20384898")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_glucose_measurement evaluation function. 95% of the population is expected to be between 70.0 and 99.0.'
    try:
        codes = ['4331286', '40308384', '37392940', '1002230', '3002666', '3004501', '3032230', '3013826', '3007821', '3032986', '3032779', '3029014', '3026728', '3031928', '3032780', '3050134', '46236948', '3025866', '3010044', '4198878', '42868682', '3013256', '3020058', '3048585', '44816672', '3028944', '3020193', '3030416', '40308385', '3020096', '3053004', '3032719', '3005550', '3012792', '37208638', '3031929', '3026536', '3030583', '40762875', '3012635', '3003435', '3003541', '3052381', '4042759', '3039997', '3036283', '3043536', '3023379', '3040820', '4218282', '3042469', '3045067', '3020317', '40762873', '3050095', '3010030', '3000931', '3019765', '3009006', '3014163', '3048856', '3045700', '3036807', '3049496', '40762876', '3049466', '3004067', '4041723', '3035352', '3013802', '4144235', '4042760', '40308386', '4198732', '4193855', '40308387', '4151548', '4198743', '3018582', '40308392', '4018317', '4195213', '40484576', '3029462', '3048522']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 70.0) & (data_df['value_as_number'] <= 99.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 70.0, 'range_high': 99.0}
        if res == False:
            fail_exp = 'Serum_glucose_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_glucose_measurement.explanation = str(output_vals)
        return res

def dftest_Urine_microalbumin_measurement(data_df):
    #("https://www.kidney.org/atoz/content/albuminuria", "https://www.ohdsi.org/data-standardization/the-common-data-model/")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Urine_microalbumin_measurement evaluation function. The value is expected to be less than 30.0.'
    try:
        codes = ['40310556', '4135536', '4152996', '40340434', '37392915', '4065521', '4021120', '4020542', '37398007', '4150342', '40310557', '3000034', '4065543', '40310558', '40310511', '40310014', '3039436', '40339924', '3039775', '1176069', '3005031', '40340390', '3040290', '40760483', '2212189', '3046828', '37392374', '4164903', '1175782', '4107077', '46236963', '2212188', '4154347', '37171232', '3571868', '37398777', '40761549', '3552318', '1761744', '3018104', '3022826', '40656532', '4017498', '40310510', '40656529', '40759673', '3005577', '3001802', '4263307', '37393926', '3025987', '40340388', '40766204', '3043179', '3043771', '40656531', '36660607', '3049506', '40559459', '4354260', '4193419', '3048516', '46235434', '40762252', '1175719', '3012516', '40761532', '40564399', '3002827', '40656530', '313502007', '57378007', '144680007', '167455002', '1021401000000107', '34535-5', '144809008']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] < 30.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = data_in_range > 0.95
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'expected_value': 30.0}
        if res == False:
            fail_exp = 'Urine_microalbumin_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Urine_microalbumin_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_creatinine_measurement(data_df):
    #"https://medlineplus.gov/lab-tests/creatinine-test/, https://www.mayoclinic.org/tests-procedures/creatinine-test/about/pac-20384646"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_creatinine_measurement evaluation function. 95% of the population is expected to be between 0.6 and 1.2.'
    try:
        codes = ['40307212', '40328452', '4276437', '37392176', '4013964']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 0.6) & (data_df['value_as_number'] <= 1.2)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 0.6, 'range_high': 1.2}
        if res == False:
            fail_exp = 'Serum_creatinine_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_creatinine_measurement.explanation = str(output_vals)
        return res

def dftest_Lipid_panel(data_df):
    #"https://www.heart.org/en/health-topics/cholesterol/about-cholesterol/what-your-cholesterol-levels-mean, https://www.mayoclinic.org/tests-procedures/cholesterol-test/about/pac-20384601"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Lipid_panel evaluation function. 95% of the population is expected to be between 0.0 and 200.0.'
    try:
        codes = ['4037130', '2212095', '37061711', '3010946', '1761868']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 0.0) & (data_df['value_as_number'] <= 200.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 0.0, 'range_high': 200.0}
        if res == False:
            fail_exp = 'Lipid_panel evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Lipid_panel.explanation = str(output_vals)
        return res

def dftest_Blood_urea_nitrogen_measurement(data_df):
    #"https://www.mayoclinic.org/tests-procedures/blood-tests/about/pac-20384989, https://www.labcorp.com"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Blood_urea_nitrogen_measurement evaluation function. 95% of the population is expected to be between 7.0 and 20.0.'
    try:
        codes = ['3028280', '3004295', '3010335', '3027219', '3050151']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 7.0) & (data_df['value_as_number'] <= 20.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 7.0, 'range_high': 20.0}
        if res == False:
            fail_exp = 'Blood_urea_nitrogen_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Blood_urea_nitrogen_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_potassium_measurement(data_df):
    #"https://www.ohdsi.org/data-standardization/the-common-data-model/, https://www.mayoclinic.org/tests-procedures/potassium-test/about/pac-20384923"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_potassium_measurement evaluation function. 95% of the population is expected to be between 3.5 and 5.5.'
    try:
        codes = ['4154489', '40315397', '37392171', '40328422', '4042571']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 3.5) & (data_df['value_as_number'] <= 5.5)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 3.5, 'range_high': 5.5}
        if res == False:
            fail_exp = 'Serum_potassium_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_potassium_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_sodium_measurement(data_df):
    #"https://www.mayoclinic.org/tests-procedures/sodium-test/about/pac-20384914, https://medlineplus.gov/lab-tests/sodium-blood-test/"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_sodium_measurement evaluation function. 95% of the population is expected to be between 135.0 and 145.0.'
    try:
        codes = ['4021154', '40307198', '40328427', '37392172', '4043089']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 135.0) & (data_df['value_as_number'] <= 145.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 135.0, 'range_high': 145.0}
        if res == False:
            fail_exp = 'Serum_sodium_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_sodium_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_chloride_measurement(data_df):
    #("https://www.mayoclinic.org", "https://www.labcorp.com", "https://www.ohdsi.org/data-standardization/the-common-data-model/")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_chloride_measurement evaluation function. 95% of the population is expected to be between 96.0 and 106.0.'
    try:
        codes = ['4153270', '40307199', '40328430', '37392173', '37175143', '4043091', '37175142', '4042572', '3014576', '46235783', '37208548', '40757500', '4019545', '4018188', '40652796', '37027122', '44810905', '4188066', '40757501', '3018572', '3013194', '4309125', '40559449', '40563951', '37038125', '4150330', '4269043', '40484030', '3035285', '3009024', '4055551', '36303415', '37399315', '1761323', '4275204', '40330229', '40308408', '3573197', '3043156', '4021154', '4033092', '37173053', '4249884', '44806562', '37208547', '40307320', '44789167', '40654549', '46235784', '4267665', '4260765', '3019550', '3039964', '37398321', '40654548', '4197838', '2212263', '3025034', '3005396', '40329047', '3033733', '36305577', '40757625', '1002263', '4260767', '4055552', '3550746', '3002111', '3020748', '37392561', '40311134', '40328418', '40311128', '40328427', '4260822', '4153006', '40354600', '4043264', '4165618', '40307198', '40328927', '40307214', '4154490', '44812081', '4276441', '4307448', '40310008']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 96.0) & (data_df['value_as_number'] <= 106.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 96.0, 'range_high': 106.0}
        if res == False:
            fail_exp = 'Serum_chloride_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_chloride_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_bicarbonate_measurement(data_df):
    #("https://labtestsonline.org/tests/bicarbonate", "https://www.mayoclinic.org/tests-procedures/blood-tests/about/pac-20384989", "https://www.ohdsi.org/data-standardization/the-common-data-model/")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_bicarbonate_measurement evaluation function. 95% of the population is expected to be between 22.0 and 29.0.'
    try:
        codes = ['4150494', '40307200', '40328433', '607489', '607488']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 22.0) & (data_df['value_as_number'] <= 29.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 22.0, 'range_high': 29.0}
        if res == False:
            fail_exp = 'Serum_bicarbonate_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_bicarbonate_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_calcium_measurement(data_df):
    #"https://www.mayoclinic.org, https://www.labcorp.com"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_calcium_measurement evaluation function. 95% of the population is expected to be between 8.5 and 10.2.'
    try:
        codes = ['4154490', '4307178', '37392174', '40328436', '40307201']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 8.5) & (data_df['value_as_number'] <= 10.2)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 8.5, 'range_high': 10.2}
        if res == False:
            fail_exp = 'Serum_calcium_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_calcium_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_magnesium_measurement(data_df):
    #("https://www.mayoclinic.org", "https://www.labcorp.com")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_magnesium_measurement evaluation function. 95% of the population is expected to be between 1.7 and 2.2.'
    try:
        codes = ['40307253', '4135561', '40328972', '4270766', '37392207']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 1.7) & (data_df['value_as_number'] <= 2.2)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 1.7, 'range_high': 2.2}
        if res == False:
            fail_exp = 'Serum_magnesium_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_magnesium_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_albumin_measurement(data_df):
    #"https://www.mayoclinic.org/tests-procedures/albumin-test/about/pac-20384922"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_albumin_measurement evaluation function. 95% of the population is expected to be between 3.5 and 5.0.'
    try:
        codes = ['40307274', '37392183', '4017497', '40328997', '607481']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 3.5) & (data_df['value_as_number'] <= 5.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 3.5, 'range_high': 5.0}
        if res == False:
            fail_exp = 'Serum_albumin_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_albumin_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_bilirubin_measurement(data_df):
    #"https://medlineplus.gov/lab-tests/bilirubin-test/, https://www.mayoclinic.org/tests-procedures/bilirubin-test/about/pac-20384812"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_bilirubin_measurement evaluation function. 95% of the population is expected to be between 0.1 and 1.2.'
    try:
        codes = ['4197972', '4198887', '4041529', '40315326', '40315341']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 0.1) & (data_df['value_as_number'] <= 1.2)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 0.1, 'range_high': 1.2}
        if res == False:
            fail_exp = 'Serum_bilirubin_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_bilirubin_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_alkaline_phosphatase_measurement(data_df):
    #("https://www.mayocliniclabs.com", "https://www.labcorp.com", "https://www.ohdsi.org/data-standardization/the-common-data-model/")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_alkaline_phosphatase_measurement evaluation function. 95% of the population is expected to be between 44.0 and 121.0.'
    try:
        codes = ['4156813', '4210713', '4195340', '4275207', '607482', '40328358', '4197973', '4308514', '4043079', '3002069', '40315343', '37398460', '3028089', '3001467', '4230636', '40563829', '4220699', '3037712', '46235077', '3035995', '4042561', '40315356', '40328370', '40328372', '40315355', '3018910', '40315357', '3028993', '40558868', '40328371', '3007970', '3021434', '3042479', '3026942', '37398241', '3036955', '3042545', '37173318', '3035400', '4154344', '4154639', '3021222', '37392184', '4193687', '3036185', '4190903', '40563830', '4190902', '3035062', '3011887', '42870304', '37392185', '3037908', '1761414', '3003860', '3037466', '3020990', '3034550', '4156812', '37398586', '3045684', '37208510', '3000235', '3047120', '40563437', '44789031', '40558869', '44816887']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 44.0) & (data_df['value_as_number'] <= 121.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 44.0, 'range_high': 121.0}
        if res == False:
            fail_exp = 'Serum_alkaline_phosphatase_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_alkaline_phosphatase_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_aspartate_aminotransferase_measurement(data_df):
    #("https://www.mayoclinic.org/tests-procedures/liver-function-tests/about/pac-20385003", "https://www.labcorp.com/tests/001123/aspartate-aminotransferase-ast")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_aspartate_aminotransferase_measurement evaluation function. 95% of the population is expected to be between 8.0 and 33.0.'
    try:
        codes = ['37392189', '40757631', '3013721', '3010587', '3022893']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 8.0) & (data_df['value_as_number'] <= 33.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 8.0, 'range_high': 33.0}
        if res == False:
            fail_exp = 'Serum_aspartate_aminotransferase_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_aspartate_aminotransferase_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_alanine_aminotransferase_measurement(data_df):
    #"https://www.mayoclinic.org, https://www.labcorp.com"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_alanine_aminotransferase_measurement evaluation function. 95% of the population is expected to be between 7.0 and 56.0.'
    try:
        codes = ['44788835', '4198730', '37393531', '3006923', '46236949']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 7.0) & (data_df['value_as_number'] <= 56.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 7.0, 'range_high': 56.0}
        if res == False:
            fail_exp = 'Serum_alanine_aminotransferase_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_alanine_aminotransferase_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_lactate_dehydrogenase_measurement(data_df):
    #"https://www.mayocliniclabs.com, https://www.labcorp.com"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_lactate_dehydrogenase_measurement evaluation function. 95% of the population is expected to be between 140.0 and 280.0.'
    try:
        codes = ['4210717', '40328413', '40315388', '4158890', '37392192']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 140.0) & (data_df['value_as_number'] <= 280.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 140.0, 'range_high': 280.0}
        if res == False:
            fail_exp = 'Serum_lactate_dehydrogenase_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_lactate_dehydrogenase_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_uric_acid_measurement(data_df):
    #"https://www.mayocliniclabs.com/test-info/"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_uric_acid_measurement evaluation function. 95% of the population is expected to be between 2.4 and 7.0.'
    try:
        codes = ['4076924', '4165617', '40307235', '40328946', '37392201']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 2.4) & (data_df['value_as_number'] <= 7.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 2.4, 'range_high': 7.0}
        if res == False:
            fail_exp = 'Serum_uric_acid_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_uric_acid_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_triglycerides_measurement(data_df):
    #"https://www.heart.org/en/health-topics/cholesterol/about-cholesterol/triglycerides, https://www.mayoclinic.org/tests-procedures/cholesterol-test/about/pac-20384601"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_triglycerides_measurement evaluation function. 95% of the population is expected to be between 0.0 and 150.0.'
    try:
        codes = ['4156816', '40329067', '40307753', '4055666', '4276570']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 0.0) & (data_df['value_as_number'] <= 150.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 0.0, 'range_high': 150.0}
        if res == False:
            fail_exp = 'Serum_triglycerides_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_triglycerides_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_high_density_lipoprotein_measurement(data_df):
    #("https://www.heart.org", "https://www.mayoclinic.org")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_high_density_lipoprotein_measurement evaluation function. 95% of the population is expected to be between 40.0 and 60.0.'
    try:
        codes = ['37392562', '46284089', '37393305', '37393338', '4195497', '4156659', '4076704', '37398699', '4042059', '40307325', '4055665', '40329056', '37394092', '44789188', '40308860', '4041557', '40330710']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 40.0) & (data_df['value_as_number'] <= 60.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 40.0, 'range_high': 60.0}
        if res == False:
            fail_exp = 'Serum_high_density_lipoprotein_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_high_density_lipoprotein_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_low_density_lipoprotein_measurement(data_df):
    #"https://www.heart.org, https://www.nhlbi.nih.gov"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_low_density_lipoprotein_measurement evaluation function. 95% of the population is expected to be between 0.0 and 100.0.'
    try:
        codes = ['37399325', '4331302', '37394094', '4012479', '37208747', '40307326', '4041556', '1247080', '37394113']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 0.0) & (data_df['value_as_number'] <= 100.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 0.0, 'range_high': 100.0}
        if res == False:
            fail_exp = 'Serum_low_density_lipoprotein_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_low_density_lipoprotein_measurement.explanation = str(output_vals)
        return res

def dftest_Urine_microalbumin_measurement_1(data_df):
    #("https://www.kidney.org/atoz/content/albuminuria", "https://www.mayoclinic.org/tests-procedures/microalbumin-test/about/pac-20384904")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Urine_microalbumin_measurement evaluation function. 95% of the population is expected to be between 0.0 and 30.0.'
    try:
        codes = ['40310556', '4135536', '4152996', '40340434', '37392915', '4065521', '4021120', '4020542', '37398007', '4150342', '40310557', '3000034', '4065543', '40310558', '40310511', '40310014', '3039436', '40339924', '3039775', '1176069', '3005031', '40340390', '3040290', '40760483', '2212189', '3046828', '37392374', '4164903', '1175782', '4107077', '46236963', '2212188', '4154347', '37171232', '3571868', '37398777', '40761549', '3552318', '1761744', '3018104', '3022826', '40656532', '4017498', '40310510', '40656529', '40759673', '3005577', '3001802', '4263307', '37393926', '3025987', '40340388', '40766204', '3043179', '3043771', '40656531', '36660607', '3049506', '40559459', '4354260', '4193419', '3048516', '46235434', '40762252', '1175719', '3012516', '40761532', '40564399', '3002827', '40656530', '313502007', '57378007', '144680007', '167455002', '1021401000000107', '34535-5', '144809008']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 0.0) & (data_df['value_as_number'] <= 30.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 0.0, 'range_high': 30.0}
        if res == False:
            fail_exp = 'Urine_microalbumin_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Urine_microalbumin_measurement_1.explanation = str(output_vals)
        return res

def dftest_Serum_creatinine_measurement_1(data_df):
    #"https://www.ohdsi.org/data-standardization/the-common-data-model/, https://www.mayocliniclabs.com/test-catalog/Clinical+and+Interpretive/8368"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_creatinine_measurement evaluation function. 95% of the population is expected to be between 0.7 and 1.3.'
    try:
        codes = ['40307212', '40328452', '4276437', '37392176', '4013964']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 0.7) & (data_df['value_as_number'] <= 1.3)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 0.7, 'range_high': 1.3}
        if res == False:
            fail_exp = 'Serum_creatinine_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_creatinine_measurement_1.explanation = str(output_vals)
        return res

def dftest_Serum_potassium_measurement_1(data_df):
    #("https://www.mayoclinic.org/tests-procedures/potassium-test/about/pac-20384923", "https://labtestsonline.org/tests/potassium")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_potassium_measurement evaluation function. 95% of the population is expected to be between 3.5 and 5.0.'
    try:
        codes = ['4154489', '40315397', '37392171', '40328422', '4042571']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 3.5) & (data_df['value_as_number'] <= 5.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 3.5, 'range_high': 5.0}
        if res == False:
            fail_exp = 'Serum_potassium_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_potassium_measurement_1.explanation = str(output_vals)
        return res

def dftest_Serum_phosphate_measurement(data_df):
    #("https://www.mayoclinic.org", "https://www.labcorp.com", "https://www.ohdsi.org/data-standardization/the-common-data-model/")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_phosphate_measurement evaluation function. 95% of the population is expected to be between 2.5 and 4.5.'
    try:
        codes = ['4153271', '4041899', '40328441', '40307202', '37392175']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 2.5) & (data_df['value_as_number'] <= 4.5)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 2.5, 'range_high': 4.5}
        if res == False:
            fail_exp = 'Serum_phosphate_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_phosphate_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_aspartate_aminotransferase_measurement_1(data_df):
    #"https://www.mayocliniclabs.com/test-catalog/Clinical+and+Interpretive/8368"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_aspartate_aminotransferase_measurement evaluation function. 95% of the population is expected to be between 8.0 and 40.0.'
    try:
        codes = ['37392189', '40757631', '3013721', '3010587', '3022893']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 8.0) & (data_df['value_as_number'] <= 40.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 8.0, 'range_high': 40.0}
        if res == False:
            fail_exp = 'Serum_aspartate_aminotransferase_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_aspartate_aminotransferase_measurement_1.explanation = str(output_vals)
        return res

def dftest_Serum_uric_acid_measurement_1(data_df):
    #"https://www.mayoclinic.org/, https://www.labcorp.com/, https://www.ohdsi.org/data-standardization/the-common-data-model/"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_uric_acid_measurement evaluation function. 95% of the population is expected to be between 2.6 and 7.2.'
    try:
        codes = ['4076924', '4165617', '40307235', '40328946', '37392201']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 2.6) & (data_df['value_as_number'] <= 7.2)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 2.6, 'range_high': 7.2}
        if res == False:
            fail_exp = 'Serum_uric_acid_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_uric_acid_measurement_1.explanation = str(output_vals)
        return res

def dftest_Serum_cholesterol_measurement(data_df):
    #("https://www.cdc.gov/cholesterol/index.htm", "https://www.heart.org/en/health-topics/cholesterol/about-cholesterol")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_cholesterol_measurement evaluation function. 95% of the population is expected to be between 200.0 and 200.0.'
    try:
        codes = ['4150330', '40307320', '40329047', '4269849', '37392561', '4195491', '4198117', '40307321', '4042057', '4260765', '4195490', '40307323', '40308864', '4055664', '3027114', '40330714', '4041554', '3019900', '37208551', '40307330', '40308862', '37394091', '3557282', '45763616', '40330712', '4042060', '3049873', '40307751', '3015344', '37397989', '40308860', '3028195', '40757504', '40330710', '4041556', '40307324', '44812280', '2212267', '37393333', '37393335', '4156659', '4042059', '4042588', '4055665', '40307327', '4216465', '40482649', '4042586', '40654583', '44787076', '40307326', '3037598', '42868678', '3044491', '42868675', '40759256', '3026453', '3008254', '37027885', '3031776', '40307325', '44787078', '40759255', '37399257', '40483110', '40566162', '40758961', '3028437', '3035899', '40563013', '44791053', '4042062', '4156815', '4042061', '46284971', '40307333', '4299360', '40307335', '4005374', '4195497', '4196842']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 200.0) & (data_df['value_as_number'] <= 200.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(codes)]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 200.0, 'range_high': 200.0}
        if res == False:
            fail_exp = 'Serum_cholesterol_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_cholesterol_measurement.explanation = str(output_vals)
        return res

