import requests
import os
import json
from auth import oauth2
from io_module import input_handler, repository_manager
from console import console
def main():
    console.rule("Input information")
    input_path, output_path, start_date, end_date = input_handler.get_input_files()
    communities = input_handler.get_input_communities(input_path)

    console.rule("GitHub Authentication")
    pat = oauth2.get_access_token()


    for community in communities:
        console.rule("Community "+community.repo_name+" from "+community.repo_owner)
        repo = repository_manager.download_repo(community.repo_owner, community.repo_name)
        for commit in repo.iter_commits():
            pass

if __name__ == "__main__":
    main()