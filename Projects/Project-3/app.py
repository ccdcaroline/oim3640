import os

from dotenv import load_dotenv
from flask import Flask, render_template, request

from helpers import find_nearest_station_with_route

load_dotenv()

app = Flask(__name__)

MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
MBTA_API_KEY = os.getenv("MBTA_API_KEY", "")  # optional


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("index.html")

    place = request.form.get("place", "").strip()

    if not place:
        return render_template("result.html", error="Please enter an address or town in Massachusetts.")

    if not MAPBOX_TOKEN:
        return render_template("result.html", error="Missing MAPBOX_TOKEN in your .env file.")

    try:
        result = find_nearest_station_with_route(place, MAPBOX_TOKEN, MBTA_API_KEY)
        return render_template(
            "result.html",
            place=place,
            location=result["location"],
            station=result["station"],
            route_geojson=result["route_geojson"],
            mapbox_token=MAPBOX_TOKEN,
        )
    except ValueError as e:
        return render_template("result.html", error=str(e))
    except Exception:
        return render_template("result.html", error="Something went wrong. Please try again.")

if __name__ == "__main__":
    app.run(debug=True) 