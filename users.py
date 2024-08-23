import argilla as rg
from dotenv import load_dotenv
import os
import random
import string
import pandas as pd
load_dotenv()

ARGILLA_URL = os.getenv('API_URL')
ARGILLA_KEY = os.getenv("API_KEY")
EVAL_WORKSPACE = os.getenv("RG_WORKSPACE")
NUM_USERS = int(os.getenv("NUMBER_USERS"))

client = rg.Argilla(
    api_url=ARGILLA_URL,
    api_key=ARGILLA_KEY
)

users = client.users

def generate_random_string(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def create_users(num_users, role="annotator"):
    list_users = []
    for _ in range(num_users):

        username = generate_random_string(8)
        password = generate_random_string(12)
        list_users.append({
            "username": username,
            "password": password,
            "role": role,
        })
    return list_users

list_users = create_users(NUM_USERS)

df_users = pd.DataFrame(list_users)
df_users.to_csv('users.csv', index=False)

for user in list_users:
    rg.User(
        username=user['username'],
        password=user['password'],
        role=user['role'],
        client=client
    ).create().add_to_workspace(client.workspaces(EVAL_WORKSPACE))

# users_to_delete = ['72vLTjd7', 'SRlOXvMS', 'mEbBPsSS', 'oYI2gaUD', '1kctgsB2', 'VlnjFXHX']
# for _ in users_to_delete:
#     client.users(_).delete()

for user in users: print(user)