"""Simple workout app base.
Run with: python prototype.py
Then visit http://127.0.0.1:5000/workout
"""

from flask import Flask

app = Flask(__name__)


def generate_workout():
    """Return a simple sample workout routine."""
    return [
        {"exercise": "Push-ups", "sets": 3, "reps": 10},
        {"exercise": "Squats", "sets": 3, "reps": 15},
        {"exercise": "Planks", "sets": 3, "duration": "30 seconds"},
    ]


@app.route('/')
def home():
    return "<p>Workout app base. Visit <a href='/workout'>/workout</a>.</p>"


@app.route('/workout')
def workout():
    routine = generate_workout()
    html = ["<h1>Today's Workout</h1>"]
    for item in routine:
        html.append(f"<p>{item['exercise']}: {item['sets']} sets")
        if 'reps' in item:
            html.append(f" of {item['reps']} reps</p>")
        elif 'duration' in item:
            html.append(f" for {item['duration']}</p>")
    return "\n".join(html)


if __name__ == '__main__':
    app.run(debug=True)
