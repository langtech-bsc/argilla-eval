import argilla as rg
from dotenv import load_dotenv
import os

load_dotenv()
RG_API_URL = os.getenv('API_URL')
RG_API_KEY = os.getenv('API_KEY')
EVAL_WORKSPACE = os.getenv('RG_WORKSPACE')

client = rg.Argilla(
    api_url=RG_API_URL, 
    api_key=RG_API_KEY
)

"""WORKSPACE CREATION"""
workspace_to_create = rg.Workspace(name=EVAL_WORKSPACE, client=client)
created_workspace = workspace_to_create.create()