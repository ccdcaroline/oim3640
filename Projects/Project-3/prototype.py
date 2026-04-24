import os
from urllib.parse import quote
from dotenv import load_dotenv
load_dotenv()
import requests
 
MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
MBTA_API_KEY = os.getenv("MBTA_API_KEY", "")  # optional
 
 
def geocode_place(place_name):
    """
    Takes a place name (string) and returns (latitude, longitude).
    Example: "Boston Common" -> (42.355, -71.065)
    """
    if not MAPBOX_TOKEN:
        raise ValueError("Missing MAPBOX_TOKEN environment variable.")
 
    url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{quote(place_name)}.json"
    params = {
        "access_token": MAPBOX_TOKEN,
        "limit": 1
    }
 
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
 
    features = data.get("features", [])
    if not features:
        raise ValueError("Place not found.")
 
    # Mapbox center = [longitude, latitude]
    lng, lat = features[0]["center"]
    return lat, lng
 
 
def nearest_mbta_stop(lat, lng):
    """
    Takes latitude/longitude and returns (stop_name, wheelchair_accessible_bool).
    """
    url = "https://api-v3.mbta.com/stops"
    params = {
        "filter[latitude]": lat,
        "filter[longitude]": lng,
        "sort": "distance",
        "page[limit]": 1
    }
 
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
 
    stops = data.get("data", [])
    if not stops:
        raise ValueError("No nearby MBTA stops found.")
 
    stop = stops[0]
    attrs = stop.get("attributes", {})
    stop_name = attrs.get("name", "Unknown stop")
 
    # MBTA wheelchair_boarding usually: 0, 1, or 2
    wb = attrs.get("wheelchair_boarding", 0)
    wheelchair_accessible = (str(wb) == "1" or wb == 1)
 
    return stop_name, wheelchair_accessible
 
 
def find_stop_near(place_name):
    lat, lng = geocode_place(place_name)
    stop_name, accessible = nearest_mbta_stop(lat, lng)
    return stop_name, accessible
 
 
def main():
    test_place = "Boston Common"
 
    try:
        stop_name, accessible = find_stop_near(test_place)
        print(f"Input place: {test_place}")
        print(f"Nearest stop: {stop_name}")
        print(f"Wheelchair accessible: {accessible}")
    except Exception as e:
        print(f"Error: {e}")
 
 
if __name__ == "__main__":
    main()
