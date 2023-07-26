from utils import (
    convert_date,
    check_date_within_timewindow,
    check_githubdate_within_timewindow,
)
from datetime import datetime
from strsimpy.metric_lcs import MetricLCS
import re
from community import community
import git
from io_module import api_manager
from console import console


def filter_commits(community: community.Community):
    """
    This function filters commits within the given time window.

    :param community: the community
    """
    filtered_commits = []
    for commit in community.data.commits:
        if check_date_within_timewindow(community, commit.committed_date):
            filtered_commits.append(commit)

    community.data.commits = filtered_commits


def filter_milestones(community: community.Community, milestones: list):
    filtered_milestones = []

    for milestone in milestones:
        if (
            milestone["state"] == "closed"
            and milestone["closed_at"] != ""
            and datetime.strptime(milestone["closed_at"], "%Y-%m-%dT%H:%M:%SZ")
            <= community.data.end_date
        ):
            filtered_milestones.append(milestone)
    return filtered_milestones


def filter_prs(community: community.Community, prs: list):
    filtered_prs = []

    for pr in prs:
        if (
            (
                check_githubdate_within_timewindow(community, pr["created_at"])
                or check_githubdate_within_timewindow(community, pr["updated_at"])
                or check_githubdate_within_timewindow(community, pr["closed_at"])
            )
            and pr["user"] is not None
            and pr["user"]["login"] is not None
            and pr["user"]["login"] in community.data.members_logins
        ):
            filtered_prs.append(pr)
    return filtered_prs


def filter_pr_comments(community: community.Community, comments: list):
    """
    Filter out all non-pull-request issue-comments that are not within the time window, do not have an author,
    or are not considered current members (i.e., have not committed in the last 90 days).
    """
    filtered_comments = []
    for comment in comments:
        if (
            (
                check_githubdate_within_timewindow(community, comment["created_at"])
                or check_githubdate_within_timewindow(community, comment["updated_at"])
            )
            and comment["user"] is not None
            and comment["user"]["login"] is not None
            and comment["user"]["login"] in community.data.members_logins
        ):
            filtered_comments.append(comment)
    return filtered_comments
