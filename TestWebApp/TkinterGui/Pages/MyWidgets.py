import tkinter as tk
from tkinter import ttk


class MySuiteButton(tk.Button):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.background = "#0275d8"
