from dataclasses import dataclass
from datetime import datetime


@dataclass
class Data:
    """
    This class stores needed data of a Community
    """

    # datetime
    start_date: any = None
    # datetime
    end_date: any = None
    first_commit_hash: str = None
    last_commit_hash: str = None
    first_commit_datetime: any = None
    last_commit_datetime: any = None
    members: list = None
    members_logins: list = None
    aliases: list = None
    map_user_followers: {} = None
    map_user_following: {} = None
    map_user_repositories: {} = None
    all_commits: list = None
    commits: list = None
    commits_comments: list = None
    modified_files_per_commit: {} = None
    milestones: list = None
    coordinates: list = None
    distances: list = None
    countries: list = None
    merged_pull_requests: list = None
    all_pull_requests: list = None
    pr_comments: list = None
    map_pr_to_comments: {} = None
    active_members: [] = None
    watchers: {} = None
    stargazers: {} = None
    contributors: int = None
    collaborators: int = None
