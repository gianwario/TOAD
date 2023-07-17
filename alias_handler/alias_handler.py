import git
import yaml
import os
from typing import List


def replace_all_aliases(commits: List[git.Commit], aliases_path: str):
    """
    This function reads computed aliases from a file and replaces author aliases with unique one

    :param commits: the list of commits from wich authors are taken
    """

    if not os.path.exists(aliases_path):
        return commits

    content = ""
    with open(aliases_path, "r", encoding="utf-8-sig") as file:
        content = file.read()
    aliases = yaml.load(content, Loader=yaml.FullLoader)

    transposed = {}
    for alias in aliases:
        for email in aliases[alias]:
            transposed[email] = alias

    return replace(commits, transposed)


def replace(commits: List[git.Commit], aliases: List):
    for commit in commits:
        copy = commit
        author = extract_author_id(commit.author)

        if author in aliases:
            copy.author.email = aliases[author]

        yield copy


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

    return distance <= maxDistance
