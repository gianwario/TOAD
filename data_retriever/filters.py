from utils import convert_commit_date
from datetime import datetime
from strsimpy.metric_lcs import MetricLCS
import re
from community import community
import git
from io_module import api_manager


def filter_commits(community: community.Community):
    """
    This function filters commits within the given time window.

    :param community: the community
    """
    filtered_commits = []
    for commit in community.data.commits:
        if (
            community.data.start_date
            <= datetime.strptime(convert_commit_date(commit.committed_date), "%Y-%m-%d")
            <= community.data.end_date
        ):
            filtered_commits.append(commit)

    print(len(community.data.commits))
    print(len(filtered_commits))
    community.data.commits = filtered_commits
