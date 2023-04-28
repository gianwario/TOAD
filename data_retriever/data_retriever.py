from console import console
from utils import convert_commit_date
def retrieve_data(community):
    console.log("Checking commits")
    if(len(community.data.commits) < 100): return False
    filter_commits_between_dates(community)
    return True



def filter_commits_between_dates(community):
    print(community.data.start_date)
    print(convert_commit_date(community.data.commits[0].committed_date))
    
