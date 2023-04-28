from community import data

class Community:
    def __init__(self, repo_owner, repo_name):
        self.repo_owner = repo_owner
        self.repo_name = repo_name

    def add_data(self, data: data.Data):
        self.data = data