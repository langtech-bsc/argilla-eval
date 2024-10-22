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

def prepare_datafiles(basepath):
    files = os.listdir(basepath)
    tests = [os.path.join(basepath, f) for f in files if f.startswith('test')]
    preds = [os.path.join(basepath, f) for f in files if f.startswith('pred')]
    tests.sort()
    preds.sort()
    data_files = list(zip(tests, preds))
    for t, p in data_files:
        if t.split("_")[1] != p.split("_")[1]:
            msg = f"{t} does not correspond to {p}"
            raise ValueError(msg)
    return data_files

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

def generate_json_pre_markdown(from_json):

    markdown = f"""<body><style>.json-pre span.button.tooltip__container svg {{fill: currentColor !important; width: 18px !important; height: 18px !important;}}</style><div class="json-pre"><details><summary>Click here to show JSON</summary><pre style="background: whitesmoke; padding: 25px;">{json.dumps(from_json, indent=2)}</pre></details></div></body>"""
    return markdown

# prepare the data files
data_files = prepare_datafiles(DATASET_PATH)

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
            ),
            rg.TextField(
                name="json_pre",
                title="JSON",
                use_markdown=True,
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
        rg.LabelQuestion(
            name="block",
            title="Is the error a continuation from the line above?",
            description="The error could be a part of a larger block. If the difference corresponds to "\
                                    "the error that was annotated before, please choose the option Yes.",
            required=True,
            labels=['No', 'Yes']

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
#data_file = load_json(DATASET_PATH)

"""DATASET CREATION"""
dataset = rg.Dataset(
    name=DATASET_NAME,
    workspace=EVAL_WORKSPACE,
    settings=settings,
    client=client
).create()

## JSON DIFF

""""LOGIN RECORDS"""
records = []
for file1, file2 in data_files:
    html_diffs = get_html_diff(file1, file2, lines=40)
    for line, html_diff in html_diffs:
        if html_diff:
            item = load_json(file1)
            record = rg.Record(
                id=f'{item["id"]}+{str(line)}',
                fields={
                    "line": str(line),
                    "visual": html_diff,
                    "ref_errors": label_markdown,
                    "json_pre": generate_json_pre_markdown(item)
                }
            )
            records.append(record)

dataset.records.log(records)