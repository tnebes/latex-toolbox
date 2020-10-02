import random
import tkinter as tk
from tkinter import ttk
from copy import deepcopy

# which types of objects can we have
CLASS_TYPES = {"MCQ": 0,
                "UnknownWords": 1,
                "UnknownWordsBox": 2,
                "InsertWordsBox": 3
                }


CEFR_LEVELS = {
    "A1": 0,
    "A2": 1,
    "B1": 2,
    "B2": 3,
    "C1": 4,
    "C2": 5
}

CEFR_OPTIONS = ["",]

for x in CEFR_LEVELS:
    CEFR_OPTIONS.append(x)

UNWANTED_CHARACTERS = (",", ".", ":", ";", "'s", "\"", "'", "’s", "’", "!", "?", "/", "(", ")")


# ==========
# set up gui
# ==========

# create an instance

win = tk.Tk()

# create a title for the window

win.title("tnebes' LaTeX ToolBox")

# do not resize the window

win.resizable(False, False)
win.geometry("800x600")

# set up the tab controller
tabControl = ttk.Notebook(win)

# show the tabs
tabControl.pack(expand=1, fill="both")




# ===================
# Configuration
# ===================

