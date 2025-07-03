# Filename: unit_test3.py

def dftest_A_foreign_key_to_a_standard_concept_identifier_for_Lisinopril(data_df):
    #("FDA Drug Label for Lisinopril: https://www.accessdata.fda.gov/drugsatfda_docs/label/2019/019777s078lbl.pdf", "ACE inhibitor-induced cough: A review of the literature, Journal of Clinical Pharmacology, 2010")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'A_foreign_key_to_a_standard_concept_identifier_for_Lisinopril treatment comparison function. Theoretical value is expected to be between 5.0 and 20.0.'
    try:
        codes = ['OMOP5144214', 'OMOP5144239', 'OMOP499160', 'OMOP9930']
        data_per = 100 * data_df[data_df['drug_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / data_df['person_id'].nunique()
        res = (5.0 <= data_per <= 20.0)
        output_vals = {'data_per': data_per, 'range_low': 5.0, 'range_high': 20.0}
        if res == False:
            fail_exp = 'A_foreign_key_to_a_standard_concept_identifier_for_Lisinopril evaluation in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_to_a_standard_concept_identifier_for_Lisinopril.explanation = str(output_vals)
        return res

def dftest_A_foreign_key_to_a_standard_concept_identifier_for_Amlodipine(data_df):
    #"https://jamanetwork.com/journals/jamanetworkopen/fullarticle/2767936"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'A_foreign_key_to_a_standard_concept_identifier_for_Amlodipine treatment comparison function. Theoretical value is expected to be 11.2.'
    try:
        codes = ['OMOP2059251', 'OMOP2183925', 'OMOP687181', 'OMOP2059']
        data_per = 100 * data_df[data_df['drug_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / data_df['person_id'].nunique()
        val  = (data_per - 11.2) / np.sqrt((data_per * (100 - data_per) + 11.2 * (100 - 11.2)) / 2)
        ratio = data_per / 11.2
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 11.2, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'A_foreign_key_to_a_standard_concept_identifier_for_Amlodipine percentage in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_to_a_standard_concept_identifier_for_Amlodipine.explanation = str(output_vals)
        return res

def dftest_A_foreign_key_to_a_standard_concept_identifier_for_Metoprolol(data_df):
    #"American Heart Association (https://www.heart.org), NIH (https://www.nih.gov)"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'A_foreign_key_to_a_standard_concept_identifier_for_Metoprolol treatment comparison function. Theoretical value is expected to be between 5.0 and 10.0.'
    try:
        codes = ['OMOP954341', 'OMOP954342', 'OMOP954136', 'OMOP954059']
        data_per = 100 * data_df[data_df['drug_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / data_df['person_id'].nunique()
        res = (5.0 <= data_per <= 10.0)
        output_vals = {'data_per': data_per, 'range_low': 5.0, 'range_high': 10.0}
        if res == False:
            fail_exp = 'A_foreign_key_to_a_standard_concept_identifier_for_Metoprolol evaluation in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_to_a_standard_concept_identifier_for_Metoprolol.explanation = str(output_vals)
        return res

def dftest_A_foreign_key_to_a_standard_concept_identifier_for_Furosemide(data_df):
    #"NCBI (https://pubmed.ncbi.nlm.nih.gov/), CDC (https://www.cdc.gov/)"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'A_foreign_key_to_a_standard_concept_identifier_for_Furosemide treatment comparison function. Theoretical value is expected to be between 1.0 and 2.0.'
    try:
        codes = ['OMOP402924', 'OMOP2308035', 'OMOP2308031', 'OMOP402939', 'OMOP402916', 'OMOP402669', 'OMOP4797056', 'OMOP2463847', 'OMOP2306003', 'OMOP402888', 'OMOP2402017', 'OMOP808497', 'OMOP402679', 'OMOP402852', 'OMOP402925', 'OMOP402847', 'OMOP402694', 'OMOP4983135', 'OMOP402894', 'OMOP2279946', 'OMOP2024937', 'OMOP402941', 'OMOP402747', 'OMOP2182857', 'OMOP402858', 'OMOP402917', 'OMOP402931', 'OMOP2087500', 'OMOP402960', 'OMOP1100838', 'OMOP808093', 'OMOP402701', 'OMOP2245254', 'OMOP2151692', 'OMOP2370500', 'OMOP402670', 'OMOP2308036', 'OMOP402696', 'OMOP5039239', 'OMOP2186220', 'OMOP402853', 'OMOP402848', 'OMOP2463846', 'OMOP2463850', 'OMOP2151691', 'OMOP2189990', 'OMOP2370502', 'OMOP2494918', 'OMOP2339404', 'OMOP2182856', 'OMOP4817479', 'OMOP402889', 'OMOP2463848', 'OMOP402680', 'OMOP807885', 'OMOP807835', 'OMOP807011', 'OMOP2213974', 'OMOP996360', 'OMOP444250', 'OMOP2151694', 'OMOP2494922', 'OMOP4786952', 'OMOP809135', 'OMOP2182855', 'OMOP402842', 'OMOP2026963', 'OMOP402690', 'OMOP5039240', 'OMOP2058247', 'OMOP444254', 'OMOP402862', 'OMOP2308033', 'OMOP2182854', 'OMOP2433001', 'OMOP402895', 'OMOP808224', 'OMOP2433000', 'OMOP2339407', 'OMOP402742', 'OMOP808442', 'OMOP2308034', 'OMOP2370501', 'OMOP806859', 'OMOP2276639', 'OMOP807260', 'OMOP444295', 'OMOP402748', 'OMOP4812991', 'OMOP402684', 'OMOP402952', 'OMOP402935', 'OMOP808508', 'OMOP4811954', 'OMOP444299', 'OMOP2511712', 'OMOP444228', 'OMOP2106006', 'OMOP2463851', 'OMOP4787167', 'OMOP2106010', 'OMOP2342760', 'OMOP4983134', 'OMOP1103335']
        data_per = 100 * data_df[data_df['drug_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / data_df['person_id'].nunique()
        res = (1.0 <= data_per <= 2.0)
        output_vals = {'data_per': data_per, 'range_low': 1.0, 'range_high': 2.0}
        if res == False:
            fail_exp = 'A_foreign_key_to_a_standard_concept_identifier_for_Furosemide evaluation in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_to_a_standard_concept_identifier_for_Furosemide.explanation = str(output_vals)
        return res

def dftest_A_foreign_key_to_a_standard_concept_identifier_for_Erythropoietin(data_df):
    #"National Kidney Foundation: https://www.kidney.org; PubMed: https://pubmed.ncbi.nlm.nih.gov; CDC Chronic Kidney Disease Statistics: https://www.cdc.gov/ckd"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'A_foreign_key_to_a_standard_concept_identifier_for_Erythropoietin treatment comparison function. Theoretical value is expected to be between 20.0 and 30.0.'
    try:
        codes = ['4306138', '43009086', '40561484', '2066937', '604277', '2066885', '42959946', '42959948', '42959947', '2066900', '2066921', '2066895', '42959938', '42959980', '2066932', '42959961', '2066933', '42959986', '42959969', '42959965', '42959984', '2066880', '2066935', '42959934', '2066881', '42959983', '42959985', '42959964', '42959982', '40527799', '2066917', '42959963', '2066915', '2066936', '42959981', '42959967', '42959962', '42959939', '42959968', '2066934', '2066883', '2066916', '2066884', '4009497', '2066882', '2066919', '2066899', '2066920', '2066931', '42959935', '2066918', '2066894', '41110257', '36878928', '604278', '42959943', '40860464', '42959945']
        data_per = 100 * data_df[data_df['drug_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / data_df['person_id'].nunique()
        res = (20.0 <= data_per <= 30.0)
        output_vals = {'data_per': data_per, 'range_low': 20.0, 'range_high': 30.0}
        if res == False:
            fail_exp = 'A_foreign_key_to_a_standard_concept_identifier_for_Erythropoietin evaluation in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_to_a_standard_concept_identifier_for_Erythropoietin.explanation = str(output_vals)
        return res

def dftest_A_foreign_key_to_a_standard_concept_identifier_for_Calcitriol(data_df):
    #"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'A_foreign_key_to_a_standard_concept_identifier_for_Calcitriol treatment comparison function. Theoretical value is expected to be between 10.0 and 20.0.'
    try:
        codes = ['4123687', '21139618', '44042131', '44168167', '2011210', '43029029', '2044573', '35159369', '2044579', '43838325', '43712167', '43856338', '41016718', '43802104', '43766093', '41204818', '41016716', '41142241', '42958487', '43694342', '43820235', '43784233', '41016717', '40802694', '40551700', '35144076', '40551699', '21159410', '2913496', '40802695', '2044575', '2044577', '43564652', '40549825', '35149488', '43265859', '40802693', '42958489', '43730199', '44097785', '2044568', '2044569', '43029030', '44030093', '43564654', '43622194', '21600819', '42958486', '43271347', '4203232', '35156017', '35197846', '2044574', '36881139', '21080721', '36884938', '2044567', '35129833', '4131903', '2044570', '43564655', '42958488', '43255082', '4195394', '35147954', '41173278', '41110787', '35140880', '35136517', '2044576', '43676545', '2044571', '21100401', '21129715', '43676542', '21110211', '43564653', '2044566', '35136781', '44025874', '35142535', '44164442', '4203224', '35149691', '42958496', '42479056', '35142277', '41266652', '42958493', '35140869', '4235684', '21149477', '2044572', '43260429', '36677581', '21602040', '41048032', '43622189', '36681037', '41019902', '41079403', '35145484', '2011211', '35139643', '42958492', '40554657', '43640350', '35150785', '2044556', '2011208', '43820231', '43564651', '35141809', '35139950', '36963335', '40556095', '40973586', '43694340', '35155654', '4236617', '4210657', '40860984', '2044588', '42958482', '40570380', '43730197', '43838327', '43640348', '43586136', '35130310', '42958485', '43730200', '35156987', '43640349', '36681038', '43640351', '42482038', '35141742', '43029033', '43766092']
        data_per = 100 * data_df[data_df['drug_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / data_df['person_id'].nunique()
        res = (10.0 <= data_per <= 20.0)
        output_vals = {'data_per': data_per, 'range_low': 10.0, 'range_high': 20.0}
        if res == False:
            fail_exp = 'A_foreign_key_to_a_standard_concept_identifier_for_Calcitriol evaluation in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_to_a_standard_concept_identifier_for_Calcitriol.explanation = str(output_vals)
        return res

def dftest_A_foreign_key_to_a_standard_concept_identifier_for_Cinacalcet(data_df):
    #"https://pubmed.ncbi.nlm.nih.gov/PMC6577"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'A_foreign_key_to_a_standard_concept_identifier_for_Cinacalcet treatment comparison function. Theoretical value is expected to be between 20.0 and 30.0.'
    try:
        codes = ['OMOP5164046', 'OMOP5164048', 'OMOP4835486', 'OMOP481']
        data_per = 100 * data_df[data_df['drug_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / data_df['person_id'].nunique()
        res = (20.0 <= data_per <= 30.0)
        output_vals = {'data_per': data_per, 'range_low': 20.0, 'range_high': 30.0}
        if res == False:
            fail_exp = 'A_foreign_key_to_a_standard_concept_identifier_for_Cinacalcet evaluation in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_to_a_standard_concept_identifier_for_Cinacalcet.explanation = str(output_vals)
        return res

