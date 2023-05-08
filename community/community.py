from community import data

class Community:
    """
    This class stores information of a Community such as the repository owner, repository name and a set of misc Data
    """ 
    def __init__(self, repo_owner, repo_name):
        self.repo_owner = repo_owner
        self.repo_name = repo_name

    def add_data(self, data: data.Data):
        self.data = data