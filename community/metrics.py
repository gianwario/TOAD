from dataclasses import dataclass


@dataclass
class Metrics:
    """
    This class stores needed data Metrics computed for a Community that will be used
    to detect Community Patterns
    """

    # computed as sqrt sqrt((geographical_variance + cultural_variance) / 2)
    dispersion: {float} = None

    cohesion: float = None

    # MEDIAN of comments per PR, monthly comments distrubtion, active members, watchers, stargazers, commits distrubution, file collaboration distrubution
    engagement: {float, float, float, float, float, float, float} = None

    # mean of membership type, milestones, lifetime of the community
    formality: {float, float, float} = None

    longevity: float = None

    # TODO operationalize as integers? (not only checks)
    # common projects between devs, follower relationships, PR interactions
    structure: {bool, bool, bool} = None
