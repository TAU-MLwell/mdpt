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
    
    diagnosis_codes = ['46271022', '443614', '443601', '443611', '45582391', '443597', '3553408', '44792018', '37017104', '44792017', '443612', '45763854', '45763855', '37017813', '1571486', '45553438', '44830172', '619679', '45582392', '44792255', '3577568', '3577571', '196991', '3553777', '45543858', '44792227', '3553776', '45553437', '44792229', '3577573', '45582394', '3553778', '3577569', '36210709', '35209276', '45768812', '44782429', '45582393', '3553779', '36716947', '198185', '1990140', '35209279', '4322556', '44792231']
    diagnosed = diagnosis_df[diagnosis_df['condition_concept_id'].astype(str).isin(diagnosis_codes)]['person_id'].unique()
    diagnosed_drug_df = drug_df[drug_df['person_id'].isin(diagnosed)]

    return diagnosed_drug_df

def test_df(df,name):
    testing = DFTests(df) 
    testing.load_files('pecking_order_Chronic_Kidney_Disease_US.py')
    result = testing.run()
    unittestResults = DFTestResults.to_json(result, show_valid_cols=True, show_untested=True, print_all_failed=True)
    unittestResults = json.loads(unittestResults)
    with open("test_results_%s_Chronic_Kidney_Disease_US.json" %name, "w") as outfile: 
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