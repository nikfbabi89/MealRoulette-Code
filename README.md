# MealRoulette-Code
import random

# Simple data storage for StudyLoop
feed = []

# -------------------------
# Meal Roulette
# -------------------------
def meal_roulette():
    meals = ["Pizza", "Pasta", "Burrito", "Salad", "Sushi"]
    choice = random.choice(meals)
    print(f"\n🍽️ Today’s meal is: {choice}")


# Main Menu
def main():
    while True:
        print("\n--- MVP Menu ---")
        print("1. Spin Meal Roulette")
        print("2. Post a Study Problem")
        print("3. Reply to a Problem")
        print("4. Show Study Feed")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            meal_roulette()
        elif choice == "2":
            problem = input("Enter your problem: ")
            post_problem(problem)
        elif choice == "3":
            display_feed()
            try:
                index = int(input("Which problem number to reply to? ")) - 1
                reply = input("Enter your reply: ")
                reply_to_problem(index, reply)
            except ValueError:
                print("⚠️ Invalid input. Please enter a number.")
        elif choice == "4":
            display_feed()
        elif choice == "5":
            print("👋 Goodbye!")
            break
        else:
            print("⚠️ Invalid choice.")

if __name__ == "__main__":
    main()
