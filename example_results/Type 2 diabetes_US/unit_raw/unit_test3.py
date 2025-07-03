# Filename: unit_test3.py

def dftest_A_foreign_key_to_a_standard_concept_identifier_for_the_drug_concept_1(data_df):
    #("CDC, National Center for Health Statistics, Prescription Drug Use Data (2019-2020)", "https://www.cdc.gov/nchs/fastats/drug-use.htm")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'A_foreign_key_to_a_standard_concept_identifier_for_the_drug_concept_ treatment comparison function. Theoretical value is expected to be 48.6.'
    try:
        codes = ['372567009', '351440', '1077295', '4958904', '937185', '2061072', '351435', '4958891', '937377', '2279494', '473514', '2401510', '4669741', '2120032', '2213513', '937199', '2342329', '4958905', '1061969', '5159401', '4958902', '2338892', '2029857', '2310714', '351402', '937390', '351021', '937493', '2151178', '4958888', '2463317', '5137843', '2149304', '2033200', '937381', '937503', '538016', '992512', '4669792', '2307558', '2463316', '4669825', '2432506', '2404841', '2185769', '2401504', '2026456', '538120', '351024', '937246', '473511', '1077294', '937257', '4958919', '937180', '937207', '937410', '2244734', '5138014', '2057719', '4681012', '4669791', '538128', '4958895', '4669730', '2088991', '937417', '2120031', '2338891', '2432508']
        
        data_per = 100 * data_df[data_df['drug_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / data_df['person_id'].nunique()
        val = (data_per - 48.6) / np.sqrt((data_per * (100 - data_per) + 48.6 * (100 - 48.6)) / 2)
        ratio = data_per / 48.6
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 48.6, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'A_foreign_key_to_a_standard_concept_identifier_for_the_drug_concept_ percentage in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
            
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
        
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_to_a_standard_concept_identifier_for_the_drug_concept_1.explanation = str(output_vals)
        return res

def dftest_A_foreign_key_to_a_standard_concept_identifier_for_the_drug_concept_2(data_df):
    #"CDC Diabetes Statistics (https://www.cdc.gov/diabetes/data/statistics-report/index.html); American Diabetes Association (https://diabetes.org)"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'A_foreign_key_to_a_standard_concept_identifier_for_the_drug_concept_ treatment comparison function. Theoretical value is expected to be between 3.0 and 5.0.'
    try:
        codes = ['OMOP4816916', 'OMOP4816020', 'OMOP4799699', 'OMOP4798813', 'OMOP4737144', 'OMOP4737145', 'OMOP4813663', 'OMOP4797243', 'OMOP4813717', 'OMOP4812901', 'OMOP4798762', 'OMOP2273865', 'OMOP5197605', 'OMOP5197609', 'OMOP5197606', 'OMOP4737140', 'OMOP5197610', 'OMOP4794795', 'OMOP5197575', 'OMOP5197476', 'OMOP4818682', 'OMOP5019550', 'OMOP5197523', 'OMOP5197576', 'OMOP5034089', 'OMOP5197524', 'OMOP5197607', 'OMOP5197477', 'OMOP448230', 'OMOP5034096', 'OMOP2281773', 'OMOP2437995', 'OMOP4737146', 'OMOP5197592', 'OMOP262366', 'OMOP262398', 'OMOP448229', 'OMOP5197573', 'OMOP5197577', 'OMOP4805512', 'OMOP5034097', 'OMOP5197525', 'OMOP448242', 'OMOP5019549', 'OMOP2150571', 'OMOP5197478', 'OMOP5197611', 'OMOP4737141', 'OMOP4988921', 'OMOP5034088', 'OMOP5197474', 'OMOP4988941', 'OMOP5197521', 'OMOP4988931', 'OMOP4988940', 'OMOP5034095', 'OMOP4988930', 'OMOP262365', 'OMOP4737142', 'OMOP4988920', 'OMOP262388', 'OMOP5197533', 'OMOP262371', 'OMOP5197574', 'OMOP262397', 'OMOP5197585', 'OMOP5197486', 'OMOP262373', 'OMOP5197547', 'OMOP5197475', 'OMOP2312991', 'OMOP4988919', 'OMOP2064342', 'OMOP2185240', 'OMOP5034087', 'OMOP2063300', 'OMOP5197496', 'OMOP5197594', 'OMOP5197597', 'OMOP1030786', 'OMOP4988929', 'OMOP4988939', 'OMOP262372', 'OMOP5197534', 'OMOP5197487', 'OMOP1030785', 'OMOP4988938', 'OMOP4988928', 'OMOP448232', 'OMOP5197522', 'OMOP2162785', 'OMOP1069661', 'OMOP5197548', 'OMOP4770239', 'OMOP988910']
        data_per = 100 * data_df[data_df['drug_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / data_df['person_id'].nunique()
        res = (3.0 <= data_per <= 5.0)
        output_vals = {'data_per': data_per, 'range_low': 3.0, 'range_high': 5.0}
        if res == False:
            fail_exp = 'A_foreign_key_to_a_standard_concept_identifier_for_the_drug_concept_ evaluation in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
            
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
        
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_to_a_standard_concept_identifier_for_the_drug_concept_2.explanation = str(output_vals)
        return res

def dftest_A_foreign_key_to_a_standard_concept_identifier_for_the_drug_concept_3(data_df):
    #"CDC National Center for Health Statistics (NCHS): Prescription Drug Use (https://www.cdc.gov/nchs/fastats/drug-use-therapeutic.htm)"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'A_foreign_key_to_a_standard_concept_identifier_for_the_drug_concept_ treatment comparison function. Theoretical value is expected to be less than nan.'
    try:
        codes = ['41015022', '41013449', '40902685', '41209149', '40479734', '37204645', '40482823', '37204646', '42539424', '21600786', '2036050', '21164301', '40749314', '2036051', '36682850', '35625834', '35745885', '43158075', '21105328', '35849793', '21174081', '41302043', '40479756', '43212818', '40834305', '40990121', '41121372', '40996389', '21144561', '21066043', '40933872', '40871653', '21085706', '43158073', '1588688', '43158074', '21105327', '41021095', '35753965', '21115147', '36680081', '41226695', '41038882', '21154487', '21134672', '40749313', '21066044', '40851956', '43168956', '40933873', '43212819', '40479733', '40865407', '41021096', '21105325', '35742520', '21105326', '43168955', '44170664', '41038881', '21164302', '40965071', '40883230', '35758094', '40883228', '41210094', '43135949', '42482588', '35754276', '40491983', '40491982', '40491949', '21130192', '44109980', '40251676', '1243715', '42482589', '41164309', '21159926', '21100924', '37205011', '41203539', '1243768', '37205012', '1242241', '21085707', '41241078', '1243767', '40491948', '21100923', '21075986', '36264758', '35759225', '21169720', '41015546', '44092977', '43272772', '21140127', '43272770', '36259600', '43272771', '43267272', '41271886', '1243766', '36891677', '41271885', '36886571', '35750879', '44163148', '37205009', '21140126', '21120433', '41022059', '3654289', '1245397', '40843546', '1245396', '43267270', '37205010', '43146866', '40835234', '43294440', '2926939', '3654290', '40883229', '43146865', '40749312', '35775102', '40874760', '35763002', '36789352', '36260222', '36789355', '40874761', '21110742', '43146477', '40936968', '36272986', '2057410', '37312784']
        
        data_per = 100 * data_df[data_df['drug_concept_id'].astype(str).isin(codes)]['person_id'].nunique() / data_df['person_id'].nunique()
        res = data_per <= 48.6
        output_vals = {'data_per': data_per, 'expected_value': 48.6}
        if res == False:
            fail_exp = 'A_foreign_key_to_a_standard_concept_identifier_for_the_drug_concept_ evaluation in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
            
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
        
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_A_foreign_key_to_a_standard_concept_identifier_for_the_drug_concept_3.explanation = str(output_vals)
        return res

