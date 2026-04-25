## Date: April 21, 2026 

**What I asked AI to do:**
- Generate a simple flask app that will provide a workout. 

**What I didn't understand in the generated code:**
- I understood majority of the code and knew what would be brought on the screen, I didnt just didn't understand why 'html.append' to add a new item was there when it only gave one workout. 

**What I learned:**
- I learned that 'html.append()' is used to build the webpage step by step, even if it seems like only one workout is being shown. Using 'append()' allows the code to dynamically add content instead of writing everything as one long string.

## Date: April 24, 2026 

**What I asked AI to do:**
- Generate a simple Flask web app that creates a workout plan based on the user’s mood, energy level, and fitness goal.

**What I didn't understand in the AI generated code:"** 
- I also didn’t understand the {% for item in plan %} part in the HTML because it looked different from regular Python.

**What I learned:** 
- request.form.get() takes the information the user typed or selected in the HTML form and lets Python use it.
- The workout is chosen from a dictionary based on the user’s goal and energy level.
- The HTML can use variables from Python, like {{ mood }} and {{ level }}, to show the results on the page.
- The {% for item in plan %} loop goes through each exercise and displays it on the webpage.
