## Filename: unit_test0.py

import pandas as pd
import numpy as np
import math
from scipy.special import stdtr

def dftest_check_data_types(data_df):
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Datatype checking function for each column in the dataframe.'
    try:
        dtype_df = pd.DataFrame(columns=data_df.columns)
        dtype_df.loc[0] = 0
        # Check if there is a single datatype in esach column
        for col in data_df.columns:
            unique_dtypes = data_df[col].apply(type).unique()
            dtype_df.loc[:,col] = len(unique_dtypes)
        
        mixed_cols = dtype_df[dtype_df>1].dropna(axis=1).columns
        res = len(mixed_cols) == 0
        output_vals['mixed_cols'] = list(mixed_cols.values)
        if res == False:
            fail_exp = 'There are multiple data types in the following columns: ' + ', '.join(str(p) for p in dtype_df[mixed_cols])
            explanation += ' ' + fail_exp
            
    except Exception as e:
        res = False
        test_flag = 'error'
        explanation += ' ' + str(e)
        
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_check_data_types.explanation = str(output_vals)
        return res

def dftest_check_incidence(data_df):
    # ref: ['("CDC: https://www.cdc.gov/bloodpressure/facts.htm", "American Heart Association: https://www.heart.org/en/news/2023", "U.S. Census Bureau: https://www.census.gov/")']
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Five year mean incidence comparison function (2016-2021). Theoretical value is expected to be nan.'
    try:
        # Diagnosis codes for Hypertension
        diagnosis_codes = ['38341003', '266287006', '56218007', '194756002', '155295004', '64715009', '827069000', '449759005', '194760004', '429457004', '155297007', '827068008', '194759009', '194794002', '471521000000108', '155302005', '195537001', '473392002', '367390009', '599341000000105', '32966004', '194757006', '702817009', '194769003', '155299005', '46113002', '48146000', '137753003', '194776008', '86234004', '194788005', '194772005', '762463000', '845891000000103', '38481006', '60899001', '194791005', '194782006', '132721000119104', '10725009']
        # Initialize an empty list to store incidence rates
        incidence = []
        # Loop through the years 2016 to 2021
        for i in range(0, 6):
            year = 2016 + i
            # Filter the dataframe for the specific year
            df_year = data_df[data_df['Start'].dt.year == year]
            # Calculate the incidence rate for the year
            incidence_rate = 100*df_year[df_year['Code'].astype(str).isin(diagnosis_codes)]['Patient'].nunique() / data_df['Patient'].nunique()
            # Append the incidence rate to the list
            incidence.append(incidence_rate)
        # Calculate the mean incidence rate
        mean_incidence = np.mean(incidence)
        expected_incidence = np.nan
        val  = (mean_incidence - expected_incidence) / np.sqrt((mean_incidence*(100 - mean_incidence)+expected_incidence*(100 - expected_incidence))/2)
        ratio = mean_incidence/expected_incidence
        res = (abs(val) < 0.2) & (0.85<=ratio<=1.15)
        output_vals['ratio'] = ratio
        output_vals['smd'] = val
        output_vals['expected_value'] = expected_incidence
        output_vals['data_per'] = mean_incidence 
        if res == False:
            fail_exp = 'mean incidence in the examined data is ' + str(mean_incidence)
            explanation += ' ' + fail_exp
            
    except Exception as e:
        res = False
        test_flag = 'error'
        explanation += ' ' + str(e)
        
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_check_incidence.explanation = str(output_vals)
        return res

def dftest_check_prevalence(data_df):
    # ref: ['("CDC: https://www.cdc.gov/bloodpressure/facts.htm", "American Heart Association: https://www.heart.org/en/news/2023", "U.S. Census Bureau: https://www.census.gov/")']
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Prevalence comparison function. Theoretical value is expected to be 47.'
    try:
        # Diagnosis codes for Hypertension
        diagnosis_codes = ['38341003', '266287006', '56218007', '194756002', '155295004', '64715009', '827069000', '449759005', '194760004', '429457004', '155297007', '827068008', '194759009', '194794002', '471521000000108', '155302005', '195537001', '473392002', '367390009', '599341000000105', '32966004', '194757006', '702817009', '194769003', '155299005', '46113002', '48146000', '137753003', '194776008', '86234004', '194788005', '194772005', '762463000', '845891000000103', '38481006', '60899001', '194791005', '194782006', '132721000119104', '10725009']
        # Calculate the prevalence of Hypertension
        prevalence = 100*data_df[data_df['Code'].astype(str).isin(diagnosis_codes)]['Patient'].nunique() / data_df['Patient'].nunique()
        expected_prevalence = 47
        val  = (prevalence - expected_prevalence) / np.sqrt((prevalence*(100 - prevalence)+expected_prevalence*(100 - expected_prevalence))/2)
        ratio = prevalence/expected_prevalence
        res = (abs(val) < 0.2) & (0.85<=ratio<=1.15)
        output_vals["ratio"] = ratio
        output_vals["smd"] = val
        output_vals["expected_value"] = expected_prevalence
        output_vals["data_per"] = prevalence
        if res == False:
            fail_exp = 'prevalence in the examined data is ' + str(prevalence)
            explanation += ' ' + fail_exp
            
    except Exception as e:
        res = False
        test_flag = 'error'
        explanation += ' ' + str(e)
        
    finally:
        output_vals["explanation"] = explanation
        output_vals["test_flag"] = test_flag
        dftest_check_prevalence.explanation = str(output_vals)
        return res

def dftest_calculate_age_distribution(data_df):
    # ref: ['("CDC: https://www.cdc.gov/bloodpressure/facts.htm", "CDC: https://stacks.cdc.gov/view/cdc/150365")']
    explanation = 'Compares mean diagnosis age of Hypertension patients to the theoretical mean age. Expected value is 55.'
    # calculate age at diagnosis
    try:
        data_df = data_df[data_df['Code'].astype(str).isin(['38341003', '266287006', '56218007', '194756002', '155295004', '64715009', '827069000', '449759005', '194760004', '429457004', '155297007', '827068008', '194759009', '194794002', '471521000000108', '155302005', '195537001', '473392002', '367390009', '599341000000105', '32966004', '194757006', '702817009', '194769003', '155299005', '46113002', '48146000', '137753003', '194776008', '86234004', '194788005', '194772005', '762463000', '845891000000103', '38481006', '60899001', '194791005', '194782006', '132721000119104', '10725009'])]
        data_df['Start'] = pd.to_datetime(data_df['Start'])
        data_df['BirthDate'] = pd.to_datetime(data_df['BirthDate'])
        data_df['diagnosis_age'] = data_df['Start'].dt.year - data_df['BirthDate'].dt.year
        data_df = data_df.sort_values(by=['Patient','Start'], ascending=True)
        unique_patients = data_df.dropna(subset=['Start'], axis=0).drop_duplicates(subset=['Patient'], keep='first')
        mean_age = unique_patients['diagnosis_age'].mean()
        theoretical_mean_age = 55
        val  = (mean_age - theoretical_mean_age) / np.sqrt((mean_age*(100 - mean_age)+theoretical_mean_age*(100 - theoretical_mean_age))/2)
        ratio = mean_age/theoretical_mean_age
        res = (abs(val) < 0.2) & (0.85<=ratio<=1.15)
        output_vals = {'data_per': mean_age, 'expected_value': theoretical_mean_age, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Mean diagnosis age in the examined data is ' + str(mean_age)
            explanation += ' ' + fail_exp
        
    except Exception as e:
        res = False
        binary = "Error"
        explanation = str(e)
        
    finally:
        output_vals = {}
        output_vals['pval'] = res
        output_vals['explanation'] = explanation
        output_vals['binary'] = binary
        dftest_calculate_age_distribution.explanation = str(output_vals)
    
    return res



# Filename: unit_test1.py

def dftest_Diabetes_mellitus_diagnosis_code_diagnosed(data_df):
    #"CDC (https://www.cdc.gov), American Heart Association (https://www.heart.org)"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Diabetes_mellitus_diagnosis_code rate comparison function. Theoretical value is expected to be 30.0.'
    try:
        diagnosed_ids = data_df[data_df['Code'].astype(str).isin(['38341003', '266287006', '56218007', '194756002', '155295004', '64715009', '827069000', '449759005', '194760004', '429457004', '155297007', '827068008', '194759009', '194794002', '471521000000108', '155302005', '195537001', '473392002', '367390009', '599341000000105', '32966004', '194757006', '702817009', '194769003', '155299005', '46113002', '48146000', '137753003', '194776008', '86234004', '194788005', '194772005', '762463000', '845891000000103', '38481006', '60899001', '194791005', '194782006', '132721000119104', '10725009'])]['Patient'].unique()
        diagnosed = data_df[data_df['Patient'].isin(diagnosed_ids)]
        codes = ['73211009', '44054006', '111552007', '46635009', '28032008']
        data_per = 100 * diagnosed[diagnosed['Code'].astype(str).isin(codes)]['Patient'].nunique() / diagnosed['Patient'].nunique()
        val = (data_per - 30.0) / np.sqrt((data_per * (100 - data_per) + 30.0 * (100 - 30.0)) / 2)
        ratio = data_per / 30.0
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 30.0, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: Diabetes_mellitus_diagnosis_code percentage in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Diabetes_mellitus_diagnosis_code_diagnosed.explanation = str(output_vals)
        return res

def dftest_Hyperlipidemia_diagnosis_code_diagnosed(data_df):
    #"CDC (https://www.cdc.gov/chronicdisease/resources/publications/factsheets/heart-disease-stroke.htm), American Heart Association (https://www.heart.org)"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Hyperlipidemia_diagnosis_code rate comparison function. Theoretical value is expected to be between 35.0 and 40.0.'
    try:
        diagnosed_ids = data_df[data_df['Code'].astype(str).isin(['38341003', '266287006', '56218007', '194756002', '155295004', '64715009', '827069000', '449759005', '194760004', '429457004', '155297007', '827068008', '194759009', '194794002', '471521000000108', '155302005', '195537001', '473392002', '367390009', '599341000000105', '32966004', '194757006', '702817009', '194769003', '155299005', '46113002', '48146000', '137753003', '194776008', '86234004', '194788005', '194772005', '762463000', '845891000000103', '38481006', '60899001', '194791005', '194782006', '132721000119104', '10725009'])]['Patient'].unique()
        diagnosed = data_df[data_df['Patient'].isin(diagnosed_ids)]
        codes = ['55822004', '267434003', '238090007', '190774002', '3723001']
        data_per = 100 * diagnosed[diagnosed['Code'].astype(str).isin(codes)]['Patient'].nunique() / diagnosed['Patient'].nunique()
        res = (35.0 <= data_per <= 40.0)
        output_vals = {'data_per': data_per, 'range_low': 35.0, 'range_high': 40.0}
        if res == False:
            fail_exp = 'Among diagnosed: Hyperlipidemia_diagnosis_code evaluation in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Hyperlipidemia_diagnosis_code_diagnosed.explanation = str(output_vals)
        return res

def dftest_Coronary_artery_disease_diagnosis_code_diagnosed(data_df):
    #"CDC (https://www.cdc.gov/heartdisease/coronary_ad.htm), American Heart Association (https://www.heart.org)"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Coronary_artery_disease_diagnosis_code rate comparison function. Theoretical value is expected to be between 25.0 and 30.0.'
    try:
        diagnosed_ids = data_df[data_df['Code'].astype(str).isin(['38341003', '266287006', '56218007', '194756002', '155295004', '64715009', '827069000', '449759005', '194760004', '429457004', '155297007', '827068008', '194759009', '194794002', '471521000000108', '155302005', '195537001', '473392002', '367390009', '599341000000105', '32966004', '194757006', '702817009', '194769003', '155299005', '46113002', '48146000', '137753003', '194776008', '86234004', '194788005', '194772005', '762463000', '845891000000103', '38481006', '60899001', '194791005', '194782006', '132721000119104', '10725009'])]['Patient'].unique()
        diagnosed = data_df[data_df['Patient'].isin(diagnosed_ids)]
        codes = ['53741008', '398274000', '194842008', '233970002', '21930005']
        data_per = 100 * diagnosed[diagnosed['Code'].astype(str).isin(codes)]['Patient'].nunique() / diagnosed['Patient'].nunique()
        res = (25.0 <= data_per <= 30.0)
        output_vals = {'data_per': data_per, 'range_low': 25.0, 'range_high': 30.0}
        if res == False:
            fail_exp = 'Among diagnosed: Coronary_artery_disease_diagnosis_code evaluation in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Coronary_artery_disease_diagnosis_code_diagnosed.explanation = str(output_vals)
        return res

def dftest_Obesity_diagnosis_code_diagnosed(data_df):
    #"CDC (https://www.cdc.gov/obesity/data/adult.html), American Heart Association (https://www.heart.org)"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Obesity_diagnosis_code rate comparison function. Theoretical value is expected to be between 40.0 and 60.0.'
    try:
        diagnosed_ids = data_df[data_df['Code'].astype(str).isin(['38341003', '266287006', '56218007', '194756002', '155295004', '64715009', '827069000', '449759005', '194760004', '429457004', '155297007', '827068008', '194759009', '194794002', '471521000000108', '155302005', '195537001', '473392002', '367390009', '599341000000105', '32966004', '194757006', '702817009', '194769003', '155299005', '46113002', '48146000', '137753003', '194776008', '86234004', '194788005', '194772005', '762463000', '845891000000103', '38481006', '60899001', '194791005', '194782006', '132721000119104', '10725009'])]['Patient'].unique()
        diagnosed = data_df[data_df['Patient'].isin(diagnosed_ids)]
        codes = ['44054006', '162864005', '161891005', '162865006']
        data_per = 100 * diagnosed[diagnosed['Code'].astype(str).isin(codes)]['Patient'].nunique() / diagnosed['Patient'].nunique()
        res = (40.0 <= data_per <= 60.0)
        output_vals = {'data_per': data_per, 'range_low': 40.0, 'range_high': 60.0}
        if res == False:
            fail_exp = 'Among diagnosed: Obesity_diagnosis_code evaluation in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Obesity_diagnosis_code_diagnosed.explanation = str(output_vals)
        return res

def dftest_Heart_failure_diagnosis_code_diagnosed(data_df):
    #"CDC (https://www.cdc.gov/heartdisease/statistics.html), American Heart Association (https://www.heart.org/en/health-topics/high-blood-pressure)"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Heart_failure_diagnosis_code rate comparison function. Theoretical value is expected to be between 20.0 and 30.0.'
    try:
        diagnosed_ids = data_df[data_df['Code'].astype(str).isin(['38341003', '266287006', '56218007', '194756002', '155295004', '64715009', '827069000', '449759005', '194760004', '429457004', '155297007', '827068008', '194759009', '194794002', '471521000000108', '155302005', '195537001', '473392002', '367390009', '599341000000105', '32966004', '194757006', '702817009', '194769003', '155299005', '46113002', '48146000', '137753003', '194776008', '86234004', '194788005', '194772005', '762463000', '845891000000103', '38481006', '60899001', '194791005', '194782006', '132721000119104', '10725009'])]['Patient'].unique()
        diagnosed = data_df[data_df['Patient'].isin(diagnosed_ids)]
        codes = ['84114007', '395105005', '703272007', '703275009', '23341000119109', '446221000', '417996009', '233924009', '56675007', '703273002', '471880001', '85232009', '42343007', '364006', '10633002', '359617009', '698594003', '101281000119107', '788950000', '111283005', '10335000', '703276005', '88805009', '426263006', '48447003', '443254009', '418304008', '153931000119109', '426611007', '80479009', '74960003', '441481004', '424404003', '314206003', '153941000119100', '153951000119103', '5375005', '10091002', '46113002', '443253003', '92506005', '609556008', '120861000119102', '5148006', '443343001', '66989003', '703274008', '441530006', '82523003', '120851000119104', '394927007', '44313006', '717840005', '16838951000119100', '609555007', '120871000119108', '443344007', '67441000119101', '462172006', '67431000119105', '25544003', '15629591000119103', '15629541000119106', '7411000175102', '15629641000119107', '120891000119109']
        data_per = 100 * diagnosed[diagnosed['Code'].astype(str).isin(codes)]['Patient'].nunique() / diagnosed['Patient'].nunique()
        res = (20.0 <= data_per <= 30.0)
        output_vals = {'data_per': data_per, 'range_low': 20.0, 'range_high': 30.0}
        if res == False:
            fail_exp = 'Among diagnosed: Heart_failure_diagnosis_code evaluation in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Heart_failure_diagnosis_code_diagnosed.explanation = str(output_vals)
        return res

# Filename: unit_test1.py

def dftest_Atrial_fibrillation_and_related_conditions_diagnosis_code_diagnosed(data_df):
    #("CDC: https://www.cdc.gov/heartdisease/atrial_fibrillation.htm", "American Heart Association: https://www.heart.org")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Atrial_fibrillation_and_related_conditions_diagnosis_code rate comparison function. Theoretical value is expected to be between 15.0 and 20.0.'
    try:
        diagnosed_ids = data_df[data_df['Code'].astype(str).isin(['38341003', '266287006', '56218007', '194756002', '155295004', '64715009', '827069000', '449759005', '194760004', '429457004', '155297007', '827068008', '194759009', '194794002', '471521000000108', '155302005', '195537001', '473392002', '367390009', '599341000000105', '32966004', '194757006', '702817009', '194769003', '155299005', '46113002', '48146000', '137753003', '194776008', '86234004', '194788005', '194772005', '762463000', '845891000000103', '38481006', '60899001', '194791005', '194782006', '132721000119104', '10725009'])]['Patient'].unique()
        diagnosed = data_df[data_df['Patient'].isin(diagnosed_ids)]
        codes = ['49436004', '1066831000000104', '233911009', '120041000119109', '17366009', '426749004', '195147006', '282825002', '5370000', '720448006', '440059007', '15964901000119107', '762247006', '440028005', '425615007', '313377641000119105', '71908006', '300996004', '1010405004', '427665004', '314208002', '1067061000000104', '40593004', '81437007', '251173003', '706923002', '426814001', '276796006', '816401000000105', '233910005', '870575001', '36665001', '251188008', '429243003', '489609371000119104', '129032061000119103', '164889003', '195069001', '95440004', '251174009', '49760004', '725145002', '233893007', '194868001', '248411000000105', '278482008', '196371000000102', '1197418004', '164890007', '44103008', '720507006']
        data_per = 100 * diagnosed[diagnosed['Code'].astype(str).isin(codes)]['Patient'].nunique() / diagnosed['Patient'].nunique()
        res = (15.0 <= data_per <= 20.0)
        output_vals = {'data_per': data_per, 'range_low': 15.0, 'range_high': 20.0}
        if res == False:
            fail_exp = 'Among diagnosed: Atrial_fibrillation_and_related_conditions_diagnosis_code evaluation in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Atrial_fibrillation_and_related_conditions_diagnosis_code_diagnosed.explanation = str(output_vals)
        return res

def dftest_Stroke_and_related_conditions_diagnosis_code_diagnosed(data_df):
    #"CDC Stroke Facts (https://www.cdc.gov/stroke/facts.htm), American Heart Association (https://www.heart.org/en/health-topics/high-blood-pressure/why-high-blood-pressure-is-a-silent-killer)"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Stroke_and_related_conditions_diagnosis_code rate comparison function. Theoretical value is expected to be 77.0.'
    try:
        diagnosed_ids = data_df[data_df['Code'].astype(str).isin(['38341003', '266287006', '56218007', '194756002', '155295004', '64715009', '827069000', '449759005', '194760004', '429457004', '155297007', '827068008', '194759009', '194794002', '471521000000108', '155302005', '195537001', '473392002', '367390009', '599341000000105', '32966004', '194757006', '702817009', '194769003', '155299005', '46113002', '48146000', '137753003', '194776008', '86234004', '194788005', '194772005', '762463000', '845891000000103', '38481006', '60899001', '194791005', '194782006', '132721000119104', '10725009'])]['Patient'].unique()
        diagnosed = data_df[data_df['Patient'].isin(diagnosed_ids)]
        codes = ['195212005', '111297002', '422504002', '371040005', '373606000', '116288000', '299403002', '720191000000104', '828261000000103', '366609000', '371041009', '1078001000000105', '195213000', '725132001', '16371781000119100', '413124000', '140921000119102', '137991000119103', '33331000119103', '413758000', '230713003', '724429004', '230739000', '2517002', '16891111000119104', '230714009', '140911000119109', '9901000119100', '25133001', '57981008', '33301000119105', '299404008', '275434003', '80051000119107', '230715005', '277381004', '16002191000119102', '77728007', '310137004', '108691000119102', '415630002', '16002391000119100', '329401000119103', '170600009', '415631003', '16002511000119104', '329631000119108', '415629007', '16002151000119107', '842441000000104', '866240007', '788882003', '415628004', '16002351000119105', '48601000119107', '788883008', '371121002', '817701000000103', '842431000000108']
        data_per = 100 * diagnosed[diagnosed['Code'].astype(str).isin(codes)]['Patient'].nunique() / diagnosed['Patient'].nunique()
        val = (data_per - 77.0) / np.sqrt((data_per * (100 - data_per) + 77.0 * (100 - 77.0)) / 2)
        ratio = data_per / 77.0
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 77.0, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: Stroke_and_related_conditions_diagnosis_code percentage in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Stroke_and_related_conditions_diagnosis_code_diagnosed.explanation = str(output_vals)
        return res

def dftest_Peripheral_vascular_disease_diagnosis_code_diagnosed(data_df):
    #"CDC (https://www.cdc.gov), American Heart Association (https://www.heart.org)"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Peripheral_vascular_disease_diagnosis_code rate comparison function. Theoretical value is expected to be between 25.0 and 30.0.'
    try:
        diagnosed_ids = data_df[data_df['Code'].astype(str).isin(['38341003', '266287006', '56218007', '194756002', '155295004', '64715009', '827069000', '449759005', '194760004', '429457004', '155297007', '827068008', '194759009', '194794002', '471521000000108', '155302005', '195537001', '473392002', '367390009', '599341000000105', '32966004', '194757006', '702817009', '194769003', '155299005', '46113002', '48146000', '137753003', '194776008', '86234004', '194788005', '194772005', '762463000', '845891000000103', '38481006', '60899001', '194791005', '194782006', '132721000119104', '10725009'])]['Patient'].unique()
        diagnosed = data_df[data_df['Patient'].isin(diagnosed_ids)]
        codes = ['321052', '40648191', '40315969', '313928', '44782775', '44782776']
        data_per = 100 * diagnosed[diagnosed['Code'].astype(str).isin(codes)]['Patient'].nunique() / diagnosed['Patient'].nunique()
        res = (25.0 <= data_per <= 30.0)
        output_vals = {'data_per': data_per, 'range_low': 25.0, 'range_high': 30.0}
        if res == False:
            fail_exp = 'Among diagnosed: Peripheral_vascular_disease_diagnosis_code evaluation in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Peripheral_vascular_disease_diagnosis_code_diagnosed.explanation = str(output_vals)
        return res

def dftest_Chronic_obstructive_pulmonary_disease_diagnosis_code_diagnosed(data_df):
    #"CDC, American Heart Association, American Journal of Respiratory and Critical Care Medicine (https://www.cdc.gov/copd/index.html, https://www.ahajournals.org/, https://www.atsjournals.org/doi/full/10.1164/rccm.2020)"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Chronic_obstructive_pulmonary_disease_diagnosis_code rate comparison function. Theoretical value is expected to be 24.0.'
    try:
        diagnosed_ids = data_df[data_df['Code'].astype(str).isin(['38341003', '266287006', '56218007', '194756002', '155295004', '64715009', '827069000', '449759005', '194760004', '429457004', '155297007', '827068008', '194759009', '194794002', '471521000000108', '155302005', '195537001', '473392002', '367390009', '599341000000105', '32966004', '194757006', '702817009', '194769003', '155299005', '46113002', '48146000', '137753003', '194776008', '86234004', '194788005', '194772005', '762463000', '845891000000103', '38481006', '60899001', '194791005', '194782006', '132721000119104', '10725009'])]['Patient'].unique()
        diagnosed = data_df[data_df['Patient'].isin(diagnosed_ids)]
        codes = ['13645005', '313299006', '313296004', '106001000119106']
        data_per = 100 * diagnosed[diagnosed['Code'].astype(str).isin(codes)]['Patient'].nunique() / diagnosed['Patient'].nunique()
        val = (data_per - 24.0) / np.sqrt((data_per * (100 - data_per) + 24.0 * (100 - 24.0)) / 2)
        ratio = data_per / 24.0
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 24.0, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: Chronic_obstructive_pulmonary_disease_diagnosis_code percentage in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Chronic_obstructive_pulmonary_disease_diagnosis_code_diagnosed.explanation = str(output_vals)
        return res

def dftest_Sleep_apnea_and_related_conditions_diagnosis_code_diagnosed(data_df):
    #("American Heart Association, peer-reviewed studies.")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Sleep_apnea_and_related_conditions_diagnosis_code rate comparison function. Theoretical value is expected to be between 30.0 and 50.0.'
    try:
        diagnosed_ids = data_df[data_df['Code'].astype(str).isin(['38341003', '266287006', '56218007', '194756002', '155295004', '64715009', '827069000', '449759005', '194760004', '429457004', '155297007', '827068008', '194759009', '194794002', '471521000000108', '155302005', '195537001', '473392002', '367390009', '599341000000105', '32966004', '194757006', '702817009', '194769003', '155299005', '46113002', '48146000', '137753003', '194776008', '86234004', '194788005', '194772005', '762463000', '845891000000103', '38481006', '60899001', '194791005', '194782006', '132721000119104', '10725009'])]['Patient'].unique()
        diagnosed = data_df[data_df['Patient'].isin(diagnosed_ids)]
        codes = ['73430006', '27405005', '78275009', '85721000119105', '724507000', '9741000119101', '103750000', '1101000119103', '230494007', '111489007', '230493001', '41975002', '442164004', '361208003', '1023001', '79280005', '16275741000119100', '789055001', '1091000119108', '430390000', '274214008', '697914005', '288581000119102', '104831000119109', '724229002', '89911000119102', '789009003', '101301000119106', '416945002', '113026004', '971918681000119107', '724506009', '13094009', '426542005', '706225001', '719976001', '63214000', '443760008', '57000008', '276545006', '723881000', '91441000119109', '272265001', '39898005', '37952003', '430337004', '1284824006', '276725001', '17057004', '276544005', '16419651000119103', '701154000', '868249004', '441910000', '230499002']
        data_per = 100 * diagnosed[diagnosed['Code'].astype(str).isin(codes)]['Patient'].nunique() / diagnosed['Patient'].nunique()
        res = (30.0 <= data_per <= 50.0)
        output_vals = {'data_per': data_per, 'range_low': 30.0, 'range_high': 50.0}
        if res == False:
            fail_exp = 'Among diagnosed: Sleep_apnea_and_related_conditions_diagnosis_code evaluation in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Sleep_apnea_and_related_conditions_diagnosis_code_diagnosed.explanation = str(output_vals)
        return res

def dftest_Depression_diagnosis_code_diagnosed(data_df):
    #"CDC (https://www.cdc.gov/), American Heart Association (https://www.heart.org/)"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Depression_diagnosis_code rate comparison function. Theoretical value is expected to be between 20.0 and 30.0.'
    try:
        diagnosed_ids = data_df[data_df['Code'].astype(str).isin(['38341003', '266287006', '56218007', '194756002', '155295004', '64715009', '827069000', '449759005', '194760004', '429457004', '155297007', '827068008', '194759009', '194794002', '471521000000108', '155302005', '195537001', '473392002', '367390009', '599341000000105', '32966004', '194757006', '702817009', '194769003', '155299005', '46113002', '48146000', '137753003', '194776008', '86234004', '194788005', '194772005', '762463000', '845891000000103', '38481006', '60899001', '194791005', '194782006', '132721000119104', '10725009'])]['Patient'].unique()
        diagnosed = data_df[data_df['Patient'].isin(diagnosed_ids)]
        codes = ['35489007', '394924000', '310497006', '310495003', '19202009']
        data_per = 100 * diagnosed[diagnosed['Code'].astype(str).isin(codes)]['Patient'].nunique() / diagnosed['Patient'].nunique()
        res = (20.0 <= data_per <= 30.0)
        output_vals = {'data_per': data_per, 'range_low': 20.0, 'range_high': 30.0}
        if res == False:
            fail_exp = 'Among diagnosed: Depression_diagnosis_code evaluation in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Depression_diagnosis_code_diagnosed.explanation = str(output_vals)
        return res

def dftest_Osteoarthritis_diagnosis_code_diagnosed(data_df):
    #"CDC, American Heart Association, Arthritis & Rheumatology (https://www.cdc.gov/arthritis/data_statistics.htm, https://onlinelibrary.wiley.com/journal/23265205)"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Osteoarthritis_diagnosis_code rate comparison function. Theoretical value is expected to be between 30.0 and 40.0.'
    try:
        diagnosed_ids = data_df[data_df['Code'].astype(str).isin(['38341003', '266287006', '56218007', '194756002', '155295004', '64715009', '827069000', '449759005', '194760004', '429457004', '155297007', '827068008', '194759009', '194794002', '471521000000108', '155302005', '195537001', '473392002', '367390009', '599341000000105', '32966004', '194757006', '702817009', '194769003', '155299005', '46113002', '48146000', '137753003', '194776008', '86234004', '194788005', '194772005', '762463000', '845891000000103', '38481006', '60899001', '194791005', '194782006', '132721000119104', '10725009'])]['Patient'].unique()
        diagnosed = data_df[data_df['Patient'].isin(diagnosed_ids)]
        codes = ['396275006', '239873007', '239876004', '254779008', '118940003']
        data_per = 100 * diagnosed[diagnosed['Code'].astype(str).isin(codes)]['Patient'].nunique() / diagnosed['Patient'].nunique()
        res = (30.0 <= data_per <= 40.0)
        output_vals = {'data_per': data_per, 'range_low': 30.0, 'range_high': 40.0}
        if res == False:
            fail_exp = 'Among diagnosed: Osteoarthritis_diagnosis_code evaluation in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Osteoarthritis_diagnosis_code_diagnosed.explanation = str(output_vals)
        return res

def dftest_Anemia_diagnosis_code_diagnosed(data_df):
    #"CDC, American Heart Association, PubMed (DOI: 10.1093/ajh/hpx123), WHO (Global Burden of Disease Study)"
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Anemia_diagnosis_code rate comparison function. Theoretical value is expected to be between 15.0 and 25.0.'
    try:
        diagnosed_ids = data_df[data_df['Code'].astype(str).isin(['38341003', '266287006', '56218007', '194756002', '155295004', '64715009', '827069000', '449759005', '194760004', '429457004', '155297007', '827068008', '194759009', '194794002', '471521000000108', '155302005', '195537001', '473392002', '367390009', '599341000000105', '32966004', '194757006', '702817009', '194769003', '155299005', '46113002', '48146000', '137753003', '194776008', '86234004', '194788005', '194772005', '762463000', '845891000000103', '38481006', '60899001', '194791005', '194782006', '132721000119104', '10725009'])]['Patient'].unique()
        diagnosed = data_df[data_df['Patient'].isin(diagnosed_ids)]
        codes = ['40624900', '40321260', '40390414', '4150154', '444238']
        data_per = 100 * diagnosed[diagnosed['Code'].astype(str).isin(codes)]['Patient'].nunique() / diagnosed['Patient'].nunique()
        res = (15.0 <= data_per <= 25.0)
        output_vals = {'data_per': data_per, 'range_low': 15.0, 'range_high': 25.0}
        if res == False:
            fail_exp = 'Among diagnosed: Anemia_diagnosis_code evaluation in the examined data is ' + str(data_per)
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Anemia_diagnosis_code_diagnosed.explanation = str(output_vals)
        return res



# Filename: unit_test2.py

def dftest_Male_gender_(data_df):
    #("America's Health Rankings: https://www.americashealthrankings.org/explore/annual/measure/Hypertension/state/MA", "U.S. Census Bureau: https://www.census.gov/quickfacts/fact/table/MA")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Male_gender_ evaluation function. Result is expected to be 48.5%.'
    try:
        codes = ['M']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['Gender'].astype(str).isin(codes)]['Patient'].nunique() / ref_for_percentage['Patient'].nunique()
        val = (data_per - 48.5) / np.sqrt((data_per * (100 - data_per) + 48.5 * (100 - 48.5)) / 2)
        ratio = data_per / 48.5
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 48.5, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Male_gender_ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Male_gender_.explanation = str(output_vals)
        return res

def dftest_Female_gender_(data_df):
    #("U.S. Census Bureau (https://www.census.gov/quickfacts/MA)", "America's Health Rankings (https://www.americashealthrankings.org/explore/annual/measure/Hypertension/state/MA)")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Female_gender_ evaluation function. Result is expected to be 51.5%.'
    try:
        codes = ['F']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['Gender'].astype(str).isin(codes)]['Patient'].nunique() / ref_for_percentage['Patient'].nunique()
        val = (data_per - 51.5) / np.sqrt((data_per * (100 - data_per) + 51.5 * (100 - 51.5)) / 2)
        ratio = data_per / 51.5
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 51.5, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Female_gender_ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Female_gender_.explanation = str(output_vals)
        return res

def dftest_White_race_(data_df):
    #("U.S. Census Bureau QuickFacts: https://www.census.gov/quickfacts/fact/table/MA/PST045224")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'White_race_ evaluation function. Result is expected to be 70.7%.'
    try:
        codes = ['white']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['Race'].astype(str).isin(codes)]['Patient'].nunique() / ref_for_percentage['Patient'].nunique()
        val = (data_per - 70.7) / np.sqrt((data_per * (100 - data_per) + 70.7 * (100 - 70.7)) / 2)
        ratio = data_per / 70.7
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 70.7, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'White_race_ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_White_race_.explanation = str(output_vals)
        return res

def dftest_Black_or_African_American_race_(data_df):
    #("U.S. Census Bureau: https://www.census.gov/quickfacts/fact/table/MA/PST045224")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Black_or_African_American_race_ evaluation function. Result is expected to be 9.0%.'
    try:
        codes = ['black']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['Race'].astype(str).isin(codes)]['Patient'].nunique() / ref_for_percentage['Patient'].nunique()
        val = (data_per - 9.0) / np.sqrt((data_per * (100 - data_per) + 9.0 * (100 - 9.0)) / 2)
        ratio = data_per / 9.0
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 9.0, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Black_or_African_American_race_ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Black_or_African_American_race_.explanation = str(output_vals)
        return res

def dftest_Asian_race_(data_df):
    #("U.S. Census Bureau QuickFacts - Massachusetts (https://www.census.gov/quickfacts/fact/table/MA/PST045224)")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Asian_race_ evaluation function. Result is expected to be 7.2%.'
    try:
        codes = ['asian']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['Race'].astype(str).isin(codes)]['Patient'].nunique() / ref_for_percentage['Patient'].nunique()
        val = (data_per - 7.2) / np.sqrt((data_per * (100 - data_per) + 7.2 * (100 - 7.2)) / 2)
        ratio = data_per / 7.2
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 7.2, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Asian_race_ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Asian_race_.explanation = str(output_vals)
        return res

def dftest_American_Indian_or_Alaska_Native_race_(data_df):
    #("U.S. Census Bureau QuickFacts - Massachusetts: https://www.census.gov/quickfacts/fact/table/MA/PST045224")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'American_Indian_or_Alaska_Native_race_ evaluation function. Result is expected to be 0.2%.'
    try:
        codes = ['native']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['Race'].astype(str).isin(codes)]['Patient'].nunique() / ref_for_percentage['Patient'].nunique()
        val = (data_per - 0.2) / np.sqrt((data_per * (100 - data_per) + 0.2 * (100 - 0.2)) / 2)
        ratio = data_per / 0.2
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 0.2, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'American_Indian_or_Alaska_Native_race_ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_American_Indian_or_Alaska_Native_race_.explanation = str(output_vals)
        return res

def dftest_Native_Hawaiian_or_Other_Pacific_Islander_race_(data_df):
    #("U.S. Census Bureau QuickFacts: https://www.census.gov/quickfacts/fact/table/MA/PST045224")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Native_Hawaiian_or_Other_Pacific_Islander_race_ evaluation function. Result is expected to be 0.1%.'
    try:
        codes = ['hawaiian', 'pacific']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['Race'].astype(str).isin(codes)]['Patient'].nunique() / ref_for_percentage['Patient'].nunique()
        val = (data_per - 0.1) / np.sqrt((data_per * (100 - data_per) + 0.1 * (100 - 0.1)) / 2)
        ratio = data_per / 0.1
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 0.1, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Native_Hawaiian_or_Other_Pacific_Islander_race_ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Native_Hawaiian_or_Other_Pacific_Islander_race_.explanation = str(output_vals)
        return res

def dftest_Other_race_(data_df):
    #("U.S. Census Bureau QuickFacts for Massachusetts: https://www.census.gov/quickfacts/fact/table/MA/PST045224")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Other_race_ evaluation function. Result is expected to be 5.4%.'
    try:
        codes = ['other']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['Race'].astype(str).isin(codes)]['Patient'].nunique() / ref_for_percentage['Patient'].nunique()
        val = (data_per - 5.4) / np.sqrt((data_per * (100 - data_per) + 5.4 * (100 - 5.4)) / 2)
        ratio = data_per / 5.4
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 5.4, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Other_race_ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Other_race_.explanation = str(output_vals)
        return res

def dftest_Hispanic_or_Latino_ethnicity_(data_df):
    #("U.S. Census Bureau QuickFacts - Massachusetts (https://www.census.gov/quickfacts/fact/table/MA/PST045224)")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Hispanic_or_Latino_ethnicity_ evaluation function. Result is expected to be 13.1%.'
    try:
        codes = ['Hispanic or Latino']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['Ethnicity'].astype(str).isin(codes)]['Patient'].nunique() / ref_for_percentage['Patient'].nunique()
        val = (data_per - 13.1) / np.sqrt((data_per * (100 - data_per) + 13.1 * (100 - 13.1)) / 2)
        ratio = data_per / 13.1
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 13.1, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Hispanic_or_Latino_ethnicity_ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Hispanic_or_Latino_ethnicity_.explanation = str(output_vals)
        return res

def dftest_Not_Hispanic_or_Latino_ethnicity_(data_df):
    #("U.S. Census Bureau QuickFacts - Massachusetts (https://www.census.gov/quickfacts/fact/table/MA/PST045224)")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Not_Hispanic_or_Latino_ethnicity_ evaluation function. Result is expected to be 79.3%.'
    try:
        codes = ['Not Hispanic or Latino']
        ref_for_percentage = data_df
        data_per = 100 * data_df[data_df['Ethnicity'].astype(str).isin(codes)]['Patient'].nunique() / ref_for_percentage['Patient'].nunique()
        val = (data_per - 79.3) / np.sqrt((data_per * (100 - data_per) + 79.3 * (100 - 79.3)) / 2)
        ratio = data_per / 79.3
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 79.3, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Not_Hispanic_or_Latino_ethnicity_ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Not_Hispanic_or_Latino_ethnicity_.explanation = str(output_vals)
        return res



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



# Filename: unit_test4.py

def dftest_Male_gender_diagnosed_with_hypertension__diagnosed(data_df):
    #("CDC - Hypertension Statistics (https://www.cdc.gov/nchs/fastats/hypertension.htm)")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Male_gender_diagnosed_with_hypertension_ evaluation function. Result is expected to be 33.2%.'
    try:
        diagnosed_ids = data_df[data_df['Code'].astype(str).isin(['38341003', '266287006', '56218007', '194756002', '155295004', '64715009', '827069000', '449759005', '194760004', '429457004', '155297007', '827068008', '194759009', '194794002', '471521000000108', '155302005', '195537001', '473392002', '367390009', '599341000000105', '32966004', '194757006', '702817009', '194769003', '155299005', '46113002', '48146000', '137753003', '194776008', '86234004', '194788005', '194772005', '762463000', '845891000000103', '38481006', '60899001', '194791005', '194782006', '132721000119104', '10725009'])]['Patient'].unique()
        diagnosed = data_df[data_df['Patient'].isin(diagnosed_ids)]
        codes = ['M']
        ref_for_percentage = data_df[data_df['Gender'].astype(str).isin(codes)]
        data_per = 100 * diagnosed[diagnosed['Gender'].astype(str).isin(codes)]['Patient'].nunique() / ref_for_percentage['Patient'].nunique()
        val = (data_per - 33.2) / np.sqrt((data_per * (100 - data_per) + 33.2 * (100 - 33.2)) / 2)
        ratio = data_per / 33.2
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 33.2, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: Male_gender_diagnosed_with_hypertension_ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Male_gender_diagnosed_with_hypertension__diagnosed.explanation = str(output_vals)
        return res

def dftest_Female_gender_diagnosed_with_hypertension__diagnosed(data_df):
    #("America's Health Rankings: https://www.americashealthrankings.org/explore/measures/Hypertension/MA")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Female_gender_diagnosed_with_hypertension_ evaluation function. Result is expected to be 18.0%.'
    try:
        diagnosed_ids = data_df[data_df['Code'].astype(str).isin(['38341003', '266287006', '56218007', '194756002', '155295004', '64715009', '827069000', '449759005', '194760004', '429457004', '155297007', '827068008', '194759009', '194794002', '471521000000108', '155302005', '195537001', '473392002', '367390009', '599341000000105', '32966004', '194757006', '702817009', '194769003', '155299005', '46113002', '48146000', '137753003', '194776008', '86234004', '194788005', '194772005', '762463000', '845891000000103', '38481006', '60899001', '194791005', '194782006', '132721000119104', '10725009'])]['Patient'].unique()
        diagnosed = data_df[data_df['Patient'].isin(diagnosed_ids)]
        codes = ['F']
        ref_for_percentage = data_df[data_df['Gender'].astype(str).isin(codes)]
        data_per = 100 * diagnosed[diagnosed['Gender'].astype(str).isin(codes)]['Patient'].nunique() / ref_for_percentage['Patient'].nunique()
        val = (data_per - 18.0) / np.sqrt((data_per * (100 - data_per) + 18.0 * (100 - 18.0)) / 2)
        ratio = data_per / 18.0
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 18.0, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: Female_gender_diagnosed_with_hypertension_ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Female_gender_diagnosed_with_hypertension__diagnosed.explanation = str(output_vals)
        return res

def dftest_White_race_diagnosed_with_hypertension__diagnosed(data_df):
    #("CDC - High Blood Pressure Statistics: https://www.cdc.gov/high-blood-pressure/data.htm")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: White_race_diagnosed_with_hypertension_ evaluation function. Result is expected to be 45%.'
    try:
        diagnosed_ids = data_df[data_df['Code'].astype(str).isin(['38341003', '266287006', '56218007', '194756002', '155295004', '64715009', '827069000', '449759005', '194760004', '429457004', '155297007', '827068008', '194759009', '194794002', '471521000000108', '155302005', '195537001', '473392002', '367390009', '599341000000105', '32966004', '194757006', '702817009', '194769003', '155299005', '46113002', '48146000', '137753003', '194776008', '86234004', '194788005', '194772005', '762463000', '845891000000103', '38481006', '60899001', '194791005', '194782006', '132721000119104', '10725009'])]['Patient'].unique()
        diagnosed = data_df[data_df['Patient'].isin(diagnosed_ids)]
        codes = ['white']
        ref_for_percentage = data_df[data_df['Race'].astype(str).isin(codes)]
        data_per = 100 * diagnosed[diagnosed['Race'].astype(str).isin(codes)]['Patient'].nunique() / ref_for_percentage['Patient'].nunique()
        val = (data_per - 45) / np.sqrt((data_per * (100 - data_per) + 45 * (100 - 45)) / 2)
        ratio = data_per / 45
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 45, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: White_race_diagnosed_with_hypertension_ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_White_race_diagnosed_with_hypertension__diagnosed.explanation = str(output_vals)
        return res

def dftest_Black_or_African_American_race_diagnosed_with_hypertension__diagnosed(data_df):
    #("https://www.heart.org/en/health-topics/high-blood-pressure/why-high-blood-pressure-is-a-silent-killer")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Black_or_African_American_race_diagnosed_with_hypertension_ evaluation function. Result is expected to be 56%.'
    try:
        diagnosed_ids = data_df[data_df['Code'].astype(str).isin(['38341003', '266287006', '56218007', '194756002', '155295004', '64715009', '827069000', '449759005', '194760004', '429457004', '155297007', '827068008', '194759009', '194794002', '471521000000108', '155302005', '195537001', '473392002', '367390009', '599341000000105', '32966004', '194757006', '702817009', '194769003', '155299005', '46113002', '48146000', '137753003', '194776008', '86234004', '194788005', '194772005', '762463000', '845891000000103', '38481006', '60899001', '194791005', '194782006', '132721000119104', '10725009'])]['Patient'].unique()
        diagnosed = data_df[data_df['Patient'].isin(diagnosed_ids)]
        codes = ['black']
        ref_for_percentage = data_df[data_df['Race'].astype(str).isin(codes)]
        data_per = 100 * diagnosed[diagnosed['Race'].astype(str).isin(codes)]['Patient'].nunique() / ref_for_percentage['Patient'].nunique()
        val = (data_per - 56) / np.sqrt((data_per * (100 - data_per) + 56 * (100 - 56)) / 2)
        ratio = data_per / 56
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 56, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: Black_or_African_American_race_diagnosed_with_hypertension_ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Black_or_African_American_race_diagnosed_with_hypertension__diagnosed.explanation = str(output_vals)
        return res

def dftest_Asian_race_diagnosed_with_hypertension__diagnosed(data_df):
    #("AHA Journals", "https://www.ahajournals.org/doi/10.1161/HYPERTENSIONAHA.122.00001")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Asian_race_diagnosed_with_hypertension_ evaluation function. Result is expected to be 24.9%.'
    try:
        diagnosed_ids = data_df[data_df['Code'].astype(str).isin(['38341003', '266287006', '56218007', '194756002', '155295004', '64715009', '827069000', '449759005', '194760004', '429457004', '155297007', '827068008', '194759009', '194794002', '471521000000108', '155302005', '195537001', '473392002', '367390009', '599341000000105', '32966004', '194757006', '702817009', '194769003', '155299005', '46113002', '48146000', '137753003', '194776008', '86234004', '194788005', '194772005', '762463000', '845891000000103', '38481006', '60899001', '194791005', '194782006', '132721000119104', '10725009'])]['Patient'].unique()
        diagnosed = data_df[data_df['Patient'].isin(diagnosed_ids)]
        codes = ['asian']
        ref_for_percentage = data_df[data_df['Race'].astype(str).isin(codes)]
        data_per = 100 * diagnosed[diagnosed['Race'].astype(str).isin(codes)]['Patient'].nunique() / ref_for_percentage['Patient'].nunique()
        val = (data_per - 24.9) / np.sqrt((data_per * (100 - data_per) + 24.9 * (100 - 24.9)) / 2)
        ratio = data_per / 24.9
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 24.9, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: Asian_race_diagnosed_with_hypertension_ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Asian_race_diagnosed_with_hypertension__diagnosed.explanation = str(output_vals)
        return res

def dftest_American_Indian_or_Alaska_Native_race_diagnosed_with_hypertension_national_average_due_to_lack_of_Massachusetts_specific_data__diagnosed(data_df):
    #("CDC Data Brief 378: https://www.cdc.gov/nchs/data/databriefs/db378.pdf")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: American_Indian_or_Alaska_Native_race_diagnosed_with_hypertension__national_average_due_to_lack_of_Massachusetts_specific_data__ evaluation function. Result is expected to be 31.8%.'
    try:
        diagnosed_ids = data_df[data_df['Code'].astype(str).isin(['38341003', '266287006', '56218007', '194756002', '155295004', '64715009', '827069000', '449759005', '194760004', '429457004', '155297007', '827068008', '194759009', '194794002', '471521000000108', '155302005', '195537001', '473392002', '367390009', '599341000000105', '32966004', '194757006', '702817009', '194769003', '155299005', '46113002', '48146000', '137753003', '194776008', '86234004', '194788005', '194772005', '762463000', '845891000000103', '38481006', '60899001', '194791005', '194782006', '132721000119104', '10725009'])]['Patient'].unique()
        diagnosed = data_df[data_df['Patient'].isin(diagnosed_ids)]
        codes = ['native']
        ref_for_percentage = data_df[data_df['Race'].astype(str).isin(codes)]
        data_per = 100 * diagnosed[diagnosed['Race'].astype(str).isin(codes)]['Patient'].nunique() / ref_for_percentage['Patient'].nunique()
        val = (data_per - 31.8) / np.sqrt((data_per * (100 - data_per) + 31.8 * (100 - 31.8)) / 2)
        ratio = data_per / 31.8
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 31.8, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: American_Indian_or_Alaska_Native_race_diagnosed_with_hypertension__national_average_due_to_lack_of_Massachusetts_specific_data__ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_American_Indian_or_Alaska_Native_race_diagnosed_with_hypertension_national_average_due_to_lack_of_Massachusetts_specific_data__diagnosed.explanation = str(output_vals)
        return res

def dftest_Native_Hawaiian_or_Other_Pacific_Islander_race_diagnosed_with_hypertension__diagnosed(data_df):
    #("Heart.org https://www.heart.org/en/news/2023/11/08/native-hawaiian-and-pacific-islander-health", "CDC - Hypertension Statistics https://www.cdc.gov/bloodpressure/facts.htm")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Native_Hawaiian_or_Other_Pacific_Islander_race_diagnosed_with_hypertension_ evaluation function. Result is expected to be 30%.'
    try:
        diagnosed_ids = data_df[data_df['Code'].astype(str).isin(['38341003', '266287006', '56218007', '194756002', '155295004', '64715009', '827069000', '449759005', '194760004', '429457004', '155297007', '827068008', '194759009', '194794002', '471521000000108', '155302005', '195537001', '473392002', '367390009', '599341000000105', '32966004', '194757006', '702817009', '194769003', '155299005', '46113002', '48146000', '137753003', '194776008', '86234004', '194788005', '194772005', '762463000', '845891000000103', '38481006', '60899001', '194791005', '194782006', '132721000119104', '10725009'])]['Patient'].unique()
        diagnosed = data_df[data_df['Patient'].isin(diagnosed_ids)]
        codes = ['hawaiian', 'pacific']
        ref_for_percentage = data_df[data_df['Race'].astype(str).isin(codes)]
        data_per = 100 * diagnosed[diagnosed['Race'].astype(str).isin(codes)]['Patient'].nunique() / ref_for_percentage['Patient'].nunique()
        val = (data_per - 30) / np.sqrt((data_per * (100 - data_per) + 30 * (100 - 30)) / 2)
        ratio = data_per / 30
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 30, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: Native_Hawaiian_or_Other_Pacific_Islander_race_diagnosed_with_hypertension_ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Native_Hawaiian_or_Other_Pacific_Islander_race_diagnosed_with_hypertension__diagnosed.explanation = str(output_vals)
        return res

def dftest_Hispanic_or_Latino_ethnicity_diagnosed_with_hypertension__diagnosed(data_df):
    #("CDC - Hypertension Statistics: https://www.cdc.gov/bloodpressure/facts.htm")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Hispanic_or_Latino_ethnicity_diagnosed_with_hypertension_ evaluation function. Result is expected to be 24.5%.'
    try:
        diagnosed_ids = data_df[data_df['Code'].astype(str).isin(['38341003', '266287006', '56218007', '194756002', '155295004', '64715009', '827069000', '449759005', '194760004', '429457004', '155297007', '827068008', '194759009', '194794002', '471521000000108', '155302005', '195537001', '473392002', '367390009', '599341000000105', '32966004', '194757006', '702817009', '194769003', '155299005', '46113002', '48146000', '137753003', '194776008', '86234004', '194788005', '194772005', '762463000', '845891000000103', '38481006', '60899001', '194791005', '194782006', '132721000119104', '10725009'])]['Patient'].unique()
        diagnosed = data_df[data_df['Patient'].isin(diagnosed_ids)]
        codes = ['Hispanic or Latino']
        ref_for_percentage = data_df[data_df['Ethnicity'].astype(str).isin(codes)]
        data_per = 100 * diagnosed[diagnosed['Ethnicity'].astype(str).isin(codes)]['Patient'].nunique() / ref_for_percentage['Patient'].nunique()
        val = (data_per - 24.5) / np.sqrt((data_per * (100 - data_per) + 24.5 * (100 - 24.5)) / 2)
        ratio = data_per / 24.5
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 24.5, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: Hispanic_or_Latino_ethnicity_diagnosed_with_hypertension_ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Hispanic_or_Latino_ethnicity_diagnosed_with_hypertension__diagnosed.explanation = str(output_vals)
        return res

def dftest_Not_Hispanic_or_Latino_ethnicity_diagnosed_with_hypertension__diagnosed(data_df):
    #("CDC Hypertension Statistics: https://www.cdc.gov/bloodpressure/facts.htm")
    output_vals = {}
    test_flag = 'ok'
    explanation = 'Among diagnosed: Not_Hispanic_or_Latino_ethnicity_diagnosed_with_hypertension_ evaluation function. Result is expected to be 29.0%.'
    try:
        diagnosed_ids = data_df[data_df['Code'].astype(str).isin(['38341003', '266287006', '56218007', '194756002', '155295004', '64715009', '827069000', '449759005', '194760004', '429457004', '155297007', '827068008', '194759009', '194794002', '471521000000108', '155302005', '195537001', '473392002', '367390009', '599341000000105', '32966004', '194757006', '702817009', '194769003', '155299005', '46113002', '48146000', '137753003', '194776008', '86234004', '194788005', '194772005', '762463000', '845891000000103', '38481006', '60899001', '194791005', '194782006', '132721000119104', '10725009'])]['Patient'].unique()
        diagnosed = data_df[data_df['Patient'].isin(diagnosed_ids)]
        codes = ['Not Hispanic or Latino']
        ref_for_percentage = data_df[data_df['Ethnicity'].astype(str).isin(codes)]
        data_per = 100 * diagnosed[diagnosed['Ethnicity'].astype(str).isin(codes)]['Patient'].nunique() / ref_for_percentage['Patient'].nunique()
        val = (data_per - 29.0) / np.sqrt((data_per * (100 - data_per) + 29.0 * (100 - 29.0)) / 2)
        ratio = data_per / 29.0
        res = (abs(val) < 0.2) & (0.85 <= ratio <= 1.15)
        output_vals = {'data_per': data_per, 'expected_value': 29.0, 'ratio': ratio, 'smd': val}
        if res == False:
            fail_exp = 'Among diagnosed: Not_Hispanic_or_Latino_ethnicity_diagnosed_with_hypertension_ percentage in the examined data is ' + str(data_per) + '%'
            explanation += ' ' + fail_exp
    except Exception as e:
        res = False
        test_flag = "error"
        explanation += ' ' + str(e).replace('"', "").replace("'", "")
    finally:
        output_vals['explanation'] = explanation
        output_vals['test_flag'] = test_flag
        dftest_Not_Hispanic_or_Latino_ethnicity_diagnosed_with_hypertension__diagnosed.explanation = str(output_vals)
        return res



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



