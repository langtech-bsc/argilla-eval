import argilla as rg
from dotenv import load_dotenv
import os
import json

load_dotenv()
RG_API_URL = os.getenv('API_URL')
RG_API_KEY = os.getenv('API_KEY')
RG_WORKSPACE = os.getenv('EVAL_WORKSPACE')


client = rg.Argilla(
    api_url=RG_API_URL, 
    api_key=RG_API_KEY
)

# """WORKSPACE CREATION"""
# workspace_to_create = rg.Workspace( name="eval_workspace", client=client)
# created_workspace = workspace_to_create.create()

"""DATASET SETTINGS"""
# settings = rg.Settings(
#     allow_extra_metadata=True,
#     guidelines="""
#     1. **Consistency:** Label each example consistently according to the defined criteria, ensuring no bias towards either variant.
#     2. **Clarity:** Focus on the specific elements being tested (e.g., text, design) and how they impact the user's experience.
#     3. **Detail:** Provide brief but clear justifications for your choice if required, highlighting key differences.
#     4. **Neutrality:** Avoid letting personal preferences influence your annotation; stick to the test's objective.
#     """,
#     fields=[
#             rg.TextField(
#                 name="prompt", 
#                 title="Prompt", 
#                 use_markdown=True,
#                 required=True,
#                 description="Field description"
#             ),
#             rg.TextField(
#                 name="answer_a", 
#                 title="Answer A", 
#                 use_markdown=True,
#                 required=True,
#                 description="Field description",
#             ),
#             rg.TextField(
#                 name="answer_b", 
#                 title="Answer B", 
#                 use_markdown=True,
#                 required=True,
#                 description="Field description",
#             )
#         ],
#     questions=[
#         rg.LabelQuestion(
#             name="label",
#             title="What is the best response given the prompt?",
#             description="Select the one that applies.",
#             required=True,
#             labels={"answer_a": "Answer A", "answer_b": "Answer B", "both": "Both", "none": "None"}
          
#         ),
#         rg.RatingQuestion(
#                 name="rating",
#                 values=[1, 2, 3, 4, 5],
#                 title="How satisfied are you with the response?",
#                 description="1 = very unsatisfied, 5 = very satisfied",
#                 required=True,
#         ),
#         rg.TextQuestion(
#             name="text",
#             title="Copy and modify the response here if there is anything you would like to modify.",
#             description="If there is anything you would modify in the response copy and edit the response in this field.",
#             use_markdown=True
#         )
#         ],
# )

# """DATASET CREATION"""
# dataset = rg.Dataset(
#     name="prompts-eval-dataset",
#     workspace="eval_workspace",
#     settings=settings,
#     client=client
# ).create()



# """RECORDS CREATION"""
# with open('dataset.json', 'r') as file:
#     data_file = json.load(file)

# records = []
# for item in data_file:
#     record = rg.Record(
#         id=item["source_id"],
#         fields={
#             "prompt": item["prompt"],
#             "answer_a": item["answer_A"],
#             "answer_b": item["answer_B"]
#         },
#         # metadata={
#         #     "lang": item["lang"],
#         #     "model_A": item["model_A"],
#         #     "model_B": item["model_B"]
#         # }
#     )
#     records.append(record)

# dataset.records.log(records)

dataset = client.datasets(name="prompts-eval-dataset", workspace=client.workspaces("eval_workspace"))
exported_records = dataset.records.to_json("./records.json")