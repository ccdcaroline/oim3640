## Date: 2026-03-27

**What I asked AI to do:**
- Generate a simple function that calculates how much water a person should drink daily based on their body weight. 

**What I didn't understand in the generated code:**
- Why we multiply weight by 0.5 and what that number actually represents. 

**What I learned:**
- The 0.5 multiplier is a common hydration formula — for every pound of body weight, you should drink half an ounce of water per day. 


## Date: 2026-04-4 

**What I asked AI to do:**
- Expand the program to let users input their weight and exercise hours, track how much water they've consumed, and display their progress toward their daily goal. 

**What I didn't understand in the generated code:**
- The global keyword and why it was needed inside functions like add_water() and set_daily_goal().
- How try and except ValueError worked together when accepting user input. 

**What I learned:**
- Variables defined outside of a function are global, but if you want to modify them inside a function you have to explicitly declare them with global, otherwise Python treats them as a local variable. 


## Date: 2026-04-13

**What I asked AI to do:**
- Add a full menu-driven interface with automatic day resetting, a quick-add option, manual reset functionality, and congratulations messages when the daily goal is reached.

**What I didn't understand in the generated code:**
- The if __name__ == "__main__" block at the bottom and why it's there

**What I learned:**
- datetime.date.today() returns the current calendar date, and by storing the date at last use and comparing it to today's date, the program can tell whether a new day has started and reset consumption automatically 
