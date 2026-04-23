"""Minimal Flask app scaffold for MTBA stations.

This is a very simple starting base that runs from
Projects/Project-3/prototype.py. It currently serves one
page with example station data.
"""

from flask import Flask

app = Flask(__name__)


def load_mtba_stations():
    """Return sample MTBA station lines and stops."""
    return {
        "Red Line": ["Alewife", "Harvard", "South Station"],
        "Green Line": ["Lechmere", "Copley", "Park Street"],
        "Orange Line": ["Oak Grove", "Downtown Crossing", "Forest Hills"],
    }


@app.route('/')
def home():
    return "<p>MTBA station viewer base app. Visit <a href='/mtba'>/mtba</a>.</p>"


@app.route('/mtba')
def mtba():
    stations = load_mtba_stations()
    html = ["<h1>MTBA Stations</h1>"]
    for line, stops in stations.items():
        html.append(f"<h2>{line}</h2>")
        html.append("<ul>")
        for stop in stops:
            html.append(f"<li>{stop}</li>")
        html.append("</ul>")
    return "\n".join(html)


if __name__ == '__main__':
    app.run(debug=True)
