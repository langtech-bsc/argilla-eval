import argilla as rg
from dotenv import load_dotenv
import os
import json
import yaml

from utils.diff2html import get_html_diff

load_dotenv()
RG_API_URL = os.getenv('API_URL')
RG_API_KEY = os.getenv('API_KEY')
EVAL_WORKSPACE = os.getenv('RG_WORKSPACE')
NUMBER_USERS = int(os.getenv('NUMBER_USERS'))
DATASET_PATH = os.getenv('DATASET_PATH')
DATASET_NAME = os.getenv('DATASET_NAME')

client = rg.Argilla(
    api_url=RG_API_URL, 
    api_key=RG_API_KEY
)

def load_json(file_path, encoding=None):
    with open(file_path, 'r', encoding=encoding) as file:
        return json.load(file)

def load_yaml(file_path, encoding=None):
    with open(file_path, 'r', encoding=encoding) as file:
        return yaml.load(file, Loader=yaml.FullLoader)

def generate_label_markdown(labels):
    markdown = ""
    for key, values in labels.items():
        markdown += f"<details>\n"
        markdown += f"<summary>{key}</summary>\n\n"
        for value in values:
            markdown += f"- {value}\n"
        markdown += f"\n</details>\n"
    return markdown

input_h_labels_dict = load_yaml('labels/taxonomy_labels_test.yml')
input_h_labels = list(input_h_labels_dict.keys())
label_markdown = generate_label_markdown(input_h_labels_dict)

"""DATASET SETTINGS"""
settings = rg.Settings(
    distribution=rg.TaskDistribution(min_submitted=NUMBER_USERS),
    allow_extra_metadata=True,
    guidelines="""
    Please label the errors according to the given taxonomy. If a new type of error is observed please introduce it to the text box.
    Insert error labeling instructions here.\n\n
"""+label_markdown,
    fields=[
            rg.TextField(
                name="visual",
                title="Visual",
                use_markdown=True,
                required=True,
                description="Field description"
            ),
            rg.TextField(
                name="ref_errors",
                title="Reference Errors",
                use_markdown=True,
                required=True,
                description="Field description"
            )
        ],
    questions=[
        rg.LabelQuestion(
            name="label",
            title="What is the corresponding error?",
            description="Select the one that applies.",
            required=True,
            labels=['None']+input_h_labels
          
        ),
        rg.TextQuestion(
            name="sublabel",
            title="What is the specific type of the given error? (Please check the error reference)",
            description="Please check the error reference, and write the subtype in the text box.",
            use_markdown=True,
            required=True
        ),
        rg.TextQuestion(
            name="text",
            title="Copy and modify the reference here if there is anything you would like to modify with the original reference.",
            description="If there is anything you would modify in the response copy and edit the response in this field.",
            use_markdown=True,
            required=False
        )
    ],
)

print(DATASET_PATH, type(DATASET_PATH))
data_file = load_json(DATASET_PATH)

"""DATASET CREATION"""
dataset = rg.Dataset(
    name=DATASET_NAME,
    workspace=EVAL_WORKSPACE,
    settings=settings,
    client=client
).create()

## JSON DIFF

html_diff = get_html_diff("sample_data/1.json", "sample_data/2.json")

""""LOGIN RECORDS"""
records = []
for item in data_file:
    record = rg.Record(
        id=item["instance_id"],
        fields={
            "visual": html_diff,
            "ref_errors": label_markdown
        }
    )
    records.append(record)

dataset.records.log(records)