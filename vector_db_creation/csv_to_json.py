import csv
import json

def make_json(csvFilePath, jsonFilePath):
    
    # create a dictionary
    data = {}
    
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf, delimiter='\t')
        
        for i,rows in enumerate(csvReader):    
            key = i
            data[key] = rows

    #write data
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))
        
#CSV input and json output file paths: 
csvFilePath = r'CONCEPT.csv'
jsonFilePath = r'concepts.json'

# make json
make_json(csvFilePath, jsonFilePath)
