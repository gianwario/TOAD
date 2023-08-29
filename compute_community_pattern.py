from community import community
from math import sqrt

# The thresholds that will be used to compute the patterns for each community.
# TODO
th_avg_geo_distance = 4000  # Kilometers
th_avg_cult_distance = 15  # %
th_formality_lvl_low = 0.1
th_formality_lvl_high = 20
th_engagement_lvl = 3.5
th_longevity = 93  # Days


def compute_community_patterns(metrics):
    (
        structure,
        dispersion,
        formality,
        longevity,
        engagement,
    ) = compute_characteristics_from_metrics(metrics)
    community_patterns = {
        "SN": False,
        "NoP": False,
        "IN": False,
        "FN": False,
        "CoP": False,
        "PT": False,
        "FG": False,
        "IC": False,
    }
    # Community exhibits structure
    if structure:
        community_patterns["SN"] = True
        # Dispersed
        if dispersion:
            community_patterns["NoP"] = True
            # Informal
            if formality <= th_formality_lvl_low:
                community_patterns["IN"] = True
            # Formal
            elif formality >= th_formality_lvl_high:
                community_patterns["FN"] = True
        # Not dispersed
        else:
            community_patterns["CoP"] = True

            # cohesion not detected

            # Low durability / short-lived
            if longevity < th_longevity:
                community_patterns["PT"] = True
            # Not informal but also not formal
            if formality >= th_formality_lvl_low and formality <= th_formality_lvl_high:
                community_patterns["FG"] = True
        # Engaged
        if engagement > th_engagement_lvl:
            community_patterns["IC"] = True
    return (structure, dispersion, formality, longevity, engagement, community_patterns)


def compute_characteristics_from_metrics(metrics):
    structure = (
        metrics.structure["repo_connections"]
        or metrics.structure["follow_connections"]
        or metrics.structure["pr_connections"]
    )
    dispersion = (
        metrics.dispersion["avg_geo_distance"] > th_avg_geo_distance
        and metrics.dispersion["cultural_distance_variance"] > th_avg_cult_distance
    )

    engagement = (
        metrics.engagement["m_comment_per_pr"]
        + metrics.engagement["mm_comment_dist"]
        + metrics.engagement["m_watchers"]
        + metrics.engagement["m_stargazers"]
        + metrics.engagement["m_active"]
        + metrics.engagement["mm_commit_dist"]
        + metrics.engagement["mm_filecollab_dist"]
    )
    formality = metrics.formality["m_membership_type"] / (
        metrics.formality["milestones"] / metrics.formality["lifetime"]
    )
    longevity = metrics.longevity

    return structure, dispersion, formality, longevity, engagement
