from utils import convert_commit_date
from datetime import datetime
from strsimpy.metric_lcs import MetricLCS
import re
from community import community
import git
from io_module import api_manager


def filter_commits_and_get_members(community: community.Community):
    """
    This function filters commits within the given time window.
    It also gets the members of the community storing them in its data.

    :param community: the community
    """
    filteder_commits = []
    authors = []
    authors_email = []
    for commit in community.data.commits:
        if (
            community.data.start_date
            <= datetime.strptime(convert_commit_date(commit.committed_date), "%Y-%m-%d")
            <= community.data.end_date
        ):
            authors_email.append(extract_author_id(commit.author))
            for co_author in commit.co_authors:
                authors_email.append(extract_author_id(co_author))
            filteder_commits.append(commit)

    print(len(community.data.commits))
    print(len(filteder_commits))
    community.data.commits = filteder_commits
    users = []
    for email in list(dict.fromkeys(authors_email)):
        print(email)
        u = api_manager.get_user_from_email(email)
        if u:
            users.append(u)
    print(len(users))
