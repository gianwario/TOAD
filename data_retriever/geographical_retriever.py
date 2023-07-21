from geopy.geocoders import Nominatim
from console import console

from community import community


def retrieve_geo_information(community: community.Community):
    geolocator = Nominatim(user_agent="yoshi3")
    updated_members = []
    for member in community.data.members:
        if member["location"] is not None:
            result = geolocator.geocode(member["location"])
            member["location"] = result.raw
        updated_members.append(member)
    community.data.members = updated_members
