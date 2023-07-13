from utils import convert_commit_date
from datetime import datetime
from strsimpy.metric_lcs import MetricLCS
import re
from community import community
import git
from io_module import api_manager


def filter_commits_and_get_members(community: community.Community):
    """
    This function filters commits within the given time window.
    It also gets the members of the community storing them in its data.

    :param community: the community
    """ 
    filteder_commits = []
    authors = []
    authors_email = []
    for commit in community.data.commits:
        if community.data.start_date <= datetime.strptime(convert_commit_date(commit.committed_date),'%Y-%m-%d') <= community.data.end_date:
            authors_email.append(extract_author_id(commit.author))
            for co_author in commit.co_authors:
                authors_email.append(extract_author_id(co_author))
            filteder_commits.append(commit)
    print(len(community.data.commits))
    print(len(filteder_commits))
    community.data.commits = filteder_commits
    users = []
    for email in list(dict.fromkeys(authors_email)):
        print(email)
        u = api_manager.get_user_from_email(email)
        if u: users.append(u)
    print(len(users))
    
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

def filter_authors_by_distance(community: community.Community, max_distance: float):
    """
    This function is used to filter some of the authors. Given the username of community members,
    it checks the distance of each couple of strings based on Longest Common Subsequence. If the distance
    is lower than the max_distance parameter, the function consider the usernames as it belongs to the same person,
    deleting one of them.

    :param community: 
    :param max_distance: the threshold used to consider two username similar
    """ 
    similars = []
    lcs = MetricLCS()
    expr = r"(.+)@"
    authors = community.data.members_username
    for author in authors:
        for other_author in authors:
            localPartAMatches = re.findall(expr, author)
            localPartBMatches = re.findall(expr, other_author)

            if len(localPartAMatches) == 0:
                localPartAMatches = [author]

            if len(localPartBMatches) == 0:
                localPartBMatches = [other_author]

            distance = lcs.distance(localPartAMatches[0], localPartBMatches[0])
            if(distance <= max_distance and distance != 0 and not [other_author, author] in similars):
                similars.append([author, other_author])

    for couple in similars:
        community.data.members_username.remove(couple[1])
    