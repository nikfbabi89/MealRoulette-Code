import random
import Classes
import tkinter as tk #Literally only for checking if an instance is a listbox or text widget.
import tkinter.font as tkfont
import ColorPresets as Col

'''
11/25/25:
Moved all function descriptions to just above the function for easier readability.

May need to splice Grab Selection into fine bits for ease of feature creation.
'''


'''GrabSelection(), Used primarily with binding listboxes, the function accepts a display for output and a bool for removing the item from the list or not when triggered. It additionally has different cases for whether you are outputing to a listbox or text widget.'''
def GrabSelection(event, Display=None, Refresh=False, Insert=False): 
    #Origianlly meant for putting stuff into a text widget, but evolved to allow removal or sharing listbox entries.
    List = event.widget
    Result = NameOfSelect(List)
    if not Result:
        return #Because just ignore it if there is no valid selection.
    Name, Index = Result
    print(Result, Name, Index)

    Message = SearchAndFormatTheChosen(Name)
    
    InsertTextDisplay(Display, Message, Refresh, Insert)

    if isinstance(Display, tk.Listbox): #Specifically only for adding meal items to another listbox on selection.
        if Insert:
            Display.insert('end', Name)
        if Refresh: #Piggyback off the refresh boolean to check if I want to remove the selection. Which by default will happen.
            List.delete(Index)
            print('Deleted Index From List')



'''InsertTextDisplay() inserts text into the passed text display. Also safe to put in without other precautions as it checks and handles if it's not a text widget. Serving as a check.'''
def InsertTextDisplay(Display, Message, Refresh=False, Insert=False):
    if isinstance(Display, tk.Text): #For sending text from a selected listbox to a text widget.
        Display.config(state='normal')
        if Refresh:
            Display.delete('1.0', tk.END) #Clear Display.
        if Insert:
            Display.insert('end', Message)
        Display.config(state='disabled')
    else:
        print('This is not a tkinter text widget.')


'''DisplayMeal(), Displays Meal Data To A Text Display.'''
def DisplayMeal(Listbox, Display):
    Name, Index = NameOfSelect(Listbox)
    Message = SearchAndFormatTheChosen(Name)

    InsertTextDisplay(Display, Message)

'''NameOfSelect(), Used primarily in other functions due to the need for the same code multiple times. The function will obtain the name of the item selected in the listbox passed to it.'''
def NameOfSelect(Listbox): #Obtain the name of the selected listbox entry.
    Selection = Listbox.curselection()
    if Selection:
        Index = Selection[0]
        Name = Listbox.get(Index)
        return Name, Index


'''ButtonToList(), Used when making the whitelist and blacklist, tied to the command of a button press. The function will use the selected items name from the "Giver" listbox and put that name into the "Reciever" listbox.'''
def ButtonToList(Giver, Reciever): #For adding items selected from listbox's to other listboxes from button clicks rather than events. Made for filter logic.
    Name, Index = NameOfSelect(Giver) #The index is given, but not used in this function.
    if Name in ListListbox(Reciever):
        return
    Reciever.insert('end', Name)


'''ListListbox(), Used to obtain a list of the items occupying the listbox passed to it, it additionally has a boolean for deciding whether the list will have dupelicate items.'''
def ListListbox(Listbox, Dupes=False): #Return a list of all the entries of the passed listbox.
    Entries = list(Listbox.get(0, tk.END))

    if not Dupes: #If you dont want duplicates.
        Entries = list(set(Entries))
        
    return Entries


'''FindMealAmongClasses(), When given a meals name, it will search the classes for a meal with the same name. It will return that meal, otherwise returning None.'''
def FindMealAmongClasses(MealName):
    FoundMeal = next((meal for meal in Classes.Meals if meal.Name == MealName), None)
    return FoundMeal


'''SearchAndFormatTheChosen(), A function to simply grab a meal from the classes and format its information to be put out into a display, which in most cases consist of text widgets. It does not automatically send it to a display, it only returns a string which is formated for display.'''
def SearchAndFormatTheChosen(Selection): 
    #Made haphazardly in 5 minutes because I needed to use the same formatting twice, this function shall take the name of the variable passed, and search for       it in the list of meal classes. Then it shall format it for the display widget I made, then return the formated entry for insertion. Could also be printed.
    TheChosenOne = FindMealAmongClasses(Selection)

    if TheChosenOne:
        TheChosenOne = f"""\n
        {TheChosenOne.Name}
        {TheChosenOne.PrepTime} Minutes To Cook.
        Ingredients: {TheChosenOne.Ingredients}
        Id's{TheChosenOne.Type} {TheChosenOne.CustomFilters}\n"""
    else:
        print('Somthing went wrong when finding the chosen one. FunctionsOfTheGUI.py')

    return TheChosenOne


'''RandomMeal(), Requiring to be passed a List, Display, Whitelistbox, Blacklistbox. it grabs the items from the listboxes to become whitelists and blacklists, sending those through the filter function to then filter out all the unwanted items from a list which is returned from the filter function. It then obtains a random number based of that filtered lists length and uses SearchAndFormatTheChosen to format it and send it out to the passed display.'''
def RandomMeal(List, Display, Whitelistbox, Blacklistbox): #Cant have the same name as the button.
    Whitelist = ListListbox(Whitelistbox, False)
    Blacklist = ListListbox(Blacklistbox, False)
    print('Whitelist:', Whitelist) #Debugging
    print('Blacklist:', Blacklist) #Debugging
    Accepted = Filter(Whitelist, Blacklist)
    print('Accepted:', Accepted) #Debugging
    
    Display.config(state='normal') #Allow edits to the display.
    Display.delete('1.0', tk.END) #Clear display before jamming more junk in.
    ListLength = len(Accepted)
    print(ListLength)
    if not ListLength:
        Display.insert('end', 'No Meals After Filtering')
    else:
        RandomNumber = random.randint(0,ListLength-1) #Random Number. Zero indexed, so we make it one less then max to account for 0.
        Selection = Accepted[RandomNumber] #<-- Woah Look, Its The Meals Name.
        Display.insert('end', f'{SearchAndFormatTheChosen(Selection)}')
        
    Display.config(state='disabled') #Disallow further edits to the display.



'''Filter(), Cretes a new list of the meals, filtered from the passed whitelist and blacklist. It returns that list for further use.'''
def Filter(Whitelist, Blacklist):
    Accepted = []

    if not Whitelist and not Blacklist:
        print('No filters, all added except for frozen meals')
        return [meal.Name for meal in Classes.Meals if meal.Status] #If neither list is populated, give it all meals. Of course all that are active.
    
    for meal in Classes.Meals:
        Ids = meal.Type + meal.Ingredients + meal.CustomFilters

        if not meal.Status:
            print('Meal: ', meal, '\n', 'Status: ', meal.Status)
            continue #Skip to the next iteration if the meal is not active.
        
        #Chack all the Ids against the filters.
        if any(Id in Blacklist for Id in Ids):
            print('Removed Item From Acceptability')
            continue #In the blacklist? skip to the next iteration.

        if not Whitelist: #Because if there is no ids in the whitelist it will overlook the whitelist completely and just not add anything to the list.
            Accepted.append(meal.Name)
            continue

        if any(Id in Whitelist for Id in Ids):
            Accepted.append(meal.Name) #appending only meal name.
            
    print('Accepted:', Accepted)
    return Accepted
        
    

'''Freeze(), Primarily bound to listboxes. Used to freeze meals by using right click rather than left click.'''
def Freeze(event): #I dont like eating frozen meals either...
    Listbox = event.widget #It seems to just get the widget that triggered the event it seems.
    
    Index = Listbox.nearest(event.y) #Because the coed decided not to work now for some reason, I need to make it select the nearest item on right click.
    Listbox.selection_clear(0, 'end')
    Listbox.selection_set(Index)
    
    Result = NameOfSelect(Listbox)
    print(Result)
    Name, ItemIndex = Result
    Meal = FindMealAmongClasses(Name)
    
    Meal.Status = not Meal.Status #Simple Toggle.

    if Meal.Status:
        Listbox.itemconfig(Index, fg='black')
    else:
        Listbox.itemconfig(Index, fg=Col.FT)
        
    #print(Meal.Status, 'Meal Status -------')


""" ClearListBox() deletes all items in the listbox, leaving it empty. Used primarily to refresh listboxes when resetting."""
def ClearListbox(Listbox):
    Listbox.delete(0, tk.END)


'''ResetMealList(), Resets the MealList and SelectedMeals listboxes from MealFrameClass.py to satisfy a request for a reset button'''
def ResetMealList(MealList, SelectedMeals): #Basically one function to call both of these at the same time so the button works.
    ClearListbox(SelectedMeals)
    InnitMealList(MealList, Classes.Meals)

'''InnitMealList(), Passed a listbox and the list of meal classes, it is called at the begginging of the GUI to display the names of meals into the listbox for selection.'''
def InnitMealList(Listbox, Meals):
    Listbox.delete(0, tk.END) #You know what, lets just refresh the list entirely so that we can call this however many times we want.
    for i in Meals:
        if not i.Status: #If the meal is frozen, keep it white.
            Listbox.insert(0, i.Name) #Getting the index is too hard, just set it to 0...
            Listbox.itemconfig(0, fg=Col.FT)
        else: #Not frozen? Hjuck it in.
            Listbox.insert('end', i.Name) #List its name to the listbox.
        


'''InnitFiltersList(), Passed a listbox to output to, it runs through the ingredients and types of every meal class in the json and groups them into a list called Id's. It then lists each of the Id's into a list for later filtering.'''
def InnitFiltersList(Listbox):
    Ids = [] #Initialize as empty.
    for meal in Classes.Meals:
        for type in meal.Type:
            Ids.append(type)
        
        for filter in meal.CustomFilters:
            Ids.append(filter) #Append the type and filters.

    Ids = list(set(Ids))
    
    for id in Ids:
        Listbox.insert('end', id) #Throw them in a list box because a checkbox menu button was too complicated.


