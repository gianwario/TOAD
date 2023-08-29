from community import community, metrics
from geodispersion import globe_data_reader
import itertools
from math import radians, degrees, sin, cos, asin, acos, sqrt
import statistics
from console import console


def compute_distances(community: community.Community):
    """
    This method computes the values needed for the community geodispersion metric (i.e. geographical variance
    and cultural variance).
    """
    globe = globe_data_reader.read_data(
        "geodispersion\GLOBE-Phase-2-Aggregated-Societal-Culture-Data.xls"
    )
    community.data.distances = compute_geographical_distances(community)
    geographical_variance = statistics.variance(community.data.distances)
    avg_geo_distance = statistics.mean(community.data.distances)
    community.metrics.dispersion["geo_distance_variance"] = geographical_variance
    community.metrics.dispersion["avg_geo_distance"] = avg_geo_distance
    cultural_variance = compute_cultural_distance(community, globe)
    community.metrics.dispersion["cultural_distance_variance"] = cultural_variance


def compute_geographical_distances(community: community.Community):
    """
    This method computes the distance in kilometers between each pair of coordinates stored in the community
    """
    distances = []
    coords = community.data.coordinates
    for i in range(len(coords)):
        c1 = coords[i]
        for j in range(len(coords)):
            if i != j:
                c2 = coords[j]
                distance = great_circle(
                    c1["lon"],
                    c1["lat"],
                    c2["lon"],
                    c2["lat"],
                )
                distances.append(distance)
    return distances


def compute_cultural_distance(community: community.Community, globe):
    """_summary_
    This method computes the cultural variance of the community using
    the Globe indexes.

    Wolf, Thom (2006) "Culture, Leadership, and Organizations: The GLOBE Study of 62 Societies  /
    House, R. J., Hanges, P.J., & Javidan, M., Eds.," Journal of Applied Christian Leadership: Vol. 1: No. 1,
    55-71.
    Available at: https://digitalcommons.andrews.edu/jacl/vol1/iss1/6
    """
    # compute the variance for all of the globe indexes
    countries = community.data.countries

    list_UASP = []
    list_FOSP = []
    list_PDSP = []
    list_C1SP = []
    list_HOSP = []
    list_POSP = []
    list_C2SP = []
    list_GESP = []
    list_ASP = []

    for index, row in globe.iterrows():
        for country in countries:
            if row["Country Name"] == country:
                list_UASP.append(row["Uncertainty Avoidance Societal Practices"])
                list_FOSP.append(row["Future Orientation Societal Practices"])
                list_PDSP.append(row["Power Distance Societal Practices"])
                list_C1SP.append(
                    row[
                        "Collectivism I Societal Practices (Institutional Collectivism)"
                    ]
                )
                list_HOSP.append(row["Humane Orientation Societal Practices"])
                list_POSP.append(row["Performance Orientation Societal Practices"])
                list_C2SP.append(
                    row["Collectivism II Societal Practices (In-group Collectivism)"]
                )
                list_GESP.append(row["Gender Egalitarianism Societal Practices"])
                list_ASP.append(row["Assertiveness Societal Practices"])

    variances = [
        statistics.variance(list_UASP),
        statistics.variance(list_FOSP),
        statistics.variance(list_PDSP),
        statistics.variance(list_C1SP),
        statistics.variance(list_HOSP),
        statistics.variance(list_POSP),
        statistics.variance(list_C2SP),
        statistics.variance(list_ASP),
    ]
    means = [
        statistics.mean(list_UASP),
        statistics.mean(list_FOSP),
        statistics.mean(list_PDSP),
        statistics.mean(list_C1SP),
        statistics.mean(list_HOSP),
        statistics.mean(list_POSP),
        statistics.mean(list_C2SP),
        statistics.mean(list_ASP),
    ]
    # determine the average of the variances to obtain the variance of cultural distance
    average_distance_variance = sum(variances) / len(variances)
    avg_distance_means = sum(means) / len(means)
    return average_distance_variance * 100


def great_circle(lon1, lat1, lon2, lat2):
    """
    The Great Circle distance formula computes the shortest distance path of two points on the surface of the sphere.
    That means, when applies this to calculate distance of two locations on Earth, the formula assumes that the Earth is spherical.
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    return 6371 * (
        acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon1 - lon2))
    )
