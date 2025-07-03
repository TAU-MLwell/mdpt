# Filename: unit_test5.py

def dftest_Serum_Creatinine_Measurement(data_df):
    #"Mayo Clinic: https://www.mayoclinic.org/tests-procedures/creatinine-test/about/pac-20384646; National Kidney Foundation: https://www.kidney.org/atoz/content/serumcreatinine"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Creatinine_Measurement evaluation function. 95% of the population is expected to be between 0.6 and 1.3.'
    try:
        codes = ['40307212']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['40307212'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 0.6) & (data_df['value_as_number'] <= 1.3)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['40307212'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 0.6, 'range_high': 1.3}
        if res == False:
            fail_exp = 'Serum_Creatinine_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Creatinine_Measurement.explanation = str(output_vals)
        return res

def dftest_Blood_Urea_Nitrogen_Measurement(data_df):
    #"WebMD: https://www.webmd.com/a-to-z-guides/blood-urea-nitrogen; Mayo Clinic: https://www.mayoclinic.org/tests-procedures/blood-urea-nitrogen/about/pac-20384821; MedlinePlus: https://medlineplus.gov/lab-tests/blood-urea-nitrogen-bun-test/"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Blood_Urea_Nitrogen_Measurement evaluation function. 95% of the population is expected to be between 7.0 and 20.0.'
    try:
        codes = ['3028280']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['3028280'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 7.0) & (data_df['value_as_number'] <= 20.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['3028280'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 7.0, 'range_high': 20.0}
        if res == False:
            fail_exp = 'Blood_Urea_Nitrogen_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Blood_Urea_Nitrogen_Measurement.explanation = str(output_vals)
        return res

def dftest_Serum_Potassium_Measurement(data_df):
    #"Cleveland Clinic: https://my.clevelandclinic.org/health/diagnostics/16888-blood-tests; Mayo Clinic: https://www.mayoclinic.org/tests-procedures/potassium-test/about/pac-20384923"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Potassium_Measurement evaluation function. 95% of the population is expected to be between 3.5 and 5.0.'
    try:
        codes = ['4154489']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['4154489'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 3.5) & (data_df['value_as_number'] <= 5.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['4154489'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 3.5, 'range_high': 5.0}
        if res == False:
            fail_exp = 'Serum_Potassium_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Potassium_Measurement.explanation = str(output_vals)
        return res

def dftest_Serum_Sodium_Measurement(data_df):
    #"Cleveland Clinic: https://my.clevelandclinic.org/health/diagnostics/16888-blood-tests"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Sodium_Measurement evaluation function. 95% of the population is expected to be between 135.0 and 145.0.'
    try:
        codes = ['4021154']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['4021154'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 135.0) & (data_df['value_as_number'] <= 145.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['4021154'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 135.0, 'range_high': 145.0}
        if res == False:
            fail_exp = 'Serum_Sodium_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Sodium_Measurement.explanation = str(output_vals)
        return res

def dftest_Serum_Calcium_Measurement(data_df):
    #"Cleveland Clinic: https://my.clevelandclinic.org/health/diagnostics/16888-blood-tests; MedlinePlus: https://medlineplus.gov/lab-tests/calcium-blood-test/"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Calcium_Measurement evaluation function. 95% of the population is expected to be between 8.5 and 10.2.'
    try:
        codes = ['4154490']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['4154490'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 8.5) & (data_df['value_as_number'] <= 10.2)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['4154490'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 8.5, 'range_high': 10.2}
        if res == False:
            fail_exp = 'Serum_Calcium_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Calcium_Measurement.explanation = str(output_vals)
        return res

def dftest_Serum_Phosphorus_Measurement(data_df):
    #"Cleveland Clinic: https://my.clevelandclinic.org/health/diagnostics/16888-blood-tests; Mayo Clinic: https://www.mayoclinic.org/tests-procedures/phosphorus-test/about/pac-20384904"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Phosphorus_Measurement evaluation function. 95% of the population is expected to be between 2.5 and 4.5.'
    try:
        codes = ['41139003']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['41139003'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 2.5) & (data_df['value_as_number'] <= 4.5)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['41139003'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 2.5, 'range_high': 4.5}
        if res == False:
            fail_exp = 'Serum_Phosphorus_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Phosphorus_Measurement.explanation = str(output_vals)
        return res

def dftest_Serum_Albumin_Measurement(data_df):
    #"Cleveland Clinic: https://my.clevelandclinic.org/health/diagnostics/16888-blood-tests; Mayo Clinic: https://www.mayoclinic.org/tests-procedures/albumin-test/about/pac-20384922"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Albumin_Measurement evaluation function. 95% of the population is expected to be between 3.5 and 5.0.'
    try:
        codes = ['40307274']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['40307274'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 3.5) & (data_df['value_as_number'] <= 5.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['40307274'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 3.5, 'range_high': 5.0}
        if res == False:
            fail_exp = 'Serum_Albumin_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Albumin_Measurement.explanation = str(output_vals)
        return res

def dftest_Hemoglobin_Measurement(data_df):
    #"Cleveland Clinic: https://my.clevelandclinic.org/health/diagnostics/16888-blood-tests"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Hemoglobin_Measurement evaluation function. 95% of the population is expected to be between 12.1 and 17.2.'
    try:
        codes = ['4154636']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['4154636'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 12.1) & (data_df['value_as_number'] <= 17.2)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['4154636'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 12.1, 'range_high': 17.2}
        if res == False:
            fail_exp = 'Hemoglobin_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Hemoglobin_Measurement.explanation = str(output_vals)
        return res

def dftest_Hematocrit_Measurement(data_df):
    #"Cleveland Clinic: https://my.clevelandclinic.org/health/diagnostics/16888-blood-tests, Mayo Clinic: https://www.mayoclinic.org/tests-procedures/hematocrit/about/pac-20384728"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Hematocrit_Measurement evaluation function. 95% of the population is expected to be between 36.0 and 50.0.'
    try:
        codes = ['3009542']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['3009542'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 36.0) & (data_df['value_as_number'] <= 50.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['3009542'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 36.0, 'range_high': 50.0}
        if res == False:
            fail_exp = 'Hematocrit_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Hematocrit_Measurement.explanation = str(output_vals)
        return res

def dftest_Glomerular_Filtration_Rate_Measurement(data_df):
    #"National Kidney Foundation: https://www.kidney.org/kidney-topics/estimate-glomerular-filtration-rate"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Glomerular_Filtration_Rate_Measurement evaluation function. 95% of the population is expected to be between 90.0 and 120.0.'
    try:
        codes = ['40771922']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['40771922'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 90.0) & (data_df['value_as_number'] <= 120.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['40771922'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 90.0, 'range_high': 120.0}
        if res == False:
            fail_exp = 'Glomerular_Filtration_Rate_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Glomerular_Filtration_Rate_Measurement.explanation = str(output_vals)
        return res

def dftest_Urine_Protein_Measurement(data_df):
    #("National Kidney Foundation: https://www.kidney.org", "American Association for Clinical Chemistry: https://www.aacc.org")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Urine_Protein_Measurement evaluation function. 95% of the population is expected to be between 0.0 and 30.0.'
    try:
        codes = ['4211845']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['4211845'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 0.0) & (data_df['value_as_number'] <= 30.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['4211845'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 0.0, 'range_high': 30.0}
        if res == False:
            fail_exp = 'Urine_Protein_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Urine_Protein_Measurement.explanation = str(output_vals)
        return res

def dftest_Urine_Albumin_Measurement(data_df):
    #("National Kidney Foundation: https://www.kidney.org/atoz/content/albuminuria", "Mayo Clinic: https://www.mayoclinic.org/tests-procedures/urine-test/about/pac-20384907")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Urine_Albumin_Measurement evaluation function. 95% of the population is expected to be between 0.0 and 30.0.'
    try:
        codes = ['4152996']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['4152996'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 0.0) & (data_df['value_as_number'] <= 30.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['4152996'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 0.0, 'range_high': 30.0}
        if res == False:
            fail_exp = 'Urine_Albumin_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Urine_Albumin_Measurement.explanation = str(output_vals)
        return res

def dftest_Urine_Creatinine_Measurement(data_df):
    #"Healthline: https://www.healthline.com/health/protein-levels-in-urine; Mayo Clinic: https://www.mayoclinic.org/tests-procedures/creatinine-test/about/pac-20384604; Lab Tests Online: https://labtestsonline.org/tests/creatinine-urine"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Urine_Creatinine_Measurement evaluation function. 95% of the population is expected to be between 20.0 and 320.0.'
    try:
        codes = ['40309992']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['40309992'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 20.0) & (data_df['value_as_number'] <= 320.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['40309992'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 20.0, 'range_high': 320.0}
        if res == False:
            fail_exp = 'Urine_Creatinine_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Urine_Creatinine_Measurement.explanation = str(output_vals)
        return res

def dftest_Parathyroid_Hormone_Measurement(data_df):
    #"Cleveland Clinic: https://my.clevelandclinic.org/health/diagnostics/16888-blood-tests; Mayo Clinic Laboratories: https://www.mayocliniclabs.com/test-catalog/Overview/8365"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Parathyroid_Hormone_Measurement evaluation function. 95% of the population is expected to be between 10.0 and 65.0.'
    try:
        codes = ['4141751']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['4141751'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 10.0) & (data_df['value_as_number'] <= 65.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['4141751'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 10.0, 'range_high': 65.0}
        if res == False:
            fail_exp = 'Parathyroid_Hormone_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Parathyroid_Hormone_Measurement.explanation = str(output_vals)
        return res

# Filename: unit_test5.py

def dftest_Serum_Bicarbonate_Measurement(data_df):
    #"Cleveland Clinic: https://my.clevelandclinic.org/health/diagnostics/16888-blood-tests"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Bicarbonate_Measurement evaluation function. 95% of the population is expected to be between 22.0 and 29.0.'
    try:
        codes = ['4150494']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['4150494'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 22.0) & (data_df['value_as_number'] <= 29.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['4150494'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 22.0, 'range_high': 29.0}
        if res == False:
            fail_exp = 'Serum_Bicarbonate_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Bicarbonate_Measurement.explanation = str(output_vals)
        return res

def dftest_Serum_Chloride_Measurement(data_df):
    #"Cleveland Clinic: https://my.clevelandclinic.org/health/diagnostics/16888-blood-tests; Mayo Clinic: https://www.mayoclinic.org/tests-procedures/chloride-test/about/pac-20384900"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Chloride_Measurement evaluation function. 95% of the population is expected to be between 96.0 and 106.0.'
    try:
        codes = ['4153270']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['4153270'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 96.0) & (data_df['value_as_number'] <= 106.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['4153270'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 96.0, 'range_high': 106.0}
        if res == False:
            fail_exp = 'Serum_Chloride_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Chloride_Measurement.explanation = str(output_vals)
        return res

def dftest_Serum_Magnesium_Measurement(data_df):
    #"Cleveland Clinic: https://my.clevelandclinic.org/health/diagnostics/16888-blood-tests"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Magnesium_Measurement evaluation function. 95% of the population is expected to be between 1.7 and 2.2.'
    try:
        codes = ['4270766']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['4270766'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 1.7) & (data_df['value_as_number'] <= 2.2)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['4270766'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 1.7, 'range_high': 2.2}
        if res == False:
            fail_exp = 'Serum_Magnesium_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Magnesium_Measurement.explanation = str(output_vals)
        return res

def dftest_Serum_Uric_Acid_Measurement(data_df):
    #"Cleveland Clinic: https://my.clevelandclinic.org/health/diagnostics/16888-blood-tests; Mayo Clinic: https://www.mayoclinic.org/tests-procedures/uric-acid-test/about/pac-20384914"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Uric_Acid_Measurement evaluation function. 95% of the population is expected to be between 2.4 and 7.0.'
    try:
        codes = ['4076924']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['4076924'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 2.4) & (data_df['value_as_number'] <= 7.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['4076924'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 2.4, 'range_high': 7.0}
        if res == False:
            fail_exp = 'Serum_Uric_Acid_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Uric_Acid_Measurement.explanation = str(output_vals)
        return res

def dftest_Serum_Total_Protein_Measurement(data_df):
    #"Cleveland Clinic: https://my.clevelandclinic.org/health/diagnostics/16888-blood-tests; Mayo Clinic: https://www.mayoclinic.org/tests-procedures/total-protein-test/about/pac-20384985"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Total_Protein_Measurement evaluation function. 95% of the population is expected to be between 6.0 and 8.3.'
    try:
        codes = ['4152983']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['4152983'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 6.0) & (data_df['value_as_number'] <= 8.3)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['4152983'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 6.0, 'range_high': 8.3}
        if res == False:
            fail_exp = 'Serum_Total_Protein_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Total_Protein_Measurement.explanation = str(output_vals)
        return res

def dftest_Serum_Alkaline_Phosphatase_Measurement(data_df):
    #"Cleveland Clinic: https://my.clevelandclinic.org/health/diagnostics/16888-blood-tests; Mayo Clinic: https://www.mayoclinic.org/tests-procedures/alkaline-phosphatase/about/pac-20384923"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Alkaline_Phosphatase_Measurement evaluation function. 95% of the population is expected to be between 44.0 and 121.0.'
    try:
        codes = ['4156813']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['4156813'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 44.0) & (data_df['value_as_number'] <= 121.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['4156813'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 44.0, 'range_high': 121.0}
        if res == False:
            fail_exp = 'Serum_Alkaline_Phosphatase_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Alkaline_Phosphatase_Measurement.explanation = str(output_vals)
        return res

def dftest_Serum_Aspartate_Aminotransferase_Measurement(data_df):
    #"Cleveland Clinic: https://my.clevelandclinic.org/health/diagnostics/16888-blood-tests; Mayo Clinic: https://www.mayoclinic.org/tests-procedures/liver-function-tests/about/pac-20394595"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Aspartate_Aminotransferase_Measurement evaluation function. 95% of the population is expected to be between 8.0 and 33.0.'
    try:
        codes = ['37392189']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['37392189'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 8.0) & (data_df['value_as_number'] <= 33.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['37392189'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 8.0, 'range_high': 33.0}
        if res == False:
            fail_exp = 'Serum_Aspartate_Aminotransferase_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Aspartate_Aminotransferase_Measurement.explanation = str(output_vals)
        return res

def dftest_Serum_Alanine_Aminotransferase_Measurement(data_df):
    #"Cleveland Clinic: https://my.clevelandclinic.org/health/diagnostics/16888-blood-tests"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Alanine_Aminotransferase_Measurement evaluation function. 95% of the population is expected to be between 7.0 and 56.0.'
    try:
        codes = ['3006923']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['3006923'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 7.0) & (data_df['value_as_number'] <= 56.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['3006923'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 7.0, 'range_high': 56.0}
        if res == False:
            fail_exp = 'Serum_Alanine_Aminotransferase_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Alanine_Aminotransferase_Measurement.explanation = str(output_vals)
        return res

def dftest_Serum_Bilirubin_Measurement(data_df):
    #"Cleveland Clinic: https://my.clevelandclinic.org/health/diagnostics/16888-blood-tests; Mayo Clinic: https://www.mayoclinic.org/tests-procedures/bilirubin-test/about/pac-20384812"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Bilirubin_Measurement evaluation function. 95% of the population is expected to be between 0.1 and 1.2.'
    try:
        codes = ['4197972']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['4197972'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 0.1) & (data_df['value_as_number'] <= 1.2)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['4197972'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 0.1, 'range_high': 1.2}
        if res == False:
            fail_exp = 'Serum_Bilirubin_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Bilirubin_Measurement.explanation = str(output_vals)
        return res

def dftest_Serum_Ferritin_Measurement(data_df):
    #"Mayo Clinic: https://www.mayoclinic.org/tests-procedures/ferritin-test/about/pac-20384928, LabCorp: https://www.labcorp.com/tests/004598/ferritin"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Ferritin_Measurement evaluation function. 95% of the population is expected to be between 24.0 and 336.0.'
    try:
        codes = ['4148588']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['4148588'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 24.0) & (data_df['value_as_number'] <= 336.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['4148588'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 24.0, 'range_high': 336.0}
        if res == False:
            fail_exp = 'Serum_Ferritin_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Ferritin_Measurement.explanation = str(output_vals)
        return res

def dftest_Serum_Transferrin_Measurement(data_df):
    #"MedicineNet: https://www.medicinenet.com/ferritin_blood_test/article.htm; Mayo Clinic: https://www.mayoclinic.org/tests-procedures/transferrin-test/about/pac-20384922; LabCorp: https://www.labcorp.com/tests/001321/transferrin"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Transferrin_Measurement evaluation function. 95% of the population is expected to be between 200.0 and 400.0.'
    try:
        codes = ['40315296']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['40315296'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 200.0) & (data_df['value_as_number'] <= 400.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['40315296'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 200.0, 'range_high': 400.0}
        if res == False:
            fail_exp = 'Serum_Transferrin_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Transferrin_Measurement.explanation = str(output_vals)
        return res

def dftest_Serum_Creatinine_Measurement_1(data_df):
    #"Mayo Clinic: https://www.mayoclinic.org/tests-procedures/creatinine-test/about/pac-20384646; NIH: https://medlineplus.gov/lab-tests/creatinine-test/"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Creatinine_Measurement evaluation function. 95% of the population is expected to be between 0.6 and 1.2.'
    try:
        codes = ['40307212']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['40307212'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 0.6) & (data_df['value_as_number'] <= 1.2)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['40307212'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 0.6, 'range_high': 1.2}
        if res == False:
            fail_exp = 'Serum_Creatinine_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Creatinine_Measurement_1.explanation = str(output_vals)
        return res

def dftest_Blood_Urea_Nitrogen_Measurement_1(data_df):
    #"WebMD: https://www.webmd.com/a-to-z-guides/blood-urea-nitrogen; Mayo Clinic: https://www.mayoclinic.org/tests-procedures/blood-urea-nitrogen/about/pac-20384821; MedlinePlus: https://medlineplus.gov/lab-tests/blood-urea-nitrogen-bun-test/"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Blood_Urea_Nitrogen_Measurement evaluation function. 95% of the population is expected to be between 7.0 and 20.0.'
    try:
        codes = ['3028280']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['3028280'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 7.0) & (data_df['value_as_number'] <= 20.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['3028280'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 7.0, 'range_high': 20.0}
        if res == False:
            fail_exp = 'Blood_Urea_Nitrogen_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Blood_Urea_Nitrogen_Measurement_1.explanation = str(output_vals)
        return res

def dftest_Serum_Albumin_Measurement_1(data_df):
    #"Cleveland Clinic: https://my.clevelandclinic.org/health/diagnostics/16888-blood-tests; MedlinePlus: https://medlineplus.gov/lab-tests/albumin-blood-test"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Albumin_Measurement evaluation function. 95% of the population is expected to be between 3.5 and 5.0.'
    try:
        codes = ['40307274']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['40307274'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 3.5) & (data_df['value_as_number'] <= 5.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['40307274'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 3.5, 'range_high': 5.0}
        if res == False:
            fail_exp = 'Serum_Albumin_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Albumin_Measurement_1.explanation = str(output_vals)
        return res

def dftest_Hemoglobin_Measurement_1(data_df):
    #"Cleveland Clinic: https://my.clevelandclinic.org/health/diagnostics/16888-blood-tests; Mayo Clinic: https://www.mayoclinic.org/tests-procedures/hemoglobin-test/about/pac-20385075"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Hemoglobin_Measurement evaluation function. 95% of the population is expected to be between 12.0 and 18.0.'
    try:
        codes = ['4154636']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['4154636'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 12.0) & (data_df['value_as_number'] <= 18.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['4154636'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 12.0, 'range_high': 18.0}
        if res == False:
            fail_exp = 'Hemoglobin_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Hemoglobin_Measurement_1.explanation = str(output_vals)
        return res

def dftest_Serum_Chloride_Measurement_1(data_df):
    #"Cleveland Clinic: https://my.clevelandclinic.org/health/diagnostics/16888-blood-tests; Mayo Clinic: https://www.mayoclinic.org/tests-procedures/chloride-test/about/pac-20384900"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Chloride_Measurement evaluation function. 95% of the population is expected to be between 96.0 and 106.0.'
    try:
        codes = ['4153270']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['4153270'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 96.0) & (data_df['value_as_number'] <= 106.0)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['4153270'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 96.0, 'range_high': 106.0}
        if res == False:
            fail_exp = 'Serum_Chloride_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Chloride_Measurement_1.explanation = str(output_vals)
        return res

def dftest_Serum_Uric_Acid_Measurement_1(data_df):
    #"Cleveland Clinic: https://my.clevelandclinic.org/health/diagnostics/16888-blood-tests; Mayo Clinic: https://www.mayoclinic.org/tests-procedures/uric-acid-test/about/pac-20384914"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Uric_Acid_Measurement evaluation function. 95% of the population is expected to be between 2.6 and 7.2.'
    try:
        codes = ['4076924']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['4076924'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 2.6) & (data_df['value_as_number'] <= 7.2)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['4076924'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 2.6, 'range_high': 7.2}
        if res == False:
            fail_exp = 'Serum_Uric_Acid_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Uric_Acid_Measurement_1.explanation = str(output_vals)
        return res

def dftest_Serum_Bilirubin_Measurement_1(data_df):
    #"Cleveland Clinic: https://my.clevelandclinic.org/health/diagnostics/16888-blood-tests; Mayo Clinic: https://www.mayoclinic.org/tests-procedures/bilirubin-test/about/pac-20384812"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_Bilirubin_Measurement evaluation function. 95% of the population is expected to be between 0.1 and 1.2.'
    try:
        codes = ['4197972']
        if data_df[data_df['measurement_concept_id'].astype(str).isin(['4197972'])]['person_id'].nunique() > 0:
            data_in_range = data_df[(data_df['measurement_concept_id'].astype(str).isin(codes)) & (data_df['value_as_number'] >= 0.1) & (data_df['value_as_number'] <= 1.2)]['person_id'].nunique() / data_df[data_df['measurement_concept_id'].astype(str).isin(['4197972'])]['person_id'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 0.1, 'range_high': 1.2}
        if res == False:
            fail_exp = 'Serum_Bilirubin_Measurement evaluation in the examined data is ' + str(100 * data_in_range) + '%'
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_Bilirubin_Measurement_1.explanation = str(output_vals)
        return res

