import os
from openai import AzureOpenAI
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential, AzureCliCredential

def connect_to_openAI(model):
    '''connect to openAI API'''
    
    if model=="gpt-35-turbo" or model=="gpt-4" or model=="gpt-4-turbo":
        client = AzureOpenAI(
        api_key=os.environ["AZURE_API_KEY"],
        api_version="2024-05-01-preview",
        azure_endpoint = os.environ["AZURE_ENDPOINT"]
    )
        agent = None
        thread = None

    elif model=="gpt-4o" or model=="gpt-4o-2" or model=="gpt-4o-3" or model=="text-embedding-3-small":
        #EastUS - for gpt4o
        client = AzureOpenAI(
            api_key=os.environ["AZURE_API_KEY_4o"],
            api_version="2024-05-01-preview",
            azure_endpoint = os.environ["AZURE_ENDPOINT_4o"]
        )
        agent = None
        thread = None

    elif model=="agentic_4o_bing":
        
        client = AIProjectClient.from_connection_string(
            #credential = InteractiveBrowserCredential(),
            credential= DefaultAzureCredential(),
            conn_str=os.environ["AGENT_CONNECTION_STRING"])
        
    return client