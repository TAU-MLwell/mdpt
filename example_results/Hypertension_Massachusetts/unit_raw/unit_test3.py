# Filename: unit_test3.py

def dftest_Medication_code_from_RxNorm_for_Lisinopril(data_df):
    #("https://clincalc.com/Drugstats/Drugs/Lisinopril")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Medication_code_from_RxNorm_for_Lisinopril treatment comparison function. Theoretical value is expected to be 25.'
    try:
        codes = ['OMOP5144214', 'OMOP5144239', 'OMOP5144188', 'OMOP682372', 'OMOP682373', 'OMOP682374']
        
        data_per = 100*data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique() / data_df['Patient'].nunique()
        val  = (data_per - 25) / np.sqrt((data_per*(100 - data_per)+25*(100 - 25))/2)
        ratio = data_per/25
        res = (abs(val) < 0.2) & (0.85<=ratio<=1.15)
        output_vals = {'data_per': data_per, 'expected_value': 25, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Medication_code_from_RxNorm_for_Lisinopril percentage in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
            
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
        
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Medication_code_from_RxNorm_for_Lisinopril.explanation = str(output_vals)
        return res

def dftest_Medication_code_from_RxNorm_for_Amlodipine(data_df):
    #"CDC Hypertension Statistics: https://www.cdc.gov/bloodpressure/facts.htm; NHANES Data on Hypertension and Medication Use: https://www.nhanes.gov"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Medication_code_from_RxNorm_for_Amlodipine treatment comparison function. Theoretical value is expected to be between 2.0 and 3.0.'
    try:
        codes = ['OMOP687086', 'OMOP710211', 'OMOP687046', 'OMOP205925', 'OMOP205926']
        data_per = 100*data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique() / data_df['Patient'].nunique()
        res = (2.0 <= data_per <= 3.0)
        output_vals = {'data_per': data_per, 'range_low': 2.0, 'range_high': 3.0}
        if res == False:
            fail_exp = 'Medication_code_from_RxNorm_for_Amlodipine evaluation in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
            
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
        
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Medication_code_from_RxNorm_for_Amlodipine.explanation = str(output_vals)
        return res

def dftest_Medication_code_from_RxNorm_for_Losartan(data_df):
    #("CDC Hypertension Statistics: https://www.cdc.gov/bloodpressure/facts.htm", "JAMA Study on Antihypertensive Prescriptions: https://jamanetwork.com")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Medication_code_from_RxNorm_for_Losartan treatment comparison function. Theoretical value is expected to be between 1.0 and 2.0.'
    try:
        codes = ['OMOP2494510', 'OMOP477163', 'OMOP4677491', 'OMOP4771632']
        data_per = 100*data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique() / data_df['Patient'].nunique()
        res = (1.0 <= data_per <= 2.0)
        output_vals = {'data_per': data_per, 'range_low': 1.0, 'range_high': 2.0}
        if res == False:
            fail_exp = 'Medication_code_from_RxNorm_for_Losartan evaluation in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
            
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
        
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Medication_code_from_RxNorm_for_Losartan.explanation = str(output_vals)
        return res

def dftest_Medication_code_from_RxNorm_for_Hydrochlorothiazide(data_df):
    #("https://www.cdc.gov/bloodpressure/medications.htm", "https://www.ahajournals.org/doi/10.1161/JAHA....")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Medication_code_from_RxNorm_for_Hydrochlorothiazide treatment comparison function. Theoretical value is expected to be between 30.0 and 40.0.'
    try:
        codes = ['OMOP407803', 'OMOP407808', 'OMOP407819', 'OMOP407776']
        data_per = 100*data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique() / data_df['Patient'].nunique()
        res = (30.0 <= data_per <= 40.0)
        output_vals = {'data_per': data_per, 'range_low': 30.0, 'range_high': 40.0}
        if res == False:
            fail_exp = 'Medication_code_from_RxNorm_for_Hydrochlorothiazide evaluation in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
            
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
        
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Medication_code_from_RxNorm_for_Hydrochlorothiazide.explanation = str(output_vals)
        return res

def dftest_Medication_code_from_RxNorm_for_Metoprolol(data_df):
    #"https://www.cdc.gov/bloodpressure/statistics.html"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Medication_code_from_RxNorm_for_Metoprolol treatment comparison function. Theoretical value is expected to be between 20.0 and 40.0.'
    try:
        codes = ['OMOP1100532', 'OMOP1022879', 'OMOP1087591', 'OMOP215001']
        data_per = 100*data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique() / data_df['Patient'].nunique()
        res = (20.0 <= data_per <= 40.0)
        output_vals = {'data_per': data_per, 'range_low': 20.0, 'range_high': 40.0}
        if res == False:
            fail_exp = 'Medication_code_from_RxNorm_for_Metoprolol evaluation in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
            
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
        
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Medication_code_from_RxNorm_for_Metoprolol.explanation = str(output_vals)
        return res

def dftest_Medication_code_from_RxNorm_for_Atenolol(data_df):
    #("https://www.cdc.gov/nchs/data/databriefs/db51", "https://www.ncbi.nlm.nih.gov/pubmed/")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Medication_code_from_RxNorm_for_Atenolol treatment comparison function. Theoretical value is expected to be between 25.0 and 32.3.'
    try:
        codes = ['OMOP406257', 'OMOP406268', 'OMOP2402962', 'OMOP230899']
        data_per = 100*data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique() / data_df['Patient'].nunique()
        res = (25.0 <= data_per <= 32.3)
        output_vals = {'data_per': data_per, 'range_low': 25.0, 'range_high': 32.3}
        if res == False:
            fail_exp = 'Medication_code_from_RxNorm_for_Atenolol evaluation in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
            
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
        
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Medication_code_from_RxNorm_for_Atenolol.explanation = str(output_vals)
        return res

def dftest_Medication_code_from_RxNorm_for_Valsartan(data_df):
    #("https://www.ahajournals.org/doi/10.1161/JAHA.120.016682", "https://pubmed.ncbi.nlm.nih.gov/")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Medication_code_from_RxNorm_for_Valsartan treatment comparison function. Theoretical value is expected to be between 10.0 and 12.0.'
    try:
        codes = ['OMOP693533', 'OMOP693440', 'OMOP693456', 'OMOP693691']
        data_per = 100*data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique() / data_df['Patient'].nunique()
        res = (10.0 <= data_per <= 12.0)
        output_vals = {'data_per': data_per, 'range_low': 10.0, 'range_high': 12.0}
        if res == False:
            fail_exp = 'Medication_code_from_RxNorm_for_Valsartan evaluation in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
            
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
        
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Medication_code_from_RxNorm_for_Valsartan.explanation = str(output_vals)
        return res

def dftest_Medication_code_from_RxNorm_for_Enalapril(data_df):
    #"CDC Hypertension Statistics (https://www.cdc.gov/bloodpressure/facts.htm), NIH ACE Inhibitor Usage (https://pubmed.ncbi.nlm.nih.gov/)"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Medication_code_from_RxNorm_for_Enalapril treatment comparison function. Theoretical value is expected to be between 1.0 and 3.0.'
    try:
        codes = ['OMOP2402244', 'OMOP2464046', 'OMOP2433165', 'OMOP230674']
        data_per = 100*data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique() / data_df['Patient'].nunique()
        res = (1.0 <= data_per <= 3.0)
        output_vals = {'data_per': data_per, 'range_low': 1.0, 'range_high': 3.0}
        if res == False:
            fail_exp = 'Medication_code_from_RxNorm_for_Enalapril evaluation in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
            
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
        
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Medication_code_from_RxNorm_for_Enalapril.explanation = str(output_vals)
        return res

def dftest_Medication_code_from_RxNorm_for_Carvedilol(data_df):
    #("https://www.statista.com/statistics/782166/ca...", "https://pubmed.ncbi.nlm.nih.gov/", "https://www.rxnorm.nlm.nih.gov/")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Medication_code_from_RxNorm_for_Carvedilol treatment comparison function. Theoretical value is expected to be between 1.0 and 3.0.'
    try:
        codes = ['OMOP1036662', 'OMOP4963242', 'OMOP1114316', 'OMOP4963243']
        data_per = 100*data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique() / data_df['Patient'].nunique()
        res = (1.0 <= data_per <= 3.0)
        output_vals = {'data_per': data_per, 'range_low': 1.0, 'range_high': 3.0}
        if res == False:
            fail_exp = 'Medication_code_from_RxNorm_for_Carvedilol evaluation in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
            
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
        
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Medication_code_from_RxNorm_for_Carvedilol.explanation = str(output_vals)
        return res

def dftest_Medication_code_from_RxNorm_for_Furosemide(data_df):
    #"https://pubmed.ncbi.nlm.nih.gov/12620696/, NHANES, CDC Hypertension Treatment Reports"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Medication_code_from_RxNorm_for_Furosemide treatment comparison function. Theoretical value is expected to be between 10.0 and 15.0.'
    try:
        codes = ['OMOP402924', 'OMOP402916', 'OMOP402669', 'OMOP240201']
        data_per = 100*data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique() / data_df['Patient'].nunique()
        res = (10.0 <= data_per <= 15.0)
        output_vals = {'data_per': data_per, 'range_low': 10.0, 'range_high': 15.0}
        if res == False:
            fail_exp = 'Medication_code_from_RxNorm_for_Furosemide evaluation in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
            
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
        
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Medication_code_from_RxNorm_for_Furosemide.explanation = str(output_vals)
        return res

def dftest_Medication_code_from_RxNorm_for_Clonidine(data_df):
    #("CDC Hypertension Guidelines: https://www.cdc.gov/bloodpressure/management.htm", "RxNorm Database: https://www.nlm.nih.gov/research/umls/rxnorm/")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Medication_code_from_RxNorm_for_Clonidine treatment comparison function. Theoretical value is expected to be less than 1.'
    try:
        codes = ['OMOP2058715', 'OMOP2152211', 'OMOP1114186', 'OMOP106258']
        
        data_per = 100*data_df[data_df['Code'].astype(str).isin(codes)]['Patient'].nunique() / data_df['Patient'].nunique()
        res = (data_per <= 1.0)
        output_vals = {'data_per': data_per, 'expected_value': '<1.0'}
        if res == False:
            fail_exp = 'Medication_code_from_RxNorm_for_Clonidine evaluation in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
            
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
        
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Medication_code_from_RxNorm_for_Clonidine.explanation = str(output_vals)
        return res

