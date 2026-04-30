import os
import random
import requests
from flask import Flask, request, render_template
from dotenv import load_dotenv

# Load .env from the same directory as this file (not current working directory)
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
load_dotenv(env_path)

app = Flask(__name__)

# Debug: Print API key status on startup
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
API_NINJAS_KEY = os.getenv("API_NINJAS_KEY", "")

print(f"=== API Keys Loaded ===")
print(f"OPENWEATHER_API_KEY: {'SET' if OPENWEATHER_API_KEY else 'MISSING'}")
print(f"API_NINJAS_KEY: {'SET' if API_NINJAS_KEY else 'MISSING'}")
print(f"env_path: {env_path}")
print(f"========================")
 
FALLBACK_EXERCISES = {
    "strength": [
        {"name": "Push-ups", "note": "Upper body strength", "difficulty": "medium", "tags": ["bodyweight", "strength"]},
        {"name": "Bodyweight Squats", "note": "Leg and glute strength", "difficulty": "medium", "tags": ["bodyweight", "strength", "lower body"]},
        {"name": "Plank", "note": "Core stability", "difficulty": "low", "tags": ["bodyweight", "strength", "core"]},
        {"name": "Lunges", "note": "Balance and lower body strength", "difficulty": "medium", "tags": ["bodyweight", "strength", "lower body"]},
        {"name": "Dumbbell Rows", "note": "Back and arm strength", "difficulty": "high", "tags": ["dumbbells", "strength", "back"]},
        {"name": "Overhead Press", "note": "Shoulder strength", "difficulty": "high", "tags": ["dumbbells", "strength", "shoulders"]},
    ],
    "fat loss": [
        {"name": "Jumping Jacks", "note": "Light cardio warm-up", "difficulty": "low", "tags": ["cardio", "fat loss"]},
        {"name": "Mountain Climbers", "note": "Full-body cardio", "difficulty": "medium", "tags": ["cardio", "fat loss", "core"]},
        {"name": "High Knees", "note": "Boost heart rate", "difficulty": "medium", "tags": ["cardio", "fat loss", "legs"]},
        {"name": "Burpees", "note": "High intensity conditioning", "difficulty": "high", "tags": ["cardio", "fat loss", "full body"]},
        {"name": "Jump Rope", "note": "Quick fat-burning cardio", "difficulty": "medium", "tags": ["cardio", "fat loss"]},
    ],
    "mobility": [
        {"name": "Cat-Cow", "note": "Spine mobility", "difficulty": "low", "tags": ["yoga", "mobility"]},
        {"name": "Hip Flexor Stretch", "note": "Lower body flexibility", "difficulty": "low", "tags": ["yoga", "flexibility"]},
        {"name": "Thoracic Rotations", "note": "Upper back mobility", "difficulty": "low", "tags": ["yoga", "mobility"]},
        {"name": "Child's Pose", "note": "Recovery and breathing", "difficulty": "low", "tags": ["yoga", "mobility"]},
        {"name": "World's Greatest Stretch", "note": "Full-body mobility", "difficulty": "medium", "tags": ["yoga", "mobility", "flexibility"]},
    ],
    "endurance": [
        {"name": "Jogging in Place", "note": "Build aerobic endurance", "difficulty": "low", "tags": ["cardio", "endurance"]},
        {"name": "Stationary Bike", "note": "Steady-state cardio", "difficulty": "medium", "tags": ["cardio", "endurance"]},
        {"name": "Jumping Lunges", "note": "Endurance and leg power", "difficulty": "high", "tags": ["cardio", "endurance", "legs"]},
        {"name": "Burpee Broad Jump", "note": "High intensity endurance", "difficulty": "high", "tags": ["cardio", "endurance"]},
        {"name": "Step-Ups", "note": "Leg endurance and coordination", "difficulty": "medium", "tags": ["bodyweight", "endurance"]},
    ],
    "flexibility": [
        {"name": "Seated Forward Fold", "note": "Hamstring flexibility", "difficulty": "low", "tags": ["yoga", "flexibility"]},
        {"name": "Standing Quad Stretch", "note": "Front leg stretch", "difficulty": "low", "tags": ["yoga", "flexibility"]},
        {"name": "Shoulder Stretch", "note": "Upper body mobility", "difficulty": "low", "tags": ["yoga", "flexibility"]},
        {"name": "Pigeon Pose", "note": "Hip flexibility", "difficulty": "medium", "tags": ["yoga", "flexibility"]},
    ],
    "balance": [
        {"name": "Single-Leg Stand", "note": "Improve balance", "difficulty": "low", "tags": ["balance", "core"]},
        {"name": "Heel-to-Toe Walk", "note": "Stability and coordination", "difficulty": "low", "tags": ["balance"]},
        {"name": "Single-Leg Deadlift", "note": "Balance with strength", "difficulty": "medium", "tags": ["balance", "legs", "dumbbells"]},
        {"name": "Bosu Ball Squats", "note": "Unstable surface training", "difficulty": "medium", "tags": ["balance", "strength"]},
    ],
}
 
STYLE_TAGS = {
    "bodyweight": ["bodyweight", "strength", "full body"],
    "dumbbells": ["dumbbells", "strength", "upper body", "lower body"],
    "cardio": ["cardio", "fat loss", "endurance"],
    "yoga": ["yoga", "mobility", "flexibility", "balance"],
    "equipment": ["dumbbells", "cardio", "strength", "endurance"],
    "any": [],
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
 
 
def normalize_level(level):
    if level == "beginner":
        return "low"
    if level == "intermediate":
        return "medium"
    if level == "advanced":
        return "high"
    return None


def select_fallback_exercises(goal, style, difficulty, count):
    candidates = FALLBACK_EXERCISES.get(goal, [])[:]
    style_tags = STYLE_TAGS.get(style, [])

    if style_tags:
        style_filtered = [item for item in candidates if any(tag in item["tags"] for tag in style_tags)]
        if style_filtered:
            candidates = style_filtered

    if difficulty:
        difficulty_filtered = [item for item in candidates if item["difficulty"] == difficulty]
        if len(difficulty_filtered) >= count:
            candidates = difficulty_filtered
        elif difficulty_filtered:
            candidates = difficulty_filtered + [item for item in candidates if item not in difficulty_filtered]

    if not candidates:
        candidates = [item for items in FALLBACK_EXERCISES.values() for item in items]

    return random.sample(candidates, k=min(count, len(candidates)))


def fetch_exercises(goal, muscle=None, style="any", difficulty=None, count=4):
    print(f"=== fetch_exercises called with goal: {goal}, muscle: {muscle}, style: {style}, difficulty: {difficulty}, count: {count} ===")
    print(f"API_NINJAS_KEY present: {bool(API_NINJAS_KEY)}")
    
    muscle_mapping = {
        "chest": "chest",
        "back": "lats",
        "arms": "biceps",
        "legs": "quadriceps",
        "shoulders": "shoulders",
        "core": "abdominals",
        "full_body": None,
    }
    
    goal_to_muscle = {
        "strength": "chest",
        "fat loss": "abdominals",
        "mobility": "lower_back",
        "endurance": "quadriceps",
        "flexibility": "hamstrings",
        "balance": "core",
    }
    
    if muscle and muscle != "full_body":
        api_muscle = muscle_mapping.get(muscle, "chest")
    else:
        api_muscle = goal_to_muscle.get(goal, "chest")
    
    print(f"Using API muscle: {api_muscle}")
 
    if not API_NINJAS_KEY:
        print("Using fallback exercises (no API key)")
        return select_fallback_exercises(goal, style, difficulty, count)

    try:
        url = "https://api.api-ninjas.com/v1/exercises"
        headers = {"X-Api-Key": API_NINJAS_KEY}
        params = {"muscle": api_muscle} if api_muscle else {}
        print(f"Calling Ninjas API with params: {params}")
        r = requests.get(url, headers=headers, params=params, timeout=8)
        r.raise_for_status()
        data = r.json()
 
        if not data:
            print("Ninjas API returned empty, using fallback")
            return select_fallback_exercises(goal, style, difficulty, count)
 
        cleaned = []
        for item in data[:20]:
            cleaned.append(
                {
                    "name": item.get("name", "Unknown exercise").title(),
                    "note": f"Difficulty: {item.get('difficulty', 'unknown')} | {item.get('type', 'general').title()}",
                    "difficulty": item.get('difficulty', 'medium'),
                }
            )
 
        exact = [item for item in cleaned if item["difficulty"] == difficulty] if difficulty else cleaned
        if len(exact) >= count:
            return random.sample(exact, k=count)
 
        if len(cleaned) >= count:
            return random.sample(cleaned, k=count)
 
        print("API returned too few exercises, using fallback")
        return select_fallback_exercises(goal, style, difficulty, count)
    except Exception as e:
        print(f"Ninjas API error: {e}")
        return select_fallback_exercises(goal, style, difficulty, count)
 
 
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
    muscle = request.form.get("muscle", "chest")
    level = request.form.get("level", "auto")
    workout_type = request.form.get("workout_type", "any")
    amount = int(request.form.get("amount", 4))
    amount = max(1, min(amount, 8))
    city = request.form.get("city", "Boston, MA")
    
    print(f"=== PLAN ROUTE ===")
    print(f"city: {city}")
    print(f"OPENWEATHER_API_KEY in plan(): {repr(OPENWEATHER_API_KEY)}")
    
    weather = get_weather(city)
    print(f"Weather result in plan(): {weather}")

    desired_difficulty = normalize_level(level)
    exercises = fetch_exercises(goal, muscle, workout_type, desired_difficulty, amount)
    intensity, weather_note, daily_plan = build_plan(mood, energy, goal, weather, exercises)
 
    return render_template(
        "plan.html",
        mood=mood,
        energy=energy,
        goal=goal,
        muscle=muscle,
        level=level,
        workout_type=workout_type,
        amount=amount,
        city=city,
        weather=weather,
        intensity=intensity,
        weather_note=weather_note,
        plan=daily_plan,
    )
 
 
if __name__ == "__main__":
    app.run(debug=True)