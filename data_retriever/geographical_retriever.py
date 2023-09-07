from geopy.geocoders import Nominatim
from console import console
import pandas as pd
from community import community
from geodispersion import globe_data_reader
import time


def retrieve_geo_information(community: community.Community):
    geolocator = Nominatim(user_agent="yoshi3")
    updated_members = []
    coordinates = []
    for member in community.data.members:
        if member["location"] is not None:
            result = None
            try:
                result = geolocator.geocode(
                    member["location"], addressdetails=True, language="en"
                )
                time.sleep(1)
            except:
                pass
            if result is not None and result.raw is not None:
                member["location"] = result.raw
                member_lat = float(member["location"]["lat"])
                member_lon = float(member["location"]["lon"])
                coord = {"lon": member_lon, "lat": member_lat}
                coordinates.append(coord)
            else:
                member["location"] = None
        updated_members.append(member)
    community.data.members = updated_members
    community.data.coordinates = coordinates


def retrieve_country_name(community: community.Community):
    countries = []

    globe = pd.DataFrame(
        globe_data_reader.read_data(
            "geodispersion/GLOBE-Phase-2-Aggregated-Societal-Culture-Data.xls"
        )
    )
    globe_countries = globe["Country Name"].tolist()

    for member in community.data.members:
        for country in globe_countries:
            if (
                member["location"] is not None
                and "address" in member["location"].keys()
                and member["location"]["address"] is not None
                and "country" in member["location"]["address"].keys()
                and member["location"]["address"]["country"] is not None
                and member["location"]["address"]["country"] in country
            ):
                countries.append(country)
    community.data.countries = countries
