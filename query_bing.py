#Copyright (c) Microsoft Corporation. All rights reserved.
#Licensed under the MIT License.

# -*- coding: utf-8 -*-

import json
import os
from pprint import pprint
import requests
import datetime as dt
from azure.ai.agents.models import BingGroundingTool



def query_bing(query):
    '''
    This sample makes a call to the Bing Web Search API with a query and returns relevant web search.
    Documentation: https://docs.microsoft.com/en-us/bing/search-apis/bing-web-search/overview
    '''

    # Add your Bing Search V7 subscription key and endpoint to your environment variables.
    subscription_key = os.environ['BING_API_KEY'] #os.environ['BING_API_KEY2'] #
    endpoint = os.environ['BING_ENDPOINT']

    # Query term(s) to search for. 
    query = f'{query}' + '&responseFilter=webpages'+f'&freshness=2020-01-01..{dt.datetime.today().date()}'  + '&count=11' + '&sortBY=Relevance'+'&offset=0'

    # Construct a request
    mkt = 'en-us'
    params = { 'q': query, 'mkt': mkt}
    headers = { 'Ocp-Apim-Subscription-Key': subscription_key }

    # Call the API
    try:
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()

        print("Headers:")
        print(response.headers)

        print("JSON Response:")
        pprint(response.json())
    except Exception as ex:
        raise ex
    
    return response.json()