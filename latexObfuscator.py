import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
import ToolboxConfig as config
import logging
import os

class LatexObfuscator():

    def __init__(self):

        self.__DEBUGGING = False

        self.TAB_NAME = "LaTeX Obfuscator"

        self.__theFile = None

        # create the tab
        self.tab = ttk.Frame(config.tabControl)

        # add the tab to the window
        config.tabControl.add(self.tab, text=self.TAB_NAME)

        # create the label frame where i can place things
        self.DescriptionLabelFrame = ttk.LabelFrame(
            self.tab, text="Description")

        # place the label frame inside the tab
        self.DescriptionLabelFrame.grid(
            column=0, row=0, padx=8, pady=8, columnspan=6, sticky="W")

        # create the description label
        self.DescriptionLabel = ttk.Label(
            self.DescriptionLabelFrame, text="Obfuscate .tex files here.")

        # place the description label
        self.DescriptionLabel.grid(column=0, row=0, columnspan=6)

        # place the button here
        self.obfuscateButton = ttk.Button(
            self.tab, text="Analyse", command=self.__Begin_Obfuscation)
        self.obfuscateButton.grid(
            column=0, row=1, sticky="NWES")


    def __Begin_Obfuscation(self):
        __currentPosition: int
        __documentBeginning: int
        __documentEnd: int
        
        # let's get the file

        self.__theFile = self.Launch_File_Browser()

        # find the beginning and the end

        __documentBeginning, __currentPosition = self.__Find_Begin(), self.__Find_Begin()
        __documentEnd = len(self.__theFile)
        print(f"Document begins at position {__documentBeginning} and ends at position {__documentEnd}.\n")

        # for each fullstop between beginning and end

        # make a counter to see which watermark goes in
        _waterMarkCounter = 0
        _waterMarkText = [r"\watermarkZero", r"\watermarkOne", r"\watermarkTwo", r"\watermarkThree"]

        # while inside the document environment
        while __currentPosition < __documentEnd:
            __currentPosition = self.__Find_Fullstop(__currentPosition)
            if __currentPosition < __documentBeginning:
                break
            if self.__DEBUGGING:
                print(f"Now at position {__currentPosition}.")
            # if it is not surrounded by numbers
            # or ends with .png,jpg,etc.
            try:
                if self.__DEBUGGING:
                    print("I am surrounded by: ", self.__theFile[__currentPosition - 1], self.__theFile[__currentPosition + 1])
                int(self.__theFile[__currentPosition - 1])
                int(self.__theFile[__currentPosition + 1])
                __currentPosition += 1
                continue
            except ValueError:
                # print("Triggered an exception!")
                # _log = logging.getLogger()
                # _log.exception("The exception is...")

                if self.__DEBUGGING:
                    print(self.__theFile[__currentPosition:__currentPosition + 4])

                # if the counter is higher than 3, revert to 0
                if (self.__theFile[__currentPosition : __currentPosition + 4] != ".jpg" or ".png"):
                    if _waterMarkCounter > 3:
                        _waterMarkCounter = 0

                    # according to each counter add the appropriate watermark
                    _currentWatermark = _waterMarkText[_waterMarkCounter]
                    # increment the counter
                    _waterMarkCounter +=1

                    # what is the watermark length? Used for increasing the current position
                    _watermarkLength = len(_currentWatermark)

                    self.__theFile = self.__Insert_Watermark(position=__currentPosition, watermarkText=_currentWatermark, file=self.__theFile)

                    # I have to add two to the current position as +1 includes the fullstop thus causing an endless loop.
                    __currentPosition += _watermarkLength + 1
                    __documentEnd = len(self.__theFile)
                    if self.__DEBUGGING:
                        print(f"Current document length is {__documentEnd}.")

        if self.__DEBUGGING:
            print(self.__theFile)
               
        # once done, save the file from the variable containing the string
        self.__Save_Obfuscated_File()


    def Launch_File_Browser(self):
        # the filedialog must be imported
        # filetypes requires a tuple containing at least two items??? last one must be all files as specified below
        self.texFile = tk.filedialog.askopenfilename(parent=config.win, title='Choose a .tex file', filetypes=(("LaTeX Files", "*.tex"), ("All files", "*.*")))
        try:
            print(self.texFile)
            with open(self.texFile, "r", encoding="utf8") as self.__texFile:
                self.texFileContents = self.__texFile.read()
            return self.texFileContents
        except FileNotFoundError:
            print("No file selected.")

    def __Get_Position(self, aString, startPosition=0, endPosition=-1):

        _theFile = self.__theFile

        return _theFile.find(aString, startPosition, endPosition)

    def __Find_Fullstop(self, startPosition):
        return self.__Get_Position(".", startPosition)

    def __Find_Begin(self):
        return self.__Get_Position(r"\begin{document}")

    # def __Find_End(self):
    #     return self.__Get_Position(r"\end{document}")

    def __Insert_Watermark(self, position, watermarkText, file):

        # create two new strings
        __beginningString, __endString = file[:position], file[position:]

        # append the watermark to the first string
        __beginningString += watermarkText

        # combine the two strings and return them
        _newString = __beginningString + __endString

        return _newString

    def __Save_Obfuscated_File(self):
        * _junk, _FILE_NAME = self.texFile.split(r"/")
        FILE_NAME = "tnebes_" + _FILE_NAME
        FILE_DIRECTORY = "./obfuscated/"
        FILE_DIRECTORY_NAME = FILE_DIRECTORY + FILE_NAME
        print(f"File directory and name is: {FILE_DIRECTORY_NAME}")

        try:
            with open(FILE_DIRECTORY_NAME, "r") as theFile:
                theFile.close()
        except FileNotFoundError:
            try:
                os.mkdir(FILE_DIRECTORY)
            except FileExistsError:
                pass
        with open(FILE_DIRECTORY_NAME, "w") as theFile:  
            theFile.write(self.__theFile)



    


