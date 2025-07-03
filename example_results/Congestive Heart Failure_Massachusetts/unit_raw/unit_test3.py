# Filename: unit_test3.py

def dftest_Lisinopril(data_df):
    #("American Heart Association (AHA): https://www.ahajournals.org/", "National Center for Biotechnology Information (NCBI): https://pubmed.ncbi.nlm.nih.gov/")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Lisinopril treatment comparison function. Theoretical value is expected to be between 25.0 and 30.0.'
    try:
        codes = ['OMOP5144214', 'OMOP5144239', 'OMOP5144188', 'OMOP682007', 'OMOP682008']
        data_per = 100 * data_df[data_df['formulary_drug_cd'].astype(str).isin(codes)]['subject_id'].nunique() / data_df['subject_id'].nunique()
        res = (25.0 <= data_per <= 30.0)
        output_vals = {'data_per': data_per, 'range_low': 25.0, 'range_high': 30.0}
        if res == False:
            fail_exp = 'Lisinopril evaluation in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Lisinopril.explanation = str(output_vals)
        return res

def dftest_Carvedilol(data_df):
    #("https://pubmed.ncbi.nlm.nih.gov/39969604/", "https://www.ahajournals.org")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Carvedilol treatment comparison function. Theoretical value is expected to be between 10.0 and 15.0.'
    try:
        codes = ['OMOP4963242', 'OMOP673567', 'OMOP1036662', 'OMOP4963243']
        data_per = 100 * data_df[data_df['formulary_drug_cd'].astype(str).isin(codes)]['subject_id'].nunique() / data_df['subject_id'].nunique()
        res = (10.0 <= data_per <= 15.0)
        output_vals = {'data_per': data_per, 'range_low': 10.0, 'range_high': 15.0}
        if res == False:
            fail_exp = 'Carvedilol evaluation in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Carvedilol.explanation = str(output_vals)
        return res

def dftest_Furosemide(data_df):
    #"https://pubmed.ncbi.nlm.nih.gov/, https://www.heart.org/"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Furosemide treatment comparison function. Theoretical value is expected to be between 80.0 and 90.0.'
    try:
        codes = ['OMOP402924', 'OMOP402916', 'OMOP402669', 'OMOP402939']
        data_per = 100 * data_df[data_df['formulary_drug_cd'].astype(str).isin(codes)]['subject_id'].nunique() / data_df['subject_id'].nunique()
        res = (80.0 <= data_per <= 90.0)
        output_vals = {'data_per': data_per, 'range_low': 80.0, 'range_high': 90.0}
        if res == False:
            fail_exp = 'Furosemide evaluation in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Furosemide.explanation = str(output_vals)
        return res

def dftest_Spironolactone(data_df):
    #"https://pubmed.ncbi.nlm.nih.gov/31951680/"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Spironolactone treatment comparison function. Theoretical value is expected to be between 30.0 and 35.0.'
    try:
        codes = ['OMOP2306915', 'OMOP2431903', 'OMOP2306917', 'OMOP310885']
        data_per = 100 * data_df[data_df['formulary_drug_cd'].astype(str).isin(codes)]['subject_id'].nunique() / data_df['subject_id'].nunique()
        res = (30.0 <= data_per <= 35.0)
        output_vals = {'data_per': data_per, 'range_low': 30.0, 'range_high': 35.0}
        if res == False:
            fail_exp = 'Spironolactone evaluation in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Spironolactone.explanation = str(output_vals)
        return res

def dftest_Digoxin(data_df):
    #"https://www.jacc.org, https://pmc.ncbi.nlm.nih.gov/articles/PMC9716..."
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Digoxin treatment comparison function. Theoretical value is expected to be between 1.0 and 2.0.'
    try:
        codes = ['OMOP4810774', 'OMOP4808566', 'OMOP4797715', 'OMOP426290']
        data_per = 100 * data_df[data_df['formulary_drug_cd'].astype(str).isin(codes)]['subject_id'].nunique() / data_df['subject_id'].nunique()
        res = (1.0 <= data_per <= 2.0)
        output_vals = {'data_per': data_per, 'range_low': 1.0, 'range_high': 2.0}
        if res == False:
            fail_exp = 'Digoxin evaluation in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Digoxin.explanation = str(output_vals)
        return res

def dftest_Valsartan(data_df):
    #"https://jamanetwork.com/journals/jama/article-abstract/2767933"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Valsartan treatment comparison function. Theoretical value is expected to be between 5.0 and 10.0.'
    try:
        codes = ['OMOP4660125', 'OMOP4660077', 'OMOP4660015', 'OMOP4660016']
        data_per = 100 * data_df[data_df['formulary_drug_cd'].astype(str).isin(codes)]['subject_id'].nunique() / data_df['subject_id'].nunique()
        res = (5.0 <= data_per <= 10.0)
        output_vals = {'data_per': data_per, 'range_low': 5.0, 'range_high': 10.0}
        if res == False:
            fail_exp = 'Valsartan evaluation in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Valsartan.explanation = str(output_vals)
        return res

def dftest_Sacubitril_Valsartan(data_df):
    #"American Heart Association (https://www.ahajournals.org/doi/10.1161/CIRCH.2021), CDC (https://www.cdc.gov/heartfailure/facts.htm)"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Sacubitril_Valsartan treatment comparison function. Theoretical value is expected to be between 13.0 and 15.0.'
    try:
        codes = ['OMOP514883', 'OMOP514772', 'OMOP514742', 'OMOP344647']
        data_per = 100 * data_df[data_df['formulary_drug_cd'].astype(str).isin(codes)]['subject_id'].nunique() / data_df['subject_id'].nunique()
        res = (13.0 <= data_per <= 15.0)
        output_vals = {'data_per': data_per, 'range_low': 13.0, 'range_high': 15.0}
        if res == False:
            fail_exp = 'Sacubitril_Valsartan evaluation in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Sacubitril_Valsartan.explanation = str(output_vals)
        return res

def dftest_Bisoprolol(data_df):
    #("American Heart Association (AHA)", "PubMed articles on Bisoprolol prescription prevalence in CHF patients globally")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Bisoprolol treatment comparison function. Theoretical value is expected to be between 20.0 and 25.0.'
    try:
        codes = ['OMOP677039', 'OMOP677156', 'OMOP1114451', 'OMOP482159']
        data_per = 100 * data_df[data_df['formulary_drug_cd'].astype(str).isin(codes)]['subject_id'].nunique() / data_df['subject_id'].nunique()
        res = (20.0 <= data_per <= 25.0)
        output_vals = {'data_per': data_per, 'range_low': 20.0, 'range_high': 25.0}
        if res == False:
            fail_exp = 'Bisoprolol evaluation in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Bisoprolol.explanation = str(output_vals)
        return res

def dftest_Ivabradine(data_df):
    #("JACC: https://www.jacc.org/doi/full/10.1016/j.jacc.2020.01.045", "PubMed: https://pubmed.ncbi.nlm.nih.gov/")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Ivabradine treatment comparison function. Theoretical value is expected to be between 1.0 and 2.0.'
    try:
        codes = ['OMOP4782017', 'OMOP4711986', 'OMOP4782005', 'OMOP4782006']
        data_per = 100 * data_df[data_df['formulary_drug_cd'].astype(str).isin(codes)]['subject_id'].nunique() / data_df['subject_id'].nunique()
        res = (1.0 <= data_per <= 2.0)
        output_vals = {'data_per': data_per, 'range_low': 1.0, 'range_high': 2.0}
        if res == False:
            fail_exp = 'Ivabradine evaluation in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Ivabradine.explanation = str(output_vals)
        return res

def dftest_Eplerenone(data_df):
    #"https://www.jacc.org/doi/full/10.1016/j.jacc.2020.03.012"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Eplerenone treatment comparison function. Theoretical value is expected to be between 10.0 and 15.0.'
    try:
        codes = ['OMOP702692', 'OMOP702693', 'OMOP702657', 'OMOP702656']
        data_per = 100 * data_df[data_df['formulary_drug_cd'].astype(str).isin(codes)]['subject_id'].nunique() / data_df['subject_id'].nunique()
        res = (10.0 <= data_per <= 15.0)
        output_vals = {'data_per': data_per, 'range_low': 10.0, 'range_high': 15.0}
        if res == False:
            fail_exp = 'Eplerenone evaluation in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Eplerenone.explanation = str(output_vals)
        return res

def dftest_Torsemide(data_df):
    #("National Center for Biotechnology Information, NCBI - https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8887...")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Torsemide treatment comparison function. Theoretical value is expected to be between 1.0 and 2.0.'
    try:
        codes = ['OMOP2119248', 'OMOP2056968', 'OMOP4685321', 'OMOP2338862']
        data_per = 100 * data_df[data_df['formulary_drug_cd'].astype(str).isin(codes)]['subject_id'].nunique() / data_df['subject_id'].nunique()
        res = (1.0 <= data_per <= 2.0)
        output_vals = {'data_per': data_per, 'range_low': 1.0, 'range_high': 2.0}
        if res == False:
            fail_exp = 'Torsemide evaluation in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally: 
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Torsemide.explanation = str(output_vals)
        return res

