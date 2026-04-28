import os
import random
import requests
from flask import Flask, request, render_template
from dotenv import load_dotenv

# Load .env from the same directory as this file
load_dotenv('.env')

app = Flask(__name__)
 
WORKOUT_DB = {
    "strength": {
        "low": ["Wall Push-ups", "Bodyweight Squats", "Glute Bridges", "Dead Bug"],
        "medium": ["Push-ups", "Squats", "Lunges", "Plank Shoulder Taps"],
        "high": ["Decline Push-ups", "Jump Squats", "Burpees", "Mountain Climbers"],
    },
    "fat loss": {
        "low": ["March in Place", "Step Touch", "Bodyweight Squats", "Knee Plank"],
        "medium": ["Jumping Jacks", "High Knees", "Lunges", "Plank"],
        "high": ["Burpees", "Jump Squats", "Mountain Climbers", "Skater Jumps"],
    },
    "mobility": {
        "low": ["Cat-Cow", "Child's Pose", "Hip Openers", "Shoulder Rolls"],
        "medium": ["World's Greatest Stretch", "Lunge Stretch", "Thoracic Rotations", "Downward Dog"],
        "high": ["Dynamic Leg Swings", "Inchworm Walkouts", "Cossack Squats", "Deep Squat Hold"],
    },
}
 
 
def energy_to_level(energy):
    if energy <= 3:
        return "low"
    elif energy <= 7:
        return "medium"
    return "high"
 
 
def generate_workout(mood, energy, goal):
    level = energy_to_level(energy)
 
    if mood == "tired":
        level = "low"
    elif mood == "stressed" and level == "high":
        level = "medium"
    elif mood == "motivated" and level == "low":
        level = "medium"
 
    choices = WORKOUT_DB[goal][level]
    selected = random.sample(choices, k=min(3, len(choices)))
 
    if level == "low":
        sets, reps = 2, "10"
    elif level == "medium":
        sets, reps = 3, "12"
    else:
        sets, reps = 4, "12"
 
    plan = [{"name": ex, "sets": sets, "reps": reps} for ex in selected]
    return level, plan
 
 
@app.route("/")
def home():
    return render_template("home.html")
 
 
@app.route("/plan", methods=["POST"])
def plan():
    mood = request.form.get("mood", "happy")
    energy = int(request.form.get("energy", 5))
    goal = request.form.get("goal", "strength")
 
    level, workout_plan = generate_workout(mood, energy, goal)
 
    return render_template(
        "plan.html",
        mood=mood,
        energy=energy,
        goal=goal,
        level=level,
        plan=workout_plan,
    )
 
 
if __name__ == "__main__":
    app.run(debug=True)