import os
import random
import requests
from flask import Flask, request, render_template
from dotenv import load_dotenv

# Load .env from the same directory as this file
load_dotenv('.env')

app = Flask(__name__)

# Debug: Print API key status on startup
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
API_NINJAS_KEY = os.getenv("API_NINJAS_KEY", "")

print(f"=== API Keys Loaded ===")
print(f"OPENWEATHER_API_KEY: {'SET' if OPENWEATHER_API_KEY else 'MISSING'}")
print(f"API_NINJAS_KEY: {'SET' if API_NINJAS_KEY else 'MISSING'}")
print(f"========================")
 
FALLBACK_EXERCISES = {
    "strength": [
        {"name": "Push-ups", "note": "Upper body strength"},
        {"name": "Bodyweight Squats", "note": "Leg and glute strength"},
        {"name": "Plank", "note": "Core stability"},
        {"name": "Lunges", "note": "Balance and lower body strength"},
    ],
    "fat loss": [
        {"name": "Jumping Jacks", "note": "Light cardio warm-up"},
        {"name": "Mountain Climbers", "note": "Full-body cardio"},
        {"name": "High Knees", "note": "Boost heart rate"},
        {"name": "Burpees", "note": "High intensity conditioning"},
    ],
    "mobility": [
        {"name": "Cat-Cow", "note": "Spine mobility"},
        {"name": "Hip Flexor Stretch", "note": "Lower body flexibility"},
        {"name": "Thoracic Rotations", "note": "Upper back mobility"},
        {"name": "Child's Pose", "note": "Recovery and breathing"},
    ],
}
 
 
def energy_to_intensity(energy, mood):
    if energy <= 3:
        intensity = "low"
    elif energy <= 7:
        intensity = "medium"
    else:
        intensity = "high"
 
    if mood == "tired":
        intensity = "low"
    elif mood == "stressed" and intensity == "high":
        intensity = "medium"
    elif mood == "motivated" and intensity == "low":
        intensity = "medium"
 
    return intensity
 
 
def get_weather(city):
    print(f"=== get_weather called with city: {city} ===")
    print(f"OPENWEATHER_API_KEY present: {bool(OPENWEATHER_API_KEY)}")
    
    if not OPENWEATHER_API_KEY:
        return {
            "source": "demo",
            "description": "clear sky (demo)",
            "temp_f": 68,
            "good_for_outdoor": True,
        }
 
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "appid": OPENWEATHER_API_KEY, "units": "imperial"}
        r = requests.get(url, params=params, timeout=8)
        r.raise_for_status()
        data = r.json()
 
        description = data["weather"][0]["description"].lower()
        temp_f = data["main"]["temp"]
 
        bad_weather_words = ["rain", "storm", "snow", "thunder", "drizzle"]
        has_bad_weather = any(word in description for word in bad_weather_words)
        extreme_temp = temp_f < 40 or temp_f > 92
 
        result = {
            "source": "openweather",
            "description": description,
            "temp_f": round(temp_f, 1),
            "good_for_outdoor": not (has_bad_weather or extreme_temp),
        }
        print(f"Weather result: {result}")
        return result
    except Exception as e:
        print(f"Weather API error: {e}")
        return {
            "source": "fallback",
            "description": "weather unavailable",
            "temp_f": 70,
            "good_for_outdoor": True,
        }
 
 
def fetch_exercises(goal):
    print(f"=== fetch_exercises called with goal: {goal} ===")
    print(f"API_NINJAS_KEY present: {bool(API_NINJAS_KEY)}")
    
    goal_to_muscle = {
        "strength": "chest",
        "fat loss": "abdominals",
        "mobility": "lower_back",
    }
    muscle = goal_to_muscle.get(goal, "chest")
 
    if not API_NINJAS_KEY:
        print("Using fallback exercises (no API key)")
        return random.sample(FALLBACK_EXERCISES[goal], k=3)
 
    try:
        url = "https://api.api-ninjas.com/v1/exercises"
        headers = {"X-Api-Key": API_NINJAS_KEY}
        params = {"muscle": muscle}
        r = requests.get(url, headers=headers, params=params, timeout=8)
        r.raise_for_status()
        data = r.json()
 
        if not data:
            print("Ninjas API returned empty, using fallback")
            return random.sample(FALLBACK_EXERCISES[goal], k=3)
 
        cleaned = []
        for item in data[:12]:
            cleaned.append(
                {
                    "name": item.get("name", "Unknown exercise").title(),
                    "note": f"Difficulty: {item.get('difficulty', 'unknown')}",
                }
            )
 
        result = random.sample(cleaned, k=min(3, len(cleaned)))
        print(f"Got {len(cleaned)} exercises from API, returning {len(result)}")
        return result
    except Exception as e:
        print(f"Ninjas API error: {e}")
        return random.sample(FALLBACK_EXERCISES[goal], k=3)
 
 
def build_plan(mood, energy, goal, weather, exercises):
    intensity = energy_to_intensity(energy, mood)
 
    weather_note = "Outdoor workout is a good option today."
    if not weather["good_for_outdoor"]:
        weather_note = "Weather is not ideal, switching to indoor-friendly intensity."
        if intensity == "high":
            intensity = "medium"
 
    if intensity == "low":
        sets, reps = 2, "10-12"
    elif intensity == "medium":
        sets, reps = 3, "12-15"
    else:
        sets, reps = 4, "12-15"
 
    plan = []
    for ex in exercises:
        plan.append(
            {
                "name": ex["name"],
                "prescription": f"{sets} sets x {reps} reps",
                "note": ex["note"],
            }
        )
 
    return intensity, weather_note, plan
 
 
@app.route("/")
def home():
    return render_template("home.html")
 
 
@app.route("/plan", methods=["POST"])
def plan():
    mood = request.form.get("mood", "happy")
    energy = int(request.form.get("energy", 5))
    goal = request.form.get("goal", "strength")
    city = request.form.get("city", "Wellesley, MA")
 
    weather = get_weather(city)
    exercises = fetch_exercises(goal)
    intensity, weather_note, daily_plan = build_plan(mood, energy, goal, weather, exercises)
 
    return render_template(
        "plan.html",
        mood=mood,
        energy=energy,
        goal=goal,
        city=city,
        weather=weather,
        intensity=intensity,
        weather_note=weather_note,
        plan=daily_plan,
    )
 
 
if __name__ == "__main__":
    app.run(debug=True)