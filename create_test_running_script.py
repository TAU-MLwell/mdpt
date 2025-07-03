import pandas as pd

pd.set_option("future.no_silent_downcasting", True)


def write_data_eval(diagnosis, region, coding):
    """
    This function writes the data evaluation function to be used on the raw data.
    """

    code_list = pd.read_csv(f"statistics/{diagnosis}_{coding}_diagnosis_codes_in_{region}.csv", encoding="utf-8")
    keywords = ['code', coding.lower() + ' code', coding.lower()]
    matching_columns = [col for col in code_list.columns if any(keyword in col.lower() for keyword in keywords)]
    code_column = matching_columns[0]

    code_list = code_list[code_column].to_list()
    code_list = [str(item) for item in code_list]

    # Read the column conversion file and extract needed field names
    col_conversion = pd.read_csv(f"test_csvs/{diagnosis}_convert_to_datastruct.csv", encoding="utf-8")
    code_field = col_conversion[col_conversion['generic'] == 'code']['column_name'].item()
    person_id_field = col_conversion[col_conversion['generic'] == 'personID']['column_name'].item()


    specific = f"{diagnosis}_{region}".replace(" ", "_")

    # Create the data evaluation function
    data_eval = f"""import json
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
    
    diagnosis_codes = {code_list}
    diagnosed = diagnosis_df[diagnosis_df['{code_field}'].astype(str).isin(diagnosis_codes)]['{person_id_field}'].unique()
    diagnosed_drug_df = drug_df[drug_df['{person_id_field}'].isin(diagnosed)]

    return diagnosed_drug_df

def test_df(df,name):
    testing = DFTests(df) 
    testing.load_files('pecking_order_{specific}.py')
    result = testing.run()
    unittestResults = DFTestResults.to_json(result, show_valid_cols=True, show_untested=True, print_all_failed=True)
    unittestResults = json.loads(unittestResults)
    with open("test_results_%s_{specific}.json" %name, "w") as outfile: 
        json.dump(unittestResults, outfile, indent=4)

    return
    
        
    
def data_eval(data_df, measurement_df, drug_df):
    ''' This function runs data evaluation using DFTest'''
    data_df['{code_field}'] = data_df['{code_field}'].astype(str)
    

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
    data_eval(data_df, measurement_df, drug_df)"""
    
    # Write the data evaluation function to a file
    name = f"data_eval_{specific}.py".replace(" ", "_")
    with open(f"output/{name}", "w") as f:
        f.write(data_eval)