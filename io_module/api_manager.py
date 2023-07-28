import requests
import os
import json
from dotenv import load_dotenv
from console import console

load_dotenv(".env")
dot_env_path = ".env"

GIT_PAT = os.environ.get("PAT", "")

# TODO X-RateLimit-Remaining
"""
This module contains functions to access the GitHub APIs
"""


def get_milestones(owner: str, name: str):
    response = paginate(
        "https://api.github.com/repos/{0}/{1}/milestones?per_page=100".format(
            owner, name
        )
    )
    return response


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


def get_pull_requests(owner: str, name: str):
    response = paginate(
        "https://api.github.com/repos/{}/{}/pulls?state=all".format(owner, name)
    )
    return response


def get_pr_details(owner: str, name: str, pr_number: str):
    response = requests.get(
        "https://api.github.com/repos/{}/{}/pulls/{}".format(owner, name, pr_number),
        auth=("YOSHI3", GIT_PAT),
    )
    resp = json.loads(response.content)
    return resp


def get_prs_comments(owner: str, name: str, since: str):
    response = paginate(
        "https://api.github.com/repos/{}/{}/pulls/comments?since={}".format(
            owner, name, since
        )
    )
    return response


def get_commits_comments(owner: str, name: str):
    response = paginate(
        "https://api.github.com/repos/{}/{}/comments".format(owner, name)
    )
    return response


def get_watchers(owner: str, name: str):
    response = paginate(
        "https://api.github.com/repos/{}/{}/subscribers".format(owner, name)
    )
    return response


def get_stargazers(owner: str, name: str):
    response = paginate(
        "https://api.github.com/repos/{}/{}/stargazers".format(owner, name)
    )
    return response


def make_request(url: str):
    response = paginate(url)
    return response


def paginate(url):
    remaining_pages = True
    data = []
    while remaining_pages:
        response = requests.get(
            url,
            params={"per_page": 100},
            auth=("YOSHI3", GIT_PAT),
        )

        for el in json.loads(response.content):
            data.append(el)
        remaining_pages = "next" in response.links

        if remaining_pages:
            url = response.links["next"]["url"]
    return data
