import glob
import numpy as np
import pandas as pd
import datetime as dt
from ask_gpt import LLMwrapper
from extraction_functions import make_df
from connect_openAI import connect_to_openAI

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def free_range_testing(diagnosis, region, coding, drug, procedure,  lab, data_struct, model):
    # gpt model for use
    global messages, client

    client = connect_to_openAI(model)

    file = glob.glob('output/*_insights.txt')
    insights = open(file[0], encoding="utf-8").read()
    file = glob.glob('output/%s_%s_%s_*.txt' %(diagnosis,coding,region))
    info = open(file[0], encoding="utf-8").read()
    
    #age_dist = pd.read_csv(f"statistics/{diagnosis}_age_distribution_in_{region}.csv")
    #drugs = pd.read_csv(f"statistics/{diagnosis}_drug_codes_in_{region}.csv")
    #procedures = pd.read_csv(f"statistics/{diagnosis}_procedure_codes_in_{region}.csv")
    #diag_codes = pd.read_csv(f"statistics/{diagnosis}_diagnosis_codes_in_{region}.csv") 
    #stats = pd.read_csv(f"statistics/{diagnosis}_statistics_in_{region}.csv")
    #comorbidities = pd.read_csv(f"statistics/{diagnosis}_comorbidities_in_{region}.csv")

    messages = []

    system_prompt = f"""We will create a table of values to evaluate. Please stick to the provided information, unless specifically asked to provide additional information
         which was not mentioned in the files. Include medical, drug, and procedure classification coding where relevant. Use {coding} for diagnosis classification codes, 
        {drug} for drug classification codes, {procedure} for procedures, {lab} for lab measurement classification codes and {coding} and gender, race and ethnicity classification for demographic coding. 
        If unsure, respond with "I am unsure."
        Make sure the CSVs do not contain anything that will prevent them from being loaded into a pandas dataframe.

        When asked for CSV tables:
        Use | (vertical bar) as the separator.
        Enclose the table in '```csv' and '```'.
        Exclude any symbols other than those specified.
        Separate the text and table clearly.
        Create all tables with the following columns: 'flag','column name','codes','data type','value column name','description','expected value',
        'expected value max','expected value min','range low','range high','comparison type','references'

        If there are multiple classification codes for a specific concept, provide them as a list in the 'codes' column (e.g, if there are multiple codes for a specific diagnosis, 
        drug, procedure, lab test or a demographic property). 
        **Please create a separate row for each subpopulation (e.g. for gender - separate rows for male and for female, as well as for the different race and ethnicity options).**

        Gender, race and ethnicity categories are in the data dictionary 'description' column and should be used as the possible code values for the demographic subpopulations.

        If there is a single expected value, fill "expected value min" and "expected value max" 'with np.nan', and fill only "expected value" with the value.
        "expected value min" is used when the expected result is greater than the expected value, "expected value max" is used when the expected result is less than the expected value.
        If we expect a range of values, fill "range low" and "range high".
        'column name' should contain the name of the column from the provided data dictionary that holds the classifiction codes.
        "value column name" should contain the name of the column from the provided data dictionary that holds the recorded value for the test or procedure or measurement, if applicable
        If there are multiple medical, drug, lab or procedure classification codes related to a specific concept name, add them as a list in the relevant classification code-related column. 
        Ensure all tables can be concatenated.
        For date-related data, use columns with datetime values, if available.
        For each diagnosis ({coding}), drug ({drug}), measurement/lab test ({lab}) and procedure ({procedure}) code, provide **only** the relevant meaning/concept name in the 
        'description' column. Double check the meaning and provide references for the statistical values.
        Provide your response step by step and offer your best possible answer. 
        Provide references for all descriptions, code meanings, and for the statistical values.
        
        When asked for CSVs or text, always format them using triple backticks as follows: '```csv' or '```text', 
        respectively, and end with '```'. At the top of each block (CSV, or text), include the required title or filename as part 
        of the response. This title or filename must appear at the start of each block:
                
        ```csv
        Title: example title
        # your csv code here
        ```
        
        If no filename or title was provided in the reqest, please avoid including a filename in the response.
        Please confirm understanding of these instructions without replying.""",

    message_queue1 = [
        # convert_to_datastruct - conversion assistance table
        f"""You are given a database schema where each row specifies a table name, column name, and description.
        Given the following schema:

        {data_struct}
        
        Identify the table name, column name, and description for the field related to patient's date of birth. Return the result in the following format:

        Table: <table_name>
        Column: <column_name>
        Description: <description>""",

        f"""Given the following schema:

        {data_struct}

        Identify the table name, column name, and description for the field that stores **diagnosis code** or **concept identifier** entries. 
        Focus on fields that reference standardized vocabularies or classification systems. 
        Return the result in the following format:

        Table: <table_name>
        Column: <column_name>
        Description: <description>""",

        f"""Look at the demography and diagnoses using the relevant columns from:
        
        {data_struct}

        Identify the table name, column name, and description for the field related to "diagnosis first date". Return the result in the following format:

        Table: <table_name>
        Column: <column_name>
        Description: <description>""",

        f"""Look at the demography and diagnoses using the relevant columns from:

        {data_struct}

        Identify the table name, column name, and description for the field related to "Person's unique identifier". Return the result in the following format:

        Table: <table_name>
        Column: <column_name>
        Description: <description>""",

        f"""Based on all your previous answers, create a table with the following columns: 
        'table_name', 'column_name', 'description', 'generic'. 
        Populate the table with these specific descriptions: birth date, diagnosis code, diagnosis first date, and unique person identifier 
        Add the following to 'generic' column, according to the proper rows: 'personID', 'birthDate', 'code', 'codeDate'. Inclue all of these.
        
        The 'code' and 'codeDate' columns must refer to the {coding} medical coding system, excluding any other coding systems that may be present. 
        'codeDate' should refer to the date and time of the diagnosis.
        'birthDate' is the date of birth of the person.
        All fields are mandatory. If a field is irrelevant, fill it with np.nan.
        Wrap the table in a CSV code block using '```csv' and '```'. 
        Add the title 'Title: convert_to_datastruct' right before the CSV block. 
        Use a vertical bar '|' as the column separator, without any extra symbols in the table. 
        Include all specified columns in the CSV, and prefer datetime columns where applicable for date-related data.
        Work step by step. Make sure all column_name value`s are correct and appear in the data dictionary. Double check your reply.
        Work step by step. Give me your best answer.""",

    ]

    messages2 = []
    #messages2.append({"role": "system", "content": system_prompt[0]})
    for i, message in enumerate(message_queue1):
        role = "user"
        messages2.append({"role": role, "content": message})
        messages2 = LLMwrapper(messages2, client, model, role=role ,temperature=0).return_conversation()
            
    message_queue = [
        # system prompt
        f"""We will create a table of values to evaluate. 
        Please stick to the provided information, unless specifically asked to provide additional information which was not mentioned in the files. 
        Include medical, drug, and procedure classification coding where relevant. Use {coding} for diagnosis classification codes, 
        {drug} for drug classification codes, {procedure} for procedures, {lab} for lab measurement classification codes and {coding} and gender, race and ethnicity classification coding for demographic coding. 
        If unsure, respond with "I am unsure."
        Make sure the CSVs do not contain anything that will prevent them from being loaded into a pandas dataframe.

        When asked for CSV tables:
        Use | (vertical bar) as the separator.
        Enclose the table in '```csv' and '```'.
        Exclude any symbols other than those specified.
        Separate the text and table clearly.
        Create all tables with the following columns: 'flag','column name','codes','data type','value column name','description','expected value',
        'expected value max','expected value min','range low','range high','comparison type','references'

        If there are multiple classification codes for a specific concept, provide them as a list in the 'codes' column (e.g, if there are multiple codes for a specific diagnosis, 
        drug, procedure, lab test or a demographic property). 
        **Please create a separate row for each categorical value under the evaluatedf category (e.g. if gender is being evaluated - separate evaluation rows for male and for female should be created).**

        Gender, race and ethnicity categories are in the data dictionary 'description' column and should be used as the possible code values for the demographic subpopulations.

        If there is a single expected value, fill "expected value min" and "expected value max" 'with np.nan', and fill only "expected value" with the value.
        "expected value min" is used when the expected result is greater than the expected value, "expected value max" is used when the expected result is less than the expected value.
        If we expect a range of values, fill "range low" and "range high".
        'column name' should contain the name of the column from the provided data dictionary that holds the classifiction codes.
        "value column name" should contain the name of the column from the provided data dictionary that holds the recorded value for the test or procedure or measurement, if applicable
        If there are multiple medical, drug, lab or procedure classification codes related to a specific concept name, add them as a list in the relevant classification code-related column. 
        Ensure all tables can be concatenated.
        For date-related data, use columns with datetime values, if available.
        For each diagnosis ({coding}), drug ({drug}), measurement/lab test ({lab}) and procedure ({procedure}) code, provide **only** the relevant meaning/concept name in the 
        'description' column. Double check the meaning and provide references for the statistical values.
        Provide your response step by step and offer your best possible answer. 
        Provide references for all descriptions, code meanings and the statistical values.
        
        When asked for CSVs or text, always format them using triple backticks as follows: '```csv' or '```text', 
        respectively, and end with '```'. At the top of each block (CSV, or text), include the required title or filename as part 
        of the response. This title or filename must appear at the start of each block:
                
        ```csv
        Title: example title
        # your csv code here
        ```
        
        If no filename or title was provided in the reqest, please avoid including a filename in the response.
        Please confirm understanding of these instructions without replying.""",

        # expected_params_comorbidities - expected statistics for comorbidities
        f"""We are going to check comorbidity prevalence among diagnosed. 
        Please use the relevant tables and columns the following data dictinary:
        
        {data_struct}
        
        and the {coding} codes provided in the following reference file: 
        
        {info} 
        
        For each comorbidity in the provided reference file, suggest expected values for patients diagnosed with {diagnosis} in {region}. 
        Please use the description column in the data dictionary to describe the content of the column.
        Each column/field name in the provided data dictionary can be evaluated as many times as needed, for as many comorbidities as possible. 
        Build a csv table with ALL of the following columns: 
        'flag', 'column name', 'codes', 'data type','value column name','description','expected value','expected value max', expected value min', 
        'range low', 'range high','comparison type','references'. 
         
        All columns are mandatory. If a field is irrelevant, fill it with np.nan. Do not suggest random population statistics. Only use columns and tables from the provided data dictionary.
        Use only codes in the reference file.
        The 'flag' column should indicate the data type and should be filled with one of the following values: 'demography', 'drug', 'procedure', 'lab' or 'diagnosis'.
        'value column name' should contain the actual name of the column from the provided data dictionary that holds the value.
        Before the CSV, include the title: "Title: expected_params_comorbidities". Do not separate it from the CSV code block.
        Use the vertical bar | as the CSV separator.
        Please include only relevant diagnosis codes in the 'codes' column.
        Surround the CSV table with ```csv and ```.
        In the 'column name' field, use the corresponding column name from the data dictionary where the comorbidity {coding} code can be found.
        For the 'comparison type', specify whether the comparison is an 'exact value', 'range', or 'percentage'. If it is a range, use numeric values only.
        Do not suggest random population statistics. Only use columns and tables from the provided data dictionary.
        In the 'codes' column, insert all the relevant {coding} medical codes from the reference file as a list. Each comorbidity should 
        appear in a separate row. Include the code meaning in the 'description' column, double check the meaning and provide references for the statistical values. 
        Keep the 'description' column short, concise and specific with exact descripton of what is evaluated.
        Expected values should be percentage of {diagnosis} patients with the comorbidity.
        Use all of the provided information to complete the CSV. Include a full list of drug codes.
        Provide as many column/field name evaluations from the given data dictionary as possible.
        Make sure the 'description' column includes the description of the column from the data dictionary, including the meaning of the corresponding {coding} codes. 
        Provide references for the code meanings and for the statistical values. Work step by step. Give me your best answer.""",

        # expected_params_drugs - expected statistics for drug prescriptions
        f"""We are going to evaluate drug use. Please use the relevant tables in the following data dictionary:
        
        {data_struct}
        
        and the {coding} codes provided in the following reference file:

        {info}

        For each column or field name in the provided data dictionary, suggest expected values for patients diagnosed with {diagnosis} in {region}. 
        Please use the description column in the data dictionary to describe the content of the column.
        Each field name can be used as many times as needed, for as many drugs as possible. 
        Build a csv table with ALL of the following columns: 
        'flag', 'column name', 'codes', 'data type','value column name','description','expected value','expected value max', 
        'expected value min', 'range low', 'range high', 'comparison type','references'. 
        
        All columns are mandatory. If a field is irrelevant, fill it with np.nan. Do not suggest random population statistics. Only use columns and tables from the provided data dictionary.
        Use only codes in the reference file.
        The 'flag' column should indicate the data type and should be filled with one of the following values: 'demography', 'drug', 'procedure', 'lab' or 'diagnosis'.
        'value column name' should contain the actual name of the column from the provided data dictionary that holds the value.
        Before the CSV, include the title: "Title: expected_params_drugs". Do not separate it from the CSV code block.
        Use the vertical bar | as the CSV separator.
        Surround the CSV table with ```csv and ```.
        In the 'column name' field, use the corresponding column/field name from the data dictionary.
        For the 'comparison type', specify whether the comparison is an 'exact value', 'range', or 'percentage'. If it is a range, use numeric values only.
        Do not suggest random population statistics. Only use columns and tables from the provided data dictionary.
        In the 'codes' column, insert all the relevant {drug} drug codes from the reference file as a list. Each drug should 
        appear in a separate row. Include the code meaning in the 'description' column, double check the meaning and provide references for the statistical values. 
        Keep the 'description' column short, concise and specific with exact descripton of what is evaluated.
        Expected values should be percentage of {diagnosis} patients who use the drug.
        Use all of the provided information to complete the CSV.
        Provide as many column/field evaluations from the given data dictionary as possible.
        For date-related data, prefer columns with datetime values where applicable.
        Make sure the 'description' column includes the description of the column from the data dictionary, including the meaning of the corresponding {coding} codes. 
        Provide references for the code meanings and for the statistical values. Work step by step. Give me your best answer.""",

    ]

    message_queue2 = [

        # expected_params_procedures - expected statistics for procedures
        f"""From the following data dictionary, please extract the table and column names which contain lab test codes and recorded value:
            
            {data_struct}

        Please include the table name, column name and description for the lab test code and recorded value. 
        Structure your answer as follows: 'Lab tests: table name, column name, description'.""",

        f"""From the following data dictionary, please extract the table and column names with procedure codes and recorded values
        in the provided data dictionary.

        Please include the table name, column name and description for the lab test code and recorded value.
        If there is no such column, please reply with 'no value column', and include only the description and code columns.
        Structure your answer as follows: 'Procedures: table name, column name, description'.""",

        f"""Based on your previous answers and the {procedure} procedure codes provided in the following reference file:
            
            {info}

        suggest expected values for the procedure in {region}.

        Each column/field name can be used for as many procedures as needed.
        Build a csv table with ALL of the following columns:
        'flag', 'column name', 'codes', 'data type','value column name','description','expected value','expected value max', expected value min', 
        'range low', 'range high','comparison type','references'. 
        
        All columns are mandatory. If a field is irrelevant, fill it with np.nan. Do not suggest random population statistics. Only use columns and tables from the provided data dictionary.
        Use only codes in the reference file.
        The 'flag' column should indicate the data type and should be filled with one of the following values: 'demography', 'drug', 'procedure', 'lab' or 'diagnosis'.
        'value column name' should contain the field name in the provided data dictionary with the procedure value, if applicable. If it doesn't exist, fill it with 'np.nan'.
        Please make sure the correct 'value column name' for procedure value is in the output csv, if applicable.
        Before the CSV, include the title: "Title: expected_params_procedures". Do not separate it from the CSV code block.
        Use the vertical bar | as the CSV separator.
        Surround the CSV table with ```csv and ```.
        In the 'column name' field, use the corresponding column name from the data dictionary.
        For the 'comparison type', specify whether the comparison is an 'exact value', 'range', or 'percentage'. If it is a range, use numeric values only.
        Do not suggest random numbers. Only use columns and tables from the provided data dictionary.
        In the 'codes' column, insert all the relevant {procedure} procedure codes from the reference file as a list. 
        Each procedure should appear in a separate row. 
        Please include the code meaning in the 'description' column, double check the meaning and provide references for the statistical values. 
        Keep the 'description' column short, concise and specific with exact descripton of what is evaluated (e.g. 'urinary tract infection icd-9 codes').
        In the values, include only the number, without percentage or units. Expected values should be normal range of values for the evaluated procedure.
        Use all of the provided information to complete the CSV.
        Provide as many column evaluations from the given data dictionary as possible.
        Make sure the 'description' column includes the description of the column from the data dictionary, including the meaning of the corresponding {coding} codes. 
        Provide references for the code meanings and for the statistical values. Work step by step. Give me your best answer.""",

        # expected_params_labs - expected statistics for lab tests
        f"""Based on your previous answers and the {lab} measurement codes provided in the provided reference file.

        suggest normal expected values for the lab test in {region}. 

        Please use the description column in the data dictionary to describe the content of the column.
        Each column/field name can be used for as many lab tests as needed. 
        Build a csv table with ALL of the following columns: 
        'flag', 'column name', 'codes', 'data type','value column name','description','expected value','expected value max', expected value min', 
        'range low', 'range high','comparison type','references'. 
        
        All columns are mandatory. If a field is irrelevant, fill it with np.nan. Do not suggest random population statistics. Only use columns and tables from the provided data dictionary.
        Use only codes in the reference file.
        Please use your previous replies.
        The 'flag' column should indicate the data type and should be filled with one of the following values: 'demography', 'drug', 'procedure', 'lab' or 'diagnosis'.
        'value column name' should contain the field name from the provided data dictionary with the lab test result value, if applicable. If it doesn't exist, fill it with 'np.nan'.
        Please make sure the correct field name for 'value column name' is in the output csv.
        Before the CSV, include the title: "Title: expected_params_labs". Do not separate it from the CSV code block.
        Use the vertical bar | as the CSV separator.
        Surround the CSV table with ```csv and ```.
        In the 'column name' field, use the corresponding column name from the data dictionary.
        For the 'comparison type', specify whether the comparison is an 'exact value', 'range', or 'percentage'. If it is a range, use numeric values only.
        Do not suggest random numbers. Only use columns and tables from the provided data dictionary.
        In the 'codes' column, insert all the relevant {lab} lab test codes from the reference file as a list. 
        Each lab test should appear in a separate row. Include the code meaning in the 'description' column, double check the meaning and provide references for the statistical values. 
        Keep the 'description' column short, concise and specific with exact descripton of what is evaluated.
        In the values, include only the number, without percentage or units. Expected values should be normal range of values for the evaluated lab test.
        Use all of the provided information to complete the CSV.
        Provide as many column evaluations from the given data dictionary as possible.
        Make sure the 'description' column includes the description of the column from the data dictionary, including the meaning of the corresponding {coding} codes. 
        Provide references for the code meanings and for the statistical values. Work step by step. Give me your best answer.""",

        f"""Please provide a single and final csv file for labs based on your previous answer. Include the required title and wrap it between '```csv' and '```'.""",

        f"""Please provide a single and final csv file for procedures based on your previous answers. **Make sure there are no duplications with the labs csv**. Include the required title and wrap it between '```csv' and '```'.""",


    ]


    messages3 = []
    messages3.append({"role": "system", "content": system_prompt[0]})
    for i, message in enumerate(message_queue2):
        role = "user"
        messages3.append({"role": role, "content": message})
        messages3 = LLMwrapper(messages3, client, model, role=role ,temperature=0).return_conversation()


    message_queue3 = [
    # expected_params_genpop_demo - expected parameters for general population demographics
        f"""Look at the diagnosis-related table and columns in the following data dictionary:

        {data_struct}

        In the description, what are the available gender classification codes, according to the description column? Please provide the codes and their meanings.""",

        f"""Look at the diagnosis-related table and columns in the provided data dictionary.
        In the description, what are the available ethnicity classification codes, according to the description column? Please provide the codes and their meanings.""",

        f"""Look at the diagnosis-related table and columns in the provided data dictionary.
        In the description, what are the available race classification codes, according to the description column? Please provide the codes and their meanings.""",

        f"""According to the data dictionary, your previous answers and the following reference file:
        
        {info}

        Please use the coding codes and categorizations provided in the reference file and the data dictionary to suggest expected values for the general population demographics in {region}.
        
        For each column/field name, suggest expected percentage values for the **general population** in {region}, according to the provided data.
        Please use the description column in the data dictionary to describe the content of the column.
        You can reuse each data field as many times as necessary to represent various population characteristics and subpopulations.

        Create a CSV table with the following columns: 'flag','column name','codes','data type','value column name','description','expected value',
        'expected value max','expected value min','range low','range high','comparison type','references'

        Follow these guidelines:
        All columns are mandatory. If a field is irrelevant, fill it with np.nan.
        Each demographic subpopulation should appear in a separate row (e.g a row for female, male, white, etc).
        The possible values for gender, race and ethnicity are stated in the 'description' column in the provided data dictionary for the relevant data field. Please use them as well.
        Please prefer the codes provided in the data dictionary and only then the codes in the reference file. You may add all options in the provided data for each subpopulation.
        The 'flag' column should indicate the data type and should be filled with one of the following values: 'demography', 'drug', 'procedure', or 'diagnosis'.
        'value column name' should contain the actual name of the column from the provided data dictionary that holds the value.
        Before the CSV, include the title: "Title: expected_params_genpop_demo". Do not separate it from the CSV code block.
        Use the vertical bar | as the CSV separator.
        Surround the CSV table with ```csv and ```.
        In the 'column name' field, use the corresponding column/field name from the data dictionary.
        For the 'comparison type', specify whether the comparison is an 'exact value', 'range', or 'percentage'. If it is a range, use numeric values only.
        If the provided expected value is a range, fill "range low" and "range high" and set 'comparison type' to be a 'range'.
        Do not suggest random population statistics. Only use columns and tables from the provided data dictionary.
        In the 'codes' column, for each gender, race and ethnicity subpopulation insert relevant classification codes **from the reference file, your previous answers and the data dictionary** as a list. 
        Add the relevant gender codes, race codes and ethnicity codes from your previous answers to the appropriate list under the 'codes' column. The codes that don't have their own row should appear in 'other' race, gender or ethnicity row.
        Each demographic subpopulation should appear in a separate row (e.g a row for male, a row for female, a row for white, a row for asian, etc.). Include the code 
        meaning in the 'description' column, double check the meaning and provide references for the statistical values. Keep the 'description' column short, concise and specific with exact 
        descripton of what is evaluated.
        Use all of the provided information to complete the CSV. 
        Provide as many column evaluations from the given data dictionary as possible.
        For date-related data, prefer columns with datetime values where applicable.
        Make sure the 'description' column includes the description of the column from the data dictionary, including the meaning of the corresponding {coding} codes. 
        If there are any additional demographic {coding} codes that might apply to {region}, please **add** them to the existing list - to check for additional codes you may use your intrinsic knowledge.
        Provide references for the code meanings and for the statistical values.
        double check your reply.
        Please make sure there is a separate row for each subpopulation (e.g. for gender - separate rows for male and for female, as well as for the different race and ethnicity options).
        The codes should correspond. Provide your best answer.""",

        f"""Please provide a single and final csv file for the general population demographics based on your previous answers. Include all gender, race, ethnicity and any other categorical fields. 
        Make sure all relevant gender, race and ethnicity classification codes are included in the 'codes' column.
        Include the required title and wrap it between '```csv' and '```'.""",

        f"""Please make sure that the previous csv file contains a separate row for each demographic subgroup (e.g a row for female, male, white, etc).
        If it does not, please recreate it so it follows the required gudelines.""",

        # expected_params_diagnosed_genpop - expected parameters for diagnosed population demographics
        f"""According to the data dictionary, your previous answers and the provided reference file.

        Please use the coding codes and categorizations provided in the reference file and the data dictionary to suggest expected values for the {diagnosis} diagnosed population demographics in {region}.
        For each column/field name, suggest expected demographic statistics values for the population diagnosed with {diagnosis} in {region}.
        Please use the description column in the data dictionary to describe the content of the column.
        Use each column as needed for as many population characteristics as possible. Build a CSV table with all the following columns:
        'flag','column name','codes','data type','value column name','description','expected value',
        'expected value max','expected value min','range low','range high','comparison type','references'

        Follow these guidelines:
        All columns are mandatory. If a field is irrelevant, fill it with np.nan.
        Each demographic subpopulation should appear in a separate row (e.g a row for female, male, white, etc).
        The possible values for gender, race and ethnicity are stated in the 'description' column in the provided data dictionary for the relevant data field. Please use them as well.
        Please prefer the codes provided in the data dictionary and only then the codes in the reference file. You may add all options in the provided data for each subpopulation.
        The 'flag' column should indicate the data type and should be filled with one of the following values: 'demography', 'drug', 'procedure', 'lab' or 'diagnosis'.
        'value column name' should contain the actual name of the column from the provided data dictionary that holds the value.
        Before the CSV, include the title: "Title: expected_params_diagnosed_genpop". Do not separate it from the CSV code block.
        Use the vertical bar | as the CSV separator.
        Surround the CSV table with ```csv and ```.
        In the 'column name' field, use the corresponding column name from the data dictionary.
        For the 'comparison type', specify whether the comparison is an 'exact value', 'range', or 'percentage'. If it is a range, use numeric values only.
        If the provided expected value is a range, fill "range low" and "range high" and set 'comparison type' to be a 'range'.
        Do not suggest random population statistics. Only use columns and tables from the provided data dictionary.
        In the 'codes' column, for each gender, race and ethnicity subpopulation insert relevant classification codes **from the reference file, your previous answers and the data dictionary** as a list. 
        Add the relevant gender codes, race codes and ethnicity codes from your previous answers to the appropriate list under the 'codes' column. The codes that don't have their own row should appear in 'other' race, gender or ethnicity row.

        Each demographic subpopulation should appear separately (e.g a row for male, a row for female, a row for white, a row for asian, etc.). Include the code 
        meaning in the 'description' column, double check the meaning and provide references for the statistical values. Keep the 'description' column short, concise and specific with exact 
        descripton of what is evaluated - state the exact gender or race or etnicity evaluated.
        In the 'expected value', 'expected value min', 'expected value max' columns, provide the percentage of **diagnosed population** with the specific demographic characteristic.
        Use all of the provided information to complete the CSV.
        Provide as many column evaluations from the given data dictionary as possible.
        For date-related data, prefer columns with datetime values where applicable.
        Make sure the 'description' column includes the description of the column from the data dictionary, including the meaning of the corresponding {coding} codes. 
        If there are any additional demographic {coding} codes that might apply to {region}, please **add** them to the existing list - to check for additional codes you may use your intrinsic knowledge.
        Provide references for the code meanings and the values. Alwaus double check your reply. Always work step by step.
        Please create a separate row for each subpopulation (e.g. for gender - separate rows for male and for female, as well as for the different race and ethnicity options).""",
        
        f"""Please provide a single and final csv file for the **diagnosed population demographics** based on your previous answers. Include all gender, race, ethnicity and any other categorical fields. 
        Make sure all relevant gender, race and ethnicity classification codes are included in the 'codes' column. 
        Include the required title and wrap it between '```csv' and '```'.
        """,
    
        f"""Please make sure that the previous csv file contains a separate row for each demographic subgroup (e.g a row for female, male, white, etc).
        If it does not, please recreate it so it follows the required gudelines.""",

    ]

    messages4 = []
    messages4.append({"role": "system", "content": system_prompt[0]})
    for i, message in enumerate(message_queue3):
        role = "user"
        messages4.append({"role": role, "content": message})
        messages4 = LLMwrapper(messages4, client, model, role=role ,temperature=0).return_conversation()

    messages5 = []
    messages5.append({"role": "system", "content": f"Please use the following data dictionary to answer the following questions: \n\n + {data_struct}"})
    messages5.append({"role": "user", "content": f"This is a csv containing proposed evaluations: \n\n {messages4[-1]['content']}"})
    messages5.append({"role": "user", "content": f"""Are there additional relevant codes in one of the rows in the provided table above, that 
                              correspond with the value under 'description' column in each row?
                              Please return the same table with the same title, with **additional** codes in each row, if applicable. Provide references. 
                              Do not change anything other than what was requested.
                              Please work step by step and provide your best answer."""})
    messages5 = LLMwrapper(messages5, client, model, role=role ,temperature=0).return_conversation()

    # get disease statistics values from OpenAI
    # communicate with Azure OpenAI API:
    for i, message in enumerate(message_queue):
        if i==0:
            messages.append({"role": "system", "content": message})
        else:
            messages1 = []
            messages1.append(messages[0])
            messages1.append({"role": "user", "content": message})
            role = "user"
            messages1 = LLMwrapper(messages1, client, model, role=role ,temperature=0).return_conversation()
            messages1.append({"role": "user", "content": f"""Are there additional relevant codes in one of the rows in the provided table above, that 
                              correspond with the value under 'description' column in each row? 
                              Please return the same table with the same title, with additional codes in each row, if applicable. Provide references. Ignore this request
                              for the 'convert_to_datastruct', 'expected_params_procedures', 'expected_params_drugs', and 'expected_params_comorbidities' tables.
                              Please work step by step and provide your best answer."""})
            messages1 = LLMwrapper(messages1, client, model, role=role ,temperature=0).return_conversation()
            messages1.append({"role": "user", "content": f"""Make sure the proposed column names for evaluation correspond with the ones in the 
                              provided data dictionary and with the requirements in the system message.

                              If it doesn't correspond to what was reuired, please change the evaluated column names according to what was required.
                              Please work step by step and provide your best answer."""})
            messages1 = LLMwrapper(messages1, client, model, role=role ,temperature=0).return_conversation()
            messages1.append({"role": "user", "content": f"""Make sure the evaluated values correspond with the ones in the 
                              provided supplementary data, data dictionary and the requirements in the first message.
                              If it doesn't correspond to what was reuired, please change the values according to what is evaluated.
                              Please work step by step, provide references and provide your best answer."""})
            messages1 = LLMwrapper(messages1, client, model, role=role ,temperature=0).return_conversation()
            messages = messages + messages1[1:]
            #del messages[-len(messages1):-1]

    
    messages += messages2[1:]
    messages += messages3[1:]
    messages += messages4[1:]
    messages += messages5[2:]

    # Write all in a txt:
    now = str(dt.datetime.now())
    count = 0

    with open('logs/%s_%s_%s_%s_test_suggestion.txt' %(diagnosis,coding,region,model), 'w', encoding="utf-8") as f:
        f.write("%s \n\n" %now)
        
        for message in messages:
            if message['role'] == 'assistant':
                if ("title:") in message['content'].lower():
                    count+=1
                    f.write(message['content'] + "\n\n")
                    title, df = make_df(message['content'])
                    df = df.replace('',np.nan).dropna(axis=1)
                    df.to_csv("test_csvs/%s_%s.csv" %(diagnosis,title), index=False)
                else:
                    f.write(message['content'] + "\n\n")
        f.close()