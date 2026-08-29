import os
import json
import time
import argparse
import pandas as pd
from create_latex import create_latex
from connect_openAI import connect_to_openAI
from free_range_testing import free_range_testing
from get_theoretical_vals import get_theoretical_vals
from create_additional_insights import create_additional_insights
from create_test_running_script import write_data_eval
from validate_test_suggestions import validate_suggestions
from write_validated_tests import write_tests as write_validated_tests

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
parser = argparse.ArgumentParser(
    description="MDPT — Medical Data Pecking Tool: generate a semantic unit-test suite for a medical dataset."
)
parser.add_argument(
    "--definition", "-d",
    default=None,
    metavar="PATH",
    help=(
        "Path to the disease definition JSON file "
        "(relative to definitions_and_dictionaries/ or absolute). "
        "Defaults to the built-in Congestive Heart Failure / MIMIC-III example."
    ),
)
parser.add_argument(
    "--data-dict", "--dd",
    default=None,
    metavar="PATH",
    help=(
        "Path to the data dictionary CSV file. "
        "Overrides the 'data_structure' field in the definition file."
    ),
)
parser.add_argument(
    "--results", "-r",
    default="results",
    metavar="FOLDER",
    help="Name of the top-level results folder (default: 'results').",
)
args = parser.parse_args()

# ---------------------------------------------------------------------------
# Load definition file
# ---------------------------------------------------------------------------
start = time.perf_counter()

os.chdir("definitions_and_dictionaries")

# Default examples (kept for reference):
#   disease_definition_path_t2d.json              — Type 2 Diabetes, US (All of Us, OMOP)
#   disease_definition_path_ckd.json              — Chronic Kidney Disease, US (All of Us, OMOP)
#   disease_definition_path_synthea_hypertension.json — Hypertension, Massachusetts (SyntheticMass, SNOMED)
#   disease_definition_path_mimic.json            — Congestive Heart Failure, Massachusetts (MIMIC-III, ICD-9)
default_definition = "disease_definition_path_mimic.json"
definition_path = args.definition if args.definition else default_definition

definition_file = json.load(open(definition_path))

Diagnosis = definition_file["population"]["diagnosis"]  # diagnosis of interest
Region    = definition_file["population"]["region"]     # geographical region of interest
Coding    = definition_file["data"]["coding"]           # coding system
Drug      = definition_file["data"]["drug"]             # drug classification system
Procedure = definition_file["data"]["procedure"]        # procedure classification system
Lab       = definition_file["data"]["lab"]              # lab test classification system

# Data dictionary: CLI flag overrides the definition file field
data_dict_path = args.data_dict if args.data_dict else definition_file["data"]["data_structure"]
data_struct = pd.read_csv(data_dict_path) if os.path.isfile(data_dict_path) else data_dict_path
if isinstance(data_struct, str):
    print("Data structure is a string — no data dictionary CSV was loaded.")

os.chdir("..")

# ---------------------------------------------------------------------------
# Create output folder structure
# ---------------------------------------------------------------------------
result_folder = args.results
if not os.path.isdir(result_folder):
    os.mkdir(result_folder)

new_folder_name = Diagnosis + "_" + Region
dircount = 0
while os.path.isdir(result_folder + "/%s/" % new_folder_name):
    dircount += 1
    new_folder_name = Diagnosis + "_" + Region + "_" + str(dircount)

os.mkdir(result_folder + "/%s/" % new_folder_name)
os.chdir(result_folder + "/%s/" % new_folder_name)
for subdir in ("logs", "output", "test_csvs", "statistics", "unit_raw", "latex", "validated", "validated/test_csvs"):
    os.mkdir(subdir)

# ---------------------------------------------------------------------------
# Run pipeline
# ---------------------------------------------------------------------------
global client, model

model = "gpt-4o-3"  # "gpt-4", "gpt-35-turbo", "gpt-4-turbo", "gpt-4o-2", "gpt-4o", "agentic_4o_bing"

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
print(f"Test generation time: {((end - start) / 60):.2f} minutes")