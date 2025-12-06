import tkinter as tk
import ColorPresets as Col
import FunctionsOfTheGUI as Fotgui


class FilterGUI(tk.Frame):
    def __init__(self, Window):
        super().__init__(Window, bg=Col.BG)

        self.FilterLabel = tk.Label(self, bg=Col.BG, fg=Col.TB, font=Col.Dfu, text='Filters\t\t\t\tWhitelist\t\t\t\tBlacklist')
        self.FilterLabel.pack(side='top', anchor='w')

        self.a2b = tk.Button(self, bg=Col.BB, fg=Col.TB, font=Col.Dfu, text='Add Selected To Blacklist', command=lambda: Fotgui.ButtonToList(self.Filters, self.Blacklistbox))
        self.a2b.pack(side='bottom', fill='x')

        self.a2w = tk.Button(self, bg=Col.BB, fg=Col.TB, font=Col.Dfu, text='Add Selected To Whitelist', command=lambda: Fotgui.ButtonToList(self.Filters, self.Whitelistbox))
        self.a2w.pack(side='bottom', fill='x')

        self.Filters = tk.Listbox(self, width=30, font=Col.Dfu)
        self.Filters.pack(side='left', fill='y', padx=5)

        self.Whitelistbox = tk.Listbox(self, width=30, font=Col.Dfu)
        self.Whitelistbox.pack(side='left', fill='y', padx=5)
        self.Whitelistbox.bind('<ButtonRelease-1>', lambda event: Fotgui.GrabSelection(event, self.Whitelistbox, True, False))

        self.Blacklistbox = tk.Listbox(self, width=30, font=Col.Dfu)
        self.Blacklistbox.pack(side='left', fill='y', padx=5)
        self.Blacklistbox.bind('<ButtonRelease-1>', lambda event: Fotgui.GrabSelection(event, self.Blacklistbox, True, False))

        Fotgui.InnitFiltersList(self.Filters)