import os
import numpy as np
import pandas as pd
import datetime as dt
from ask_gpt import LLMwrapper
from query_bing import query_bing
from vector_query import get_concepts
from connect_openAI import connect_to_openAI
from extraction_functions import make_df, make_list, json_to_df, make_py, make_all_py, extract_code

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
np.set_printoptions(threshold=np.inf)

def validate_suggestions(diagnosis, region, coding, drug, procedure, lab, model):
    """This function validates the suggestions by checking the reference values and providing feedback on their correctness."""

    global messages, client

    client = connect_to_openAI(model)

    

    tests = pd.read_csv(f"test_csvs/{diagnosis}_expected_params_comorbidities.csv", encoding="utf-8")
    tests.replace('np.nan', np.nan, inplace=True)
    
    tests2 = pd.read_csv(f"test_csvs/{diagnosis}_expected_params_genpop_demo.csv", encoding="utf-8")
    tests2.replace('np.nan', np.nan, inplace=True)
    
    tests3 = pd.read_csv(f"test_csvs/{diagnosis}_expected_params_drugs.csv", encoding="utf-8")
    tests3.replace('np.nan', np.nan, inplace=True)
    
    tests4 = pd.read_csv(f"test_csvs/{diagnosis}_expected_params_diagnosed_genpop.csv", encoding="utf-8")
    tests4.replace('np.nan', np.nan, inplace=True)
    
    tests5 = pd.read_csv(f"test_csvs/{diagnosis}_expected_params_procedures.csv", encoding="utf-8")
    tests5 = pd.concat([tests5, pd.read_csv(f"test_csvs/{diagnosis}_expected_params_labs.csv", encoding="utf-8")], axis=0)
    tests5.replace('np.nan', np.nan, inplace=True)
    
    stats = pd.read_csv(f"statistics/{diagnosis}_statistics_in_{region}.csv", encoding="utf-8")
    stats.replace('np.nan', np.nan, inplace=True)
    stats.columns = stats.columns.str.replace(" ","")

    age = pd.read_csv(f"statistics/{diagnosis}_age_stats_in_{region}.csv", encoding="utf-8")
    age.replace('np.nan', np.nan, inplace=True)
    age.columns = age.columns.str.replace(" ","")
    
    for count, table in enumerate([tests, tests2, tests3, tests4, tests5]):
        if count == 3 or count == 0:
            diagnosed = 'True'
        else:
            diagnosed = 'False'

        table.columns = table.columns.str.strip()
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
        messages = []
        replies = []
        replies2 = []

        for index, row in table.iterrows():
            messages.append({"role": "user", "content": f"""For the following test, please evaluate the reference value by searching for the correct reference value. 
        It appears as the expected value or range. Please make sure that the reference value is correct. 
        If there is no available data for {region}, please provide the reference value for the whole country, continent or global statistics.
        If it is incorrect, please provide the correct value. If you are unsure, please indicate that as well. 
        For disease-related tests, the reference value represents the prevalence of that disease among patients with {diagnosis} in {region}.
        Demographics - unless diagnosed is 'True', the percentage is relative to the general population in {region}. 
        For those diagnosed with {diagnosis} in {region}, diagnosed flag will be 'True', and the percentage is the percentage of {diagnosis} patients among the evaluated statistic 
        (e.g, percentage of diagnosed women among all women or percentage of patients prescribed a drug among all patients with {diagnosis}).
        
        The test suggestion is as follows:
        
        Column names: {list(row.index)}
        Values: {row.values}

        diagnosed: {diagnosed}

        Please provide your feedback in the following format:
        1. Test description: [your answer]
        2. Correct reference value: [your answer]
        3. Provided reference value: [your answer]
        4. Feedback: [your answer - Correct or Incorrect or Unsure]
        5. Fuction recommendation: [your answer - Fix (if incorrect), No fix (if correct), Remove (if unsure)]"""})
            
            thread = client.agents.create_thread()
            role = "user"

            reply = LLMwrapper(messages=messages, client=client, model=model, assistant=True, role=role, temperature=0, thread=thread).return_conversation()

            replies.append(reply[-1]['content'])

            ref_loc = replies[-1].find("References:")

            messages.append({"role": "user", "content": f"""If according to your feedback the test suggestion needs fixing due to reference value correction, 
                     please provide it betweeen triple backticks (```csv). use a vertical line | as separator.
                    do not change anything but the reference value and the comparison type, if needed.
                    Strictly stick to the original field names and order. To the field names add 'fixed' and 'remove'.
                    Set 'fixed' to be 'True' to the test suggestion if the function needs to be fixed. Set it to be 'False' otherwise.   
                     Make sure the fixed value corrersponds with the correct value you found.
                    If the expected value is a range and not a single value, please fill the range_high and range_low columns with the correct values, and remove the incorrect value. In that case - change the comparison_type to 'range'.
                    Please make sure the numbers are in the correct location (minimum and maximum or high and low).
                    The comparison_type can also be set to 'less_than' or 'greater_than', in there is a minimum or a maximum only value, respectively.
                    If you recommended removing the test, please set the 'remove' column in the test suggestion to be 'True'. No need to fix it in that case. 
                    If the column needs to be fixed, fix it, set 'fixed' to be 'True' and set 'remove' column to be 'False'.
                    If a test repeats - in terms of 'description' and 'expected_value' or range columns, please set the 'remove' column to be 'True' for the repeated test suggestion.
                    Please add the following references (including urls) to the 'references' column in the corrected csv. Add all the values in the 'references' column in parentheses "".
                                                 
                             {replies[-1][ref_loc:]}

                    Return the test anyway, even if it is correct, with the additional columns (both set to 'False', if fix or removal isn't suggested)."""})

            reply = LLMwrapper(messages=messages, client=client, model=model, assistant=True, role=role, temperature=0, thread=thread).return_conversation()

            replies2.append(reply[-1]['content'])

        dfs = []
        for i, reply in enumerate(replies2):
            d = make_df(reply)[1]
            #d = d.transpose().reset_index(drop=True).transpose().set_index(0)
            #d = d.transpose()
            dfs.append(d)

        df = pd.concat(dfs, axis=0, ignore_index=True)
        df.replace('False', False, inplace=True)
        df.replace('True', True, inplace=True)
        df.replace('np.nan', np.nan, inplace=True)
        df.replace('nan', np.nan, inplace=True)
        df.replace('None', np.nan, inplace=True)
        df.replace('none', np.nan, inplace=True)
        df.replace('NaN', np.nan, inplace=True)
        if count == 0:
            name = f"{diagnosis}_expected_params_comorbidities.csv"
        elif count == 1:
            name = f"{diagnosis}_expected_params_genpop_demo.csv"
        elif count == 2:
            name = f"{diagnosis}_expected_params_drugs.csv"
        elif count == 3:
            name = f"{diagnosis}_expected_params_diagnosed_genpop.csv"
        elif count == 4:
            name = f"{diagnosis}_expected_params_procedures.csv"
        elif count == 5:
            name = f"{diagnosis}_statistics_in_{region}.csv"

        df[df['remove']==False].to_csv(f"validated/test_csvs/{name}", index=False, encoding="utf-8")


    # edit statistics
    messages = []
    replies = []

    messages.append({"role": "user", "content": f"""For the following statistics, please evaluate the reference value by searching for the correct reference value. 
        It appears as the expected value or range. Please make sure that the reference value is correct. 
        If there is no available data for {region}, please provide the reference value for the whole country, continent or global statistics.
        If it is incorrect, please provide the correct value. If you are unsure, please indicate that as well. 
        
        The statistics are for {diagnosis} in {region}:
        
        {stats}

        Please provide your feedback in the following format for each statistic:
        1. Statistic: [your answer]
        2. Correct reference value: [your answer]
        3. Provided reference value: [your answer]
        4. Feedback: [your answer - Correct or Incorrect or Unsure]
        5. Recommendation: [your answer - Fix (if incorrect), No fix (if correct), Remove (if unsure)]"""})
            
    thread = client.agents.create_thread()
    role = "user"

    reply = LLMwrapper(messages=messages, client=client, model=model, assistant=True, role=role, temperature=0, thread=thread).return_conversation()

    replies.append(reply[-1]['content'])

    ref_loc = replies[-1].find("References:")

    messages.append({"role": "user", "content": f"""Please provide the modified statistics in a similar format as the original, betweeen triple backticks (```csv). 
                     use a vertical line | as separator.
                     If according to your feedback the statitic suggestion needs fixing due to reference value correction, please correct it.
            do not change anything but the reference value.
            Strictly stick to the original field names and order.
            Make sure the fixed value corrersponds with the correct value you found.
            If you recommended removing the statistic, replace the relevant statistic with 'np.nan'. 
            Please add the following references (including urls) to the 'reference' column in the corrected csv. Add all the values in the 'reference' column in parentheses "".
                                            
            {replies[-1][ref_loc:]}

            """})

    reply = LLMwrapper(messages=messages, client=client, model=model, assistant=True, role=role, temperature=0, thread=thread).return_conversation()
    d = make_df(reply[-1]['content'])[1]
    name = f"{diagnosis}_statistics_in_{region}_validated.csv"
    d.to_csv(f"statistics/{name}", index=False, encoding="utf-8")


    messages = []
    replies = []

    messages.append({"role": "user", "content": f"""For the following statistics, please evaluate the reference value by searching for the correct reference value. 
        It appears as the expected value or range. Please make sure that the reference value is correct. 
        If there is no available data for {region}, please provide the reference value for the whole country, continent or global statistics.
        If it is incorrect, please provide the correct value. If you are unsure, please indicate that as well. 
        
        The statistics are for {diagnosis} in {region}:
        
        {age}

        Please provide your feedback in the following format for each statistic:
        1. Statistic: [your answer]
        2. Correct reference value: [your answer]
        3. Provided reference value: [your answer]
        4. Feedback: [your answer - Correct or Incorrect or Unsure]
        5. Recommendation: [your answer - Fix (if incorrect), No fix (if correct), Remove (if unsure)]"""})
            
    thread = client.agents.create_thread()
    role = "user"

    reply = LLMwrapper(messages=messages, client=client, model=model, assistant=True, role=role, temperature=0, thread=thread).return_conversation()

    replies.append(reply[-1]['content'])

    ref_loc = replies[-1].find("References:")

    messages.append({"role": "user", "content": f"""Please provide the modified statistics in a similar format as the original, betweeen triple backticks (```csv). 
                     use a vertical line | as separator.
                     If according to your feedback the statitic suggestion needs fixing due to reference value correction, please correct it.
            do not change anything but the reference value.
            Strictly stick to the original field names and order.
            Make sure the fixed value corrersponds with the correct value you found.
            If you recommended removing the statistic, replace the relevant statistic with 'np.nan'. 
            Please add the following references (including urls) to the 'reference' column in the corrected csv. Add all the values in the 'reference' column in parentheses "".
                                            
            {replies[-1][ref_loc:]}

            """})

    reply = LLMwrapper(messages=messages, client=client, model=model, assistant=True, role=role, temperature=0, thread=thread).return_conversation()
    d = make_df(reply[-1]['content'])[1]
    name = f"{diagnosis}_age_stats_in_{region}_validated.csv"
    d.to_csv(f"statistics/{name}", index=False, encoding="utf-8")
