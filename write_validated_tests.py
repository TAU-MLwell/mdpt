import os
import math
import numpy as np
import pandas as pd
import datetime as dt
from ask_gpt import LLMwrapper
from extraction_functions import make_py, make_all_py
from connect_openAI import connect_to_openAI

pd.set_option("future.no_silent_downcasting", True)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def create_tests(row, data_df, coding, diagnosis, code_list, col_conversion):
    row.index = row.index.str.strip()

    if row['codes'][0] == '[':
        row['codes'] = row['codes'][1:-1]
    
    row['codes'] = row['codes'].replace('"', "")
    row_code_list = row['codes'].split(",")
    row_code_list = [str(item) for item in row_code_list]
    row_code_list = [item.strip() for item in row_code_list]
    row['codes'] = row_code_list

    person_id_col = col_conversion[col_conversion['generic']=='personID']['column_name'].item()
    code_col = col_conversion[col_conversion['generic']=='code']['column_name'].item()
    code_date_col = col_conversion[col_conversion['generic']=='codeDate']['column_name'].item()
    birth_date_col = col_conversion[col_conversion['generic']=='birthDate']['column_name'].item()

    desc = row['description']
    desc = desc.replace("'", "").replace('"',"")
    
    for letter in desc:
        if letter.isnumeric() == False and letter.isalpha() == False:
            desc = desc.replace(letter, "_")

    curr_test_title = "dftest_" + desc.replace("np.nan", "")
    
    while '__' in curr_test_title:
        curr_test_title = curr_test_title.replace("__", "_")

    if data_df == "diagnosed":
        curr_test_title = curr_test_title + "_diagnosed"
    else:
        curr_test_title = curr_test_title
        
    curr_test = f"def {curr_test_title}(data_df):\n"
    curr_test += f"    #{row['references']}\n"
    curr_test += "    output_vals = {}\n"
    #curr_test += "    try:\n"
    curr_test += "test_flag = 'ok'"
    if data_df == "subpop_data":
        curr_test+= f"""subpop_ids = data_df[data_df['gender_column_name']==<gender code according to the description>\n"""
        curr_test+= f"""subpop_data = data_df[data_df[{person_id_col}].isin(subpop_ids)]\n"""
        
    elif data_df == "diagnosed":
        curr_test1 = f"""    diagnosed_ids = data_df[data_df[{code_col}].astype(str).isin({code_list})][{person_id_col}].unique()\n"""
        curr_test1+= f"""    diagnosed = data_df[data_df[{person_id_col}].isin(diagnosed_ids)]\n"""
        desc = "Among diagnosed: " + desc
    
    if (row['flag'].lower() =='diagnosis'):
        if (row['comparison_type'].lower() == 'percentage'):
            curr_test += f"""
            explanation = '{desc} rate comparison function. Theoretical value is expected to be {row['expected_value']}.'
            try:"""
            if data_df == "diagnosed":
                curr_test += curr_test1
            curr_test+= f"""codes = {row['codes']}
            data_per = 100*{data_df}[{data_df}['{row['column_name']}'].astype(str).isin(codes)][{person_id_col}].nunique() / {data_df}[{person_id_col}].nunique()  
            val  = (data_per - {row['expected_value']}) / np.sqrt((data_per*(100 - data_per)+{row['expected_value']}*(100 - {row['expected_value']}))/2)
            ratio = data_per/{row['expected_value']}
            res = (abs(val) < 0.2) & (0.85<=ratio<=1.15)
            output_vals = {{'data_per': data_per, 'expected_value': {row['expected_value']}, 'ratio': ratio, 'smd': val}}
            if res == False:
                fail_exp = '{desc} percentage in the examined data is ' + str(data_per)
                explanation += ' ' + fail_exp
                """
            return curr_test, curr_test_title
        
        elif (row['comparison_type'].lower() == 'range'):
            min_val = min([x for x in [float(row['expected_value_min']), float(row['range_low']), float(row['expected_value'])] if not math.isnan(x)])
            max_val = max([x for x in [float(row['expected_value_max']), float(row['range_high']), float(row['expected_value'])] if not math.isnan(x)])
            curr_test += f"""
            explanation = '{desc} rate comparison function. Theoretical value is expected to be between {min_val} and {max_val}.'
            try:"""
            if data_df == "diagnosed":
                curr_test += curr_test1
            
            curr_test+= f"""
                codes = {row['codes']}
                data_per = 100*{data_df}[{data_df}['{row['column_name']}'].astype(str).isin(codes)][{person_id_col}].nunique() / {data_df}[{person_id_col}].nunique()
                res = (min_val<=(data_per)<=max_val)
                output_vals = {{'data_per': data_per, 'range_low': {min_val}, 'range_high': {max_val}}}
                if res == False:
                    fail_exp = '{desc} evaluation in the examined data is ' + str(100*data_per) + '%'
                    explanation += ' ' + fail_exp
                    """
            return curr_test, curr_test_title
        else:
            return -1


    elif (row['flag'].lower() == 'drug'):

        if data_df == "diagnosed":
            curr_test += curr_test1 #drugs among diagnosed
        
        for col in ['expected_value_min','range_low','expected_value', 'range_high','expected_value_max']:
            try:
                row[col] = row[col].replace('%', '').replace('>', '').replace('<', '')
            except:
                pass
            row[col] = pd.to_numeric(row[col], errors='coerce')


        if row['comparison_type'] == ('range' or 'Range') and ((pd.isna(row['expected_value'])==False) or (((pd.isna(row['expected_value_min'])==False) and (pd.isna(row['expected_value_max'])==False)) or ((pd.isna(row['range_high'])==False) and (pd.isna(row['range_low'])==False)))):
            min_val = min([x for x in [float(row['expected_value_min']), float(row['range_low']), float(row['expected_value'])] if not math.isnan(x)])
            max_val = max([x for x in [float(row['expected_value_max']), float(row['range_high']), float(row['expected_value'])] if not math.isnan(x)])
            curr_test += f"""
            explanation = '{desc} treatment comparison function. Theoretical value is expected to be between {min_val} and {max_val}.'
            try:"""
            if data_df == "diagnosed":
                curr_test += curr_test1
            
            curr_test+= f"""
                codes = {row['codes']}
                data_per = 100*{data_df}[{data_df}['{row['column_name']}'].astype(str).isin(codes)][{person_id_col}].nunique() / {data_df}[{person_id_col}].nunique()
                res = (min_val<=(data_per)<=max_val)
                output_vals = {{'data_per': data_per, 'range_low': {min_val}, 'range_high': {max_val}}}
                if res == False:
                    fail_exp = '{desc} evaluation in the examined data is ' + str(100*data_per) + '%'
                    explanation += ' ' + fail_exp
                    """
            return curr_test, curr_test_title
                
        elif row['comparison_type'] == 'percentage':
    
            curr_test += f"""
                explanation = '{desc} treatment comparison function. Theoretical value is expected to be {row['expected_value']}.'
                try:
                    codes = {row['codes']}
                    
                    data_per = 100*{data_df}[{data_df}['{row['column_name']}'].astype(str).isin(codes)][{person_id_col}].nunique() / {data_df}[{person_id_col}].nunique()
                    val  = (data_per - {row['expected_value']}) / np.sqrt((data_per*(100 - data_per)+{row['expected_value']}*(100 - {row['expected_value']}))/2)
                    ratio = data_per/{row['expected_value']}
                    res = (abs(val) < 0.2) & (0.85<=ratio<=1.15)
                    output_vals = {{'data_per': data_per, 'expected_value': {row['expected_value']}, 'ratio': ratio, 'smd': val}}
                    if res == False:
                        fail_exp = '{desc} percentage in the examined data is ' + str(data_per)
                        explanation += ' ' + fail_exp
                        """
            return curr_test, curr_test_title
        
        elif row['comparison_type'] == 'less_than':
            for col in ['expected_value_min','range_low','expected_value', 'range_high','expected_value_max']:
                try:
                    row[col] = row[col].replace('%', '').replace('>', '').replace('<', '')
                except:
                    pass
            row[col] = pd.to_numeric(row[col], errors='coerce')

            max_val = max([x for x in [float(row['expected_value_max']), float(row['range_high']), float(row['expected_value']), float(row['expected_value_min']), float(row['range_low'])] if not math.isnan(x)])
    
            curr_test += f"""
                explanation = '{desc} treatment comparison function. Theoretical value is expected to be less than {row['expected_value']}.'
                try:
                    codes = {row['codes']}
                    
                    data_per = 100*{data_df}[{data_df}['{row['column_name']}'].astype(str).isin(codes)][{person_id_col}].nunique() / {data_df}[{person_id_col}].nunique()
                    res = (data_per)<=max_val
                    output_vals = {{'data_per': data_per, 'expected_value': <{max_val}}}
                    if res == False:
                        fail_exp = '{desc} evaluation in the examined data is ' + str(100*data_per) + '%'
                        explanation += ' ' + fail_exp
                        """
            return curr_test, curr_test_title
        
        else:
            return -1
    
    
    elif (row['flag'].lower() == ('demography' or 'demography_diagnosed')) and ((pd.isna(row['expected_value'])==False) or (pd.isna(row['expected_value_min'])==False)):
        if (pd.isna(row['expected_value_max'])==False) and (pd.isna(row['expected_value_min'])==False):
            curr_test += f"""
            explanation = '{desc} - rate is expected to be between {row['expected_value_min']} and {row['expected_value_max']}.'
            try:"""
            if data_df == "diagnosed":
                curr_test += curr_test1 
            curr_test+= f"""codes = {row['codes']}"""
            
            if data_df == "diagnosed":
                curr_test += f"""
                    #% of diagnosed patients with the demographic code of interest
                    ref_for_percentage = data_df[data_df['{row['column_name']}'].astype(str).isin(codes)]
                    """
            else:
                curr_test += f"""
                    ref_for_percentage = {data_df}
                    """
            
            curr_test += f"""
                percentage = 100*{data_df}[{data_df}['{row['column_name']}'].astype(str).isin(codes)][{person_id_col}].nunique() / ref_for_percentage[{person_id_col}].nunique()
                res = ({row['expected_value_min']} <= percentage <= {row['expected_value_max']})
                output_vals = {{'percentage': percentage, 'expected_value_min': {row['expected_value_min']}, 'expected_value_max': {row['expected_value_max']}}}
                if res == False:
                    fail_exp = '{desc} percentage of diagnosed in the evaluated subpopulation in the examined data is ' + str(percentage) + '%'
                    explanation += ' ' + fail_exp
                    """
            return curr_test, curr_test_title
        elif (pd.isna(row['expected_value'])==False):
            curr_test += f"""
            explanation = '{desc} evaluation function. Result is expected to be {row['expected_value']}.'
            try:"""
            if data_df == "diagnosed":
                curr_test += curr_test1 
            curr_test+= f"""codes = {row['codes']}"""
            
            if data_df == "diagnosed":
                curr_test += f"""
                    ref_for_percentage = data_df[data_df['{row['column_name']}'].astype(str).isin(codes)]
                    """
            else:
                curr_test += f"""
                    ref_for_percentage = {data_df}
                    """
            curr_test += f"""
                data_per = 100*{data_df}[{data_df}['{row['column_name']}'].astype(str).isin(codes)][{person_id_col}].nunique() / ref_for_percentage[{person_id_col}].nunique()
                val  = (data_per - {row['expected_value']}) / np.sqrt((data_per*(100 - data_per)+{row['expected_value']}*(100 - {row['expected_value']}))/2)
                ratio = data_per/{row['expected_value']}
                res = (abs(val) < 0.2) & (0.85<=ratio<=1.15)
                output_vals = {{'data_per': data_per, 'expected_value': {row['expected_value']}, 'ratio': ratio, 'smd': val}}
                if res == False:
                    fail_exp = '{desc} percentage in the examined data is ' + str(percentage) + '%'
                    explanation += ' ' + fail_exp
                    """
            return curr_test, curr_test_title
        else:
            return -1
    
    elif (row['flag'].lower() == 'procedure' or row['flag'].lower() == 'lab'):
        if row['comparison_type'] == ('range' or 'Range') or ((pd.isna(row['expected_value'])==False) and (((pd.isna(row['expected_value_min'])==False) and (pd.isna(row['expected_value_max'])==False)) or ((pd.isna(row['range_high'])==False) and (pd.isna(row['range_low'])==False)))):

            if (row['range_high'] == 'np.nan') or (pd.isna(row['range_high'])):
                if pd.isna(row['expected_value_max']) & pd.isna(row['expected_value']):
                    row['range_high'] = np.inf
                elif pd.isna(row['expected_value_max']) and not pd.isna(row['expected_value']):
                    row['range_high'] = row['expected_value']
                else:
                    row['range_high'] = row['expected_value_max']
                
            if (row['range_low'] == 'np.nan') or (pd.isna(row['range_low'])):
                if pd.isna(row['expected_value_min']) & pd.isna(row['expected_value']):
                    row['range_low'] = 0
                elif pd.isna(row['expected_value_min']) and not pd.isna(row['expected_value']):
                    row['range_low'] = row['expected_value']
                else:
                    row['range_low'] = row['expected_value_min']

            curr_test += f"""
            explanation = '{desc} evaluation function. 95% of the population is expected to be between {row['range_low']} and {row['range_high']}.'
            try:"""
            if data_df == "diagnosed":
                curr_test += curr_test1

            curr_test+= f"""
                codes = {row['codes']}
                if {data_df}[{data_df}['{row['column_name']}'].astype(str).isin({row['codes']})][{person_id_col}].nunique() > 0:
                    data_in_range = {data_df}[({data_df}['{row['column_name']}'].astype(str).isin(codes)) & ({data_df}['{row['value_column_name']}'] >= {row['range_low']}) & ({data_df}['{row['value_column_name']}'] <= {row['range_high']})][{person_id_col}].nunique() / {data_df}[{data_df}['{row['column_name']}'].astype(str).isin({row['codes']})][{person_id_col}].nunique()
                    res = (0.9<=(data_in_range/0.95)<=1.1)
                else:
                    data_in_range = 0
                    res = False
                
                output_vals = {{'data_in_range': 100*data_in_range, 'range_low': {row['range_low']}, 'range_high': {row['range_high']}}}
                if res == False:
                    fail_exp = '{desc} evaluation in the examined data is ' + str(100*data_in_range) + '%'
                    explanation += ' ' + fail_exp
                    """
            return curr_test, curr_test_title
        elif row['comparison_type'] == 'less_than':

            row['expected_value_max'] = max([x for x in [float(row['expected_value_max']), float(row['range_high']), float(row['expected_value'])] if not math.isnan(x)])

            curr_test += f"""
            explanation = '{desc} evaluation function. The value is expected to be less than {row['expected_value_max']}.'
            try:"""
            if data_df == "diagnosed":
                curr_test += curr_test1
            curr_test+= f"""
                codes = {row['codes']}
                if {data_df}[{data_df}['{row['column_name']}'].astype(str).isin({row['codes']})][{person_id_col}].nunique() > 0:
                    data_in_range = {data_df}[({data_df}['{row['column_name']}'].astype(str).isin(codes)) & ({data_df}['{row['value_column_name']}'] < {row['expected_value_max']})][{person_id_col}].nunique() / {data_df}[{data_df}['{row['column_name']}'].astype(str).isin({row['codes']})][{person_id_col}].nunique()
                    res = data_in_range > 0.95
                else:
                    data_in_range = 0
                    res = False

                output_vals = {{'data_in_range': 100*data_in_range, 'expected_value': {row['expected_value_max']}}}
                if res == False:
                    fail_exp = '{desc} evaluation in the examined data is ' + str(100*data_in_range) + '%'
                    explanation += ' ' + fail_exp
                    """
            return curr_test, curr_test_title
        elif row['comparison_type'] == 'more_than':

            if (row['expected_value_min'] == 'np.nan') or (pd.isna(row['expected_value_min'])):
                row['expected_value_min'] = min([row['expected_value'], row['range_low']])

            curr_test += f"""
            explanation = '{desc} evaluation function. The value is expected to be more than {row['expected_value_min']}.'
            try:"""
            if data_df == "diagnosed":
                curr_test += curr_test1
            
            curr_test+= f"""
                codes = {row['codes']}
                    
                if {data_df}[{data_df}['{row['column_name']}'].astype(str).isin({row['codes']})][{person_id_col}].nunique() > 0:
                    data_in_range = {data_df}[({data_df}['{row['column_name']}'].astype(str).isin(codes)) & ({data_df}['{row['value_column_name']}'] > {row['expected_value_min']})][{person_id_col}].nunique() / {data_df}[{data_df}['{row['column_name']}'].astype(str).isin({row['codes']})][{person_id_col}].nunique()
                    res = data_in_range > 0.95
                else:
                    data_in_range = 0
                    res = False

                output_vals = {{'data_in_range': 100*data_in_range, 'expected_value': {row['expected_value_min']}}}
                if res == False:
                    fail_exp = '{desc} evaluation in the examined data is ' + str(100*data_in_range) + '%'
                    explanation += ' ' + fail_exp
                    """
            return curr_test, curr_test_title
           
        else:
            return -1

    elif ((row['flag'].lower() == 'procedure' or row['flag'].lower() == 'lab') and (pd.isna(row['expected_value'])==False)):
        if row['comparison_type'] == ('range' or 'Range') and (((pd.isna(row['expected_value_max'])==False) and (pd.isna(row['expected_value_min'])==False)) or ((pd.isna(row['range_high'])==False) and (pd.isna(row['range_low'])==False))):
            curr_test += f"""
            explanation = '{desc} evaluation function. 95% of the population is expected to be between {row['range_low']} and {row['range_high']}.'
            try:"""
            if data_df == "diagnosed":
                curr_test += curr_test1
            curr_test+= f"""
                codes = {row['codes']}
                
                data_in_range = {data_df}[({data_df}['{row['column_name']}'].astype(str).isin(codes)) & ({data_df}['{row['value_column_name']}'] >= {row['range_low']}) & ({data_df}['{row['value_column_name']}'] <= {row['range_high']})][{person_id_col}].nunique() / {data_df}[{data_df}['{row['column_name']}'].astype(str).isin({row['codes']})][{person_id_col}].nunique()
                res = (0.9<=(data_in_range/0.95)<=1.1)
                output_vals = {{'data_in_range': 100*data_in_range, 'range_low': {row['range_low']}, 'range_high': {row['range_high']}}}
                if res == False:
                    fail_exp = '{desc} evaluation in the examined data is ' + str(100*data_in_range) + '%'
                    explanation += ' ' + fail_exp
                    """
            return curr_test, curr_test_title
        elif (row['comparison_type'] == 'less_than') or (pd.isna(row['expected_value']) and (pd.isna(row['expected_value_max'])==False or pd.isna(row['range_high'])==False) and (pd.isna(row['expected_value_min']) and pd.isna(row['range_low']))):
            if (row['expected_value_max'] == 'np.nan') or (row['expected_value_max'] == np.nan):
                row['expected_value_max'] = row['range_high']
            curr_test += f"""
            explanation = '{desc} evaluation function. The value is expected to be less than {row['expected_value_max']}.'
            try:"""
            if data_df == "diagnosed":
                curr_test += curr_test1
            curr_test+= f"""
                codes = {row['codes']}
                
                data_in_range = {data_df}[({data_df}['{row['column_name']}'].astype(str).isin(codes) & ({data_df}['{row['value_column_name']}'] < {row['expected_value_max']})][{person_id_col}].nunique() / {data_df}[{data_df}['{row['column_name']}'].astype(str).isin({row['codes']})][{person_id_col}].nunique()
                res = data_in_range > 0.95
                output_vals = {{'data_in_range': 100*data_in_range, 'expected_value': {row['expected_value_max']}}}
                if res == False:
                    fail_exp = '{desc} evaluation in the examined data is ' + str(100*data_in_range) + '%'
                    explanation += ' ' + fail_exp
                    """
            return curr_test, curr_test_title
        elif (row['comparison_type'] == ('greater_than' or 'more_than')) or (pd.isna(row['expected_value']) and (pd.isna(row['expected_value_max']) and pd.isna(row['range_high'])) and (pd.isna(row['expected_value_min'])==False or pd.isna(row['range_low'])==False)):
            if (row['expected_value_min'] == 'np.nan') or (row['expected_value_min'] == np.nan):
                row['expected_value_min'] = row['range_low']
            curr_test += f"""
            explanation = '{desc} evaluation function. The value is expected to be greater than {row['expected_value_min']}.'
            try:"""
            if data_df == "diagnosed":
                curr_test += curr_test1
            curr_test+= f"""
                codes = {row['codes']}
                
                data_in_range = {data_df}[({data_df}['{row['column_name']}'].astype(str).isin(codes) & ({data_df}['{row['value_column_name']}'] > {row['expected_value_min']})][{person_id_col}].nunique() / {data_df}[{data_df}['{row['column_name']}'].astype(str).isin({row['codes']})][{person_id_col}].nunique()
                res = data_in_range > 0.95
                output_vals = {{'data_in_range': 100*data_in_range, 'expected_value': {row['expected_value_min']}}}
                if res == False:
                    fail_exp = '{desc} evaluation in the examined data is ' + str(100*data_in_range) + '%'
                    explanation += ' ' + fail_exp
                    """
            return curr_test, curr_test_title
        else:
            return -1
    else:
        return -1


def write_tests(diagnosis, region, coding, drug, procedure, lab, data_struct, model):
    global messages, client

    client = connect_to_openAI(model)
    
    tests = pd.read_csv(f"validated/test_csvs/{diagnosis}_expected_params_comorbidities.csv", encoding="utf-8")
    tests.replace('np.nan', np.nan, inplace=True)
    
    tests2 = pd.read_csv(f"validated/test_csvs/{diagnosis}_expected_params_genpop_demo.csv", encoding="utf-8")
    tests2.replace('np.nan', np.nan, inplace=True)
    
    tests3 = pd.read_csv(f"validated/test_csvs/{diagnosis}_expected_params_drugs.csv", encoding="utf-8")
    tests3.replace('np.nan', np.nan, inplace=True)
    
    tests4 = pd.read_csv(f"validated/test_csvs/{diagnosis}_expected_params_diagnosed_genpop.csv", encoding="utf-8")
    tests4.replace('np.nan', np.nan, inplace=True)
    
    tests5 = pd.read_csv(f"validated/test_csvs/{diagnosis}_expected_params_procedures.csv", encoding="utf-8")
    #tests5 = pd.concat([tests5, pd.read_csv(f"test_csvs/{diagnosis}_expected_params_labs.csv", encoding="utf-8")], axis=0)
    tests5.replace('np.nan', np.nan, inplace=True)

    tests5.drop_duplicates(subset=['description','expected_value','range_low','range_high','expected_value_min','expected_value_max'], inplace=True)
    
    stats = pd.read_csv(f"statistics/{diagnosis}_statistics_in_{region}_validated.csv", encoding="utf-8")
    stats.replace('np.nan', np.nan, inplace=True)
    stats.columns = stats.columns.str.replace(" ","")
    
    col_conversion = pd.read_csv(f"test_csvs/{diagnosis}_convert_to_datastruct.csv", encoding="utf-8")
    col_conversion.column_name = col_conversion.column_name.str.capitalize()
    stats.columns = stats.columns.str.replace(" ","")
    age_dist_stats = pd.read_csv(f"statistics/{diagnosis}_age_stats_in_{region}_validated.csv", encoding="utf-8")
    age_dist_stats.columns = age_dist_stats.columns.str.replace(" ","")
    
    code_list = pd.read_csv(f"statistics/{diagnosis}_{coding}_diagnosis_codes_in_{region}.csv", encoding="utf-8")
    word_to_find = 'code'
    matching_columns = [col for col in code_list.columns if ('code' or coding.lower()+' code' or coding).lower() in col.lower()]
    code_column = matching_columns[0]

    code_list = code_list[code_column].to_list()
    code_list = [str(item) for item in code_list]

    person_id_col = col_conversion[col_conversion['generic']=='personID']['column_name'].item()
    code_col = col_conversion[col_conversion['generic']=='code']['column_name'].item()
    code_date_col = col_conversion[col_conversion['generic']=='codeDate']['column_name'].item()
    birth_date_col = col_conversion[col_conversion['generic']=='birthDate']['column_name'].item()

    written_tests = []
    written_additional_tests = []

    written_additional_tests.append(f"## Filename: unit_test0.py\n\n")

    chk_types = f"""
    import pandas as pd
    import numpy as np
    import math
    from scipy.special import stdtr

    def dftest_check_data_types(data_df):
        output_vals = {{}}
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
            return res\n"""

    written_additional_tests.append(chk_types)

    chk_incidence = f"""
    def dftest_check_incidence(data_df):
        # ref: {stats['reference'].values}
        output_vals = {{}}
        test_flag = 'ok'
        explanation = 'Five year mean incidence comparison function (2016-2021). Theoretical value is expected to be {stats['Incidence'][len(stats)-1]}.'
        try:
            # Diagnosis codes for {diagnosis}
            diagnosis_codes = {code_list}
            # Initialize an empty list to store incidence rates
            incidence = []
            # Loop through the years 2016 to 2021
            for i in range(0, 6):
                year = 2016 + i
                # Filter the dataframe for the specific year
                df_year = data_df[data_df[{code_date_col}].dt.year == year]
                # Calculate the incidence rate for the year
                incidence_rate = 100*df_year[df_year[{code_col}].astype(str).isin(diagnosis_codes)][{person_id_col}].nunique() / data_df[{person_id_col}].nunique()
                # Append the incidence rate to the list
                incidence.append(incidence_rate)
            # Calculate the mean incidence rate
            mean_incidence = np.mean(incidence)
            expected_incidence = {stats['Incidence'][len(stats)-1]}
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
            return res\n"""

    written_additional_tests.append(chk_incidence)

    chk_prevalence = f"""
    def dftest_check_prevalence(data_df):
        # ref: {stats['reference'].values}
        output_vals = {{}}
        test_flag = 'ok'
        explanation = 'Prevalence comparison function. Theoretical value is expected to be {stats['Prevalence'][len(stats)-1]}.'
        try:
            # Diagnosis codes for {diagnosis}
            diagnosis_codes = {code_list}
            # Calculate the prevalence of {diagnosis}
            prevalence = 100*data_df[data_df[{code_col}].astype(str).isin(diagnosis_codes)][{person_id_col}].nunique() / data_df[{person_id_col}].nunique()
            expected_prevalence = {stats['Prevalence'][len(stats)-1]}
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
            return res\n"""
    
    written_additional_tests.append(chk_prevalence)

    try:
        chk_age_dist_smlrty = f"""
        def dftest_calculate_age_distribution(data_df):
            # ref: {age_dist_stats['reference'].values}
            # Calculates and compares age distribution of {diagnosis} patients
            limit = 0.05
            #calculate age distribution of patients
            try:
                
                data_df = data_df[data_df['{code_col}'].astype(str).isin({code_list})]
                data_df['{code_date_col}'] = pd.to_datetime(data_df['{code_date_col}'])
                data_df[{birth_date_col}] = pd.to_datetime(data_df[{birth_date_col}])
                data_df['diagnosis_age'] = data_df['{code_date_col}'].dt.year - data_df[{birth_date_col}].dt.year
                data_df = data_df.sort_values(by=['{person_id_col}','{code_date_col}'], ascending=True)
                unique_patients = data_df.dropna(subset=['{code_date_col}'], axis=0).drop_duplicates(subset=['{person_id_col}'], keep='first')
                data_dist = unique_patients['diagnosis_age'].value_counts()
                data_stats = unique_patients['diagnosis_age'].describe()
                var_data = data_stats['std'].item()**2
                var_th = {age_dist_stats['std'].item()**2}
                df = ((var_data/data_stats['count'].item()) + (var_th/({age_dist_stats['count'].item()})))**2/(var_data**2/((data_stats['count'].item()**2) * (data_stats['count'].item() -1)) + var_th**2/({age_dist_stats['count'].item()**2} * ({age_dist_stats['count'].item()} - 1)))
                Sx_data = data_stats['std'].item()/math.sqrt(data_stats['count'].item())
                Sx_th = {age_dist_stats['std'].item()}/math.sqrt({age_dist_stats['count'].item()})
                tt = (data_stats['mean_age'].item() - {age_dist_stats['mean_age'].item()})/math.sqrt(Sx_data+Sx_th)
                pval = 2*stdtr(df, -np.abs(tt))
                res = pval
                
                if pval > limit:
                    binary = "Pass"
                    explanation = 'Age distribution matches the theoretical distribution - {age_dist_stats['mean_age'].item()} +- {age_dist_stats['std'].item()}'
                else:
                    binary = "Fail"
                    explanation = 'Age distribution is expected to be ' + str({age_dist_stats['mean_age'].item()}) + ' +- ' + str({age_dist_stats['std'].item()}) + '; in the data it is ' + str(data_stats['mean_age'].item()) + ' +- ' + str(data_stats['std'].item())
            
            except Exception as e:
                res = False
                binary = "Error"
                explanation = str(e)
                
            finally:
                output_vals = {{}}
                output_vals['pval'] = res
                output_vals['explanation'] = explanation
                output_vals['binary'] = binary
                dftest_calculate_age_distribution.explanation = str(output_vals)
            
            return res

            """

        written_additional_tests.append(chk_age_dist_smlrty)
        
    except:
        chk_mean_age_smlrty = f"""
        def dftest_calculate_age_distribution(data_df):
            # ref: {age_dist_stats['reference'].values}
            explanation = 'Compares mean diagnosis age of {diagnosis} patients to the theoretical mean age. Expected value is {age_dist_stats['mean_age'].item()}.'
            # calculate age at diagnosis
            try:
                data_df = data_df[data_df['{code_col}'].astype(str).isin({code_list})]
                data_df['{code_date_col}'] = pd.to_datetime(data_df['{code_date_col}'])
                data_df[{birth_date_col}] = pd.to_datetime(data_df[{birth_date_col}])
                data_df['diagnosis_age'] = data_df['{code_date_col}'].dt.year - data_df[{birth_date_col}].dt.year
                data_df = data_df.sort_values(by=['{person_id_col}','{code_date_col}'], ascending=True)
                unique_patients = data_df.dropna(subset=['{code_date_col}'], axis=0).drop_duplicates(subset=['{person_id_col}'], keep='first')
                mean_age = unique_patients['diagnosis_age'].mean()
                theoretical_mean_age = {age_dist_stats['mean_age'].item()}
                val  = (mean_age - theoretical_mean_age) / np.sqrt((mean_age*(100 - mean_age)+theoretical_mean_age*(100 - theoretical_mean_age))/2)
                ratio = mean_age/theoretical_mean_age
                res = (abs(val) < 0.2) & (0.85<=ratio<=1.15)
                output_vals = {{'data_per': mean_age, 'expected_value': theoretical_mean_age, 'ratio': ratio, 'smd': val}}
                if res == False:
                    fail_exp = 'Mean diagnosis age in the examined data is ' + str(mean_age).
                    explanation += ' ' + fail_exp
                
            except Exception as e:
                res = False
                binary = "Error"
                explanation = str(e)
                
            finally:
                output_vals = {{}}
                output_vals['pval'] = res
                output_vals['explanation'] = explanation
                output_vals['binary'] = binary
                dftest_calculate_age_distribution.explanation = str(output_vals)
            
            return res

            """

        written_additional_tests.append(chk_mean_age_smlrty)
    finally:
        written_additional_tests = "".join(written_additional_tests)


    for count, table in enumerate([tests, tests2, tests3, tests4, tests5]):
        if count == 3 or count == 0:
            diagnosed = True
        else:
            diagnosed = False

        written_tests_table = []
        written_tests_table.append(f"# Filename: unit_test{count+1}.py\n\n")
        table.columns = [col.lower().replace(" ", "_") for col in table.columns]
        newcols = []
        for column in table.columns:
            while column[0] == '_':
                column = column[1:]
            while column[-1] == '_':
                column = column[:-1]
            newcols.append(column)
        table.columns = newcols

        table.replace({"np.nan": np.nan}, inplace=True)
        func_counter = 0

        for index, row in table.iterrows():
            if row['data_type']=='date' or row['data_type']=='datetime':
                continue
            elif row['codes']==np.nan and row['column_name']!=row['value_column_name']:
                continue
            elif (row['expected_value']=='np.nan' and row['expected_value_max']=='np.nan' and row['expected_value_min']=='np.nan'):
                continue
            elif (row['expected_value']==np.nan and row['expected_value_max']==np.nan and row['expected_value_min']==np.nan):
                continue
            elif (pd.isnull(row['expected_value']) and pd.isnull(row['expected_value_max']) and pd.isnull(row['expected_value_min']) and pd.isnull(row['range_low']) and pd.isnull(row['range_high'])):
                continue
            elif ((pd.isnull(row['expected_value'])==False or pd.isnull(row['expected_value_max'])==False or pd.isnull(row['expected_value_min'])==False or pd.isnull(row['range_low'])==False or pd.isnull(row['range_high'])==False) and pd.isnull(row['codes'])):
                continue
            else:
                if (('_men' or '_women') in row['description'].lower()) and (pd.isnull(row['codes'])==False):
                    res = create_tests(row, "subpop_data", coding, diagnosis, code_list, col_conversion)
                    if res == -1:
                        continue
                    else:
                        curr_test, curr_test_title = res

                elif diagnosed:
                    res = create_tests(row, "diagnosed", coding, diagnosis, code_list, col_conversion)
                    if res == -1:
                        continue
                    else:
                        curr_test, curr_test_title = res

                elif (pd.isnull(row['codes'])==False):
                    res = create_tests(row, "data_df", coding, diagnosis, code_list, col_conversion)
                    if res == -1:
                        continue
                    else:
                        curr_test, curr_test_title = res
                               
                curr_test += f"""
                    except Exception as e:
                        res = False
                        test_flag = "error"
                        explanation += ' ' + str(e).replace('"', "").replace("'", "")
                        
                    finally: 
                        output_vals['explanation'] = explanation
                        output_vals['test_flag'] = test_flag
                        {curr_test_title}.explanation = str(output_vals)
                        return res\n\n"""
                func_counter += 1
                written_tests_table.append(curr_test)
        written_tests_table.append(f"\n\n # {func_counter} functions\n\n")
        written_tests.append("".join(written_tests_table))
    
   
    messages = []
  
    message_queue = [f"""Your job is to review a given python code and adjust the provided functions according to the following data dictionary:

            {data_struct}

            The dataset uses {coding} for medical codes, {drug} for drug classification, {lab} for lab test classification and {procedure} for procedure classification. Make minimal 
            adjustments to the functions, ensuring that all code remains within the function bodies and aligns with the field names in the dataset. 
            Avoid using placeholders or leaving any variables for the user to fill in. Do not provide examples or use demonstration values. Refrain 
            from using SQL queries; instead, stick strictly to the provided code and adjust it according to the dataset field names (columns). 
            Give me your best answer. If needed, search the web. Always provide references. 
            When asked for Python code, CSVs or text, always format them using triple backticks as follows: '```python', '```csv' and '```text', respectively, and end with '```'.
            At the top of each block (Python code, CSV, or text), include the required title or filename as part of the response. This title or filename must appear at the start of each block:
            
            ```python
            Filename: example file name
            # your python code here
            ```
            
            or 
            
            ```csv
            Title: example title
            # your csv code here
            ```
            
            If no filename or title was provided in the reqest, please avoid including a filename in the response.

            When asked to adjust field names or columns, modify only the provided code to match the field names (columns) specified in the data dictionary. Do not remove any comments from the code. 
            Avoid creating new functions or writing code beyond the adjustments requested—stick strictly to the given code. If required, fill in medical diagnosis, drug, lab, or procedure codes where angle 
            brackets are present. Provide references and verify your response when necessary. Do **not** refactor the Python code. 
            Do **not** add any additional function. 
            Do **not** remove commnets from the code.
            Do **not** uncoment filename lines or existing comments.
            Do **not** add any additional symbols or signs.
            **Do not** modify the parentheses or brackets in the code.
            If data is missing, do not impute hypothetical or fake data.
            If multiple tests have the same name, add '_1', '_2', etc. to the function name.
            Please confirm understanding of these instructions without replying.""",

            f"""Please adjust the following functions in the context of the provided data dictionary.
            
            Make sure field (column) names match the ones in the data dictionary. 
            Change the python code as little as possible. Keep the code as close to its original form. The functions are as follows: \n\n\n""" 
            + written_additional_tests + f"""\n\n\n Wrap the code in a python code block. No need for example run. Do not leave any variables for the user to fill. 
            Work step by step and make sure all field/column names match the ones in the provided data dictionary. Do not suggest refactoring. Adjust only column 
            names. Do **not** remove commnets from the code or uncoment them. Do **not** add any additional functions. 
             **Avoid adding un-needed signs and symbols.**
             **Do not add parentheses**
            If multiple tests have the same name, add '_1', '_2', etc. to the function name.
            Please remove symbols (like percentage signs) where might cause errors (e.g when NOT in strings).
            Replace 'nan'/'NaN' variations with np.nan""",

    ]

    count = 1
    for k,table_tests in enumerate(written_tests):
        if table_tests == '':
            continue
        else:
            message_queue.append(f"""In the context of the following data dictionary: 
                                 
                                 {data_struct} 
                                 
                                 Please adjust the following list of functions. Make sure field (column) names match the ones in the provided data dictionary. 
                                 Other than the column names, keep the functions exactly as provided. Do not refactor the python code. The functions are as follows:
                                 
                                 {table_tests} 
                                 
                                 Wrap the code in a python code block. Do not leave any variables for the user to fill. 
                                 Work step by step and make sure all field/column names match the ones in the provided data dictionary. 
                                 Do not refactor the given functions; keep them as close as possible to the way they are written. 
                                 **Avoid removing any comments in the provided functions. **
                                 **Avoid adding un-needed signs and symbols.**
                                 **Do not add parentheses**
                                 If multiple tests have the same name, add '_1', '_2', etc. to the function name.
                                 Please remove symbols (like percentage signs) where might cause errors (e.g when NOT in strings).
                                 Avoid random function writing. Stick to the provided code and adjust it to fit the requirements. 
                                 Do **not** refactor the Python code. Do not add any additional functions. Do not remove functions, 
                                 unless they are exact dupicates in all aspects.""")
            count += 1
    

    specific = f"{diagnosis}_{region}".replace(" ", "_")

    
    # communicate with Azure OpenAI API:
    for i, message in enumerate(message_queue):
        messages1 = []
        if i==0:
            messages.append({"role": "system", "content": message})
            role = "system"            
        else:
            role = "user"
            messages1.append(messages[0])
            messages1.append({"role": "user", "content": message})
            role = "user"
            messages1 = LLMwrapper(messages1, client, model, role=role ,temperature = 0).return_conversation()

            messages += messages1[1:]

    # Write all in a txt:
    now = str(dt.datetime.now())
    count = 0
    
    #os.chdir('validated')
    with open('logs/%s_tests.txt' %(diagnosis), 'w', encoding='UTF-8') as f:
        f.write("%s \n\n" %now)
        with open(f"output/pecking_order_{specific}.py", 'w', encoding='UTF-8') as f2:
            for message in messages:
                if message['role'] == 'assistant':
                    f.write(message['content'] + "\n\n")
                    if (("```python") in message['content']):
                        code = make_all_py(message['content'], count)
                    if ("Filename:") in message['content']:
                        f2.write(code+"\n\n")
                
        f2.close()
        f.close()
    
    return