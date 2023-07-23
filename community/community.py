from community import data
from community import metrics


class Community:
    """
    This class stores information of a Community such as the repository owner, repository name,
    Datas needed to perform computations, computed Metrics and Communiy Pattern detected

    """

    def __init__(self, repo_owner, repo_name):
        self.repo_owner = repo_owner
        self.repo_name = repo_name

    def add_data(self, data: data.Data):
        self.data = data

    def add_metrics(self, metrics: metrics.Metrics):
        self.metrics = metrics
