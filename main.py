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

data_files = [
 ("test_i01.09.json", "pred_i01.09.json"),
 ("test_i01.1003-1.json", "pred_i01.1003-1.json"),
 ("test_i01.1004-3.json", "pred_i01.1004-3.json"),
 ("test_i01.1007-4.json", "pred_i01.1007-4.json"),
 ("test_i01.1010-4.json", "pred_i01.1010-4.json"),
 ("test_i02.00.json", "pred_i02.00.json"),
 ("test_i02.02.json", "pred_i02.02.json"),
 ("test_i02.06.json", "pred_i02.06.json"),
 ("test_i02.09.json", "pred_i02.09.json"),
 ("test_i02.1004.json", "pred_i02.1004.json"),
 ("test_i02.1008-3.json", "pred_i02.1008-3.json"),
  ("test_i04.02-4-2.json", "pred_i04.02-4-2.json"),
 ("test_i04.06-1-2.json", "pred_i04.06-1-2.json"),
 ("test_i04.10-4-4.json", "pred_i04.10-4-4.json"),
 ("test_i04.11-1-3.json", "pred_i04.11-1-3.json"),
 ("test_i04.12-2-4.json", "pred_i04.12-2-4.json"),
 ("test_i04.14-4-3.json", "pred_i04.14-4-3.json"),
 ("test_i04.15-5-2.json", "pred_i04.15-5-2.json"),
 ("test_i04.20-3-2.json", "pred_i04.20-3-2.json"),
 ("test_i04.21-4-1.json", "pred_i04.21-4-1.json"),
 ("test_i04.24-2-2.json", "pred_i04.24-2-2.json"),
 ("test_i04.27-5-2.json", "pred_i04.27-5-2.json"),
 ("test_i04.28-4-2.json", "pred_i04.28-4-2.json"),
 ("test_i04.29-3-1.json", "pred_i04.29-3-1.json"),
 ("test_i04.36-3-1.json", "pred_i04.36-3-1.json"),
 ("test_i04.38-3-4.json", "pred_i04.38-3-4.json"),
 ("test_i04.40-3-1.json", "pred_i04.40-3-1.json"),
 ("test_i04.41-5-1.json", "pred_i04.41-5-1.json"),
 ("test_i04.51-4-2.json", "pred_i04.51-4-2.json"),
 ("test_i04.53-5-1.json", "pred_i04.53-5-1.json"),
 ("test_i04.54-2-1.json", "pred_i04.54-2-1.json"),
 ("test_i04.59-1-3.json", "pred_i04.59-1-3.json"),
 ("test_i04.60-3-1.json", "pred_i04.60-3-1.json"),
 ("test_i04.65-4-3.json", "pred_i04.65-4-3.json"),
 ("test_i04.70-1.json", "pred_i04.70-1.json"),
 ("test_i04.71-1-4.json", "pred_i04.71-1-4.json"),
 ("test_i04.76-2-3.json", "pred_i04.76-2-3.json"),
 ("test_i04.79-1-1.json", "pred_i04.79-1-1.json"),
 ("test_i04.80-2-3.json", "pred_i04.80-2-3.json"),
 ("test_i04.87-3-4.json", "pred_i04.87-3-4.json"),
 ("test_i04.90-4-1.json", "pred_i04.90-4-1.json"),
 ("test_i05.1110.json", "pred_i05.1110.json"),
 ("test_i05.113-3.json", "pred_i05.113-3.json"),
 ("test_i05.1154.json", "pred_i05.1154.json"),
 ("test_i05.116-3.json", "pred_i05.116-3.json"),
 ("test_i05.120-2.json", "pred_i05.120-2.json"),
 ("test_i05.1218.json", "pred_i05.1218.json"),
 ("test_i05.1225.json", "pred_i05.1225.json"),
 ("test_i05.1242.json", "pred_i05.1242.json"),
 ("test_i05.138.json", "pred_i05.138.json"),
 ("test_i05.163-2.json", "pred_i05.163-2.json"),
 ("test_i05.168-1.json", "pred_i05.168-1.json"),
 ("test_i05.174-2.json", "pred_i05.174-2.json"),
 ("test_i05.181-1.json", "pred_i05.181-1.json"),
 ("test_i05.196-2.json", "pred_i05.196-2.json"),
 ("test_i05.199-2.json", "pred_i05.199-2.json"),
 ("test_i05.430.json", "pred_i05.430.json"),
 ("test_i05.438.json", "pred_i05.438.json"),
 ("test_i05.449.json", "pred_i05.449.json"),
 ("test_i05.473.json", "pred_i05.473.json"),
 ("test_i05.485.json", "pred_i05.485.json"),
 ("test_i05.493.json", "pred_i05.493.json"),
 ("test_i05.520.json", "pred_i05.520.json"),
 ("test_i05.572.json", "pred_i05.572.json"),
 ("test_i05.580.json", "pred_i05.580.json"),
 ("test_i05.596.json", "pred_i05.596.json"),
 ("test_i05.636.json", "pred_i05.636.json"),
 ("test_i05.650.json", "pred_i05.650.json"),
 ("test_i05.689.json", "pred_i05.689.json"),
 ("test_i06.02-5.json", "pred_i06.02-5.json"),
 ("test_i06.05-4.json", "pred_i06.05-4.json"),
 ("test_i06.07-1.json", "pred_i06.07-1.json"),
 ("test_i06.08-2-2.json", "pred_i06.08-2-2.json"),
 ("test_i06.08-4-1.json", "pred_i06.08-4-1.json"),
 ("test_i06.11-4-1.json", "pred_i06.11-4-1.json"),
 ("test_i06.13-4-2.json", "pred_i06.13-4-2.json"),
 ("test_i06.14-4.json", "pred_i06.14-4.json"),
 ("test_i06.15-3.json", "pred_i06.15-3.json"),
 ("test_i06.16-3.json", "pred_i06.16-3.json"),
 ("test_i06.17-5.json", "pred_i06.17-5.json"),
 ("test_i06.19-2.json", "pred_i06.19-2.json"),
 ("test_i06.21-1-1.json", "pred_i06.21-1-1.json"),
 ("test_i06.23-2.json", "pred_i06.23-2.json"),
 ("test_i06.23-5-2.json", "pred_i06.23-5-2.json"),
 ("test_i06.23-5.json", "pred_i06.23-5.json"),
 ("test_i06.25-1-1.json", "pred_i06.25-1-1.json"),
 ("test_i06.27-1.json", "pred_i06.27-1.json"),
 ("test_i06.27-5.json", "pred_i06.27-5.json"),
 ("test_i06.27-6.json", "pred_i06.27-6.json"),
 ("test_i06.28-2.json", "pred_i06.28-2.json"),
 ("test_i06.30-3.json", "pred_i06.30-3.json"),
 ("test_i06.30-6-2.json", "pred_i06.30-6-2.json"),
 ("test_i06.31-1-3.json", "pred_i06.31-1-3.json"),
 ("test_i06.33-4-3.json", "pred_i06.33-4-3.json"),
 ("test_i06.33-6.json", "pred_i06.33-6.json"),
 ("test_i06.34-1-2.json", "pred_i06.34-1-2.json"),
 ("test_i06.35-6.json", "pred_i06.35-6.json"),
 ("test_i06.36-4-1.json", "pred_i06.36-4-1.json"),
 ("test_i06.38-4-1.json", "pred_i06.38-4-1.json"),
 ("test_i06.39-6.json", "pred_i06.39-6.json"),
 ("test_i07.01-12-02.json", "pred_i07.01-12-02.json"),
 ("test_i07.01-13-02.json", "pred_i07.01-13-02.json"),
 ("test_i07.02-10.json", "pred_i07.02-10.json"),
 ("test_i07.03-06-02.json", "pred_i07.03-06-02.json"),
 ("test_i07.03-07-01.json", "pred_i07.03-07-01.json"),
 ("test_i07.03-15-02.json", "pred_i07.03-15-02.json"),
 ("test_i07.04-01-02.json", "pred_i07.04-01-02.json"),
 ("test_i07.04-04-02.json", "pred_i07.04-04-02.json"),
 ("test_i07.04-06.json", "pred_i07.04-06.json"),
 ("test_i07.05-06-01.json", "pred_i07.05-06-01.json"),
 ("test_i07.05-06.json", "pred_i07.05-06.json"),
 ("test_i07.05-07-01.json", "pred_i07.05-07-01.json"),
 ("test_i07.05-08.json", "pred_i07.05-08.json"),
 ("test_i07.05-12.json", "pred_i07.05-12.json"),
 ("test_i07.06-02-01.json", "pred_i07.06-02-01.json"),
 ("test_i07.06-15-02.json", "pred_i07.06-15-02.json"),
 ("test_i07.07-01-01.json", "pred_i07.07-01-01.json"),
 ("test_i07.07-05-01.json", "pred_i07.07-05-01.json"),
 ("test_i07.07-13-02.json", "pred_i07.07-13-02.json"),
 ("test_i07.08-05.json", "pred_i07.08-05.json"),
 ("test_i07.08-15.json", "pred_i07.08-15.json"),
 ("test_i07.09-02-02.json", "pred_i07.09-02-02.json"),
 ("test_i07.09-07.json", "pred_i07.09-07.json"),
 ("test_i07.09-11.json", "pred_i07.09-11.json"),
 ("test_i07.10-02-02.json", "pred_i07.10-02-02.json"),
 ("test_i07.10-03-01.json", "pred_i07.10-03-01.json"),
 ("test_i07.10-07.json", "pred_i07.10-07.json"),
 ("test_i07.10-09-01.json", "pred_i07.10-09-01.json"),
 ("test_i07.11-03-01.json", "pred_i07.11-03-01.json"),
 ("test_i07.11-11-02.json", "pred_i07.11-11-02.json")
]

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

#input_h_labels_dict = load_yaml('labels/taxonomy_labels_test.yml')
input_h_labels_dict = load_yaml('labels/error_taxonomy.yml')
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
                name="line",
                title="Line",
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
    name="json-errors-dataset2",#,
    workspace=EVAL_WORKSPACE,
    settings=settings,
    client=client
).create()

## JSON DIFF

""""LOGIN RECORDS"""
records = []
for file1, file2 in data_files:
    html_diffs = get_html_diff(f'sample_data/output/{file1}', f'sample_data/output/{file2}', lines=40)
    for line, html_diff in html_diffs:
        if html_diff:
            item = load_json(f'sample_data/output/{file1}')
            record = rg.Record(
                id=f'{item["id"]}+{str(line)}',
                fields={
                    "line": str(line),
                    "visual": html_diff,
                    "ref_errors": label_markdown
                }
            )
            records.append(record)

dataset.records.log(records)