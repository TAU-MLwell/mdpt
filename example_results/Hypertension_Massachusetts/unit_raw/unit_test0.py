# Filename: unit_test5.py

def dftest_Blood_pressure_measurement(data_df):
    #("American Heart Association (AHA): https://www.heart.org/en/health-topics/high-blood-pressure/understanding-blood-pressure-readings", "CDC Blood Pressure Guidelines: https://www.cdc.gov/bloodpressure/index.htm")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Blood_pressure_measurement evaluation function. 95% of the population is expected to be between 120.0 and 80.0.'
    try:
        codes = ['4326744', '3017490', '3027598', '4264765', '903119', '40758413', '3004249', '3018336', '1003132', '4239021', '3013032', '45876174', '3035856', '3032204', '4060833', '44792136', '1003128', '1002943', '40299297', '4268883', '44807258', '46286741', '40462159', '46233683', '3003798', '46286749', '4298391', '4292062', '4152194', '46286740', '45876183', '3012888', '4155154', '3032708', '45876176', '21492238', '1030227', '903107', '45876175', '44789315', '3028803', '1002753', '903132', '44805969', '46286894', '3009395', '4154790', '45770407', '4226401', '3005374', '4298393', '36717616', '3031680', '3046109', '3019962', '1002668', '3033616', '44809183', '36032120', '3012526', '21492241', '3012311', '3555547', '36031928', '46233682', '45876184', '3031203', '4065263', '3022152', '45876178', '4295063', '40307036', '36716481', '36716479', '4218778', '4300738', '37394516', '40546154', '40547143', '4046988', '4136881', '37394515', '4079611', '4178268', '4106549', '4168708', '40330136', '40308322', '1246425', '4184999', '37204163', '35610600', '40488869', '40330228', '4134689', '40307033', '44789316', '40308407']
        if data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique() > 0:
            data_in_range = data_df[(data_df['Code'].astype(str).isin(codes)) & (data_df['Value'] >= 120.0) & (data_df['Value'] <= 80.0)]['Patient'].nunique() / data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 120.0, 'range_high': 80.0}
        if res == False:
            fail_exp = 'Blood_pressure_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Blood_pressure_measurement.explanation = str(output_vals)
        return res

def dftest_Lipid_panel_measurement(data_df):
    #("American Heart Association (https://www.heart.org)", "National Cholesterol Education Program (NCEP) guidelines")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Lipid_panel_measurement evaluation function. 95% of the population is expected to be between 150.0 and 200.0.'
    try:
        codes = ['3560539', '4055665', '45763616', '37393335', '44812280', '4156815', '40307751', '40329067', '4196842', '40307330', '4042586', '40482649', '4042061', '37398699', '40563013', '4156659', '40566162', '37399257', '40483110', '40307753']
        if data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique() > 0:
            data_in_range = data_df[(data_df['Code'].astype(str).isin(codes)) & (data_df['Value'] >= 150.0) & (data_df['Value'] <= 200.0)]['Patient'].nunique() / data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 150.0, 'range_high': 200.0}
        if res == False:
            fail_exp = 'Lipid_panel_measurement evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Lipid_panel_measurement.explanation = str(output_vals)
        return res

def dftest_Serum_glucose_level(data_df):
    #("American Diabetes Association (https://diabetes.org)", "LOINC (https://loinc.org)")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_glucose_level evaluation function. 95% of the population is expected to be between 70.0 and 100.0.'
    try:
        codes = ['2345-7', '2951-2', '17856-6', '2160-0']
        if data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique() > 0:
            data_in_range = data_df[(data_df['Code'].astype(str).isin(codes)) & (data_df['Value'] >= 70.0) & (data_df['Value'] <= 100.0)]['Patient'].nunique() / data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 70.0, 'range_high': 100.0}
        if res == False:
            fail_exp = 'Serum_glucose_level evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_glucose_level.explanation = str(output_vals)
        return res

def dftest_Serum_cholesterol_level(data_df):
    #("American Heart Association: https://www.heart.org", "CDC Cholesterol Guidelines: https://www.cdc.gov/cholesterol/index.htm", "[LOINC](https://loinc.org)")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_cholesterol_level evaluation function. 95% of the population is expected to be between 0.0 and 200.0.'
    try:
        codes = ['2093-3', '2571-8', '2089-1']
        if data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique() > 0:
            data_in_range = data_df[(data_df['Code'].astype(str).isin(codes)) & (data_df['Value'] >= 0.0) & (data_df['Value'] <= 200.0)]['Patient'].nunique() / data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 0.0, 'range_high': 200.0}
        if res == False:
            fail_exp = 'Serum_cholesterol_level evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_cholesterol_level.explanation = str(output_vals)
        return res

def dftest_Serum_HDL_cholesterol_level(data_df):
    #("American Heart Association (https://www.heart.org)", "National Cholesterol Education Program (https://www.nhlbi.nih.gov)")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_HDL_cholesterol_level evaluation function. 95% of the population is expected to be between 40.0 and 50.0.'
    try:
        codes = ['2572-6', '2085-9', '13457-7']
        if data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique() > 0:
            data_in_range = data_df[(data_df['Code'].astype(str).isin(codes)) & (data_df['Value'] >= 40.0) & (data_df['Value'] <= 50.0)]['Patient'].nunique() / data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 40.0, 'range_high': 50.0}
        if res == False:
            fail_exp = 'Serum_HDL_cholesterol_level evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_HDL_cholesterol_level.explanation = str(output_vals)
        return res

def dftest_Serum_LDL_cholesterol_level(data_df):
    #"(American Heart Association: https://www.heart.org, National Cholesterol Education Program: https://www.nhlbi.nih.gov)"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_LDL_cholesterol_level evaluation function. The value is expected to be less than 100.0.'
    try:
        codes = ['13457-7', '2089-1', '18262-6']
        if data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique() > 0:
            data_in_range = data_df[(data_df['Code'].astype(str).isin(codes)) & (data_df['Value'] < 100.0)]['Patient'].nunique() / data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique()
            res = data_in_range > 0.95
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'expected_value': 100.0}
        if res == False:
            fail_exp = 'Serum_LDL_cholesterol_level evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_LDL_cholesterol_level.explanation = str(output_vals)
        return res

def dftest_Serum_triglycerides_level(data_df):
    #("American Heart Association (https://www.heart.org)", "National Cholesterol Education Program (https://www.nhlbi.nih.gov)")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_triglycerides_level evaluation function. 95% of the population is expected to be between 0.0 and 150.0.'
    try:
        codes = ['3043-7', '3044-5', '3045-2']
        if data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique() > 0:
            data_in_range = data_df[(data_df['Code'].astype(str).isin(codes)) & (data_df['Value'] >= 0.0) & (data_df['Value'] <= 150.0)]['Patient'].nunique() / data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 0.0, 'range_high': 150.0}
        if res == False:
            fail_exp = 'Serum_triglycerides_level evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_triglycerides_level.explanation = str(output_vals)
        return res

def dftest_Serum_potassium_level(data_df):
    #"(MedlinePlus: https://medlineplus.gov/lab-tests/potassium-blood-test/, Mayo Clinic: https://www.mayoclinic.org/tests-procedures/potassium-test/about/pac-20384923, LOINC: https://loinc.org)"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_potassium_level evaluation function. 95% of the population is expected to be between 3.5 and 5.1.'
    try:
        codes = ['17856-6', '2160-0', '2345-7']
        if data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique() > 0:
            data_in_range = data_df[(data_df['Code'].astype(str).isin(codes)) & (data_df['Value'] >= 3.5) & (data_df['Value'] <= 5.1)]['Patient'].nunique() / data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 3.5, 'range_high': 5.1}
        if res == False:
            fail_exp = 'Serum_potassium_level evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_potassium_level.explanation = str(output_vals)
        return res

def dftest_Serum_creatinine_level(data_df):
    #("Mayo Clinic: https://www.mayoclinic.org/tests-procedures/creatinine-test/about/pac-20384646", "NIH: https://medlineplus.gov/lab-tests/creatinine-test/")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_creatinine_level evaluation function. 95% of the population is expected to be between 0.6 and 1.2.'
    try:
        codes = ['2160-0', '2345-7', '2951-2']
        if data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique() > 0:
            data_in_range = data_df[(data_df['Code'].astype(str).isin(codes)) & (data_df['Value'] >= 0.6) & (data_df['Value'] <= 1.2)]['Patient'].nunique() / data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 0.6, 'range_high': 1.2}
        if res == False:
            fail_exp = 'Serum_creatinine_level evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_creatinine_level.explanation = str(output_vals)
        return res

def dftest_Serum_sodium_level(data_df):
    #("Mayo Clinic: https://www.mayoclinic.org/tests-procedures/sodium-test/about/pac-20384988", "Lab Tests Online: https://labtestsonline.org/tests/sodium-test")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_sodium_level evaluation function. 95% of the population is expected to be between 135.0 and 145.0.'
    try:
        codes = ['2951-2', '17856-6', '2160-0']
        if data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique() > 0:
            data_in_range = data_df[(data_df['Code'].astype(str).isin(codes)) & (data_df['Value'] >= 135.0) & (data_df['Value'] <= 145.0)]['Patient'].nunique() / data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 135.0, 'range_high': 145.0}
        if res == False:
            fail_exp = 'Serum_sodium_level evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_sodium_level.explanation = str(output_vals)
        return res

def dftest_Serum_calcium_level(data_df):
    #("Mayo Clinic: https://www.mayoclinic.org", "LabCorp: https://www.labcorp.com")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_calcium_level evaluation function. 95% of the population is expected to be between 8.5 and 10.2.'
    try:
        codes = ['2345-7', '2951-2', '17856-6']
        if data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique() > 0:
            data_in_range = data_df[(data_df['Code'].astype(str).isin(codes)) & (data_df['Value'] >= 8.5) & (data_df['Value'] <= 10.2)]['Patient'].nunique() / data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 8.5, 'range_high': 10.2}
        if res == False:
            fail_exp = 'Serum_calcium_level evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_calcium_level.explanation = str(output_vals)
        return res

def dftest_Serum_magnesium_level(data_df):
    #("Mayo Clinic: https://www.mayoclinic.org", "LabCorp: https://www.labcorp.com")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_magnesium_level evaluation function. 95% of the population is expected to be between 1.7 and 2.3.'
    try:
        codes = ['17856-6', '2160-0', '2345-7']
        if data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique() > 0:
            data_in_range = data_df[(data_df['Code'].astype(str).isin(codes)) & (data_df['Value'] >= 1.7) & (data_df['Value'] <= 2.3)]['Patient'].nunique() / data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 1.7, 'range_high': 2.3}
        if res == False:
            fail_exp = 'Serum_magnesium_level evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_magnesium_level.explanation = str(output_vals)
        return res

def dftest_Serum_chloride_level(data_df):
    #("Mayo Clinic: https://www.mayoclinic.org/tests-procedures/chloride-test/about/pac-20384900", "Lab Tests Online: https://labtestsonline.org/tests/chloride-test")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_chloride_level evaluation function. 95% of the population is expected to be between 98.0 and 106.0.'
    try:
        codes = ['2160-0', '2345-7', '2951-2']
        if data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique() > 0:
            data_in_range = data_df[(data_df['Code'].astype(str).isin(codes)) & (data_df['Value'] >= 98.0) & (data_df['Value'] <= 106.0)]['Patient'].nunique() / data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 98.0, 'range_high': 106.0}
        if res == False:
            fail_exp = 'Serum_chloride_level evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_chloride_level.explanation = str(output_vals)
        return res

def dftest_Serum_bicarbonate_level(data_df):
    #("Lab Tests Online: https://labtestsonline.org/tests/bicarbonate-test", "Mayo Clinic: https://www.mayoclinic.org/tests-procedures/co2-test/about/pac-20384901")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_bicarbonate_level evaluation function. 95% of the population is expected to be between 22.0 and 29.0.'
    try:
        codes = ['2951-2', '17856-6', '2160-0']
        if data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique() > 0:
            data_in_range = data_df[(data_df['Code'].astype(str).isin(codes)) & (data_df['Value'] >= 22.0) & (data_df['Value'] <= 29.0)]['Patient'].nunique() / data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 22.0, 'range_high': 29.0}
        if res == False:
            fail_exp = 'Serum_bicarbonate_level evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_bicarbonate_level.explanation = str(output_vals)
        return res

def dftest_Serum_urea_nitrogen_level(data_df):
    #("MedlinePlus: https://medlineplus.gov/lab-tests/blood-urea-nitrogen-bun-test/", "Mayo Clinic: https://www.mayoclinic.org/tests-procedures/blood-urea-nitrogen/about/pac-20384821")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_urea_nitrogen_level evaluation function. 95% of the population is expected to be between 7.0 and 20.0.'
    try:
        codes = ['2345-7', '2951-2', '17856-6']
        if data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique() > 0:
            data_in_range = data_df[(data_df['Code'].astype(str).isin(codes)) & (data_df['Value'] >= 7.0) & (data_df['Value'] <= 20.0)]['Patient'].nunique() / data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 7.0, 'range_high': 20.0}
        if res == False:
            fail_exp = 'Serum_urea_nitrogen_level evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_urea_nitrogen_level.explanation = str(output_vals)
        return res

def dftest_Serum_uric_acid_level(data_df):
    #("Mayo Clinic: https://www.mayoclinic.org", "Labcorp: https://www.labcorp.com")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_uric_acid_level evaluation function. 95% of the population is expected to be between 3.5 and 7.2.'
    try:
        codes = ['17856-6', '2160-0', '2345-7']
        if data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique() > 0:
            data_in_range = data_df[(data_df['Code'].astype(str).isin(codes)) & (data_df['Value'] >= 3.5) & (data_df['Value'] <= 7.2)]['Patient'].nunique() / data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 3.5, 'range_high': 7.2}
        if res == False:
            fail_exp = 'Serum_uric_acid_level evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_uric_acid_level.explanation = str(output_vals)
        return res

def dftest_Serum_total_protein_level(data_df):
    #("Mayo Clinic Reference Ranges: https://www.mayocliniclabs.com", "Labcorp Reference Ranges: https://www.labcorp.com")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_total_protein_level evaluation function. 95% of the population is expected to be between 6.0 and 8.3.'
    try:
        codes = ['2160-0', '2345-7', '2951-2']
        if data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique() > 0:
            data_in_range = data_df[(data_df['Code'].astype(str).isin(codes)) & (data_df['Value'] >= 6.0) & (data_df['Value'] <= 8.3)]['Patient'].nunique() / data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 6.0, 'range_high': 8.3}
        if res == False:
            fail_exp = 'Serum_total_protein_level evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_total_protein_level.explanation = str(output_vals)
        return res

def dftest_Serum_albumin_level(data_df):
    #("Mayo Clinic: https://www.mayoclinic.org/tests-procedures/albumin-test/about/pac-20384922", "LabCorp: https://www.labcorp.com/tests/001115/albumin-serum")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_albumin_level evaluation function. 95% of the population is expected to be between 3.5 and 5.0.'
    try:
        codes = ['2951-2', '17856-6', '2160-0']
        if data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique() > 0:
            data_in_range = data_df[(data_df['Code'].astype(str).isin(codes)) & (data_df['Value'] >= 3.5) & (data_df['Value'] <= 5.0)]['Patient'].nunique() / data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 3.5, 'range_high': 5.0}
        if res == False:
            fail_exp = 'Serum_albumin_level evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_albumin_level.explanation = str(output_vals)
        return res

def dftest_Serum_globulin_level(data_df):
    #("Mayo Clinic Laboratories: https://www.mayocliniclabs.com", "LabCorp: https://www.labcorp.com")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_globulin_level evaluation function. 95% of the population is expected to be between 2.0 and 3.5.'
    try:
        codes = ['2345-7', '2951-2', '17856-6']
        if data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique() > 0:
            data_in_range = data_df[(data_df['Code'].astype(str).isin(codes)) & (data_df['Value'] >= 2.0) & (data_df['Value'] <= 3.5)]['Patient'].nunique() / data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 2.0, 'range_high': 3.5}
        if res == False:
            fail_exp = 'Serum_globulin_level evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_globulin_level.explanation = str(output_vals)
        return res

def dftest_Serum_bilirubin_level(data_df):
    #("Mayo Clinic: https://www.mayoclinic.org", "LabCorp: https://www.labcorp.com")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_bilirubin_level evaluation function. 95% of the population is expected to be between 0.1 and 1.2.'
    try:
        codes = ['17856-6', '2160-0', '2345-7']
        if data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique() > 0:
            data_in_range = data_df[(data_df['Code'].astype(str).isin(codes)) & (data_df['Value'] >= 0.1) & (data_df['Value'] <= 1.2)]['Patient'].nunique() / data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 0.1, 'range_high': 1.2}
        if res == False:
            fail_exp = 'Serum_bilirubin_level evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_bilirubin_level.explanation = str(output_vals)
        return res

def dftest_Serum_alkaline_phosphatase_level(data_df):
    #("Mayo Clinic Reference Ranges: https://www.mayocliniclabs.com", "Labcorp Reference Ranges: https://www.labcorp.com")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_alkaline_phosphatase_level evaluation function. 95% of the population is expected to be between 44.0 and 147.0.'
    try:
        codes = ['2160-0', '2345-7', '2951-2']
        if data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique() > 0:
            data_in_range = data_df[(data_df['Code'].astype(str).isin(codes)) & (data_df['Value'] >= 44.0) & (data_df['Value'] <= 147.0)]['Patient'].nunique() / data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 44.0, 'range_high': 147.0}
        if res == False:
            fail_exp = 'Serum_alkaline_phosphatase_level evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_alkaline_phosphatase_level.explanation = str(output_vals)
        return res

def dftest_Serum_aspartate_aminotransferase_level(data_df):
    #("Mayo Clinic: https://www.mayoclinic.org/tests-procedures/liver-function-tests/about/pac-20385003", "Labcorp: https://www.labcorp.com/tests/2160-0-aspartate-aminotransferase-ast")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_aspartate_aminotransferase_level evaluation function. 95% of the population is expected to be between 8.0 and 40.0.'
    try:
        codes = ['2951-2', '17856-6', '2160-0']
        if data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique() > 0:
            data_in_range = data_df[(data_df['Code'].astype(str).isin(codes)) & (data_df['Value'] >= 8.0) & (data_df['Value'] <= 40.0)]['Patient'].nunique() / data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 8.0, 'range_high': 40.0}
        if res == False:
            fail_exp = 'Serum_aspartate_aminotransferase_level evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_aspartate_aminotransferase_level.explanation = str(output_vals)
        return res

def dftest_Serum_alanine_aminotransferase_level(data_df):
    #("Mayo Clinic: https://www.mayoclinic.org", "MedlinePlus: https://medlineplus.gov")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_alanine_aminotransferase_level evaluation function. 95% of the population is expected to be between 7.0 and 56.0.'
    try:
        codes = ['2345-7', '2951-2', '17856-6']
        if data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique() > 0:
            data_in_range = data_df[(data_df['Code'].astype(str).isin(codes)) & (data_df['Value'] >= 7.0) & (data_df['Value'] <= 56.0)]['Patient'].nunique() / data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 7.0, 'range_high': 56.0}
        if res == False:
            fail_exp = 'Serum_alanine_aminotransferase_level evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_alanine_aminotransferase_level.explanation = str(output_vals)
        return res

def dftest_Serum_gamma_glutamyl_transferase_level(data_df):
    #("Mayo Clinic Reference Ranges: https://www.mayocliniclabs.com", "Lab Tests Online Reference Ranges: https://labtestsonline.org")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_gamma_glutamyl_transferase_level evaluation function. 95% of the population is expected to be between 6.0 and 71.0.'
    try:
        codes = ['17856-6', '2160-0', '2345-7']
        if data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique() > 0:
            data_in_range = data_df[(data_df['Code'].astype(str).isin(codes)) & (data_df['Value'] >= 6.0) & (data_df['Value'] <= 71.0)]['Patient'].nunique() / data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 6.0, 'range_high': 71.0}
        if res == False:
            fail_exp = 'Serum_gamma_glutamyl_transferase_level evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_gamma_glutamyl_transferase_level.explanation = str(output_vals)
        return res

def dftest_Serum_lactate_dehydrogenase_level(data_df):
    #("Mayo Clinic Laboratories: https://www.mayocliniclabs.com", "LabCorp Reference Ranges: https://www.labcorp.com")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_lactate_dehydrogenase_level evaluation function. 95% of the population is expected to be between 105.0 and 333.0.'
    try:
        codes = ['2160-0', '2345-7', '2951-2']
        if data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique() > 0:
            data_in_range = data_df[(data_df['Code'].astype(str).isin(codes)) & (data_df['Value'] >= 105.0) & (data_df['Value'] <= 333.0)]['Patient'].nunique() / data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 105.0, 'range_high': 333.0}
        if res == False:
            fail_exp = 'Serum_lactate_dehydrogenase_level evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_lactate_dehydrogenase_level.explanation = str(output_vals)
        return res

def dftest_Serum_C_reactive_protein_level(data_df):
    #("Mayo Clinic: https://www.mayoclinic.org", "Labcorp: https://www.labcorp.com")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Serum_C_reactive_protein_level evaluation function. 95% of the population is expected to be between 0.0 and 3.0.'
    try:
        codes = ['2951-2', '17856-6', '2160-0']
        if data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique() > 0:
            data_in_range = data_df[(data_df['Code'].astype(str).isin(codes)) & (data_df['Value'] >= 0.0) & (data_df['Value'] <= 3.0)]['Patient'].nunique() / data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique()
            res = (0.9 <= (data_in_range / 0.95) <= 1.1)
        else:
            data_in_range = 0
            res = False

        output_vals = {'data_in_range': 100 * data_in_range, 'range_low': 0.0, 'range_high': 3.0}
        if res == False:
            fail_exp = 'Serum_C_reactive_protein_level evaluation in the examined data is ' + str(100 * data_in_range)
            explanation += ' ' + fail_exp

    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")

    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Serum_C_reactive_protein_level.explanation = str(output_vals)
        return res

