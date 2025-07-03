import os
import re
import ast
import json
import pandas as pd

def make_df(text):
    """
    Extracts a CSV table from the input 'text' and returns its title and a DataFrame.
    The title is extracted from the text, and the DataFrame is created from the CSV data.
    If the CSV data is empty, a message indicating that the data is unavailable is returned.
    """
    N1 = text.find("```csv\n") 
    N2 = text[N1+1:].find("\n```")
    titleLoc = text.lower().find("title:")
    titleLocEnd = text[titleLoc+6:].find("\n")
    if titleLoc > titleLocEnd:
        OldTitleLoc = titleLoc
        titleLoc = text[OldTitleLoc+2:].lower().find("title:")
        titleLoc = titleLoc + OldTitleLoc + 2
        titleLocEnd = text[titleLoc+6:].find("\n")
        
    title = text[titleLoc+6:titleLoc+6+titleLocEnd]
    NewTitle = ""
    count = 0
    for letter in title:
        if letter.isalpha():
           NewTitle += letter
        elif letter.isdigit():
           NewTitle += letter
        else:
            if (letter == "_" or letter == " " or letter == "-") and (count > 0):
                NewTitle += letter
            else:
                if count == 0:
                    NewTitle += ""
                else:
                    NewTitle += "_"
        count += 1
    if NewTitle == "" and titleLoc == -1: ## TODO: check if this is correct
        titleLocEnd = N1
        titleLoc = 0
    else:
        while NewTitle[0]==" " or NewTitle[0]=="*" or NewTitle[0]=="`" or NewTitle[0].isnumeric():
            NewTitle = NewTitle[1:]
    
    NewText = text[titleLocEnd+titleLoc+7:N1+N2+1].split("\n")
    num = 0
    for sub in NewText:
            if "|" not in sub:
                num+=1
    count = 0
    while count < num:
        for sub in NewText:
            if "|" not in sub: 
                NewText.remove(sub)
                count+=1
                break
    
    NewText2 = []
    for item in NewText:
        if item[0] == '\"':
            item = item[1:]
            if item[-1] == '\"':
                item = item[:-1]
                NewText2.append(item)
            else:
                NewText2.append(item)
        else:
            if item[-1] == '\"':
                item = item[:-1]
                NewText2.append(item)
            else:
                NewText2.append(item)

    df = pd.DataFrame([sub.split("|") for sub in NewText2])
    if df.empty:
        return "Data is unavailable", df
    else:
        df.columns = df.iloc[0]
        df.columns = df.columns.str.strip() #added later
        df = df[1:]
        df = df.map(lambda x: x.strip() if isinstance(x, str) else x) #added later
        return NewTitle, df

def make_py(text,count):
    """
    Extracts a Python code block from the input 'text' and writes it to a file.
    The filename is derived from the text (e.g., in a comment "# Filename: unit_test5.py").
    If no filename is found, a default name is generated (e.g., "unit_test1.py").
    Returns the extracted code block as a string.
    """
    N1 = text.find("```python\n") 
    N2 = text[N1+1:].find("\n```")
    titleLoc = text.lower().find("filename:")
    titleLocEnd = text[titleLoc+1:].find(".py")
    title = text[titleLoc+9:titleLoc+1+titleLocEnd].strip()
    while title[0]==" " or title[0]=="*" or title[0]=="`":
        title = title[1:]
    NewText = text[N1+10:N1+N2+1]
    if titleLocEnd == -1:
        title = f"unit_test{count+1}"
    with open("unit_raw/%s.py" %title,"wb") as fout:
        fout.write(NewText.encode())
    return NewText


def make_all_py(text, count):
    """
    Extracts all Python code blocks in the input 'text' and writes each to a file.
    If a filename is found (e.g., in a comment "# Filename: unit_test5.py"),
    that file name is used for the first extracted block.
    For subsequent blocks (or if no filename is found), a default name is generated.
    Returns a list of extracted code block strings.
    """
    # Find all Python code blocks between ```python and ```
    code_blocks = re.findall(r"```python\s*(.*?)\s*```", text, re.DOTALL)
    
    # Try to extract an overall filename from the text (case-insensitive)
    # For example: "# Filename: unit_test5.py"
    title_match = re.search(r"[Ff]ilename:\s*(\S+\.py)", text)
    base_title = None
    if title_match:
        base_title = title_match.group(1).strip()
        # Clean up leading characters if needed
        while base_title and base_title[0] in " *`":
            base_title = base_title[1:]
    
    output_blocks = []
    for i, block in enumerate(code_blocks, start=1):
        # Use the found filename for the first block if available
        if base_title and i == 1:
            filename = base_title
        else:
            filename = f"unit_test{count}.py"
        
        output_blocks.append(block+"\n\n")

    full_output = "".join(output_blocks)
    # Write the code block to a file
    with open(f"unit_raw/{filename}", "wb") as fout:
        fout.write(full_output.encode())

    return full_output


def extract_code(text):
    """
    Extracts all Python code blocks in the input 'text' and writes each to a file.
    If a filename is found (e.g., in a comment "# Filename: unit_test5.py"),
    that file name is used for the first extracted block.
    For subsequent blocks (or if no filename is found), a default name is generated.
    Returns a list of extracted code block strings.
    """
    # Find all Python code blocks between ```python and ```
    code_blocks = re.findall(r"```python\s*(.*?)\s*```", text, re.DOTALL)
    
    # Try to extract an overall filename from the text (case-insensitive)
        
    output_blocks = []
    for i, block in enumerate(code_blocks, start=1):
        # Use the found filename for the first block if available
        
        output_blocks.append(block+"\n\n")
        
    full_output = "".join(output_blocks)

    return full_output


def make_list(text):
    """
    Extracts a list from the input 'text' and returns it as a string.
    The list is expected to be in a specific format (e.g., between ```list and ```).
    If the list is not found, it tries to find it between ```plaintext and ```.
    """
    N1 = text.find("```list\n")
    ind = 8
    if N1 == -1:
        N1 = text.find("```plaintext\n")
        ind = 13
    
    N2 = text[N1+1:].find("\n```")
    return text[N1+ind:N1+N2+1]

def json_to_df(data): #for converting the json response for vector search to a dataframe
    try:
        if os.path.isfile(data): #if the passed data is a file path
            with open(data, 'r') as json_file:
                data = json.load(json_file)
        else:
            data = data
    except:
        data = data

    tempList = []
    for item in data['documents'][0]:
        tempList.append(ast.literal_eval(item))
    
    return pd.DataFrame(tempList)[['concept_id', 'concept_name', 'vocabulary_id', 'standard_concept', 'concept_code', 'invalid_reason']]