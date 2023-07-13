import requests
import os
import json
from auth import oauth2
from io_module import input_handler, repository_manager
from data_retriever.data_retriever import retrieve_data_and_check_validity
from console import console
from community.data import Data

def main():
    console.rule("Input information")
    input_path, output_path, start_date, end_date = input_handler.get_input_files()
    communities = input_handler.get_input_communities(input_path)

    console.rule("GitHub Authentication")
    pat = oauth2.get_access_token()


    for community in communities:
        console.rule("Community "+community.repo_name+" from "+community.repo_owner)
        
        data = Data()
        data.start_date = start_date
        data.end_date = end_date
        community.add_data(data)
        
        repo = repository_manager.download_repo(community.repo_owner, community.repo_name)
        community.data.commits = list(repo.iter_commits())
        if not retrieve_data_and_check_validity(community): 
            console.print("[bold red]Invalid repository")
            raise SystemExit(0)


if __name__ == "__main__":
    main()