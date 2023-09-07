from community import community
import statistics
from console import console
import datetime
from utils import convert_date


def compute_engagement_data(community: community.Community):
    """
    This method computes the values needed for the community engagement metric.
    """
    m_comment_per_pr = median_comments_per_pr(community)
    if m_comment_per_pr is None:
        return False
    community.metrics.engagement["m_comment_per_pr"] = m_comment_per_pr
    community.metrics.engagement[
        "mm_comment_dist"
    ] = median_monthly_comments_distribution(community)
    community.metrics.engagement["m_watchers"] = median_contains_dict(
        community.data.watchers, community.data.members_logins
    )
    community.metrics.engagement["m_stargazers"] = median_contains_dict(
        community.data.stargazers, community.data.members_logins
    )
    community.metrics.engagement["m_active"] = median_contains_list(
        community.data.active_members, community.data.members_logins
    )
    community.metrics.engagement["mm_commit_dist"] = median_monthly_commit_distribution(
        community
    )
    community.metrics.engagement[
        "mm_filecollab_dist"
    ] = median_monthly_filecollab_distribution(community)
    return True


def median_comments_per_pr(community: community.Community):
    pr_to_comments = community.data.map_pr_to_comments
    comments_per_pr = []
    if len(pr_to_comments) < 1:
        console.print("[bold red]No pull requests within time window")
        return None
    for pr in pr_to_comments:
        comments_per_pr.append(len(pr_to_comments[pr]))
    comments_per_pr = sorted(comments_per_pr)
    return statistics.median(comments_per_pr)


def median_monthly_comments_distribution(community: community.Community):
    commit_comments = community.data.commits_comments
    pr_comments = community.data.pr_comments
    comment_dates_per_member = {}
    for member in community.data.members_logins:
        comment_dates_per_member[member] = []
    for comment in commit_comments:
        date = (
            comment["updated_at"]
            if (
                comment["updated_at"] != None
                and comment["updated_at"] > comment["created_at"]
            )
            else comment["created_at"]
        )
        comment_dates_per_member[comment["user"]["login"]].append(
            datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
        )
    for comment in pr_comments:
        date = (
            comment["updated_at"]
            if (
                comment["updated_at"] != None
                and comment["updated_at"] > comment["created_at"]
            )
            else comment["created_at"]
        )
        comment_dates_per_member[comment["user"]["login"]].append(
            datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
        )

    m_commentpermonth_permember = []

    for member in community.data.members_logins:
        comments_per_month = {}
        if len(comment_dates_per_member[member]) > 0:
            for date in comment_dates_per_member[member]:
                if date.month in comments_per_month.keys():
                    comments_per_month[date.month] = comments_per_month[date.month] + 1
                else:
                    comments_per_month[date.month] = 0

            m_commentpermonth_permember.append(
                statistics.mean(comments_per_month.values())
            )
    m_commentpermonth_permember = sorted(m_commentpermonth_permember)
    if len(m_commentpermonth_permember) > 0:
        return statistics.median(m_commentpermonth_permember)
    else:
        return 0


def median_contains_dict(users: list, members_logins: list):
    values = []

    for member in users:
        if member["login"] in members_logins:
            values.append(1)
        else:
            values.append(0)
    values = sorted(values)
    if len(values) > 0:
        return statistics.median(values)
    else:
        return 0


def median_contains_list(users: list, members_logins: list):
    values = []

    for member in users:
        if member in members_logins:
            values.append(1)
        else:
            values.append(0)
    values = sorted(values)
    if len(values) > 0:
        return statistics.median(values)
    else:
        return 0


def median_monthly_commit_distribution(community: community.Community):
    commits = community.data.commits
    commit_dates_per_member = {}
    for member in community.data.members_logins:
        commit_dates_per_member[member] = []
    for commit in commits:
        if commit.author.email in commit_dates_per_member.keys():
            commit_dates_per_member[commit.author.email].append(
                datetime.datetime.strptime(
                    convert_date(commit.committed_date), "%Y-%m-%d"
                )
            )
    m_commitpermonth_permember = []

    for member in community.data.members_logins:
        commits_per_month = {}
        if len(commit_dates_per_member[member]) > 0:
            for date in commit_dates_per_member[member]:
                if date.month in commits_per_month.keys():
                    commits_per_month[date.month] = commits_per_month[date.month] + 1
                else:
                    commits_per_month[date.month] = 0

            m_commitpermonth_permember.append(
                statistics.mean(commits_per_month.values())
            )
    m_commitpermonth_permember = sorted(m_commitpermonth_permember)
    if len(m_commitpermonth_permember) > 0:
        return statistics.median(m_commitpermonth_permember)
    else:
        return 0


def median_monthly_filecollab_distribution(community: community.Community):
    files_changed, monthly_files_changed = extract_committer_per_file(community)
    count_committer_perfile_permonth = {}
    for i in range(3):
        monthly_committers_per_file = monthly_files_changed[i]
        for f in monthly_committers_per_file:
            if f not in count_committer_perfile_permonth.keys():
                count_committer_perfile_permonth[f] = {}
                count_committer_perfile_permonth[f][i] = 0
            count_committer_perfile_permonth[f][i] = len(monthly_committers_per_file[f])
    mean_committer_perfile_permonth = []
    for f in count_committer_perfile_permonth:
        mean_committer_perfile_permonth.append(
            statistics.mean(count_committer_perfile_permonth[f].values())
        )
    mean_committer_perfile_permonth = sorted(mean_committer_perfile_permonth)
    if len(mean_committer_perfile_permonth) > 0:
        return statistics.median(mean_committer_perfile_permonth)
    else:
        return 0


def extract_committer_per_file(community: community.Community):
    files_changed = {}
    monthly_files_changed = {}
    monthly_files_changed[0] = {}
    monthly_files_changed[1] = {}
    monthly_files_changed[2] = {}
    for commit in community.data.modified_files_per_commit:
        for f in community.data.modified_files_per_commit[commit]:
            date = None
            for lc in community.data.commits:
                if lc.hexsha == commit:
                    if f in files_changed.keys():
                        files_changed[f].append(lc.author.email)
                    else:
                        files_changed[f] = [lc.author.email]
                    date = datetime.datetime.strptime(
                        convert_date(lc.committed_date), "%Y-%m-%d"
                    )
                    if date is not None:
                        month = check_month(community, date)
                        if month is not None and month in monthly_files_changed.keys():
                            if f in monthly_files_changed[month].keys():
                                monthly_files_changed[month][f].append(lc.author.email)
                            else:
                                monthly_files_changed[month][f] = [lc.author.email]
    return files_changed, monthly_files_changed


def check_month(community: community.Community, date):
    if (
        community.data.end_date
        > date
        > (community.data.start_date + datetime.timedelta(days=60))
    ):
        return 2
    elif (
        community.data.end_date
        > date
        > (community.data.start_date + datetime.timedelta(days=30))
    ):
        return 1
    elif community.data.end_date > date > community.data.start_date:
        return 0
