import os
import json
import time
import requests
import numpy as np
import pandas as pd
import datetime as dt
from ask_gpt import LLMwrapper
from query_bing import query_bing
from vector_query import get_concepts
from connect_openAI import connect_to_openAI
from extraction_functions import make_df, make_list, json_to_df

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def get_theoretical_vals(diagnosis, region, coding, drug, procedure, lab, model):
    """This function generated the reference theoretical values for the diagnosis of interest in the region of interest. It uses the Azure OpenAI API to generate the answers, along with querying 
    the pre-created vector database for the concepts and searching Bing using its API. The function generates the following tables: diagnosis codes, comorbidities, drug codes, lab tests and procedures, and demographics.
    It also provides a list of statistics for the diagnosis in the region, and an additional information from medical, sociodemographic and policy points of view."""

    global messages, client
    
    client = connect_to_openAI(model)

    messages = []

    searchs = query_bing(f'prevalence of {diagnosis} in {region}')
    searchs1 = query_bing(f'incidence of {diagnosis} in {region}')
    searchs2 = query_bing(f'mortality rate of {diagnosis} in {region}')
    searchs3 = query_bing(f'lifetime risk of {diagnosis} in {region}')
    searchs4 = query_bing(f'survival rate of {diagnosis} in {region}')
    search1 = query_bing(f'age distribution among {diagnosis} patients in {region}')
    search2 = query_bing(f'mean age and standard deviation of {diagnosis} in {region}')
    search3 = query_bing(f'Total {region} population size')
    search4 = query_bing(f'Number of diagnosed with {diagnosis} in {region}')
    # system prompt + generating statistics and additional insights for the diagnosis of interest in the region of interest
    message_queue1 = [f"""You are a public health and medical expert. Answer as concisely as possible. Answer for the provided diagnosis, region, coding system, 
            and drug classification system. Make sure the coding in all your answers fits the requirements. The following questions are about {diagnosis} 
            in {region}. When searching for references, have them as up-to-date as possible. Search for regional data and provide references. If regional data is unavailable, 
            reply with global data. If there is no available data, answer with 'Data is unavailable'. If you are unsure, answer with 'I am unsure.'
            Work step by step. 
            **When asked for diagnosis codes, provide only the rerquired codes and don't randomly assign codes.**
            **When asked for any classification codes, provide the required codes without truncation.**
            **Stick to the required coding systems.**
            If asked about diagnosis/drug/procedure codes, the fields in the reference data are 'concept_id' which includes OMOP codes, 'concept_name' which 
            are the names of the codes, 'concept_code' which are the source vocabulary codes, 'vocabulary_id' is the name of the source vocabulary.
            In OMOP coding, the standard dictionary is SNOMED and RxNorm, and the required field is concept_id. For exery other coding, the required field is concept_code.
            For demographic variables, always include the race, gender and ethnicity vocabularies.
            When asked for csv tables, divide them using a vertical line |. Add the required title before the csv, exactly as written in the request. 
            Please avoid other symbols arount the title. Give me your best answer and provide references. When asked for Python code, CSVs or text, always format them using triple 
            backticks as follows: '```python', '```csv' and '```text', respectively, and end with '```'. At the top of each block (Python code, CSV, or text), include 
            the required title or filename as part of the response. This title or filename must appear at the start of each block:
            
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
            Please provide references including a **valid** url or a publication for each answer.
            Please confirm understanding of these instructions without replying.""",

            f"""What is the prevalence of {diagnosis} in {region}? Provide the percentage of diagnosed. 
            Prioritize more recent data, preferably from government sources.
            Please use the following information and provide numbers:

            {searchs['webPages']['value']}
            
            Numbers are mandatory. Please provide references.""",

            f"""What is the incidence of {diagnosis} in {region}? Provide the percentage of diagnosied. 
            Prioritize more recent data, preferably from government sources.
            Please use the following information and provide numbers:

            {searchs1['webPages']['value']}
            
            Numbers are mandatory. Please provide references.""",

            f"""What is the mortality rate of people with {diagnosis} in {region}? Provide the percentage. 
            Prioritize more recent data, preferably from government sources.
            Please use the following information and provide numbers:

            {searchs2['webPages']['value']}

            Numbers are mandatory. Please provide references.""",

            f"""What is the lifetime risk of developing {diagnosis} in {region}? Provide the percentage. 
            Prioritize more recent data, preferably from government sources.
            Please use the following information and provide numbers:

            {searchs3['webPages']['value']}
            
            Numbers are mandatory. Please provide references.""",

            f"""What is the survival rate of people with {diagnosis} in {region}? Provide the percentage. 
            Prioritize more recent data, preferably from government sources.
            Please use the following information and provide numbers:

            {searchs4['webPages']['value']}
            
            Numbers are mandatory. Please provide references.""",

            f"""What is the total population size in {region}? Provide the number in millions. 
            Prioritize more recent data, preferably from government sources.
            Please use the following information and provide numbers:

            {search3['webPages']['value']}
            
            Numbers are mandatory. Please provide references.""",


            f"""Please provide statistics for people diagnosed with {diagnosis} in {region}. Include Prevalence, Incidence, Mortality rate, Lifetime risk, and Survival. 
            Provide all statistics in percentage. Please use your previous replies as reference.     
            Arrange them in a csv table with a vertical line as delimiter. Please add references. Add 'Title: 
            statistics_in_{region}' before the CSV. Do not add any other symbols (such as dashes or hypens) to the table. 
            Structure the table as follows: Prevalence | Incidence | Mortality rate | Lifetime risk | Survival | total population size in millions | reference.
            Give me your best answer. Please provide references.""",
    ]

            #f"""Please provide age distribution among diagnosed patients with {diagnosis} in {region}. Please provide the age groups and the percentage of
            #patients in each group. Use the following information:
            #
            #{search1['webPages']['value']}      
            #
            #if you can't find relevant data, use your intrinsic knowledge.      
            #
            #Arrange them in a csv table with a vertical line 
            #as delimiter. Please add references. Add 'Title: age_distribution_in_{region}' before the CSV. Wrap the csv in '```csv' and '```'. Do not add 
            #any other symbols (such as dashes or hypens) to the table. Give me your best answer. If needed, search the web and provide references.""",

    message_queue2 = [f"""Please provide mean and standard deviation of {diagnosis} diagnosis age in {region}. 
                      Please use the following information and prioritize more recent data:

                    {search1['webPages']['value']}

                    {search2['webPages']['value']}

                    If there is no information in the provided data, please use your knowledge.
                    Numbers are mandatory. Please provide references.""",

            f"""Please provide the number of diagnosed with {diagnosis} in {region}. please write a full number 
                (e.g instead of '10 million' write 10000000). Use the following reference:
            
                {search4['webPages']['value']}

                If there is no information in the provided data, please provide it based on the prevalence and total population size.

                Numbers are mandatory. Please provide references.""",

            f"""Please provide the age statistics for {diagnosis} in {region}. Include mean age, standard deviation, and count.
            Use your previous replies as reference. If there is no data in the provided information, please use your knowledge.           
            
            Arrange them in a csv table with a vertical line as delimiter. 
            Please add references. Add 'Title: age_stats_in_{region}' before the CSV. Do not add any other symbols (such as dashes or hypens) to the table. 
            Give me your best answer. Structure the table as follows: mean_age | std | count | reference. Make sure all columns are filled. Please provide references for the opercentage values.""", 
            ]

    
    # communicate with Azure OpenAI API:
    for i, message in enumerate(message_queue1):
        if i==0:
            role = "system"
        else:
            role = "user"
        
        messages.append({"role": role, "content": message})
        messages = LLMwrapper(messages, client, model, role=role ,temperature = 0).return_conversation()

    messages1 = []
    messages1.append(messages[0])
    messages1.append(messages[-1])
    for i, message in enumerate(message_queue2):
        role = "user"
        messages1.append({"role": "user", "content": message})
        messages1 = LLMwrapper(messages1, client, model, role=role ,temperature = 0).return_conversation()
    
    messages = messages + messages1[2:]

    diagnosis_codes = get_concepts('concept_name: ' + diagnosis +  ' domain_id: Condition ' + 'vocabulary_id: ' + coding + ' standard_concept: S' , n_results=50)
    diagnosis_codes = json_to_df(diagnosis_codes)

    # in the following code blocks each of them generates a csv table of different kind. It starts from generating a list of concept names (a concept can be a drug, a diagnosis, a procedure, etc.).
    # For each concept name a list of codes is generated, and the prevalence of the concept among the patients or the general population is added (based on LLM answers).

    # diagnosis codes
    messages1 = []
    messages1.append(messages[0])
    messages1.append({"role": "user", "content":f"""Please arrange the following file in a csv table with a vertical line as delimiter: 
                     {diagnosis_codes}.
                    Start with general {diagnosis} {coding} codes, preferably standard ones (with "S").
                    The csv table should include "{coding} code" and "concept name" columns. One {coding} code and concept name for each row. 
                    From the provided list, please include all possible {diagnosis} {coding} codes. Provide a full list of codes without truncation. Work step by step. Do not generate random 
                    codes or diagnoses, use only the ones provided. Add 'Title: {coding}_diagnosis_codes_in_{region}' before the CSV. Give me your best answer."""})   

    messages1 = LLMwrapper(messages=messages1, client=client, model=model, assistant=False, role=role, temperature = 0).return_conversation()

    messages = messages + messages1[1:]
   
    # comorbidities
    messages1 = []
    messages1.append(messages[0])

    messages1.append({"role": "user", "content":f"""Please provide a list of 15 most prevalent comorbidities among {diagnosis} patients. 
                    The concept names of the comorbidities should appear as they appear in {coding} dignosis codes.
                     provide a comma separated list of the commorbidities separated by '```list' and '```'."""})
    
    messages1 = LLMwrapper(messages=messages1, client=client, model=model, assistant=False, role=role, temperature = 0).return_conversation()

    comorbidity_list = make_list(messages1[-1]['content'])
    comorbidity_list = comorbidity_list.split(", ")

    comorbidities = []
    comorbidities1 = []
    for idx, comorbidity in enumerate(comorbidity_list):
        messages2 = []
        messages2.append(messages[0])
        comorbidities.append(json_to_df(get_concepts('concept_name: ' + comorbidity + ' domain_id: Condition ' + 'vocabulary_id: ' + coding + ' standard_concept: S', n_results=100)))

        messages2.append({"role": "user", "content":f"""Please provide a comprehensive and full list of {coding} codes for {comorbidity}.  Provide a full list of codes without truncation.
                         Use the following table:

                         {comorbidities[idx]}

                        Please include all possible options. Start with general {comorbidity} {coding} codes, preferably standard ones (with "S"). 
                        The csv table should include "{coding} codes" and "comorbidity" columns. Write comorbidity name and a list of all relevant {coding} 
                        codes in one row. Separate the csv using a vertical line as delimiter.
                        First include all possible {comorbidity} {coding} codes without complications. Work step by step. Do not generate random codes.
                        Use only the ones provided. Give me your best answer."""})
                        
        messages2 = LLMwrapper(messages=messages2, client=client, model=model, assistant=False, role=role, temperature = 0).return_conversation()

        search = query_bing(f'Prevalence of {comorbidity} among {diagnosis} patients in {region}')
        messages2.append({"role": "user", "content":f"""Please add a "prevalence" column with prevalence of {comorbidity} among {diagnosis} patients. 
                          Add a reference column with reference to the prevalence value. Prioritize more recent data, preferably from government sources.
                          use the following information:

                          {search['webPages']['value']}

                        Give me your best answer. Do not change or remove any other column. Separate the csv using a vertical line as delimiter."""})
    
        messages2 = LLMwrapper(messages=messages2, client=client, model=model, assistant=False, role=role, temperature = 0).return_conversation()

        comorbidities1.append(make_df(messages2[-1]['content']))

    #messages = messages + messages1[1:]

    messages3 = []
    messages3.append(messages[0])
    messages3.append({"role": "user", "content":f"""Please provide a full table of comorbidities, based on the following table:
                      
                     {comorbidities1}

                     
                     provide a table with the following columns: comorbidity|{coding} codes|prevalence. Wrap the csv in '```csv' and '```'.
                     Use a vertical line as delimiter. Add 'Title: comorbidities_in_{region}' before the CSV."""})
    
    messages3 = LLMwrapper(messages=messages3, client=client, model=model, assistant=False, role=role, temperature = 0).return_conversation()
    messages1 = messages1 + messages3[1:]

    messages = messages + messages1[1:]
    
    # drug codes
    messages1 = []
    messages1.append(messages[0])

    messages1.append({"role": "user", "content":f"""Please provide a list of 15 specific drug names and/or ingredients used to treat {diagnosis}. 
                     Be as specific as possible. The concept names of the drugs should appear as they appear in {drug} drug codes.
                     Provide a comma separated list of the above drugs separated by '```list' and '```'."""})
    
    messages1 = LLMwrapper(messages=messages1, client=client, model=model, assistant=False, role=role, temperature = 0).return_conversation()

    drug_list = make_list(messages1[-1]['content'])
    drug_list = drug_list.split(", ") 

    drugs = []
    drugs1 = []
    for idx, drug_name in enumerate(drug_list):
        messages2 = []
        messages2.append(messages[0])
        drugs.append(json_to_df(get_concepts('concept_name: ' + drug_name + 'domain_id: Drug' + 'vocabulary_id: ' + drug + ' standard_concept: S', n_results=140)))

        messages2.append({"role": "user", "content":f"""Please provide a comprehensive list of {drug} codes for {drug_name}. Provide a full list of codes without truncation.
                          Use the following table:
                         
                         {drugs[idx]}
                         
                        Please include all possible options. Start with general {drug_name} {drug} codes, preferably standard ones (with "S"). 
                        The csv table should include "{drug} codes" and "drug" columns. Write a list of all relevant {drug_name} {drug} codes under "{drug} codes", 
                        and drug name under "drug", in one row. Work step by step. Do not generate random codes, use only the ones provided. 
                        Arrange them in a csv table with a vertical line as delimiter. Give me your best answer."""})
        
        messages2 = LLMwrapper(messages=messages2, client=client, model=model, assistant=False, role=role, temperature = 0).return_conversation()

        search = query_bing(f'Percentage of {diagnosis} patients prescribed {drug_name} in {region}')
        messages2.append({"role": "user", "content":f"""Please add a "percentage" column with percentage of {diagnosis} patients treated with the drug and a 
                        "reference" column for the percentage information source with te relevant references. Prioritize more recent data, preferably from government sources.
                        use the following information:

                        {search['webPages']['value']}
                          
                        Give me your best answer. Do not change or remove any other column."""}) 
    
        messages2 = LLMwrapper(messages=messages2, client=client, model=model, assistant=False, role=role, temperature = 0).return_conversation()

        drugs1.append(make_df(messages2[-1]['content']))
        #messages1 += messages2[1:]
    
    #messages = messages + messages1
    #del messages[-len(messages1)+3:-2]
    
    messages3 = []
    messages3.append(messages[0])
    messages3.append({"role": "user", "content":f"""Please provide a full table of drugs, based on the following table:
                     
                      {drugs1} 
                     
                      Please create a csv with the following columns: {drug} codes|drug|percentage|reference. Wrap the csv in '```csv' and '```'.
                      Please arange it so all similar codes are aggregated under the '{drug} code' column without truncation, description of the same drug name under 'drug'.
                     Use a vertical line as delimiter. Add 'Title: drug_codes_in_{region}' before the CSV."""})
    
    messages3 = LLMwrapper(messages=messages3, client=client, model=model, assistant=False, role=role, temperature = 0).return_conversation()
    messages1 = messages1 + messages3[1:]
    messages = messages + messages1[1:]
    del messages[-len(messages1)+2:-1]

    # lab tests and procedures
    messages1 = []
    messages1.append(messages[0])

    messages1.append({"role": "user", "content":f"""Please provide a list of top 25 specific lab tests and procedure names performed on {diagnosis} patients  
                        in {region}. Be as specific as possible with procedure or lab test name. Avoid panel names, include individual tests. 
                        The concept names of the procedures and lab tests should appear as they appear in {procedure} procedure codes and {lab} terminology.
                        Provide a comma separated list of the lab tests and procedures separated by '```list' and '```'."""})
    
    messages1 = LLMwrapper(messages=messages1, client=client, model=model, assistant=False, role=role, temperature = 0).return_conversation()
    LabProc = make_list(messages1[-1]['content']) 
    LabProc = LabProc.split(", ") 

    Labs = []
    Labs1 = []
    for idx, lab in enumerate(LabProc):
        messages2 = []
        messages2.append(messages[0])
        l1 = json_to_df(get_concepts('concept_name: ' + lab + 'domain_id: measurement' + 'vocabulary_id: ' + lab + ' standard_concept: S', n_results=70))
        p1 = json_to_df(get_concepts('concept_name: ' + lab + 'domain_id: procedure' + 'vocabulary_id: ' + procedure + ' standard_concept: S', n_results=70))
        lp = pd.concat([l1,p1], axis=0)
        lp.drop_duplicates(inplace=True)

        Labs.append(lp)

        messages2.append({"role": "user", "content":f"""Please provide a comprehensive list of {lab} codes for the following lab test or procedure: 
                        
                        {Labs[idx]}
                        
                        Arrange them in a csv table with a vertical line as delimiter. Please include all possible options.
                        The csv table should include "procedure codes" and "procedure" columns. Write a list of all relevant {lab} or {procedure} codes
                        under "procedure codes", and procedure name under "procedure", in one row.
                        Work step by step. Do not generate random codes. Provide a full list of codes without truncation.
                        Use only the ones provided. Give me your best answer."""}) 

        messages2 = LLMwrapper(messages=messages2, client=client, model=model, assistant=False, role=role, temperature = 0).return_conversation()

        search = query_bing(f'Normal range of {lab} in {region}')
        messages2.append({"role": "user", "content":f"""Please add a "normal range" column with normal ranges of results for each of the lab tests or procedures. 
                        Prioritize more recent data, preferably from government sources. Please use the following:
                          
                          {search['webPages']['value']}

                          Add a "reference" column for the normal range information source with the relevant references.
                          Give me your best answer. Do not change or remove any other column."""})
    
        messages2 = LLMwrapper(messages=messages2, client=client, model=model, assistant=False, role=role, temperature = 0).return_conversation()

        Labs1.append(make_df(messages2[-1]['content']))
        #messages1 += messages2[1:]
        #messages = messages + messages1
        #del messages[-len(messages1)+2:-2]
    
    messages3 = []
    messages3.append(messages[0])
    messages3.append({"role": "user", "content":f"""Please provide a full table of lab tests and procedures, based on the following table:
                      
                     {Labs1} 
                     
                     Please create a csv with the following columns: {coding} codes|procedure|normal range.
                     Wrap the csv in '```csv' and '```'. Use a vertical line as delimiter. Add 'Title: 'procedure_codes_in_{region}' before the CSV."""})
    
    messages3 = LLMwrapper(messages=messages3, client=client, model=model, assistant=False, role=role, temperature = 0).return_conversation()
    messages1 = messages1 + messages3[1:]

    messages = messages + messages1[1:]

    #del messages[-len(messages1)+3:-2]
    
    # gender
    messages1 = []
    messages1.append(messages[0])
    search = query_bing(f'Gender identity distribution in {region}')
    messages1.append({"role": "user", "content":f"""List all possible {coding} concept names for all possible gender options in {region}. 
                      Prioritize more recent data, preferably from government sources. Please use the following as reference as well:

                        {search['webPages']['value']}

                      Provide a comma separated list of the concepts separated by '```list' and '```'.
                     Just write it as single list, do not declare the category title (gender, race, ethnicity)."""})
    
    messages1 = LLMwrapper(messages=messages1, client=client, model=model, assistant=False, role=role, temperature = 0).return_conversation()
    
    gender = make_list(messages1[-1]['content'])
    gender = gender.split(", ")

    gender_list = []
    demo_list1 = []
    for idx, demo in enumerate(gender):
        messages2 = []
        messages2.append(messages[0])
        gender_list.append(json_to_df(get_concepts("concept_name: " + demo + 'domain_id: Gender' + 'standard_concept: S', n_results=50)))

        """ according to: {demo_list[idx]}"""
        
        messages2.append({"role": "user", "content":f"""Please provide a comprehensive list of gender {coding} codes according to:
                           {gender_list[idx]}.
                        Arrange them in a csv table with a vertical line as delimiter.
                        Please include all possible options for {demo}. Drop irrelevant options.
                        The csv table should include "{coding} code" and "demographic feature" columns. 
                        Each categorical feature - gender value -  should appear in a separate row.
                        For each row, write all the relevant {coding} codes in the "{coding} code" column without truncation, and the appropriate demographic 
                        feature in "demographic feature" column. 
                        "demographic feature" column should contain the specific gender, race or ethnicity subtype concept name.
                        Work step by step. Do not generate random codes. Use only the ones provided. Give me your best answer."""})
        
        messages2 = LLMwrapper(messages=messages2, client=client, model=model, assistant=False, role=role, temperature = 0).return_conversation()

        search = query_bing(f'Percentage of {demo} in {region}')
        messages2.append({"role": "user", "content":f"""Please add "percentage" column with the percentage of {demo} in {region}. 
                        Prioritize more recent data, preferably from government sources. Please use the following:
                          
                          {search['webPages']['value']}

                          Add a reference in the "reference" column for the percentage information source with the relevant references.
                          Give me your best answer. Do not change or remove any other column."""})
    
        messages2 = LLMwrapper(messages=messages2, client=client, model=model, assistant=False, role=role, temperature = 0).return_conversation()

        search = query_bing(f'Percentage of {demo} diagnosed with {diagnosis} in {region}')
        messages2.append({"role": "user", "content":f"""Please add "diagnosed percentage" column with the percentage of {demo} diagnosed with {diagnosis} in {region}. 
                        Prioritize more recent data, preferably from government sources. Please use the following:
                          
                          {search['webPages']['value']}

                          Add a reference in the "reference" column for the diagnosed percentage information source with the relevant references.
                          Give me your best answer. Do not change or remove any other column"""})
    
        messages2 = LLMwrapper(messages=messages2, client=client, model=model, assistant=False, role=role, temperature = 0).return_conversation()
        
        demo_list1.append(make_df(messages2[-1]['content'])[1])
        #messages1 += messages2[1:]

    messages = messages + messages1[1:]
        #del messages[-len(messages1)+2:-2]

    '''messages.append({"role": "user", "content":f"""Please arange the data according to the following table: {demo_list1}. Aggregate similar codes into a single row - codes under
    '{coding} code', description of the similar codes under 'demographic feature'. Remove non-demographic codes. Keep the rest."""})
    
    messages = LLMwrapper(messages=messages, client=client, model=model, assistant=False, role=role, temperature = 0).return_conversation()
    
    messages.append({"role": "user", "content":f"""To the table you just created, add a column with population percentage in {region}. Give me your best answer.
                        Do not change or remove any other column. Add 'Title: demography_coding' before the CSV."""})'''
    
    # race
    messages1 = []
    messages1.append(messages[0])
    messages1.append({"role": "user", "content":f"""List all possible {coding} concept names for all possible race options in {region}. 
                      Provide a comma separated list of the concepts separated by '```list' and '```'.
                     Just write it as single list, do not declare the category title (gender, race, ethnicity)."""})
    
    messages1 = LLMwrapper(messages=messages1, client=client, model=model, assistant=False, role=role, temperature = 0).return_conversation()
    
    race = make_list(messages1[-1]['content'])
    race = race.split(", ")

    race_list = []
    for idx, demo in enumerate(race):
        messages2 = []
        messages2.append(messages[0])
        race_list.append(json_to_df(get_concepts("concept_name: " + demo + 'domain_id: Race' + 'standard_concept: S', n_results=70)))

        """ according to: {demo_list[idx]}"""
        
        messages2.append({"role": "user", "content":f"""Please provide a comprehensive list of race {coding} codes according to:
                           {race_list[idx]}.
                        Arrange them in a csv table with a vertical line as delimiter. Please include all possible options for {demo}.
                        The csv table should include "{coding} codes" and "demograpic feature" columns. 
                        Each categorical feature - race value -  should appear in a separate row.
                        In each row, write the relevant {demo} {coding} codes in the "{coding} codes" column without truncation, and "{demo}" in the "demograpic feature" column. 
                        Work step by step. Do not generate random codes. Use only the ones provided. Give me your best answer."""})
        
        messages2 = LLMwrapper(messages=messages2, client=client, model=model, assistant=False, role=role, temperature = 0).return_conversation()
        search = query_bing(f'Percentage of {demo} in {region}')
        messages2.append({"role": "user", "content":f"""Please add "percentage" column with the percentage of {demo} in {region}. 
                        Prioritize more recent data, preferably from government sources. Please use the following:
                          
                          {search['webPages']['value']}

                          Add a reference in the "reference" column for the percentage information source with the relevant references.
                          Give me your best answer. Do not change or remove any other column."""})
    
        messages2 = LLMwrapper(messages=messages2, client=client, model=model, assistant=False, role=role, temperature = 0).return_conversation()

        search = query_bing(f'Percentage of {demo} diagnosed with {diagnosis} in {region}')
        messages2.append({"role": "user", "content":f"""Please add "diagnosed percentage" column with the percentage of {demo} diagnosed with {diagnosis} in {region}. 
                        Prioritize more recent data, preferably from government sources. Please use the following:
                          
                          {search['webPages']['value']}

                          Add a reference in the "reference" column for the diagnosed percentage information source with the relevant references.
                          Give me your best answer. Do not change or remove any other column"""})
    
        messages2 = LLMwrapper(messages=messages2, client=client, model=model, assistant=False, role=role, temperature = 0).return_conversation()
        demo_list1.append(make_df(messages2[-1]['content'])[1])
        #messages1 += messages2[1:]

    messages = messages + messages1[1:]
        #del messages[-len(messages1)+2:-2]

    # ethnicity
    messages1 = []
    messages1.append(messages[0])
    messages1.append({"role": "user", "content":f"""List all possible {coding} concept names for all possible ethnicity options in {region}. 
                      Provide a comma separated list of the concepts separated by '```list' and '```'.
                     Just write it as single list, do not declare the category title (gender, race, ethnicity)."""})
    
    messages1 = LLMwrapper(messages=messages1, client=client, model=model, assistant=False, role=role, temperature = 0).return_conversation()
    
    ethnicity = make_list(messages1[-1]['content'])
    ethnicity = ethnicity.split(", ")

    ethnicity_list = []
    for idx, demo in enumerate(ethnicity):
        messages2 = []
        messages2.append(messages[0])
        ethnicity_list.append(json_to_df(get_concepts("concept_name: " + demo + 'domain_id: Ethnicity' + 'standard_concept: S', n_results=50)))

        """ according to: {demo_list[idx]}"""
        
        messages2.append({"role": "user", "content":f"""Please provide a comprehensive list of ethnicity {coding} codes according to:
                           {ethnicity_list[idx]}.
                        Arrange them in a csv table with a vertical line as delimiter. Please include all possible options for {demo}.
                        The csv table should include "{coding} codes" and "demograpic feature" columns. 
                        Each categorical feature - ethnicity value -  should appear in a separate row.
                        In each row, write the relevant {demo} {coding} codes in the "{coding} codes" column without truncation, and "{demo}" in the "demograpic feature" column. 
                        Work step by step. Do not generate random codes. Use only the ones provided. Give me your best answer."""})
        
        messages2 = LLMwrapper(messages=messages2, client=client, model=model, assistant=False, role=role, temperature = 0).return_conversation()

        search = query_bing(f'Percentage of {demo} in {region}')
        messages2.append({"role": "user", "content":f"""Please add "percentage" column with the percentage of {demo} in {region}. 
                        Prioritize more recent data, preferably from government sources. Please use the following:
                          
                          {search['webPages']['value']}

                          Add a reference in the "reference" column for the percentage information source with the relevant references.
                          Give me your best answer. Do not change or remove any other column."""})
    
        messages2 = LLMwrapper(messages=messages2, client=client, model=model, assistant=False, role=role, temperature = 0).return_conversation()

        search = query_bing(f'Percentage of {demo} diagnosed with {diagnosis} in {region}')
        messages2.append({"role": "user", "content":f"""Please add "diagnosed percentage" column with the percentage of {demo} diagnosed with {diagnosis} in {region}. 
                        Prioritize more recent data, preferably from government sources. Please use the following:
                          
                          {search['webPages']['value']}

                          Add a reference in the "reference" column for the diagnosed percentage information source with the relevant references.
                          Give me your best answer. Do not change or remove any other column"""})
    
        messages2 = LLMwrapper(messages=messages2, client=client, model=model, assistant=False, role=role, temperature = 0).return_conversation()


        demo_list1.append(make_df(messages2[-1]['content'])[1])
        #messages1 += messages2[1:]

    messages = messages + messages1[1:]
        #del messages[-len(messages1)+2:-2]

    #all demographics:
    messages1 = []
    messages1.append(messages[0])
    search = query_bing(f'gender statistics in {region}')
    search1 = query_bing(f'race statistics in {region}')
    search2 = query_bing(f'ethnicity statistics in {region}')
    messages1.append({"role": "user", "content":f"""Take the following table:
                      
                     {demo_list1}

                     Arrange it so that all similar codes are aggregated into a single column as a list under '{coding} code', description of the similar codes under 'demographic feature'.
                     Add population percentage in {region} under 'Percentage' column based on known statistics. For the statistics, provide **reliable and valid** references - a url or a publication.
                    
                     use the following as reference:

                        {search['webPages']['value']}

                        {search1['webPages']['value']}

                        {search2['webPages']['value']}

                     Use a vertical line as delimiter.
                     **Do not** change or remove any other column. 
                     Add 'Title: demography_coding' before the CSV. 
                     Wrap the csv in '```csv' and '```'.
                     Give me your best answer. Provide references."""})
    
    messages1 = LLMwrapper(messages=messages1, client=client, model=model, assistant=False, role=role, temperature = 0).return_conversation()    

    messages = messages + messages1[1:]

    #all demographics among diagnosed:
    messages1 = []
    messages1.append(messages[0])
    search = query_bing(f'gender statistics among patients with {diagnosis} in {region}')
    search1 = query_bing(f'race statistics among patients with {diagnosis} in {region}')
    search2 = query_bing(f'ethnicity statistics among patients with {diagnosis} in {region}')
    messages1.append({"role": "user", "content":f"""Take the following table:
                      
                     {demo_list1}

                     Arrange it so that all similar codes are aggregated into a single column as a list under '{coding} code', description of the similar codes under 'demographic feature'.
                     Add diagnosed population percentage in {region} under 'Percentage' column based on known statistics. For the statistics, provide **reliable and valid** references - a url or a publication.
                     Make sure the statistics you provide are the percentage of diagnosed patients among specific demographic groups.
                    
                     use the following as reference:

                        {search['webPages']['value']}

                        {search1['webPages']['value']}

                        {search2['webPages']['value']}

                     Use a vertical line as delimiter.
                     **Do not** change or remove any other column. 
                     Add 'Title: diagnosed_demography_coding' before the CSV. 
                     Wrap the csv in '```csv' and '```'.
                     Give me your best answer. Provide references."""})
    
    messages1 = LLMwrapper(messages=messages1, client=client, model=model, assistant=False, role=role, temperature = 0).return_conversation()    

    messages = messages + messages1[1:]
    

    # Write all in a txt, and save the statistics and concept codes in a csv
    now = str(dt.datetime.now())
    count = 0

    with open('output/%s_%s_%s_%s.txt' %(diagnosis,coding,region,model), 'w', encoding="utf-8") as f:
        f.write("%s \n\n" %now)
        
        for message in messages:
            if message['role'] == 'assistant':
                f.write(message['content'] + "\n\n")
                if ("title:") in message['content'].lower():
                    count+=1
                    title, df = make_df(message['content'])
                    title = title.replace(" ","")
                    df = df.replace('',np.nan).dropna(axis=1)
                    df.to_csv("statistics/%s_%s.csv" %(diagnosis,title), index=False)
        f.close()

    return