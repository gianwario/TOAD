from console import console
from datetime import datetime
import git
from community import community
from io_module import api_manager
from data_retriever import filters

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
    filters.filter_commits_and_get_members(community)
    if len(community.data.commits) < 100:
        console.print("[bold red]There must be at least 100 commits")
        return False
    filters.filter_authors_by_distance(community, 0.4)
    retrieve_member_data(community)
    if len(community.data.members) < 2:
        console.print("[bold red]There must be at least 2 members")
        return False        
    milestones = api_manager.get_closed_milestones(community.repo_owner, community.repo_name)
    if len(milestones) < 1 : 
        console.print("[bold red]There must be at least 1 milestone")
        return False
    #controllo su dati geografici
    return True


def retrieve_member_data(community: community.Community):
    '''
    Retrieves the GitHub user information from the usernames contained in the community data
    :param community: the community containing members usernames
    '''
    members = []
    bots = []
    organizations = []
    for username in community.data.members_username:
        print(username)
        api_manager.get_user_from_username(username)

def retrieve_structure_data(community: community.Community):
    '''
            /// <summary>
        /// Method that retrieves all GitHub data that is needed to compute only the structure metrics and modifies the 
        /// community data to store that information. It retrieves a mapping from a member to their followers, a mapping 
        /// from a member to their following, and a mapping from a member to their owned repositories.
        /// </summary>
        /// <param name="community">The community for which we need to retrieve GitHub Data.</param>
        /// <returns>No object or value is returned by this method when it completes.</returns>
        /// <exception cref="Exception">Thrown when something goes wrong while retrieving GitHub data.</exception>
    '''


    pass
