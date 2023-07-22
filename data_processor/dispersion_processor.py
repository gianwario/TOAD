from community import community
from geodispersion import globe_data_reader


import itertools
from math import radians, degrees, sin, cos, asin, acos, sqrt


def compute_dispersion(community: community.Community):
    globe = globe_data_reader.read_data(
        "geodispersion\GLOBE-Phase-2-Aggregated-Societal-Culture-Data.xls"
    )
    print(compute_geographical_distances(community))
    compute_cultural_dispersion(community, globe)


def compute_geographical_distances(community: community.Community):
    distances = []
    coords = unique_combinations(community.data.coordinates)
    for couple in coords:
        distance = great_circle(
            couple[0]["lon"],
            couple[0]["lat"],
            couple[1]["lon"],
            couple[1]["lat"],
        )
        distances.append(distance)
    print(distances)
    return distances


def compute_cultural_dispersion(community: community.Community, globe):
    pass


def great_circle(lon1, lat1, lon2, lat2):
    """
    The Great Circle distance formula computes the shortest distance path of two points on the surface of the sphere.
    That means, when applies this to calculate distance of two locations on Earth, the formula assumes that the Earth is spherical.
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    return 6371 * (
        acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon1 - lon2))
    )


def unique_combinations(elements):
    l = list(itertools.combinations(elements, 2))

    unique = []

    for el in l:
        if el in unique:
            continue
        else:
            unique.append(el)
    return unique
