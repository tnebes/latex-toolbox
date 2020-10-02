import os
import random
import ToolboxTab as tabs
import UnknownWordAnalysis as Analyser
import latexObfuscator as obfuscator
import utilityTab as utility

import tkinter as tk
from tkinter import ttk
from copy import deepcopy
import ToolboxConfig as config


def main():

    # =================
    # First tab - MCQ
    # =================
    
    # NOTE: ALWAYS USE THIS ORDER. INSTANTIATE THE TAB, THE ENTRY BOXES, THE TEXT BOX, BUTTONS, ETC. 

    MCQTab = tabs.tab(tabName="MCQ", description="", label="Create MCQs here.", objectType="MCQ")
    MCQTabFrame = MCQTab.get_identity()
    MCQTab.Create_Entry_Boxes(numberOfEntries=5, indentedRest=True, anotherColumn=False, addExtra=False)
    MCQTab.Create_Text_Box()
    MCQTab.Create_Buttons(latex=True, clear=True, copy=True, randomise=True)

    # =================
    # Second tab - Unknown Words Task
    # =================

    UnknownWordsTab = tabs.tab(tabName="U. Words", description="", label="Create unknown word task here.", objectType="UnknownWords")
    unknownWordsTabFrame = UnknownWordsTab.get_identity()
    UnknownWordsTab.Create_Entry_Boxes(indentedRest=False, numberOfEntries=7, anotherColumn=True, addExtra=True)
    UnknownWordsTab.Create_Text_Box()
    UnknownWordsTab.Create_Buttons(latex=True, clear=True, copy=True, randomise=True)

    # =================
    # Third tab - Unknown Words Box
    # =================

    UnknownWordsBoxTab = tabs.tab(tabName="U. Words Box", description="", label="Create a box filled with unknown words here.", objectType="UnknownWordsBox")
    UnknownWordsBoxTab.Create_Entry_Boxes(indentedRest=False, numberOfEntries=8, anotherColumn=True, addExtra=False)
    UnknownWordsBoxTab.Create_Text_Box()
    UnknownWordsBoxTab.Create_Buttons(latex=True, clear=True, copy=True, randomise=False)

    # =================
    # Fourth tab - Insert Words Box
    # ================= 

    InsertWordsBoxTab = tabs.tab(tabName="Insert Words Box", description="", label="Create a box filled with words\nto be inserted into a text here.", objectType="InsertWordsBox")
    InsertWordsBoxTab.Create_Entry_Boxes(indentedRest=False, numberOfEntries=8, anotherColumn=False, addExtra=False)
    InsertWordsBoxTab.Create_Text_Box()
    InsertWordsBoxTab.Create_Buttons(latex=True, clear=True, copy=True, randomise=True)

    # =================
    # Fifth tab - Word Analysis
    # =================

    WordAnalyserTab = Analyser.WordAnalysis()

    # =================
    # Sixth tab - Latex Obfuscator
    # =================

    LatexObfuscate = obfuscator.LatexObfuscator()

    # =================
    # Final tab - Utilities
    # =================

    TheUtilityTab = utility.UtilityTab()
    TheUtilityTab.create_grade_calculator()

    # ==============
    # Start GUI
    # ==============

    config.tabControl.pack()
    os.system('cls')
    print("=================\nThis toolbox was created by T Nebes in 2019.\n=================\n\nReady for input!")
    config.win.mainloop()


# =============
# Execute
# =============
if __name__ == '__main__':  
    main()
