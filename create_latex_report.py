import os
import json
import datetime as dt
import re

def escape_latex(text):
    """
    Escape underscore and percent characters in text unless already escaped.
    """
    text = str(text)
    # The following regex substitutes an underscore not preceded by a backslash
    text = re.sub(r'(?<!\\)_', r'\\_', text)
    text = re.sub(r'(?<!\\)%', r'\\%', text)
    return text

def process_test_results(test_results):
    """
    Process a test_results dictionary.
    Aggregates tests (by test_name) so that each test (except 'dftest_check_data_types')
    appears only once. If multiple instances exist and one passes, keep that one.
    For 'dftest_check_data_types', store the first encountered instance.

    Also collects tests that encountered errors (test_flag == "error").

    Returns a tuple:
      (aggregated rows [list of dicts], error_tests [list of dicts])
    """
    aggregated = {}
    check_data_types_row = None
    error_tests = []  # List to collect tests with errors

    for col_key in test_results:
        if col_key in ['columns_tested', 'total_columns', 'valid_columns']:
            continue

        col = test_results[col_key]
        if 'tested' in col and not col['tested']:
            continue

        for test_key in col:
            if test_key in ['column', 'columns_number']:
                continue

            test_entry = col[test_key]
            test_name = test_entry.get('test_name', '')

            exp_str = test_entry.get('test_explanation', '')
            # Replace single quotes with double quotes and "nan" with "-999"
            exp_str = exp_str.replace("'", "\"").replace("nan", "-999")
            try:
                exp = json.loads(exp_str)
            except Exception:
                continue

            # If the test_flag indicates error, record it and skip further processing.
            if exp.get('test_flag', '') == 'error':
                error_tests.append({
                    "test_name": test_name,
                    "display_name": test_name[7:].replace('_', ' ') if test_name.startswith("dftest_") else test_name,
                    "explanation": exp.get("explanation", "No explanation provided.")
                })
                continue

            result_bool = test_entry.get('result', False)
            result_text = "Pass" if result_bool else "Fail"
            prefix = "\\highlightPass" if result_bool else "\\highlightFail"

            expected_val = ""
            actual_val = ""
            smd_val = ""
            ratio_val = ""
            prefix_smd = ""
            prefix_ratio = ""

            if "expected_value" in exp:
                expected_val = str(exp["expected_value"])
                if "data_per" in exp:
                    try:
                        actual_val = f"{float(exp['data_per']):.2f}"
                    except:
                        actual_val = str(exp['data_per'])
                elif "data_in_range" in exp:
                    try:
                        actual_val = f"{float(exp['data_in_range']):.2f}"
                    except:
                        actual_val = str(exp['data_in_range'])
                if "smd" in exp:
                    try:
                        smd = float(exp["smd"])
                        smd_val = f"{smd:.2f}"
                        if abs(smd) < 0.2:
                            prefix_smd = "\\highlightKeep"
                        else:
                            prefix_smd = "\\highlightFail"
                    except:
                        smd_val = str(exp["smd"])
                if "ratio" in exp:
                    try:
                        ratio = float(exp["ratio"])
                        ratio_val = f"{ratio:.2f}"
                        if 0.85 <= ratio <= 1.15:
                            prefix_ratio = "\\highlightKeep"
                        else:
                            prefix_ratio = "\\highlightFail"
                    except:
                        ratio_val = str(exp["ratio"])
            elif "data_in_range" in exp:
                expected_val = "95\\%"
                try:
                    actual_val = f"{float(exp['data_in_range']):.2f}"
                except:
                    actual_val = str(exp['data_in_range'])
                # SMD and ratio remain empty.

            row = {
                "test_name": test_name,
                "display_name": test_name[7:].replace('_', ' ') if test_name.startswith("dftest_") else test_name,
                "result_text": result_text,
                "prefix": prefix,
                "expected": expected_val,
                "actual": actual_val,
                "smd": f"{prefix_smd}{{{smd_val}}}" if smd_val else "",
                "ratio": f"{prefix_ratio}{{{ratio_val}}}" if ratio_val else ""
            }

            # For tests (other than check data types) with no valid expected value,
            # override to show "No Reference" (and remove -999).
            if test_name != "dftest_check_data_types" and (expected_val.strip() == "" or expected_val.strip() == "-999"):
                row["result_text"] = "No Reference"
                row["prefix"] = "\\highlightNoRef"
                row["expected"] = ""
                row["smd"] = ""
                row["ratio"] = ""

            if test_name == "dftest_check_data_types":
                if check_data_types_row is None:
                    check_data_types_row = row
            else:
                if test_name in aggregated:
                    # If one version shows Fail and the new version passes, override.
                    if aggregated[test_name]['result_text'] == "Fail" and row["result_text"] == "Pass":
                        aggregated[test_name] = row
                else:
                    aggregated[test_name] = row

    rows = list(aggregated.values())
    if check_data_types_row:
        rows.append(check_data_types_row)
    return rows, error_tests

def generate_longtable(rows, caption, label):
    """
    Given a list of row dictionaries, returns a string representing a longtable
    wrapped in an adjustbox so that it fits within the text width.
    Each row dict is expected to have keys:
      'display_name', 'prefix', 'result_text', 'expected', 'actual', 'smd', and 'ratio'.
    Before printing, underscores and percent signs are escaped.
    """
    table = ""
    table += "\\begin{longtable}{p{7.5cm} c c c c c}\n"
    table += f"\\label{{{escape_latex(label)}}}\\\\\n"
    table += "\\textbf{Test name} & \\textbf{Result} & \\textbf{Expected value} & \\textbf{Actual value} & \\textbf{SMD} & \\textbf{ratio}\\\\\n"
    table += "\\hline\n"
    table += "\\endfirsthead\n"
    table += "\\multicolumn{6}{c}{{\\bfseries Continued from previous page}}\\\\\n"
    table += "\\hline\n"
    table += "\\textbf{Test name} & \\textbf{Result} & \\textbf{Expected value} & \\textbf{Actual value} & \\textbf{SMD} & \\textbf{ratio}\\\\\n"
    table += "\\hline\n"
    table += "\\endhead\n"
    table += "\\hline \\multicolumn{6}{r}{{Continued on next page}}\\\\\n"
    table += "\\endfoot\n"
    table += "\\hline\n"
    table += "\\endlastfoot\n"

    for row in rows:
        # Escape underscores and percent signs in text fields.
        display = escape_latex(row['display_name'])
        result = escape_latex(row['result_text'])
        expected = escape_latex(row['expected'])
        actual = escape_latex(row['actual'])
        # For smd and ratio, we assume they are generated by our code (including macros) so they are left as-is.
        smd = row['smd']
        ratio = row['ratio']
        table += f"{display} & {row['prefix']}{{{result}}} & {expected} & {actual} & {smd} & {ratio} \\\\ \n"
        table += "\\hline\n"
    table += "\\end{longtable}\n"
    return table


# --- Main Code ---

definition_path = "definitions_and_dictionaries/disease_definition.json"
data_reports_path = "data_reports"


with open(definition_path, "r") as f:
    definition_file = json.load(f)

Diagnosis = definition_file['population']['diagnosis']
Region = definition_file['population']['region']

today = str(dt.datetime.now().date())
specific = f"{Diagnosis}_{Region}".replace(" ", "_")

os.chdir(data_reports_path)
with open(f"test_results_diagnoses_demography_{specific}.json", "r") as f:
    test_results_demography = json.load(f)
with open(f"test_results_measurements_{specific}.json", "r") as f:
    test_results_measurements = json.load(f)
with open(f"test_results_drugs_{specific}.json", "r") as f:
    test_results_drugs = json.load(f)

# Process each file to get aggregated rows and error lists.
rows_demography, errors_demography = process_test_results(test_results_demography)
rows_drugs, errors_drugs = process_test_results(test_results_drugs)
rows_measurements, errors_measurements = process_test_results(test_results_measurements)

table_demography = generate_longtable(rows_demography,
    f"Demography and Diagnosis Tests for {Diagnosis} in {Region}",
    "tab:demo_diagnosis")
table_drugs = generate_longtable(rows_drugs,
    f"Drug Tests for {Diagnosis} in {Region}",
    "tab:drugs")
table_measurements = generate_longtable(rows_measurements,
    f"Measurement Tests for {Diagnosis} in {Region}",
    "tab:measurements")


os.chdir("final_reports")
base_folder_name = f"{Diagnosis}_{Region}_DQE_report"
new_folder_name = base_folder_name
dircount = 0
while os.path.isdir(new_folder_name):
    dircount += 1
    new_folder_name = f"{base_folder_name}_{dircount}"
os.mkdir(new_folder_name)
os.chdir(new_folder_name)

# Construct the complete LaTeX document.
beginning = (
    "\\documentclass[11pt]{article}\n"
    "\\setlength{\\parindent}{0pt}\n"
    "\\usepackage[margin=0.6in]{geometry}\n"
    "\\usepackage{xcolor}\n"
    "\\usepackage{mathptmx}\n"
    "\\usepackage{amsmath}\n"
    "\\usepackage{graphicx}\n"
    "\\usepackage{booktabs}\n"
    "\\usepackage{longtable}\n"
    "\\usepackage{adjustbox}\n"
    "\\usepackage{float}\n"
    "\\definecolor{grassgreen}{RGB}{50,170,50}\n\n"
    "\\newcommand{\\highlightFail}[1]{\\textcolor{red}{#1}}\n"
    "\\newcommand{\\highlightPass}[1]{\\textcolor{grassgreen}{#1}}\n"
    "\\newcommand{\\highlightKeep}[1]{\\textcolor{black}{#1}}\n"
    "\\newcommand{\\highlightNoRef}[1]{\\textcolor{orange}{#1}}\n\n"
    "\\title{" + Diagnosis.capitalize() + " in " + Region + " - Data Quality Evaluation Report}\n\n"
    "\\begin{document}\n"
    "\\maketitle\n\n"
)

sections = (
    "\\section{Demography and Diagnosis Tests}\n\n" + table_demography + "\n\n" +
    "\\section{Drug Tests}\n\n" + table_drugs + "\n\n" +
    "\\section{Measurement Tests}\n\n" + table_measurements + "\n\n"
)

end = "\\end{document}"

latex_content = beginning + sections + end

tex_filename = f"{Diagnosis} in {Region} data evaluation report_{today}.tex"
with open(tex_filename, "w", encoding="UTF-8") as f:
    f.write(latex_content)

# Optionally, compile the LaTeX file:
# subprocess.run(["latexmk", "-pdf", tex_filename])