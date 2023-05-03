import requests
import os
import json
from dotenv import load_dotenv
load_dotenv('.env')
dot_env_path = ".env"

GIT_PAT = os.environ.get('PAT',"")

#X-RateLimit-Remaining

def get_closed_milestones(owner: str, name: str):
    response = requests.get("https://api.github.com/repos/{0}/{1}/milestones".format(owner, name), auth=("YOSHI3", GIT_PAT)) 
    resp = json.loads(response.content)
    return resp