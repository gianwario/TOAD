from dataclasses import dataclass, asdict, field


@dataclass
class Metrics:
    """
    This class stores needed data Metrics computed for a Community that will be used
    to detect Community Patterns
    """

    # true if both cultural and geographical dispersion exceed thresholds
    dispersion: {} = None

    # cohesion: float = None

    # MEDIAN of comments per PR, monthly comments distrubtion, active members, watchers, stargazers, commits distrubution, file collaboration distrubution
    engagement: {} = None

    # mean of membership type, milestones, lifetime of the community
    formality: {} = None

    longevity: float = None

    # common projects between devs, follower relationships, PR interactions
    structure: {} = None

    @property
    def __dict__(self):
        return asdict(self)
