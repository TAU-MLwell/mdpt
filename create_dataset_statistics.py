import os
import numpy as np
import datetime as dt
from openai import AzureOpenAI
import pandas as pd
import json
from connect_openAI import connect_to_openAI
from ask_gpt import ask_gpt


def make_py(text):
    N1 = text.find("```python\n") 
    N2 = text[N1+1:].find("\n```")
    titleLoc = text.lower().find("filename:")
    titleLocEnd = text[titleLoc+1:].find(".py")
    title = text[titleLoc+9:titleLoc+1+titleLocEnd]
    NewTitle = ""
    for letter in title:
        if letter.isalpha() or letter.isdigit():
           NewTitle += letter
        else:
            if letter == "_" or letter == " " or letter == "-":
                NewTitle += letter
    if NewTitle[0] == ' ' or NewTitle[0] == '`':
        NewTitle = NewTitle[1:]
    NewText = text[N1+10:N1+N2+1]
    with open("%s.py" %NewTitle,"wb") as fout:
        fout.write(NewText.encode())
    return 


def create_dataset_statistics(diagnosis, region, coding, drug, procedure, data_struct):
    # gpt model for use
    global messages, client, model

    model ="gpt-4o" # "gpt-4" , "gpt-35-turbo", "gpt-4-turbo"

    #while os.isdir('results_%s' %diagnosis)==False:
    
    for item in os.listdir():
        if ("results" and diagnosis) in item:
            work_dir = item
    
    try:
        os.chdir(work_dir)
    except:
        print('No such directory')
    
    for item in os.listdir():
        if '.txt' in item:
            continue
        elif 'age distribution' in item.lower():
            age_dist = pd.read_csv(item)
        elif drug.lower() in item.lower():
            drugs = pd.read_csv(item)
        elif procedure.lower() in item.lower():
            procedures = pd.read_csv(item)
        elif ('codes' or coding.lower() in item.lower()) and ('comorbidities' not in item.lower()) and ('statistics' not in item.lower()):
            diag_codes = pd.read_csv(item) 
        elif 'statistics' in item.lower():
            stats = pd.read_csv(item)
        elif 'comorbidities' in item.lower():
            comorbidities = pd.read_csv(item)
        elif 'laboratory' or 'lab' in item.lower():
            laboratory = pd.read_csv(item)
            
    stats_header = stats.columns

    # connect to OpenAI api
    client = connect_to_openAI(model)

    messages = []


    message_queue = [
        
        f"You are a data-science expert. I would like to calculate various parameters from {data_struct}. Please provide a list of all tables and columns in it. Double check column names. Add references. Give me your best answer.",

        f"Assume the {data_struct} data was loaded into a single pandas dataframe as is. Column names remain as they are in the original {data_struct} dataset. Write a python function that calculates the {stats_header.values} of {diagnosis} patients in the dataset. use {diag_codes}"
        f"Make sure it arranges the data in a dataframe structures as follows: Prevalence | Incidence | Mortality rate | Lifetime risk | Survival | total population size in the dataset (millions)"
        f"Save the data as a csv file. Suggest a name for the python code with a 'Filename:' prefix at the top of your reply. Do it step by step. give me your best answer.",

        f"Assume the {data_struct} data was loaded into a single pandas dataframe as is. please write a function that calculates the diagnosis age distribution among diagnosed with {diagnosis} in the dataset."
        f"Make sure the code saves the results in a csv file. Suggest a name for the python code with a 'Filename:' prefix at the top of your reply. Do it step by step. give me your best answer.",

        f"Assume the {data_struct} data was loaded into a single pandas dataframe as is. please write a function that calculates the percentage of {diagnosis} patients treated with each of the drugs in {drugs} in the dataset. Suggest a name for the python code with a 'Filename:' prefix at the top of your reply. Do it step by step. give me your best answer.",

        f"Assume the {data_struct} data was loaded into a single pandas dataframe as is. please write a function that calculates the percentage of {diagnosis} patients going through the procedures in {procedures} in the dataset. Suggest a name for the python code with a 'Filename:' prefix at the top of your reply. Do it step by step. give me your best answer.",

        f"Assume the {data_struct} data was loaded into a single pandas dataframe as is. please write a function that calculates the percentage of procedures with out-of-normal-range results from  {procedures} for {diagnosis} patients in the dataset. Suggest a name for the python code with a 'Filename:' prefix at the top of your reply. Do it step by step. give me your best answer."
        
        f"Based on {data_struct} list of columns, evaluate percentage of missing data in each column. Save the results in a csv file. Suggest a name for the python code with a 'Filename:' prefix at the top of your reply. Do it step by step. give me your best answer."

        f"Assume the {data_struct} data was loaded into a single pandas dataframe as is. evaluate the correct order of events for {diagnosis} patients. Evaluate percentage of incorrect order. Save the results in a csv file. Suggest a name for the python code with a 'Filename:' prefix at the top of your reply. Do it step by step. give me your best answer."

        #f"Based on {data_struct}, evaluate the correlation between each pair of columns. Save the results in a csv file. Suggest a name for the saved python file with a 'Filename:' prefix at the top of your reply."

    ]

    # get disease statistics values from OpenAI
    for message in message_queue:
        messages.append({"role": "user", "content": message})
        reply = ask_gpt(message, client, model, pr=False)
        messages.append({"role": "assistant", "content": reply})

    

    now = str(dt.datetime.now())
    today = str(dt.datetime.now().date())
    count = 0

    with open('%s_%s_%s_%s_%s.txt' %(today,diagnosis,coding,region,model), 'w', encoding="utf-8") as f:
        f.write("%s \n\n" %now)
        
        for message in messages:
            if message['role'] == 'assistant':
                if ("```python") in message['content'].lower():
                    count+=1
                    f.write(message['content'] + "\n\n")
                    make_py(message['content'])
                else:
                    f.write(message['content'] + "\n\n")
        f.close()

    os.chdir('..')
    return