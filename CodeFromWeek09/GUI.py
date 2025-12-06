'''You Will Find Literally Almost No Gui Here... Check the files FilterFrameClass.py and MealFrameClass.py for all those Gui bits, Other then that, here lies the window and tab system.'''
import tkinter as tk #Because its about GUI.
from tkinter import ttk #Used to create notebooks for tabs.

import Classes #Used to load the meals into the meal list from MealFrameClass

import FunctionsOfTheGUI as Fotgui #Used to give the GUI its functions and is the heart of functional GUI.
import MealFrameClass #The Meal Screen.
import FilterFrameClass #The Filter Screen.

Window = tk.Tk()
Window.title('Meal Roulette')
Window.state('zoomed')  # Convenient to not have to manually fullscreen the window.

Style = ttk.Style()
Style.theme_use('alt') #Changes the look of the tabs bar, your choices are 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative'
    
Tabs = ttk.Notebook(Window)
Tabs.pack(expand=True, fill='both')
    
#Behold, My Seperate Screens!
FilterScreen = FilterFrameClass.FilterGUI(Window) #Load the Filter Screen from the FilterFrameClass script.
MealScreen = MealFrameClass.MealGUI(Window, FilterScreen.Whitelistbox, FilterScreen.Blacklistbox)  #Load Up the Meal Screen from the MealFrameClass script.

Tabs.add(MealScreen, text='Meals')
Tabs.add(FilterScreen, text='Filters')

Fotgui.InnitMealList(MealScreen.MealList, Classes.Meals)
#Window.mainloop() #Removed for functional purposes, check driver for this line of code.
