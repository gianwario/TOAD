from dataclasses import dataclass
@dataclass
class Data():
    start_date:str=None
    end_date:str=None
    first_commit_hash:str=None
    last_commit_hash:str=None
    first_commit_datetime:str=None
    last_commit_datetime:str=None
    members: list=None
    members_username: list=None
    map_user_followers: {str, list}=None
    map_user_following: {str, list}=None
    map_user_repositories: {str, list}=None
    commits: list=None

    '''
        public IReadOnlyList<Milestone> Milestones { get; set; }
        public List<GitHubCommit> CommitsWithinTimeWindow { get; set; }
        public IReadOnlyList<CommitComment> CommitComments { get; set; }
        public List<PullRequest> MergedPullRequests { get; set; }
        public Dictionary<PullRequest, List<IssueComment>> MapPullReqsToComments { get; set; }
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

        public List<Location> Coordinates { get; set; }
        public List<string> Countries { get; set; }
        public int Contributors { get; set; }
        public int Collaborators { get; set; }
    '''
    

