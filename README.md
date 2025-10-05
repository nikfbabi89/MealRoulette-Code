import json
import random
import os

DATA_FILE = "meals.json"

def load_meals():
    """Load meals and their freeze status from JSON file."""
    if not os.path.exists(DATA_FILE):
        default_meals = [
            {"name": "Tacos", "frozen": False},
            {"name": "Salmon + Rice", "frozen": False},
            {"name": "Pasta Primavera", "frozen": False},
            {"name": "Veggie Omelette", "frozen": False}
        ]
        save_meals(default_meals)
        return default_meals
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_meals(meals):
    """Save the meals list (with freeze status) to JSON."""
    with open(DATA_FILE, "w") as f:
        json.dump(meals, f, indent=2)

def spin_meal(meals):
    """Return a random unfrozen meal."""
    unfrozen_meals = [m["name"] for m in meals if not m["frozen"]]
    if not unfrozen_meals:
        return "No available meals to spin. All are frozen!"
    return f"Your meal is: {random.choice(unfrozen_meals)}"

def add_meal(meals):
    """Add a new meal to the list."""
    new_meal = input("Enter a new meal to add: ").strip()
    if new_meal:
        meals.append({"name": new_meal, "frozen": False})
        save_meals(meals)
        print(f"Added '{new_meal}' successfully!")
    else:
        print("No meal entered.")

def toggle_freeze(meals):
    """Freeze or unfreeze a meal."""
    print("\nMeals:")
    for i, meal in enumerate(meals, 1):
        status = "❄️ Frozen" if meal["frozen"] else "🔥 Active"
        print(f"{i}. {meal['name']} - {status}")
    try:
        choice = int(input("\nSelect a meal number to toggle freeze: "))
        if 1 <= choice <= len(meals):
            meals[choice - 1]["frozen"] = not meals[choice - 1]["frozen"]
            save_meals(meals)
            state = "frozen" if meals[choice - 1]["frozen"] else "unfrozen"
            print(f"{meals[choice - 1]['name']} is now {state}.")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Please enter a valid number.")

if __name__ == "__main__":
    meals = load_meals()

    print("\n🍽️ Welcome to Meal Roulette!")
    print("1. Spin for a meal")
    print("2. Add a meal")
    print("3. Freeze/unfreeze a meal")

    choice = input("Choose an option (1–3): ").strip()

    if choice == "1":
        print(spin_meal(meals))
    elif choice == "2":
        add_meal(meals)
    elif choice == "3":
        toggle_freeze(meals)
    else:
        print("Invalid choice.")

