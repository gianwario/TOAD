from console import console
import time
from datetime import datetime
import git
from community import community
from io_module import api_manager
from data_retriever import filters
from alias_handler import alias_handler
from data_retriever import geographical_retriever
from progress.bar import Bar
from utils import check_githubdate_within_timewindow


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
    milestones = filters.filter_milestones(milestones)
    if len(milestones) < 1:
        console.print("[bold red]There must be at least 1 closed milestone")
        # return False
    console.log("Retrieving geographical information")
    geographical_retriever.retrieve_geo_information(community)
    geographical_retriever.retrieve_country_name(community)

    # TODO how many geo info do we need to consider the repository valid?
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
    for member in community.data.members:
        (
            followers_login,
            following_login,
            repo_names,
        ) = retrieve_data_per_member(member)
        map_user_followers[member["login"]] = followers_login
        map_user_following[member["login"]] = following_login
        map_user_repositories[member["login"]] = repo_names
    community.data.map_user_followers = map_user_followers
    community.data.map_user_following = map_user_following
    community.data.map_user_repositories = map_user_repositories

    filtered_prs = retrieve_and_filter_pull_requests(community)

    # for each pull request that has been merged, retrieve detailed data
    merged_pr_detailed = []
    for pr in filtered_prs:
        if pr["merged_at"] is not None:
            merged_pr_detailed.append(
                api_manager.get_pr_details(
                    community.repo_owner, community.repo_name, pr["number"]
                )
            )
    community.data.merged_pull_requests = merged_pr_detailed
    # retrieve pull request comments and map them to pull requests gatghered

    pass


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

    followers_login = [f["login"] for f in followers]
    following_login = [f["login"] for f in following]
    repo_names = [r["name"] for r in repos]

    return followers_login, following_login, repo_names


def retrieve_and_filter_pull_requests(community: community.Community):
    prs = api_manager.get_pull_requests(community.repo_owner, community.repo_name)
    return filters.filter_prs(prs)


def retrieve_and_filter_pr_comments(community: community.Community):
    """
        Method that retrieves from GitHub comments from the pull requests gathered.
        Note that it uses the IssuesAPI over the PullsAPI since the some comments are
        considered as Issue Comment from GitHub and could not be retrieved through the PullsAPI.


                IssueCommentRequest issueCommentRequest = new IssueCommentRequest { Since = Filters.StartDateTimeWindow };
                IReadOnlyList<IssueComment> comments =
                    await GitHubRateLimitHandler.Delegate(Client.Issue.Comment.GetAllForRepository, repoOwner, repoName, issueCommentRequest, MaxSizeBatches);

                Console.WriteLine("Filtering pull request comments...");
                List<IssueComment> filteredComments = Filters.FilterComments(comments, memberUsernames);

                return filteredComments;


    YYYY-MM-DDTHH:MM:SSZ
    """
    dt = time.gmtime(community.data.start_date)
    since = (
        tr(dt.tm_year)
        + "-"
        + str(dt.tm_mon)
        + "-"
        + str(dt.tm_mday)
        + "T"
        + str(dt.tm_hour)
        + ":"
        + str(dt.tm_min)
        + ":"
        + str(dt.tm_sec)
        + "Z"
    )
    comments = api_manager.get_issue_comments(
        community.repo_owner, community.repo_name, since
    )
    filtered_comments = filters.filter_pr_comments(comments)


# TODO
def map_prs_to_comments(community: community.Community):
    pass
