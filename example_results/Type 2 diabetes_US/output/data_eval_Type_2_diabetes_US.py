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
    
    diagnosis_codes = ['201826', '4099651', '4230254', '45757508', '4193704', '40482801', '4151282', '4200875', '3569411', '443732', '4304377', '40485020', '45757474', '4130162']
    diagnosed = diagnosis_df[diagnosis_df['condition_concept_id'].astype(str).isin(diagnosis_codes)]['person_id'].unique()
    diagnosed_drug_df = drug_df[drug_df['person_id'].isin(diagnosed)]

    return diagnosed_drug_df

def test_df(df,name):
    testing = DFTests(df) 
    testing.load_files('pecking_order_Type_2_diabetes_US.py')
    result = testing.run()
    unittestResults = DFTestResults.to_json(result, show_valid_cols=True, show_untested=True, print_all_failed=True)
    unittestResults = json.loads(unittestResults)
    with open("test_results_%s_Type_2_diabetes_US.json" %name, "w") as outfile: 
        json.dump(unittestResults, outfile, indent=4)

    return
    
        
    
def data_eval(data_df, measurement_df, drug_df):
    ''' This function runs data evaluation using DFTest'''
    data_df['condition_concept_id'] = data_df['condition_concept_id'].astype(str)
    

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