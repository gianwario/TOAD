from community import community
from utils import convert_date
from datetime import datetime
from console import console


def compute_longevity_data(community: community.Community):
    community.metrics.longevity = mean_committer_longevity(community)


def mean_committer_longevity(community: community.Community):
    commits = community.data.commits
    commit_date_per_committer = {}
    """ 
    We use committer date instead of author date, since that's when the commit was last applied: 
    https://stackoverflow.com/questions/18750808/difference-between-author-and-committer-in-git
    """
    for c in commits:
        if (
            c.committer.email is not None
            and c.committer.email in community.data.members_logins
        ):
            if c.committer.email in commit_date_per_committer.keys():
                commit_date_per_committer[c.committer.email].append(
                    datetime.strptime(convert_date(c.committed_date), "%Y-%m-%d")
                )
            else:
                commit_date_per_committer[c.committer.email] = [
                    datetime.strptime(convert_date(c.committed_date), "%Y-%m-%d")
                ]
    total_longevity_indays = 0
    for committer in commit_date_per_committer:
        last_commit_datetime = datetime.strptime("1980-01-01", "%Y-%m-%d")
        first_commit_datetime = datetime.today()
        for date in commit_date_per_committer[committer]:
            if date > last_commit_datetime:
                last_commit_datetime = date
            if date < first_commit_datetime:
                first_commit_datetime = date
        delta = first_commit_datetime - last_commit_datetime
        total_longevity_indays += abs(delta.days)
    return total_longevity_indays / len(commit_date_per_committer)
