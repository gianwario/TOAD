from community import community
from geodispersion import globe_data_reader


import itertools
from math import radians, degrees, sin, cos, asin, acos, sqrt
import statistics


def compute_distances(community: community.Community):
    globe = globe_data_reader.read_data(
        "geodispersion\GLOBE-Phase-2-Aggregated-Societal-Culture-Data.xls"
    )
    community.data.distances = compute_geographical_distances(community)
    geographical_variance = statistics.variance(community.data.distances)
    community.data.geo_distance_variance = geographical_variance
    cultural_variance = compute_cultural_distance(community, globe)
    community.data.cultural_distance_variance = cultural_variance


def compute_geographical_distances(community: community.Community):
    distances = []
    coords = community.data.coordinates
    for c1 in coords:
        coords.remove(c1)
        for c2 in coords:
            distance = great_circle(
                c1["lon"],
                c1["lat"],
                c2["lon"],
                c2["lat"],
            )
            distances.append(distance)
    return distances


def compute_cultural_distance(community: community.Community, globe):
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
                # list_ASP.append(row["Assertiveness Societal Practices"])
    # TODO check Assertiveness Societal Practices as it gives an error
    variances = [
        statistics.variance(list_UASP),
        statistics.variance(list_FOSP),
        statistics.variance(list_PDSP),
        statistics.variance(list_C1SP),
        statistics.variance(list_HOSP),
        statistics.variance(list_POSP),
        statistics.variance(list_C2SP),
        # statistics.variance(list_ASP),
    ]
    # determine the average of the variances to obtain the variance of cultural distance
    average_distance_variance = sum(variances) / len(variances)
    return average_distance_variance


def great_circle(lon1, lat1, lon2, lat2):
    """
    The Great Circle distance formula computes the shortest distance path of two points on the surface of the sphere.
    That means, when applies this to calculate distance of two locations on Earth, the formula assumes that the Earth is spherical.
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    return 6371 * (
        acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon1 - lon2))
    )
