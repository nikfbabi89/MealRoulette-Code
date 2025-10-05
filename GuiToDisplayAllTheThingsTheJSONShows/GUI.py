import tkinter as tk
from tkinter import ttk
from tkinter import Checkbutton, font
import ColorPresets as Col
import FunctionsOfTheGUI as Fotgui

Window = tk.Tk()
Window.title('Meal Roulette')
Window.state('zoomed')  # Convenient to not have to manually fullscreen the window.
Window.config(bg=Col.BG)

'''
Frames and tabs
'''
Style = ttk.Style()
Style.theme_use('alt') #Changes the look of the tabs bar, your choices are 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative'
    
Tabs = ttk.Notebook(Window)
Tabs.pack(expand=True, fill='both')
    
#Behold, My Seperate Screens!
MealScreen = tk.Frame(Window, bg=Col.BG)
FilterScreen = tk.Frame(Window, bg=Col.BG) #Screen got too packed, moved filtering to another tab.

Tabs.add(MealScreen, text='Meals')
Tabs.add(FilterScreen, text='Filters')

'''
Widgets
'''
Display = tk.Text(MealScreen, bg=Col.TWB, font=Col.Dfu)
Display.place(x=800, y=5)
Display.config(state='disabled')

Labels = tk.Label(MealScreen, bg=Col.BG, fg=Col.TB, text='  Meals List\t        Selected Meals', font=('Arial', 20, 'bold'))
Labels.place(x=10, y=650)

SelectedMeals = tk.Listbox(MealScreen, width=40, height=40, bg=Col.TWB, font=Col.Dfu)
SelectedMeals.place(x=300, y=5)
SelectedMeals.bind('<ButtonRelease-1>', lambda event: Fotgui.GrabSelection(event, SelectedMeals, True))

MealList = tk.Listbox(MealScreen, width=40, height=40, bg=Col.TWB, font=Col.Dfu)  #List lower than display so that the binding works when display.
MealList.place(x=5, y=5)
MealList.bind('<ButtonRelease-1>', lambda event: Fotgui.GrabSelection(event, SelectedMeals, False))# I must be playing Silksong, because I need to bind.
MealList.bind('<ButtonRelease-1>', lambda event: Fotgui.GrabSelection(event, Display, False), add='+') #A second binding to use grab selection twice.
# On another note, I use ButtonRelease-1 instead of ListboxSelect because listbox select only updates on changing the selection rather than 
# ButtonRelease-1, which works more like a button when triggered. Though if you click on empty space at the bottom of the list box, it will choose the 
# last index.

Randomize = tk.Button(MealScreen, text='Randomize', width=80, bg=Col.BB, fg=Col.TB, font=Col.Dfu, command=lambda: Fotgui.RandomMeal(MealList, Display, Whitelistbox, Blacklistbox))
Randomize.place(x=800, y=400)  # Also needs to be last to be able to call the meal list widget.

'''
Filters, Whitelist, Blacklist
'''

FilterLabel = tk.Label(FilterScreen, bg=Col.BG, fg=Col.TB, font=Col.Dfu, text='Filters\t\t\t\tWhitelist\t\t\t\tBlacklist')
FilterLabel.pack(side='top', anchor='w')

a2b = tk.Button(FilterScreen, bg=Col.BB, fg=Col.TB, font=Col.Dfu, text='Add Selected To Blacklist', command=lambda: Fotgui.ButtonToList(Filters, Blacklistbox))
a2b.pack(side='bottom', fill='x')

a2w = tk.Button(FilterScreen, bg=Col.BB, fg=Col.TB, font=Col.Dfu, text='Add Selected To Whitelist', command=lambda: Fotgui.ButtonToList(Filters, Whitelistbox))
a2w.pack(side='bottom', fill='x')

Filters = tk.Listbox(FilterScreen, width=30, font=Col.Dfu)
Filters.pack(side='left', fill='y', padx=5)

Whitelistbox = tk.Listbox(FilterScreen, width=30, font=Col.Dfu)
Whitelistbox.pack(side='left', fill='y', padx=5)
Whitelistbox.bind('<ButtonRelease-1>', lambda event: Fotgui.GrabSelection(event, Whitelistbox, True))

Blacklistbox = tk.Listbox(FilterScreen, width=30, font=Col.Dfu)
Blacklistbox.pack(side='left', fill='y', padx=5)
Blacklistbox.bind('<ButtonRelease-1>', lambda event: Fotgui.GrabSelection(event, Blacklistbox, True))

Fotgui.InnitFiltersList(Filters)

    

#Window.mainloop() #Removed for functional purposes, check driver for this line of code.

''' Debug Meal Options
MealList.insert('end','Some Meal Or Somthing') #Temporary, remove on further development.
MealList.insert('end','Meal Zero') #Temporary, remove on further development.
MealList.insert('end','Meal One') #Temporary, remove on further development.
MealList.insert('end','Meal Two') #Temporary, remove on further development.
MealList.insert('end','Meal Three') #Temporary, remove on further development.
MealList.insert('end','Meal Four') #Temporary, remove on further development.
MealList.insert('end','Meal Five') #Temporary, remove on further development.
MealList.insert('end','Meal Six') #Temporary, remove on further development.
'''
