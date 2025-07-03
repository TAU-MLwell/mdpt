import json
import numpy as np
import pandas as pd
import datetime as dt
from dftest.style import StyleFile, Style
from dftest.DFTests import DFTests, DFTestResults, ColumnResults

def diagnosed_drugs(drug_df, diagnosis_df):
    '''
    This function takes all patient ids of patients with a certain diagnosis and returns 
    a drug dataframe with only the drugs of those patients.
    '''
    
    diagnosis_codes = ['428.0', '428.2', '428.9', '398.91', '428.2', '428.0']
    diagnosed = diagnosis_df[diagnosis_df['icd9_code'].astype(str).isin(diagnosis_codes)]['subject_id'].unique()
    diagnosed_drug_df = drug_df[drug_df['subject_id'].isin(diagnosed)]

    return diagnosed_drug_df

def test_df(df,name):
    testing = DFTests(df) 
    testing.load_files('pecking_order_Congestive_Heart_Failure_Massachusetts.py')
    result = testing.run()
    unittestResults = DFTestResults.to_json(result, show_valid_cols=True, show_untested=True, print_all_failed=True)
    unittestResults = json.loads(unittestResults)
    with open("test_results_%s_Congestive_Heart_Failure_Massachusetts.json" %name, "w") as outfile: 
        json.dump(unittestResults, outfile, indent=4)

    return
    
        
    
def data_eval(data_df, measurement_df, drug_df):
    ''' This function runs data evaluation using DFTest'''
    data_df['icd9_code'] = data_df['icd9_code'].astype(str)
    

    test_df(data_df, 'diagnoses_demography')
    test_df(measurement_df, 'measurements')
    drug_diag = diagnosed_drugs(drug_df, data_df)
    test_df(drug_df, 'drugs')

    return
    
def main():
    # Load the data
    data_df = pd.read_csv(YOUR_DATA_FILE) #data_df should contain both diagnosis and demography data
    measurement_df = pd.read_csv(YOUR_MEASUREMENT_FILE)
    drug_df = pd.read_csv(YOUR_DRUG_FILE)
    
    # Run the data evaluation
    data_eval(data_df, measurement_df, drug_df)