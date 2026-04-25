import os
from urllib.parse import quote

import requests
from flask import Flask, render_template, request

app = Flask(__name__)

MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
MBTA_API_KEY = os.getenv("MBTA_API_KEY", "")  # optional


def geocode_place(place_name):
    if not MAPBOX_TOKEN:
        raise ValueError("Missing MAPBOX_TOKEN environment variable.")

    url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{quote(place_name)}.json"
    params = {"access_token": MAPBOX_TOKEN, "limit": 1}
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    features = data.get("features", [])
    if not features:
        raise ValueError("Place not found.")

    lng, lat = features[0]["center"]
    return lat, lng


def nearest_mbta_stop(lat, lng):
    url = "https://api-v3.mbta.com/stops"
    params = {
        "filter[latitude]": lat,
        "filter[longitude]": lng,
        "sort": "distance",
        "page[limit]": 1
    }

    if MBTA_API_KEY:
        params["api_key"] = MBTA_API_KEY

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    stops = data.get("data", [])
    if not stops:
        raise ValueError("No nearby MBTA stops found.")

    attrs = stops[0].get("attributes", {})
    stop_name = attrs.get("name", "Unknown stop")
    wb = attrs.get("wheelchair_boarding", 0)
    accessible = (str(wb) == "1" or wb == 1)

    return stop_name, accessible


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        place = request.form.get("place", "").strip()

        if not place:
            return render_template("result.html", error="Please enter a place name.")

        try:
            lat, lng = geocode_place(place)
            stop_name, accessible = nearest_mbta_stop(lat, lng)
            return render_template(
                "result.html",
                place=place,
                stop_name=stop_name,
                accessible=accessible
            )
        except requests.exceptions.RequestException:
            return render_template("result.html", error="API request failed. Try again.")
        except ValueError as e:
            return render_template("result.html", error=str(e))
        except Exception:
            return render_template("result.html", error="Unexpected error. Try again.")

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)