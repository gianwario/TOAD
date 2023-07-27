from dataclasses import dataclass
from datetime import datetime


@dataclass
class Data:
    """
    This class stores needed data of a Community
    """

    # datetime
    start_date: any = None
    # datetime
    end_date: any = None
    first_commit_hash: str = None
    last_commit_hash: str = None
    first_commit_datetime: any = None
    last_commit_datetime: any = None
    members: list = None
    members_logins: list = None
    aliases: list = None
    map_user_followers: {} = None
    map_user_following: {} = None
    map_user_repositories: {} = None
    commits: list = None
    commits_comments: list = None
    modified_files_per_commit: {} = None
    milestones: list = None
    coordinates: list = None
    distances: list = None
    countries: list = None
    geo_distance_variance: float = None
    cultural_distance_variance: float = None
    merged_pull_requests: list = None
    all_pull_requests: list = None
    pr_comments: list = None
    map_pr_to_comments: {} = None
    """ 
        
        // Regarding the difference between Watchers and Stargazers:
        // https://developer.github.com/changes/2012-09-05-watcher-api/
        // Watchers/Subscribers are users watching the repository. Watching a repository registers the user to receive
        // notifications on new discussions, as well as events in the user's activity feed.
        // Stargazers are users starring the repository. Repository starring is a feature that lets users bookmark
        // repositories. Stars are shown next to repositories to show an approximate level of interest. Stars have no
        // effect on notifications or the activity feed.


        public HashSet<string> ActiveMembers { get; set; }
        public HashSet<string> Watchers { get; set; }
        public HashSet<string> Stargazers { get; set; }

        public int Contributors { get; set; }
        public int Collaborators { get; set; }
    """
