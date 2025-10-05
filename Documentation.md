# 9/22/25
Roles are delegated to each group member

Person A: Nichole, Set up the project folder and initialize a Git repository (GitHub or GitLab). Push the base structure (main.py, requirements.txt, README.md) so the group can clone and contribute.

Person B: Allgood, Implement the first core function (Meal Roulette: random spin; StudyLoop: add_post)

Person C: Spencer, Handle displaying results/output (Meal Roulette: show chosen meal; StudyLoop: show_posts)

Person D: Vincent, Test what has been built so far, write brief documentation, and suggest improvements based on bugs or clarity issues

# 9/23/25
Allgood creates core code, this code utilizes JSON to store meal data, a few meals are created and stored into JSON.

Has a meal class so different meals can be created as objects allowing for more flexibility with food items.

Includes various filters to help catogorize different meals.

Randomizer to randomly pick a meal and includes a way to view debugging messages.

Has a whitelist and blacklisting feature that allows you to remove items from the wheel by blacklisting by checking certain types or custom filters. Whitelisting can be used to only spin a certain type of food
otherwise it will spin every meal that isn't excluded by blacklist if no whitelisting is done. The user can also set a max prep time so it will only spin meals that are within that prep time range.
# 9/24/25 - 9/27/25
Nichole creates repository and creates base structure of the program

Spencer creates gui code

# 9/28/25
Spencer pushes his gui code into the repository and Allgood pushes her core function code into the repository as well, MVP is turned in.
