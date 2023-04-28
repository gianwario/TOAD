import os
import git  
from os import path
from console import console

def download_repo(repo_owner, repo_name):
    # build path
    repo_path = os.path.join(
        "repositories",
        "{}.{}".format(repo_owner, repo_name),
    )

    # get repository reference
    repo = None
    if not os.path.exists(repo_path):
        console.print("[bold magenta]Downloading repository...")
        repo = git.Repo.clone_from(
            "https://github.com/"+repo_owner+"/"+repo_name,
            repo_path,
            progress=Progress(),
            odbt=git.GitCmdObjectDB,
        )
    else:
        repo = git.Repo(repo_path, odbt=git.GitCmdObjectDB)
    return repo



class Progress(git.remote.RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=""):
        print(self._cur_line, end="\r")
