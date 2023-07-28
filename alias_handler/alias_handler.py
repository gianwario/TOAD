import git
import os
from console import console

from io_module import api_manager
from dotenv import load_dotenv
from community import community
from progress.bar import Bar


load_dotenv(".env")
dot_env_path = ".env"

SIMILARITY_MAX_DISTANCE = os.environ.get("SIMILARITY_MAX_DISTANCE", "")


"""
credit: https://github.com/Nuri22/csDetector/blob/master/authorAliasExtractor.py
"""


def alias_extraction(community: community.Community):
    # we get two data structure, one containing a mapping of emails of community members for which login username is available,
    # the other one containing a list of users with no public login available
    commits_login, commits_without_login = get_commits_information(community)

    aliases = {}
    used = {}

    for email in commits_login:
        login = commits_login[email]
        alias_emails = aliases.setdefault(login, [])
        alias_emails.append(email)
        used[email] = login

    # we check each of the members with no login available to understand if the email may belong to one of the already mapped users
    if len(commits_without_login) > 0:
        for authorA in commits_without_login:
            match_found = False

            # go through used values
            for used_login in used:
                if authorA == used_login:
                    match_found = True
                    continue

                if check_similarity(authorA, used_login, SIMILARITY_MAX_DISTANCE):
                    alias = used[used_login]
                    aliases[alias].append(authorA)
                    used[authorA] = alias
                    match_found = True
                    break

            if match_found:
                continue

            # go through already extracted keys
            for key in aliases:
                if authorA == key:
                    match_found = True
                    continue

                if check_similarity(authorA, key, SIMILARITY_MAX_DISTANCE):
                    aliases[key].append(authorA)
                    used[authorA] = key
                    match_found = True
                    break

            if match_found:
                continue

            # go through all authors
            for authorB in commits_without_login:
                if authorA == authorB:
                    continue

                if check_similarity(authorA, authorB, SIMILARITY_MAX_DISTANCE):
                    aliased = aliases.setdefault(authorA, [])
                    aliased.append(authorB)
                    used[authorB] = authorA
                    break

    return aliases


def get_commits_information(community: community.Community):
    commits = community.data.commits

    # get all distinct author emails from the commit list of the community
    emails = set(extract_author_id(commit.author) for commit in commits)

    # for each email, get the SHA of one single commit from the author
    commits_sha = {}
    for email in emails:
        commit = next(
            commit
            for commit in community.data.commits
            if extract_author_id(commit.author) == email
        )

        commits_sha[email] = commit.hexsha

    # using the GitHub API, we try to retrieve the LOGIN of the author by querying the commit informations
    commits_login = dict()
    commits_without_login = []

    with Bar("Computing aliases...", max=len(commits_sha)) as bar:
        for email in commits_sha:
            sha = commits_sha[email]
            commit = api_manager.get_commit_by_sha(
                community.repo_owner, community.repo_name, sha
            )
            if not "author" in commit.keys():
                continue

            if not commit["author"] is None and not commit["author"]["login"] is None:
                commits_login[email] = commit["author"]["login"]
            else:
                commits_without_login.append(email)
            bar.next()

    return commits_login, commits_without_login


def replace_all_aliases(commits: list[git.Commit], aliases):
    """
    This function reads computed aliases from a file and replaces author aliases with unique one

    :param commits: the list of commits from wich authors are taken
    """

    transposed = {}
    for alias in aliases:
        for email in aliases[alias]:
            transposed[email] = alias

    updated_commits = []
    for commit in commits:
        copy = commit
        author = extract_author_id(commit.author)
        committer = extract_author_id(commit.committer)
        if author in transposed:
            copy.author.email = transposed[author]

        if committer in transposed:
            copy.committer.email = transposed[author]

        updated_commits.append(copy)

    return updated_commits


def extract_author_id(author: git.Actor):
    """
    This function maps members username to be email if possible, otherwise his name.

    :param author: the author (as a git Actor class)
    """
    user_id = ""
    if author.email is None:
        user_id = author.name
    else:
        user_id = author.email
    return user_id.lower().strip()


def check_similarity(authorA: str, authorB: str, max_distance: float):
    """
    Given the username of two authors, this function checks the distance of the couple
    of strings based on Longest Common Subsequence.

    :param authorA, authorB: the two authors username
    :param max_distance: the threshold used to consider two username similar
    """
    lcs = MetricLCS()
    expr = r"(.+)@"

    localPartAMatches = re.findall(expr, authorA)
    localPartBMatches = re.findall(expr, authorB)

    if len(localPartAMatches) == 0:
        localPartAMatches = [authorA]

    if len(localPartBMatches) == 0:
        localPartBMatches = [authorB]

    distance = lcs.distance(localPartAMatches[0], localPartBMatches[0])

    return distance <= max_distance
