import requests
import os
import json
from dotenv import load_dotenv
load_dotenv('.env')
dot_env_path = ".env"

GIT_PAT = os.environ.get('PAT',"")

#X-RateLimit-Remaining
"""
This module contains functions to access the GitHub APIs
""" 


def get_closed_milestones(owner: str, name: str):
    response = requests.get("https://api.github.com/repos/{0}/{1}/milestones".format(owner, name), auth=("YOSHI3", GIT_PAT)) 
    resp = json.loads(response.content)
    return resp

def get_user_from_email(email: str):
    response = requests.get("https://api.github.com/search/users?q="+email+"+in:email", auth=("YOSHI3", GIT_PAT)) 
    resp = json.loads(response.content)
    if(len(resp.get('items')) > 0):
        return resp.get('items')

def get_user_data_from_username(username: str):
    response = requests.get("https://api.github.com/users/"+username, auth=("YOSHI3", GIT_PAT)) 
    resp = json.loads(response.content)
    print(resp)
    return resp
