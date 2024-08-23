import argilla as rg
from dotenv import load_dotenv
import os
load_dotenv()

ARGILLA_URL = os.getenv('API_URL')
ARGILLA_KEY = os.getenv("API_KEY")
EVAL_WORKSPACE = os.getenv("RG_WORKSPACE")

client = rg.Argilla(
    api_url=ARGILLA_URL,
    api_key=ARGILLA_KEY
)

users = client.users

list_users = [
    {"username": "username_a", "password":"password_a", "role":"annotator"},
    {"username": "username_b", "password":"password_b", "role":"annotator"},
    {"username": "username_c", "password":"password_c", "role":"annotator"},
]

# for user in list_users:
#     rg.User(
#         username=user['username'],
#         password=user['password'],
#         role=user['role'],
#         client=client
#     ).create().add_to_workspace(client.workspaces(EVAL_WORKSPACE))


# client.users('username_a').delete()
# client.users('username_b').delete()
# client.users('username_a').delete()


for user in users: print(user)