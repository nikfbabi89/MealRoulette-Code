#Modularity, one of the best things ive learned.
import tkinter as tk #Used for all GUI
import ColorPresets as Col #Used to customize GUI easily.
import FunctionsOfTheGUI as Fotgui #The beating heart of functional GUI.

class MealGUI(tk.Frame): #The acting frame. Who knew inheritance was so useful.
    def __init__(self, Window=None, Whitelistbox=None, Blacklistbox=None): #Default None
        super().__init__(Window, bg=Col.BG) #My understanding is that super() makes the whole thing inherit the frame class from tkinter.

        self.Instr = '''Left click an entry in the Meal List to select it
Left click it in the Selected Meals List to remove it from your listed meals
Right click while selected to filter that meal out, do this again to undo toggle
Use tabs to navigate to the filter screen'''
        
        self.Instructions = tk.Label(self, bg=Col.BG, fg=Col.TB, font=Col.Dfu, text=self.Instr)
        self.Instructions.pack(side='top')

        self.Labels = tk.Label(self, bg=Col.BG, fg=Col.TB, text='  Meals List\t        Selected Meals', font=('Arial', 20, 'bold'))
        self.Labels.pack(side='bottom', anchor='w')

        self.MealList = tk.Listbox(self, width=40, height=40, bg=Col.TWB, font=Col.Dfu)  #List lower than display so that the binding works when display.
        self.MealList.pack(side='left', anchor='w', padx=5, fill='y') #Must be playing Silksong, because I'm binding.
        self.MealList.bind('<ButtonRelease-1>', lambda event: Fotgui.GrabSelection(event, self.Display, True, True)) #2nd binding to grab selection twice. (Moved Up)
        self.MealList.bind('<ButtonRelease-1>', lambda event: Fotgui.GrabSelection(event, self.SelectedMeals, True, True), add='+') #First Binding to grab selection.
        self.MealList.bind('<ButtonRelease-3>', lambda event: Fotgui.Freeze(event), add='+') #A third binding to allow freeze functions. Right click though.
        self.MealList.bind('<<ListboxSelect>>', lambda event: Fotgui.DisplayMeal(self.MealList, self.Display), add='+') #On highlight, list the info. Disfunctional.
        #On another note, I use ButtonRelease-1 instead of ListboxSelect because listbox select only updates on changing the selection rather than 
        #ButtonRelease-1, which works more like a button when triggered. Though if you click on empty space at the bottom of the list box,
        #it will choose the last index.
        
        self.SelectedMeals = tk.Listbox(self, width=40, height=40, bg=Col.TWB, font=Col.Dfu)
        self.SelectedMeals.pack(side='left', anchor='w', padx=5, fill='y')
        self.SelectedMeals.bind('<ButtonRelease-1>', lambda event: Fotgui.GrabSelection(event, self.MealList, True, True))

        self.Reset = tk.Button(self, text='Reset', bg=Col.BB, fg=Col.TB, font=Col.Dfu, command=lambda: Fotgui.ResetMealList(self.MealList, self.SelectedMeals))
        self.Reset.pack(side='bottom')
        
        self.Display = tk.Text(self, bg=Col.TWB, font=Col.Dfu)
        self.Display.pack(side='top', anchor='e')
        self.Display.config(state='disabled')
        
        self.Randomize = tk.Button(self, text='Randomize', width=80, bg=Col.BB, fg=Col.TB, font=Col.Dfu, command=lambda: Fotgui.RandomMeal(self.MealList, self.Display, Whitelistbox, Blacklistbox))
        self.Randomize.pack(side='right', anchor='center')  # Also needs to be last to be able to call the meal list widget.

