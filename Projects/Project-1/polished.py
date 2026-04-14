import datetime

# Global variables to track state
daily_goal = 0.0
consumed_today = 0.0
last_reset_date = datetime.date.today()

def calculate_daily_goal(weight, exercise_hours):
    """Calculate daily water goal in ounces: 0.5 oz per pound + 8 oz per hour of exercise"""
    base_goal = weight * 0.5
    exercise_bonus = exercise_hours * 8
    return base_goal + exercise_bonus

def set_daily_goal():
    """Set the daily water goal by asking for weight and exercise"""
    global daily_goal, consumed_today, last_reset_date

    # Check if it's a new day and reset if needed
    today = datetime.date.today()
    if today != last_reset_date:
        consumed_today = 0.0
        last_reset_date = today
        print("New day detected! Resetting consumption to 0.")

    try:
        weight = float(input("Enter your body weight in pounds: "))
        if weight <= 0:
            print("Weight must be positive.")
            return

        exercise_hours = float(input("Enter hours of exercise today: "))
        if exercise_hours < 0:
            print("Exercise hours cannot be negative.")
            return

        daily_goal = calculate_daily_goal(weight, exercise_hours)
        print(f"Your daily water goal is {daily_goal:.1f} ounces.")
    except ValueError:
        print("Please enter valid numbers.")

def add_water():
    """Add water consumption"""
    global consumed_today

    try:
        amount = float(input("Enter amount of water consumed in ounces: "))
        if amount <= 0:
            print("Amount must be positive.")
            return

        consumed_today += amount
        print(f"Added {amount:.1f} ounces. Total consumed: {consumed_today:.1f} ounces.")

        if daily_goal and consumed_today >= daily_goal:
            print("Congratulations! You've reached your daily water goal!")
    except ValueError:
        print("Please enter a valid number.")


def quick_add_water():
    """Quickly add a default water amount"""
    global consumed_today
    amount = 8.0
    consumed_today += amount
    print(f"Quick add: {amount:.1f} ounces. Total consumed: {consumed_today:.1f} ounces.")

    if daily_goal and consumed_today >= daily_goal:
        print("Congratulations! You've reached your daily water goal!")


def view_progress():
    """Show current progress"""
    if daily_goal == 0:
        print("Please set your daily goal first.")
        return

    remaining = max(0, daily_goal - consumed_today)
    print(f"Goal: {daily_goal:.1f} ounces")
    print(f"Consumed: {consumed_today:.1f} ounces")
    print(f"Remaining: {remaining:.1f} ounces")

    if consumed_today >= daily_goal:
        print("Goal achieved!")
    else:
        progress_percent = (consumed_today / daily_goal) * 100
        print(f"Progress: {progress_percent:.1f}%")

def reset_day():
    """Manually reset for new day"""
    global consumed_today, last_reset_date
    consumed_today = 0.0
    last_reset_date = datetime.date.today()
    print("Reset for new day. Consumption set to 0.")

def main():
    """Main menu loop"""
    while True:
        print("\n--- Water Intake Tracker ---")
        print("1. Set Daily Goal")
        print("2. Add Water Consumed")
        print("3. Quick Add 8 oz")
        print("4. View Progress")
        print("5. Reset for New Day")
        print("6. Exit")

        choice = input("Choose an option (1-6): ").strip()

        if choice == '1':
            set_daily_goal()
        elif choice == '2':
            add_water()
        elif choice == '3':
            quick_add_water()
        elif choice == '4':
            view_progress()
        elif choice == '5':
            reset_day()
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1-6.")

if __name__ == "__main__":
    main()