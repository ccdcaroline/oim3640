from urllib.parse import quote
import requests


def geocode_place(place_name, mapbox_token):
    url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{quote(place_name)}.json"
    params = {"access_token": mapbox_token, "limit": 1}

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    features = data.get("features", [])
    if not features:
        raise ValueError("Place not found.")

    lng, lat = features[0]["center"]
    return {"lat": lat, "lng": lng}


def nearest_mbta_stop(lat, lng, mbta_api_key=""):
    url = "https://api-v3.mbta.com/stops"
    params = {
        "filter[latitude]": lat,
        "filter[longitude]": lng,
        "sort": "distance",
        "page[limit]": 1
    }

    if mbta_api_key:
        params["api_key"] = mbta_api_key

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    stops = data.get("data", [])
    if not stops:
        raise ValueError("No nearby MBTA stops found.")

    attrs = stops[0].get("attributes", {})
    wheelchair_accessible = str(attrs.get("wheelchair_boarding", 0)) == "1"

    return {
        "name": attrs.get("name", "Unknown stop"),
        "lat": attrs.get("latitude"),
        "lng": attrs.get("longitude"),
        "wheelchair_accessible": wheelchair_accessible
    }