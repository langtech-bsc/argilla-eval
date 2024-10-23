
import argilla as rg
from dotenv import load_dotenv
import os
import json
load_dotenv()

RG_API_URL = os.getenv('API_URL')
RG_API_KEY = os.getenv('API_KEY')
EVAL_WORKSPACE = os.getenv('RG_WORKSPACE')
DATASET_PATH = os.getenv('DATASET_PATH')
DATASET_NAME = os.getenv('DATASET_NAME')

client = rg.Argilla(
    api_url=RG_API_URL, 
    api_key=RG_API_KEY
)

def load_json(file_path, encoding=None):
    with open(file_path, 'r', encoding=encoding) as file:
        return json.load(file, encoding=encoding)
    
data_file = load_json(DATASET_PATH)

""""QUERY RECORDS"""
dataset = client.datasets(name=DATASET_NAME, workspace=client.workspaces(EVAL_WORKSPACE))
exported_records = dataset.records.to_json("./records.json")

record_file = load_json('records.json', encoding='utf-8')
data_dict = {item['instance_id']: item for item in data_file}

""""ADDING ORIGINAL PROPERTIES"""
for record_object in record_file:
    instance_id = int(record_object['id'])
    if instance_id in data_dict:
        record_object.update({
            "lang": data_dict[instance_id]["lang"],
            "model_A": data_dict[instance_id]["model_A"],
            "model_B": data_dict[instance_id]["model_B"],
        })

with open('records.json', 'w', encoding='utf-8') as json_file:
    json.dump(record_file, json_file, ensure_ascii=False, indent=4)