import tkinter as tk
from tkinter import ttk
from copy import deepcopy
import ToolboxConfig as config
import WebsiteScraper as scraper


class WordAnalysis():

    def __init__(self):

        TAB_NAME = "Word Analyser"

        # create the tab
        self.tab = ttk.Frame(config.tabControl)

        # add the tab to the window
        config.tabControl.add(self.tab, text=TAB_NAME)

        # create the label frame where i can place things
        self.DescriptionLabelFrame = ttk.LabelFrame(
            self.tab, text="Description")

        # place the label frame inside the tab
        self.DescriptionLabelFrame.grid(
            column=0, row=0, padx=8, pady=8, columnspan=6, sticky="W")

        # create the description label
        self.DescriptionLabel = ttk.Label(
            self.DescriptionLabelFrame, text="Analyse word CEFR difficulty\nin this tab.")

        # place the description label
        self.DescriptionLabel.grid(column=0, row=0, columnspan=6)

        # place the input textbox
        self.inputTextBox = tk.Text(self.tab, width=32, height=32, relief="sunken", font=("Helvetica", 8))
        self.inputTextBox.grid(column=0, row=1, sticky="W", padx=32, pady=32,
                               rowspan=5, columnspan=3)

        # place the button here
        self.analyseButton = ttk.Button(
            self.tab, text="Analyse", command=self.Start_Analysis)
        self.analyseButton.grid(
            column=3, row=3, sticky="NWES")

        # place the output textbox
        self.outputTextBox = tk.Text(self.tab, width=32, relief="sunken")
        self.outputTextBox.grid(column=4, row=1, sticky="E", padx=32, pady=32,
                                rowspan=5, columnspan=3)

        #   add optionmenu for difficulty
        self.CEFROptionMenuString = tk.StringVar()

        # what will be show as the first thing
        self.CEFROptionMenuString.set("Choose difficulty")

        # initialise the option menu
        self.CEFROptionMenu = ttk.OptionMenu(
            self.tab, self.CEFROptionMenuString, *config.CEFR_OPTIONS)

        # place it somewhere.
        self.CEFROptionMenu.grid(column=3, row=0)

        # what is the current difficulty?
        self.__currentDifficulty = "A1"

    def Start_Analysis(self):
        self.outputTextBox.delete(1.0, "end")
        self.__currentDifficulty = self.Get_CEFR_Difficulty()
        self.Send_To_Analyser(self.Get_Textbox_Contents())

    def Get_CEFR_Difficulty(self):
        self.__selectedCEFROption = self.CEFROptionMenuString.get()
        if self.Check_If_In_CEFR():
            return self.__selectedCEFROption
        else:
            print("Error. Invalid CEFR chosen.")

    def Check_If_In_CEFR(self):
        return self.__selectedCEFROption in config.CEFR_OPTIONS

    #   send each word to the analyser

    def Get_Textbox_Contents(self):
        self.__textboxString = self.inputTextBox.get(1.0, "end")
        for i in config.UNWANTED_CHARACTERS:
            self.__textboxString = self.__textboxString.replace(i, "")
        self.__textboxString = self.__textboxString.split()
        print(self.__textboxString)
        return self.__textboxString

    def Send_To_Analyser(self, __textboxList):
        if len(__textboxList) > 0:
            for __word in __textboxList:
                self.__currentWordDifficulty = scraper.Find_Word_Difficulty(
                    __word)
                self.Compare_Difficulties(__word, self.__currentWordDifficulty)
            print("\n\tFinished looking up words for the text!\n")
        else:
            print("Text to be analysed too short.")

    def Compare_Difficulties(self, __word, __givenWordDifficulty):
        # print(f"DEBUG DEBUG DEBUG.\n CURRENT SELECTED DIFFICULTY IS -- {__givenWordDifficulty} {config.CEFR_LEVELS.get(__givenWordDifficulty)} AND THE WORD'S DIFFICULTY IS {self.__currentDifficulty} ")
        if __givenWordDifficulty:
            try:
                if config.CEFR_LEVELS.get(__givenWordDifficulty) >= config.CEFR_LEVELS.get(self.__currentDifficulty):
                    self.Write_To_Output_Textbox(__word, __givenWordDifficulty)
                print(f"Adding \"{__word}\" : {__givenWordDifficulty} to output box.\n==========\n")
            except TypeError:
                # print(config.CEFR_LEVELS.get(__givenWordDifficulty), self.__currentDifficulty)
                pass

    def Write_To_Output_Textbox(self, __word, __difficulty):
        self.outputTextBox.insert("end", __word + " : " + __difficulty + "\n")
        
    #   if word is equally or more difficult than the entrybox difficulty
    #       if the value of key is >= the value of key A2 e.g.
    #   add it to the textbox in form of {word} : {difficulty}
    #
