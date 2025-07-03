import os
import json
import numpy as np
import pandas as pd
import datetime as dt
from ask_gpt import LLMwrapper
from openai import AzureOpenAI
from connect_openAI import connect_to_openAI

def create_additional_insights(diagnosis, region, coding, drug, procedure, lab, model):
    # gpt model for use
    global messages, client
    
    client = connect_to_openAI(model)

    messages = []

    message_queue = [
                f"You are an expert in {diagnosis} in {region}. Answer as concisely as possible. Answer for the provided diagnosis, region, coding system, and drug classification system.",
               
               f"For a person who is unfamiliar with {diagnosis}, both in {region} and worldwide, can you share crucial information for epidemiological research? describe it in its medical"
               f"and guideline contexts in {region}. Please provide references and arrange this in a structured text. separate the reply with '```text' and '```'.",
               
               f"Were there any global and local policy changes since 2000, regarding the diagnosis and treatment of {diagnosis}? Include years. Please provide references and arrange this in "
               f"a structured text. separate the reply with '```text' and '```'.",
    ]

    
    # communicate with Azure OpenAI API:
    for i, message in enumerate(message_queue):
        if i==0:
            messages.append({"role": "system", "content": message})
            role = "system"
        else:
            messages.append({"role": "user", "content": message})
            role = "user"
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
        messages = LLMwrapper(messages, client, model, role=role).return_conversation()

    # Write all in a document:
    now = str(dt.datetime.now())
    today = str(dt.datetime.now().date())
    count = 0

    with open('output/%s_insights.txt' %(diagnosis), 'w', encoding="utf-8") as f:
        for message in messages:
            if message['role'] == 'assistant':
                if ("```text\n") in message['content'].lower():
                    N1 = message['content'].find("```text\n")
                    N2 = message['content'][N1+1:].find("\n```")
                    NewText = message['content'][N1+8:N1+N2+1]
                    f.write(NewText + "\n\n")

        f.close()

    return
