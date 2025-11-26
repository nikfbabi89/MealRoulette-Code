#MealFrameClass and FilterFrameClass are both held in seperate .py files for modularity.

class Meal:
    def __init__(self, Name, PrepTime, Type, Ingredients, CustomFilters, Status):
        self.Name = Name
        self.PrepTime = PrepTime
        self.Type = Type #Type and CustomFIlters can basicly be the same thing. Mix em both together and only check one list for all those ID's.
        self.Ingredients = Ingredients
        self.CustomFilters = CustomFilters
        self.Status = Status

    def __repr__(self):
        return f"{self.Name} ({'/'.join(self.Type)}, {self.PrepTime} Mins)"

    def TellMeEverything(self):
        print(f'{self.Name},\n {self.PrepTime},\n {self.Type},\n {self.Ingredients},\n {self.CustomFilters}')


'''
Load Meal Classes. If I load meal classes here instead of the driver, I can utilize this module to give me all the classes and their info.
Because originally the randomization function looked through the json data directly instead of utilizing these classes that I completely forgot about...
Albiet the only reason I remember these is that I want to print the output easier.
'''
# ----- Load JSON into Classes -----
import json

with open('MealData.json', 'r') as File:
    Data = json.load(File)

#Data = json.loads(MealData.JsonData)
User = None #UserConfig(Data["UserConfig"]["Username"]) #Ehh, I dont need it now anyways.
Meals = [Meal(X["Name"], X["PrepTime"], X["Type"], X["Ingredients"], X["CustomFilters"], True) for X in Data["Meals"]]
                                                                                        #It's going to be true by default.





'''

class UserConfig:
    def __init__(self, Username):
        self.Username = Username


class MealRoulette:
    def __init__(self, Meals):
        self.Meals = Meals

    # Spin Method 
    def Spin(self, WhiteList=None, BlackList=None, MaxPrepTime=None, Debug=False):
        WhiteList = WhiteList or []
        BlackList = BlackList or []

        Filtered = []
        if Debug:
            print("---- Filtering Debug ----")
        for Meal in self.Meals:
            Reasons = []
            Passed = []

            # Whitelist
            if WhiteList and any(W in Meal.Type for W in WhiteList):
                Passed.append(f"Passed WhiteList ({WhiteList})")
            elif WhiteList:
                Reasons.append(f"Not in WhiteList ({WhiteList})")

            # Blacklist
            if all(B not in Meal.Type and B not in Meal.CustomFilters for B in BlackList):
                Passed.append(f"Passed BlackList ({BlackList})")
            elif BlackList:
                Reasons.append(f"In BlackList ({BlackList})")

            # MaxPrepTime
            if MaxPrepTime is None or Meal.PrepTime <= MaxPrepTime:
                Passed.append(f"Passed MaxPrepTime ({MaxPrepTime})")
            elif MaxPrepTime is not None:
                Reasons.append(f"PrepTime {Meal.PrepTime} > MaxPrepTime {MaxPrepTime}")

            # Decide inclusion
            if not Reasons:
                Filtered.append(Meal)
                if Debug:
                    print(f"Included: {Meal} -> {', '.join(Passed)}")
            elif Debug:
                print(f"Excluded: {Meal} -> {', '.join(Reasons)}")

        if Debug:
            print("------------------------")

        if not Filtered:
            if Debug:
                print("No Meals Available After Filtering.")
            return None

        Choice = random.choice(Filtered)
        print(f" Selected Meal: {Choice}")
        return Choice

''' #Nahh, I dont need this right now.
'''
# ----- Testing -----
print(f"User: {User.Username}")

# Spin with debug
Roulette.Spin(WhiteList=["Lunch"], BlackList=["Grill", "Turkey", "Dinner"], MaxPrepTime=20, Debug=True)

print("---- Debug Off ---")

# Spin without debug
Roulette.Spin(
    WhiteList=["Lunch"], 
    BlackList=["Grill", "Turkey", "Dinner"], 
    MaxPrepTime=20
)


#Spin a bunch of times without debug (test randomizer)
for i in range(10):
    Roulette.Spin(
    WhiteList=["Lunch"], 
    BlackList=["Grill", "Turkey", "Dinner"], 
    MaxPrepTime=20
)
'''
