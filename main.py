import argilla as rg
from dotenv import load_dotenv
import os
import json

load_dotenv()
RG_API_URL = os.getenv('API_URL')
RG_API_KEY = os.getenv('API_KEY')
EVAL_WORKSPACE = os.getenv('RG_WORKSPACE')
NUMBER_USERS = int(os.getenv('NUMBER_USERS'))
DATASET_PATH = os.getenv('DATASET_PATH')
DATASET_NAME = os.getenv('DATASET_NAME')

TABLE_EX_STRING = """
<table>
<tr>
<th> Good </th>
<th> Bad </th>
</tr>
<tr>
<td>

```c++
int foo() {
    int result = 4;
    return result;
}
```

</td>
<td>

```c++
int foo() {
    int x = 4;
    return x;
}
```

</td>
</tr>
</table>
"""

client = rg.Argilla(
    api_url=RG_API_URL, 
    api_key=RG_API_KEY
)

def load_json(file_path, encoding=None):
    with open(file_path, 'r', encoding=encoding) as file:
        return json.load(file)

"""DATASET SETTINGS"""
settings = rg.Settings(
    distribution=rg.TaskDistribution(min_submitted=NUMBER_USERS),
    allow_extra_metadata=True,
    guidelines="""
    1. **Consistency:** Label each example consistently according to the defined criteria, ensuring no bias towards either variant.
    2. **Clarity:** Focus on the specific elements being tested (e.g., text, design) and how they impact the user's experience.
    3. **Detail:** Provide brief but clear justifications for your choice if required, highlighting key differences.
    4. **Neutrality:** Avoid letting personal preferences influence your annotation; stick to the test's objective.
    """,
    fields=[
            rg.TextField(
                name="visual",
                title="Visual",
                use_markdown=True,
                required=True,
                description="Field description"
            ),

            rg.TextField(
                name="prompt", 
                title="Prompt", 
                use_markdown=True,
                required=True,
                description="Field description"
            ),
            rg.TextField(
                name="answer_a", 
                title="Answer A", 
                use_markdown=True,
                required=True,
                description="Field description",
            ),
            rg.TextField(
                name="answer_b", 
                title="Answer B", 
                use_markdown=True,
                required=True,
                description="Field description",
            )
        ],
    questions=[
        rg.LabelQuestion(
            name="label",
            title="What is the best response given the prompt?",
            description="Select the one that applies.",
            required=True,
            labels={"answer_a": "Answer A", "answer_b": "Answer B", "both": "Both", "none": "None"}
          
        ),
        rg.RatingQuestion(
                name="rating",
                values=[1, 2, 3, 4, 5],
                title="How satisfied are you with the response?",
                description="1 = very unsatisfied, 5 = very satisfied",
                required=True,
        ),
        rg.TextQuestion(
            name="text",
            title="Copy and modify the response here if there is anything you would like to modify.",
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

""""LOGIN RECORDS"""
records = []
for item in data_file:
    record = rg.Record(
        id=item["instance_id"],
        fields={
            "visual": TABLE_EX_STRING,
            "prompt": item["prompt"],
            "answer_a": item["answer_A"],
            "answer_b": item["answer_B"]
        }
    )
    records.append(record)

dataset.records.log(records)