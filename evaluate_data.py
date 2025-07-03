import os
import json
import time
import pandas as pd
from write_tests import write_tests
from create_latex import create_latex
from connect_openAI import connect_to_openAI
from free_range_testing import free_range_testing
from get_theoretical_vals import get_theoretical_vals 
from create_additional_insights import create_additional_insights
from create_test_running_script import write_data_eval
from validate_tests import validate_tests
from validate_test_suggestions import validate_suggestions
from write_validated_tests  import write_tests as write_validated_tests

start = time.perf_counter()

os.chdir('definitions_and_dictionaries')
# Load the disease definition file
#definition_file = json.load(open("disease_definition_path_t2d.json"))
#definition_file = json.load(open("disease_definition_path_ckd.json"))
#definition_file = json.load(open("disease_definition_path_synthea_hypertension.json"))
definition_file = json.load(open("disease_definition_path_mimic.json"))


result_folder = 'results_for_paper2' # 'results' # 'results_for_paper'


Diagnosis = definition_file['population']['diagnosis'] # diagnosis of interest
Region = definition_file['population']['region'] # geographical region of interest
Coding = definition_file['data']['coding'] # coding system
Drug = definition_file['data']['drug'] # drug classification system
Procedure = definition_file['data']['procedure'] # procedure classification system  
Lab = definition_file['data']['lab'] # lab test classification system

data_struct = pd.read_csv(definition_file['data']['data_structure']) if os.path.isfile(definition_file['data']['data_structure']) else definition_file['data']['data_structure'] # data structure
if type(data_struct)==str:
    print('Data structure is a string, no file was loaded.')

os.chdir('..')

#check if there's a results folder (otherwise create one)
#if os.path.isdir('results')==False: os.mkdir('results')
if os.path.isdir(result_folder)==False: os.mkdir(result_folder)



# Create a new folder for the diagnosis
new_folder_name = Diagnosis+'_'+Region
dircount=0
while os.path.isdir(result_folder+'/%s/' %(new_folder_name))==True:
    dircount+=1
    new_folder_name = Diagnosis+'_'+Region+'_'+str(dircount)
os.mkdir(result_folder + '/%s/' %(new_folder_name))
os.chdir(result_folder + '/%s/' %(new_folder_name))
os.mkdir('logs/')
os.mkdir('output/')
os.mkdir('test_csvs/')
os.mkdir('statistics/')
os.mkdir('unit_raw/')
os.mkdir('latex/')
os.mkdir('validated/')
os.mkdir('validated/test_csvs/')



global client, model

model = "gpt-4o-3" # "gpt-4" , "gpt-35-turbo", "gpt-4-turbo" #"gpt-4o-2" #"gpt-4o" "agentic_4o_bing" #

# Run the functions
get_theoretical_vals(Diagnosis, Region, Coding, Drug, Procedure, Lab, model) 
create_additional_insights(Diagnosis, Region, Coding, Drug, Procedure, Lab, model)
create_latex(Diagnosis, Region, Coding, Drug, Procedure, Lab, model) 
free_range_testing(Diagnosis, Region, Coding, Drug, Procedure, Lab, data_struct, model)

model = "agentic_4o_bing"
validate_suggestions(Diagnosis, Region, Coding, Drug, Procedure, Lab, model)

model = "gpt-4o-3" 
write_validated_tests(Diagnosis, Region, Coding, Drug, Procedure, Lab, data_struct, model)
write_data_eval(Diagnosis, Region, Coding)

end = time.perf_counter()
print(f"Test generation time: {((end-start)/60):.2f} minutes")