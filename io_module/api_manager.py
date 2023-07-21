import requests
import os
import json
from dotenv import load_dotenv

load_dotenv(".env")
dot_env_path = ".env"

GIT_PAT = os.environ.get("PAT", "")

# X-RateLimit-Remaining
"""
This module contains functions to access the GitHub APIs
"""


def get_milestones(owner: str, name: str):
    response = requests.get(
        "https://api.github.com/repos/{0}/{1}/milestones".format(owner, name),
        auth=("YOSHI3", GIT_PAT),
    )
    resp = json.loads(response.content)
    return resp


def get_user_data_from_login(login: str):
    response = requests.get(
        "https://api.github.com/users/" + login, auth=("YOSHI3", GIT_PAT)
    )
    resp = json.loads(response.content)
    return resp


def get_commit_by_sha(owner: str, name: str, sha: str):
    response = requests.get(
        "https://api.github.com/repos/{}/{}/commits/{}".format(owner, name, sha),
        auth=("YOSHI3", GIT_PAT),
    )
    resp = json.loads(response.content)
    return resp
