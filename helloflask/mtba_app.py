"""Minimal Flask app for viewing MTBA stations.

Run from the helloflask folder:
    python mtba_app.py

Then open http://127.0.0.1:5000/mtba in a browser.
"""

from flask import Flask, render_template

app = Flask(__name__)


def load_mtba_stations():
    """Return a small sample of MTBA station lines and stops."""
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
    return render_template('mtba.html', stations=stations)


if __name__ == '__main__':
    app.run(debug=True)
