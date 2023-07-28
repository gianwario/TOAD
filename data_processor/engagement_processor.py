from community import community
import statistics
from console import console
import datetime
from utils import convert_date


def compute_engagement_data(community: community.Community):
    """
    engagement.MedianNrCommentsPerPullReq =
                MedianNrCommentsPerPullReq(data.MapPullReqsToComments);
            engagement.MedianMonthlyPullCommitCommentsDistribution = MedianMonthlyCommentsDistribution(
                data.CommitComments,
                data.MapPullReqsToComments.Values.SelectMany(x => x).ToList(),
                data.MemberUsernames
            );
            engagement.MedianActiveMember = MedianContains(data.ActiveMembers, data.MemberUsernames);
            engagement.MedianWatcher = MedianContains(data.Watchers, data.MemberUsernames);
            engagement.MedianStargazer = MedianContains(data.Stargazers, data.MemberUsernames);
            engagement.MedianMonthlyCommitDistribution = MedianMonthlyCommitDistribution(data.CommitsWithinTimeWindow, data.MemberUsernames);
            engagement.MedianMonthlyFileCollabDistribution = MedianMonthlyFileCollabDistribution(data.CommitsWithinTimeWindow, data.MemberUsernames);

    """
    m_comment_per_pr = median_comments_per_pr(community)
    mm_comment_dist = median_monthly_comments_distribution(community)
    m_watchers = median_contains(community.data.watchers, community.data.members_logins)
    m_stargazers = median_contains(
        community.data.stargazers, community.data.members_logins
    )
    m_active = median_contains(
        community.data.active_members, community.data.members_logins
    )
    mm_commit_dist = median_monthly_commit_distribution(community)
    mm_filecollab_dist = median_monthly_filecollab_distribution(community)


def median_comments_per_pr(community: community.Community):
    pr_to_comments = community.data.map_pr_to_comments
    comments_per_pr = []
    if len(pr_to_comments) < 1:
        console.print("[bold red]No pull requests within time window")
        raise SystemExit(0)
    for pr in pr_to_comments:
        comments_per_pr.append(len(pr_to_comments[pr]))
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

    return statistics.median(m_commentpermonth_permember)


def median_contains(users: list, members_logins: list):
    values = []
    for member in users:
        if member in members_logins:
            values.append(1)
        else:
            values.append(0)
    return statistics.median(values)


def median_monthly_commit_distribution(community: community.Community):
    commits = community.data.commits
    commit_dates_per_member = {}
    for member in community.data.members_logins:
        commit_dates_per_member[member] = []
    for commit in commits:
        commit_dates_per_member[commit.author.email].append(
            datetime.datetime.strptime(convert_date(commit.committed_date), "%Y-%m-%d")
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
    return statistics.median(m_commitpermonth_permember)


def median_monthly_filecollab_distribution(community: community.Community):
    extract_committer_per_file(community)


def extract_committer_per_file(community: community.Community):
    files_changed = {}
    for commit in community.data.modified_files_per_commit:
        for f in community.data.modified_files_per_commit[commit]:
            if f in files_changed.keys():
                for lc in community.data.commits:
                    if lc.hexsha == commit:
                        files_changed[f].append(lc.author.email)
            else:
                files_changed[f] = []
    print(files_changed)
    # TODO start here damn
    return files_changed


def extract_committer_per_file_per_mont(community: community.Community):
    month_0 = []
    month_1 = []
    month_2 = []
