from utils import (
    convert_date,
    check_date_within_timewindow,
    check_githubdate_within_timewindow,
)
from datetime import datetime
from community import community
from io_module import api_manager
from console import console
from progress.bar import Bar


def filter_commits(community: community.Community):
    """
    This function filters commits within the given time window.

    :param community: the community
    """
    filtered_commits = []
    for commit in community.data.all_commits:
        try:
            if check_date_within_timewindow(
                community, commit.committed_date
            ) or check_date_within_timewindow(community, commit.authored_date):
                filtered_commits.append(commit)
        except:
            continue

    community.data.commits = filtered_commits


def filter_milestones(community: community.Community, milestones: list):
    filtered_milestones = []

    for milestone in milestones:
        try:
            if milestone["closed_at"] is not None and (
                datetime.strptime(milestone["closed_at"], "%Y-%m-%dT%H:%M:%SZ")
                <= community.data.end_date
            ):
                filtered_milestones.append(milestone)
        except:
            continue
    return filtered_milestones


def filter_prs(community: community.Community, prs: list):
    filtered_prs = []

    for pr in prs:
        try:
            if (
                pr["closed_at"] is not None
                and pr["created_at"] is not None
                and pr["updated_at"] is not None
                and (
                    check_githubdate_within_timewindow(community, pr["created_at"])
                    or check_githubdate_within_timewindow(community, pr["updated_at"])
                    or check_githubdate_within_timewindow(community, pr["closed_at"])
                )
                and pr["user"] is not None
                and pr["user"]["login"] is not None
                and pr["user"]["login"] in community.data.members_logins
            ):
                filtered_prs.append(pr)
        except:
            continue
    return filtered_prs


def filter_comments(community: community.Community, comments: list):
    """
    Filter out all comments that are not within the time window, do not have an author,
    or are not considered current members (i.e., have not committed in the last 90 days).
    """
    filtered_comments = []
    with Bar("Filtering comments", max=len(comments)) as bar:
        for comment in comments:
            try:
                if (
                    comment["created_at"] is not None
                    and comment["updated_at"] is not None
                    and (
                        check_githubdate_within_timewindow(
                            community, comment["created_at"]
                        )
                        or check_githubdate_within_timewindow(
                            community, comment["updated_at"]
                        )
                    )
                    and comment["user"] is not None
                    and comment["user"]["login"] is not None
                    and comment["user"]["login"] in community.data.members_logins
                ):
                    filtered_comments.append(comment)
            except:
                continue
            bar.next()
    return filtered_comments


def filter_first_last_commits(commits: list):
    last_commit_datetime = datetime.strptime("1980-01-01", "%Y-%m-%d")
    last_commit_hash = ""
    first_commit_datetime = datetime.today()
    first_commit_hash = ""

    for commit in commits:
        current_commit_date = datetime.strptime(
            convert_date(commit.committed_date), "%Y-%m-%d"
        )
        if current_commit_date > last_commit_datetime:
            last_commit_datetime = current_commit_date
            last_commit_hash = commit.hexsha
        if current_commit_date < first_commit_datetime:
            first_commit_datetime = current_commit_date
            first_commit_hash = commit.hexsha
    return (
        first_commit_datetime,
        first_commit_hash,
        last_commit_datetime,
        last_commit_hash,
    )
