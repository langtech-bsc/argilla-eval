import argilla as rg
from dotenv import load_dotenv
import os
from datasets import load_dataset

load_dotenv()
ARGILLA_URL = os.getenv('API_URL')
ARGILLA_KEY = os.getenv("API_KEY")
FIRST_WORKSPACE = os.getenv("FIRST_WORKSPACE")

# ROOT USER : OWNER
# ROOT PASSWORD : 12345678

client = rg.Argilla(
    api_url=ARGILLA_URL,
    api_key=ARGILLA_KEY
)

user_a = rg.User(
    username="user_a",
    first_name="first_a",
    last_name="last_a",
    role="annotator",
    password="password_a",
    client=client
).create()

user_b = rg.User(
    username="user_b",
    first_name="first_b",
    last_name="last_b",
    role="annotator",
    password="password_b",
    client=client
).create()


for worspace in client.workspaces: 
    print(worspace.name)
    for user in worspace.users: print(user)


print("CREATE WORKSPACE")
workspace_to_create = rg.Workspace(
    name="ab_workspace",
    client=client
)
ab_workspace = workspace_to_create.create()


settings = rg.Settings(
    guidelines="This is an AB-Testing task. Choose the best response given the prompt.",
    fields=[
        rg.TextField(name="prompt_question", title="Question", use_markdown=True),
        rg.TextField(name="prompt_a", title="Prompt A", use_markdown=True), 
        rg.TextField(name="prompt_b", title="Prompt B", use_markdown=True)
        ],
    questions=[
        # rg.LabelQuestion(
        #     name="label",
        #     labels=["positive", "negative", "neutral"]
        # ),
        rg.LabelQuestion(
            name="label",
            title="What is the best response given the prompt",
            description="Select the one that applies.",
            required=True,
            labels={"prompt_a": "prompt_a", "prompt_b": "prompt_b"},
        )
        ],
)

dataset = rg.Dataset(
    name="sentiment_analysis",
    workspace="ab_workspace",
    settings=settings,
    client=client
)

dataset.create()
data = load_dataset("Intel/orca_dpo_pairs", split="train[1:5]").to_list()
dataset.records.log(records=data, mapping={"question":"prompt_question", "chosen": "prompt_a", "rejected": "prompt_b"})

workspace = client.workspaces("ab_workspace")

dataset = client.datasets(name="sentiment_analysis", workspace=workspace)

user_a = client.users("user_a").add_to_workspace(client.workspaces("ab_workspace"))
user_b = client.users("user_b").add_to_workspace(client.workspaces("ab_workspace"))

# Exporting records
# exported_records = dataset.records.to_dict()

# print(exported_records)
# for record in exported_records:
#     print(record)