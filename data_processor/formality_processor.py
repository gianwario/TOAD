from community import community
from console import console
from data_retriever import filters


def compute_formality_data(community: community.Community):
    """
    This method computes the values needed for the community formality metric.
    """
    community.metrics.formality["m_membership_type"] = mean_membership_type(community)
    community.metrics.formality["milestones"] = len(community.data.milestones)
    community.metrics.formality["lifetime"] = abs(lifetime_in_days(community))


def mean_membership_type(community: community.Community):
    authors = []
    committers = []
    for commit in community.data.commits:
        authors.append(commit.author.email)
        committers.append(commit.committer.email)

    for pr in community.data.merged_pull_requests:
        if (
            pr["merged_by"] is not None
            and pr["merged_by"]["login"] in community.data.members_logins
        ):
            committers.append(pr["merged_by"]["login"])

    contributors = set(authors).difference(set(committers))
    collaborators = set([item for item in committers if "github" not in item])
    """
    if (len(contributors) + len(collaborators)) != len(community.data.members_logins):
        console.print(
            "[bold red]Found fewer or more contributors and collaborators than members"
        )
        raise SystemExit(0)
    """
    community.data.contributors = len(contributors)
    community.data.collaborators = len(collaborators)

    return (len(contributors) + len(collaborators) * 2) / len(
        community.data.members_logins
    )


def lifetime_in_days(community: community.Community):
    (
        first_commit_datetime,
        first_commit_hash,
        last_commit_datetime,
        last_commit_hash,
    ) = filters.filter_first_last_commits(community.data.all_commits)
    delta = first_commit_datetime - last_commit_datetime
    return delta.days
