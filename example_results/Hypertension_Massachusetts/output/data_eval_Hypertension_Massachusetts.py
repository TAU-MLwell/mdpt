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
    
    diagnosis_codes = ['38341003', '266287006', '56218007', '194756002', '155295004', '64715009', '827069000', '449759005', '194760004', '429457004', '155297007', '827068008', '194759009', '194794002', '471521000000108', '155302005', '195537001', '473392002', '367390009', '599341000000105', '32966004', '194757006', '702817009', '194769003', '155299005', '46113002', '48146000', '137753003', '194776008', '86234004', '194788005', '194772005', '762463000', '845891000000103', '38481006', '60899001', '194791005', '194782006', '132721000119104', '10725009']
    diagnosed = diagnosis_df[diagnosis_df['Code'].astype(str).isin(diagnosis_codes)]['Patient'].unique()
    diagnosed_drug_df = drug_df[drug_df['Patient'].isin(diagnosed)]

    return diagnosed_drug_df

def test_df(df,name):
    testing = DFTests(df) 
    testing.load_files('pecking_order_Hypertension_Massachusetts.py')
    result = testing.run()
    unittestResults = DFTestResults.to_json(result, show_valid_cols=True, show_untested=True, print_all_failed=True)
    unittestResults = json.loads(unittestResults)
    with open("test_results_%s_Hypertension_Massachusetts.json" %name, "w") as outfile: 
        json.dump(unittestResults, outfile, indent=4)

    return
    
        
    
def data_eval(data_df, measurement_df, drug_df):
    ''' This function runs data evaluation using DFTest'''
    data_df['Code'] = data_df['Code'].astype(str)
    

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