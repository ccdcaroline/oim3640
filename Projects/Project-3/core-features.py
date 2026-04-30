import os

import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request

from helpers import geocode_place, nearest_mbta_stop

load_dotenv()

app = Flask(__name__)

MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
MBTA_API_KEY = os.getenv("MBTA_API_KEY", "")  # optional


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("core_index.html")

    place = request.form.get("place", "").strip()

    if not place:
        return render_template("core_result.html", error="Please enter a place name.")

    if not MAPBOX_TOKEN:
        return render_template("core_result.html", error="Missing MAPBOX_TOKEN in .env file.")

    try:
        location = geocode_place(place, MAPBOX_TOKEN)
        stop = nearest_mbta_stop(location["lat"], location["lng"], MBTA_API_KEY)

        return render_template(
            "core_result.html",
            place=place,
            stop_name=stop["name"],
            wheelchair_accessible=("Yes" if stop["wheelchair_accessible"] else "No"),
        )

    except ValueError as e:
        return render_template("core_result.html", error=str(e))
    except requests.exceptions.RequestException:
        return render_template("core_result.html", error="API request failed. Please try again.")
    except Exception:
        return render_template("core_result.html", error="Unexpected error. Please try again.")


if __name__ == "__main__":
    app.run(debug=True) 