import requests
import os
from console import console
from dotenv import load_dotenv, set_key
load_dotenv('.env')
dot_env_path = ".env"

def execute_oauth2(header, payload):
    r = requests.post('https://github.com/login/device/code',headers=header,json=payload)
    data = r.json()
    #print(data)
    device_code = data['device_code']
    uri = data['verification_uri']
    user_code = data['user_code']
    console.print("[bold magenta]To authorize this app, go to {} and enter the code {}".format(uri,user_code))
    console.input('[bold magenta]Press any key to continue once you have input the code successfully')
    return device_code

def generate_new_token(header, payload):
    r = requests.post( "https://github.com/login/oauth/access_token", headers=header, json=payload)
    #print(r.json())
    set_key(dot_env_path, "PAT", r.json()['access_token'])   
    return r.json()['access_token']

def get_access_token():
    pat = os.environ.get('PAT',"")
    if not pat:
        console.print("[bold magenta]Retrieving Personal Access Token from GitHub")
        client_id = os.environ.get('CLIENT_ID',"")
        header = {"Content-Type": "application/json", "Accept": "application/json"}
        payload1 = {"client_id": client_id,}
        device_code = execute_oauth2(header, payload1)
        payload2 = {
            "client_id": client_id,
            "device_code": device_code,
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
        }
        pat = generate_new_token(header, payload2)
    else:
        console.print("[bold magenta]Retrieving stored Personal Access Token")
    return pat