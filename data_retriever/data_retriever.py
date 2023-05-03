from console import console
from utils import convert_commit_date
from datetime import datetime
import git
from community import community
from strsimpy.metric_lcs import MetricLCS
import re
from io_module import api_manager

def retrieve_data_and_check_validity(community: community.Community):
    console.log("Checking commits")
    filter_commits_and_get_members(community)
    filter_authors_by_distance(community, 0.4)
    milestones = api_manager.get_closed_milestones(community.repo_owner, community.repo_name)
    if(len(community.data.commits) < 100 or len(community.data.members) < 2 or len(milestones) < 1): return False
    return True



def filter_commits_and_get_members(community: community.Community):
    filteder_commits = []
    authors = []
    authors_id = []
    for commit in community.data.commits:
        if community.data.start_date <= datetime.strptime(convert_commit_date(commit.committed_date),'%Y-%m-%d') <= community.data.end_date:
            authors.append(commit.author)
            authors_id.append(extract_author_id(commit.author))
            for co_author in commit.co_authors:
                authors.append(co_author)
                authors_id.append(extract_author_id(co_author))
            filteder_commits.append(commit)

    community.data.commits = filteder_commits
    community.data.members = list(dict.fromkeys(authors))
    community.data.members_username = list(dict.fromkeys(authors_id))
    
def extract_author_id(author: git.Actor):
    user_id = ""
    if author.email is None:
        user_id = author.name
    else:
        user_id = author.email
    return user_id.lower().strip()

def filter_authors_by_distance(community: community.Community, max_distance: float):
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
    