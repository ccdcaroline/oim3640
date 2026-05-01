from math import asin, cos, radians, sin, sqrt
from urllib.parse import quote

import requests

# Massachusetts bounding box: west,south,east,north
MA_BBOX = "-73.508142,41.237964,-69.928393,42.886589"

# simple in-memory cache so we don't refetch stations each search
STATIONS_CACHE = None


def geocode_ma_place(place, mapbox_token):
    """
    Geocode an address/town in Massachusetts.
    """
    attempts = [
        place.strip(),
        f"{place.strip()}, Massachusetts",
        f"{place.strip()}, MA",
    ]

    for query in attempts:
        url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{quote(query)}.json"
        params = {
            "access_token": mapbox_token,
            "limit": 1,
            "country": "us",
            "bbox": MA_BBOX,
            "types": "address,poi,place,locality,neighborhood",
        }

        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        features = data.get("features", [])
        if features:
            f = features[0]
            lng, lat = f["center"]
            return {
                "name": f.get("place_name", query),
                "lat": lat,
                "lng": lng,
            }

    raise ValueError("Could not find that location in Massachusetts. Try a full address or town name.")


def fetch_mbta_stations(mbta_api_key=""):
    """
    Fetch MBTA rail/ferry stations (not bus stops), with pagination.
    """
    global STATIONS_CACHE
    if STATIONS_CACHE is not None:
        return STATIONS_CACHE

    all_stations = []
    offset = 0
    page_size = 1000

    while True:
        url = "https://api-v3.mbta.com/stops"
        params = {
            "filter[route_type]": "0,1,2,4",   # light rail, heavy rail, commuter rail, ferry
            "page[limit]": page_size,
            "page[offset]": offset,
        }
        if mbta_api_key:
            params["api_key"] = mbta_api_key

        response = requests.get(url, params=params, timeout=20)
        response.raise_for_status()
        data = response.json()

        chunk = data.get("data", [])
        if not chunk:
            break

        for stop in chunk:
            attrs = stop.get("attributes", {})
            lat = attrs.get("latitude")
            lng = attrs.get("longitude")
            if lat is None or lng is None:
                continue

            wheelchair_code = attrs.get("wheelchair_boarding", 0)
            if str(wheelchair_code) == "1":
                wheelchair_text = "Yes"
            elif str(wheelchair_code) == "2":
                wheelchair_text = "No"
            else:
                wheelchair_text = "Unknown"

            all_stations.append({
                "id": stop.get("id"),
                "name": attrs.get("name", "Unknown station"),
                "lat": lat,
                "lng": lng,
                "wheelchair_accessible": wheelchair_text,
            })

        if len(chunk) < page_size:
            break

        offset += page_size

    if not all_stations:
        raise ValueError("Could not load MBTA stations.")

    STATIONS_CACHE = all_stations
    return STATIONS_CACHE


def haversine_miles(lat1, lng1, lat2, lng2):
    """
    Straight-line distance in miles.
    """
    r = 3958.8
    dlat = radians(lat2 - lat1)
    dlng = radians(lng2 - lng1)

    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlng / 2) ** 2
    c = 2 * asin(sqrt(a))
    return r * c


def find_nearest_station(lat, lng, stations):
    nearest = None
    best = float("inf")

    for s in stations:
        d = haversine_miles(lat, lng, s["lat"], s["lng"])
        if d < best:
            best = d
            nearest = s

    if nearest is None:
        raise ValueError("No MBTA station found.")

    station = nearest.copy()
    station["distance_miles"] = round(best, 2)
    return station


def get_route_geojson(origin_lng, origin_lat, dest_lng, dest_lat, mapbox_token):
    """
    Get a route line from address -> station using Mapbox Directions.
    """
    coordinates = f"{origin_lng},{origin_lat};{dest_lng},{dest_lat}"
    url = f"https://api.mapbox.com/directions/v5/mapbox/driving/{coordinates}"
    params = {
        "access_token": mapbox_token,
        "geometries": "geojson",
        "overview": "full",
    }

    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()
    data = response.json()

    routes = data.get("routes", [])
    if not routes:
        return None

    return routes[0].get("geometry")


def find_nearest_station_with_route(place, mapbox_token, mbta_api_key=""):
    location = geocode_ma_place(place, mapbox_token)
    stations = fetch_mbta_stations(mbta_api_key)
    station = find_nearest_station(location["lat"], location["lng"], stations)
    route_geojson = get_route_geojson(
        location["lng"], location["lat"], station["lng"], station["lat"], mapbox_token
    )

    return {
        "location": location,
        "station": station,
        "route_geojson": route_geojson,
    } 