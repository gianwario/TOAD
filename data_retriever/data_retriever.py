from console import console
import time
from datetime import datetime, date, timedelta
import git
from community import community
from io_module import api_manager
from data_retriever import filters
from alias_handler import alias_handler
from data_retriever import geographical_retriever
from progress.bar import Bar
from utils import check_githubdate_within_timewindow, convert_date


def retrieve_data_and_check_validity(community: community.Community):
    """
    This function is used to check the validity of a repository before continuing with the execution.
    A Community is valid if:
    it has at least 100 commits (all time),
    it has at least 10 members active in the last 90 days,
    it has at least 1 milestone (all time),
    it has enough location data to compute dispersion.

    :param community: the community to be checked
    :return: true if valid, false otherwise
    """
    console.log("Checking commits")
    filters.filter_commits(community)
    console.print("Total number of commits: " + str(len(community.data.all_commits)))
    console.print(
        "Valid commits between "
        + str(community.data.start_date)
        + " and "
        + str(community.data.end_date)
        + " : "
        + str(len(community.data.commits))
    )
    if len(community.data.commits) < 100:
        console.print("[bold red]There must be at least 100 commits")
        return False
    retrieve_member_data(community)

    if len(community.data.members) < 2:
        console.print("[bold red]There must be at least 2 members")
        return False
    console.log("Checking number of closed milestones")
    milestones = api_manager.get_milestones(community.repo_owner, community.repo_name)
    milestones = filters.filter_milestones(community, milestones)
    if len(milestones) < 1:
        console.print("[bold red]There must be at least 1 closed milestone")
        return False
    community.data.milestones = milestones
    console.log("Retrieving geographical information")

    geographical_retriever.retrieve_geo_information(community)
    geographical_retriever.retrieve_country_name(community)

    if (
        community.data.countries is None
        or len(community.data.countries) == 0
        or len(community.data.coordinates) == 0
    ):
        console.print(
            "[bold red]Geographical information is not enough to compute geodispersion"
        )
        return False
    return True


def retrieve_member_data(community: community.Community):
    """
    Retrieves the GitHub user information from the commits contained in the community data.
    It does so by extracting logins and aliases from the GitHub API.
    After querying the APIs to gather the information neeeded, this method updates the community data
    with members considered real users, their login username and the computed aliases

    It also updated the commits by replacing the emails with the aliases.

    :param community: the analyzed community
    """
    aliases = alias_handler.alias_extraction(community)

    members = []

    users = []
    bots = []
    organizations = []

    community.data.aliases = aliases
    community.data.members_logins = [key for key in aliases.keys()]

    community.data.commits = alias_handler.replace_all_aliases(
        community.data.commits, aliases
    )
    with Bar(
        "Retrieving community members data...", max=len(community.data.members_logins)
    ) as bar:
        for login in community.data.members_logins:
            members.append(api_manager.get_user_data_from_login(login))
            bar.next()

    for member in members:
        if member is not None and "type" in member.keys():
            if member["type"] == "User":
                users.append(member)
            elif member["type"] == "Bot":
                bots.append(member)
            elif member["type"] == "Organization":
                organizations.append(member)
            else:
                pass

    console.print("[blue]" + str(len(users)) + " users were classified as a user.")
    console.print("[blue]" + str(len(bots)) + " users were classified as a bot.")
    console.print(
        "[blue]"
        + str(len(organizations))
        + " users were classified as an organization."
    )

    community.data.members = users


def retrieve_structure_data(community: community.Community):
    """
    Method that retrieves all GitHub data that is needed to compute only the structure metrics and modifies the
    community data to store that information. It retrieves a mapping from a member to their followers, a mapping
    from a member to their following, and a mapping from a member to their owned repositories.

    :param community: The community for which we need to retrieve GitHub Data
    """
    map_user_followers = {}
    map_user_following = {}
    map_user_repositories = {}
    with Bar("Filtering members data", max=len(community.data.members)) as bar:
        for member in community.data.members:
            (
                followers_login,
                following_login,
                repo_names,
            ) = retrieve_data_per_member(member)
            map_user_followers[member["login"]] = followers_login
            map_user_following[member["login"]] = following_login
            map_user_repositories[member["login"]] = repo_names
            bar.next()
    community.data.map_user_followers = map_user_followers
    community.data.map_user_following = map_user_following
    community.data.map_user_repositories = map_user_repositories

    filtered_prs = retrieve_and_filter_pull_requests(community)
    community.data.all_pull_requests = filtered_prs
    # for each pull request that has been merged, retrieve detailed data
    merged_pr_detailed = []
    with Bar("Retrieving details for pull requests", max=len(filtered_prs)) as bar:
        for pr in filtered_prs:
            if pr["merged_at"] is not None:
                merged_pr_detailed.append(
                    api_manager.get_pr_details(
                        community.repo_owner, community.repo_name, pr["number"]
                    )
                )
            bar.next()
    community.data.merged_pull_requests = merged_pr_detailed
    # retrieve pull request comments and map them to pull requests gatghered

    console.log("Retrieving and mapping comments to pull requests")
    retrieve_and_filter_pr_comments(community)
    map_prs_to_comments(community)


def retrieve_data_per_member(member):
    """
    Given a community member we retrieve his/her followers and following, and we retrieve the repositories he/she worked on.
    """

    if (
        member["followers_url"] is None
        or member["following_url"] is None
        or member["repos_url"] is None
    ):
        return

    followers = api_manager.make_request(member["followers_url"])
    following = api_manager.make_request(str(member["following_url"]).split("{")[0])
    repos = api_manager.make_request(member["repos_url"])

    followers_login = [f["login"] for f in followers if "login" in f.keys()]
    following_login = [f["login"] for f in following if "login" in f.keys()]
    repo_names = [r["name"] for r in repos if "name" in r.keys()]

    return followers_login, following_login, repo_names


def retrieve_and_filter_pull_requests(community: community.Community):
    console.log("Retrieving pull requests")
    prs = api_manager.get_pull_requests(community.repo_owner, community.repo_name)
    return filters.filter_prs(community, prs)


def retrieve_and_filter_pr_comments(community: community.Community):
    comments = api_manager.get_prs_comments(
        community.repo_owner, community.repo_name, community.data.start_date.isoformat()
    )

    filtered_comments = filters.filter_comments(community, comments)

    community.data.pr_comments = filtered_comments


def map_prs_to_comments(community: community.Community):
    """
    Given a list of pull requests for a repository, this method retrieves the pull request review comments
    for each pull request and maps them in a dictionary. Filters all pull request comments by
    non-committers, i.e., users that are not considered members.

    """
    pr_to_comments = {}
    for pr in community.data.all_pull_requests:
        pr_to_comments[str(pr["number"])] = []

    for comment in community.data.pr_comments:
        prs = []
        split_url = comment["pull_request_url"].split("/")
        comment_pr_num = split_url[len(split_url) - 1]
        if comment_pr_num in pr_to_comments:
            pr_to_comments[comment_pr_num].append(comment)
    community.data.map_pr_to_comments = pr_to_comments


def retrieve_miscellaneous_data(community: community.Community):
    retrieve_commits_details(community)
    console.log("Retrieving active users")
    retrieve_active_users(community)
    console.log("Retrieving watchers and stargazers")
    retrieve_watchers_and_stargazers(community)


def retrieve_commits_details(community: community.Community):
    commits = community.data.commits
    modified_files_per_commit = {}
    with Bar("Retrieving commits details...", max=len(commits)) as bar:
        for commit in commits:
            files = list(commit.stats.files.keys())
            modified_files_per_commit[commit.hexsha] = files
            bar.next()

    community.data.modified_files_per_commit = modified_files_per_commit
    console.log("Retrieving first and last commit details")
    (
        first_commit_datetime,
        first_commit_hash,
        last_commit_datetime,
        last_commit_hash,
    ) = filters.filter_first_last_commits(commits)
    community.data.first_commit_datetime = first_commit_datetime
    community.data.first_commit_hash = first_commit_hash
    community.data.last_commit_datetime = last_commit_datetime
    community.data.last_commit_hash = last_commit_hash
    console.log("Retrieving commit comments")
    comments = api_manager.get_commits_comments(
        community.repo_owner, community.repo_name
    )
    community.data.commits_comments = filters.filter_comments(community, comments)


def retrieve_active_users(community: community.Community):
    active_users = []
    date_30 = community.data.end_date - timedelta(days=30)
    for commit in community.data.commits:
        if (commit.author.email not in active_users) and (
            date_30
            <= datetime.strptime(convert_date(commit.authored_date), "%Y-%m-%d")
            <= community.data.end_date
        ):
            active_users.append(commit.author.email)
        if (
            commit.committer.email != commit.author.email
            and (commit.committer.email not in active_users)
            and (
                date_30
                <= datetime.strptime(convert_date(commit.committed_date), "%Y-%m-%d")
                <= community.data.end_date
            )
        ):
            active_users.append(commit.committer.email)
    community.data.active_members = active_users


def retrieve_watchers_and_stargazers(community: community.Community):
    community.data.watchers = api_manager.get_watchers(
        community.repo_owner, community.repo_name
    )
    community.data.stargazers = api_manager.get_stargazers(
        community.repo_owner, community.repo_name
    )

    pass
