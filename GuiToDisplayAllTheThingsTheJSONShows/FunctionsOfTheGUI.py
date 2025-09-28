import random
import Classes
import tkinter as tk #Literally only for checking if an instance is a listbox or text widget.

def GrabSelection(event, Display, Removal): #Origianlly meant for putting stuff into a text widget, but evolved to allow removal or sharing listbox entries.
    List = event.widget
    Name, Index = NameOfSelect(List)
        
    if isinstance(Display, tk.Text): #For sending text from a selected listbox to a text widget.
        Display.config(state='normal')
        Display.delete('1.0', tk.END) #Clear Display.
        Display.insert('end', f'{SearchAndFormatTheChosen(Name)}')
        Display.config(state='disabled')
    elif isinstance(Display, tk.Listbox): #Specifically only for adding meal items to another listbox on selection.
        if Removal == True: #If I want to remove a selection.
            List.delete(Index)
        else: #If its meant to insert items into the listbox on selection.
            Display.insert('end', Name)


def NameOfSelect(Listbox): #Obtain the name of the selected listbox entry.
    Selection = Listbox.curselection()
    if Selection:
        Index = Selection[0]
        Name = Listbox.get(Index)
        return Name, Index



def ButtonToList(Giver, Reciever): #For adding items selected from listbox's to other listboxes from button clicks rather than events. Made for filter logic.
    Name, Index = NameOfSelect(Giver) #The index is given, but not used in this function.
    Reciever.insert('end', Name)



def ListListbox(Listbox, Dupes): #Return a list of all the entries of the passed listbox.
    Entries = list(Listbox.get(0, tk.END))

    if not Dupes: #If you dont want duplicates.
        Entries = list(set(Entries))
        
    return Entries



def SearchAndFormatTheChosen(Selection): 
    #Made haphazardly in 5 minutes because I needed to use the same formatting twice, this function shall take the name of the variable passed, and search for       it in the list of meal classes. Then it shall format it for the display widget I made, then return the formated entry for insertion. Could also be printed.
    TheChosenOne = next((meal for meal in Classes.Meals if meal.Name == Selection), None)

    if TheChosenOne:
        TheChosenOne = f"""\n
        {TheChosenOne.Name} *Randomized
        {TheChosenOne.PrepTime} Minutes To Cook.
        Ingredients: {TheChosenOne.Ingredients}
        Id's{TheChosenOne.Type} {TheChosenOne.CustomFilters}\n"""
    else:
        print('Somthing went wrong when finding the chosen one. FunctionsOfTheGUI.py')

    return TheChosenOne



def RandomMeal(List, Display, Whitelistbox, Blacklistbox): #Cant have the same name as the button.
    Whitelist = ListListbox(Whitelistbox, False)
    Blacklist = ListListbox(Blacklistbox, False)
    print(Whitelist)
    print(Blacklist)
    Accepted = Filter(Whitelist, Blacklist)
    
    Display.config(state='normal') #Allow edits to the display.
    Display.delete('1.0', tk.END) #Clear display before jamming more junk in.
    ListLength = len(Accepted)
    print(ListLength)
    if not ListLength:
        Display.insert('end', 'No Meals After Filtering')
    else:
        RandomNumber = random.randint(0,ListLength-1) #Random Number. Zero indexed, so we make it one less then max to account for 0.
        Selection = List.get(RandomNumber) #<-- Woah Look, Its The Meals Name.
        Display.insert('end', f'{SearchAndFormatTheChosen(Selection)}')
        
    Display.config(state='disabled') #Disallow further edits to the display.



def Filter(Whitelist, Blacklist):
    Accepted = []

    if not Whitelist and not Blacklist:
        return [meal.Name for meal in Classes.Meals] #If neither list is populated, give it all meals.
    
    for meal in Classes.Meals:
        Ids = meal.Type + meal.Ingredients + meal.CustomFilters
        for Id in Ids:
            if Id in Whitelist and Id not in Blacklist:
                Accepted.append(meal.Name) #appending only meal name.
                print('Removed Item From Acceptability')
                
    return Accepted



def InnitMealList(Listbox, Meals):
    for i in Meals:
        Listbox.insert('end', i.Name) #List its name to the listbox.


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


