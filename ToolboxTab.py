import tkinter as tk
from tkinter import ttk
from copy import deepcopy
import ToolboxConfig as config
import ToolboxLatex as latex


class tab():

    def __init__(self, tabName, description, label, objectType):

        # this object's type is... this is used when calling functions in main.
        self.__objectType = config.CLASS_TYPES.get(objectType)
        # create the tab
        self.tab = ttk.Frame(config.tabControl)
        # add the tab to the window
        config.tabControl.add(self.tab, text=tabName)

        def Create_Label_Description(description, label):
            # create a default description if none is given
            if not description:
                __description = "Description"
            else:
                __description = description
            # create the label frame where i can place things
            self.DescriptionLabelFrame = ttk.LabelFrame(
                self.tab, text=__description)
            # place the label frame inside the tab
            self.DescriptionLabelFrame.grid(
                column=0, row=0, padx=8, pady=8, columnspan=6, sticky="W")
            # create the description label
            self.DescriptionLabel = ttk.Label(
                self.DescriptionLabelFrame, text=label)
            # place the description label
            self.DescriptionLabel.grid(column=0, row=0, columnspan=6)

        Create_Label_Description(description, label)

        self.entryBoxes1 = []
        self.entryBoxes2 = []
        self.entryBoxes1Content = []
        self.entryBoxes2Content = []
        self.textBox: object

        self.__currentColumn = 0
        self.__columnSpanIncrease = 1  # temporarily set to 1
        self.__columnSize = 0
        self.__currentRow = 0
        self.__extraEntryRow = 0
        self.__rowSize = 0

        self.__entryBoxSize = 2

    def get_identity(self):
        return self.tab

    def Create_Entry_Boxes(self, indentedRest, numberOfEntries, anotherColumn, addExtra):

        for i in range(numberOfEntries):
            self.__currentColumn = 0
            # should all entries except entry 0 be indented? (e.g. MCQ)

            def Indent_Other_Entries(indentedRest):
                if i > 0 and indentedRest:
                    self.__columnSpanIncrease = 2
                    return 48
                else:
                    self.__columnSpanIncrease = 1
                    return 0
            # a StringVar() contains the object. Can be collected with .get()
            __entryBoxContent = tk.StringVar()
            # instantiating an entry box
            __entryBox = ttk.Entry(
                self.tab, width=32, textvariable=__entryBoxContent)
            # place the entry box somewhere
            __entryBox.grid(column=self.__currentColumn, row=i + 1, padx=8 +
                            Indent_Other_Entries(indentedRest), pady=8, sticky="W", columnspan=self.__entryBoxSize + self.__columnSpanIncrease)
            # finally, add them to the list
            self.entryBoxes1.append(__entryBox)
            self.entryBoxes1Content.append(__entryBoxContent)

            # if we have to add another column of entries

            if (anotherColumn or (addExtra and numberOfEntries)):
                self.__currentColumn = 1
                if anotherColumn:
                    __entryBoxContent = tk.StringVar()
                    __entryBox = ttk.Entry(
                        self.tab, width=32, textvariable=__entryBoxContent)
                    # the padx is enlarged if the entries are supposed to be indented.
                    __entryBox.grid(column=self.__currentColumn + self.__entryBoxSize + self.__columnSpanIncrease, row=i + 1, padx=8 + Indent_Other_Entries(
                        indentedRest), pady=8, sticky="W", columnspan=self.__entryBoxSize + self.__columnSpanIncrease)
                    self.entryBoxes2.append(__entryBox)
                    self.entryBoxes2Content.append(__entryBoxContent)
                # if have to add an extra row of one entry and ONLY if we have gotten to the end of the for loop
                if addExtra and numberOfEntries - i == 1:
                    __entryBoxContent = tk.StringVar()
                    __entryBox = ttk.Entry(
                        self.tab, width=32, textvariable=__entryBoxContent)
                    __entryBox.grid(column=self.__currentColumn + self.__entryBoxSize + self.__columnSpanIncrease, row=i + 2, padx=8 + Indent_Other_Entries(
                        indentedRest), pady=8, sticky="W", columnspan=self.__entryBoxSize + self.__columnSpanIncrease)
                    self.entryBoxes2.append(__entryBox)
                    self.entryBoxes2Content.append(__entryBoxContent)

        # let's get how large the column should be to create a text box.
        # i have no idea what i have done here.
        self.__currentColumn += ((self.__entryBoxSize *
                                  (self.__currentColumn + 1)) + self.__columnSpanIncrease) + 1
        # print(self.__currentColumn)

        # let's get how large the entries are so that we can create a layout that is based on the rowsize of the entries
        # what am i doing
        self.__rowSize = numberOfEntries
        self.__currentRow = self.__rowSize + 1

        if addExtra:
            # same goes here - if he have an extra one, the textbox needs to be enlarged by that much.
            self.__extraEntryRow = 1

    def Create_Text_Box(self):
        self.textBox = tk.Text(self.tab, width=38, relief="sunken")
        self.__textBoxColumnLocation = self.__currentColumn
        self.__textBoxRowLocation = 5 + self.__rowSize + self.__extraEntryRow
        self.textBox.grid(column=self.__textBoxColumnLocation, row=0, sticky="E", padx=32, pady=32,
                          rowspan=5 + self.__rowSize + self.__extraEntryRow, columnspan=3)
        # increase current column as we have made a rather large textbox.
        self.__currentColumn += 4
        # icrease the row size as well. maybe?
        # self.__rowSize += 1

    def Create_Latex_Code(self):
        # TODO that function will take the passed data and then write to the text box and copy the contents of the textbox to the clipboard.

        def Get_Entry_Box_Contents():
            # initialise the temporary lists
            _entryBox1Content = []
            _entryBox2Content = []

            for i in self.entryBoxes1Content:
                if i.get() != "":
                    _entryBox1Content.append(i.get())
            for i in self.entryBoxes2Content:
                if i.get() != "":
                    _entryBox2Content.append(i.get())

            if _entryBox1Content and _entryBox2Content:
                _theContents = _entryBox1Content, _entryBox2Content
                print(f"Collected from {self}: {_theContents}")
                return _theContents
            elif _entryBox1Content:
                _theContents = _entryBox1Content
                print(f"Collected from {self}: {_theContents}")
                return _theContents
            else:
                print(
                    "Nothing has been passed from Get_Entry_Box_Contents() to latex.Function_Decider()")

        # write into the textbox
        def __Write_Text_Box(theCode):
            # proceed only if the input is not empty
            if theCode:
                # first we need to clear the textbox if we wish to write to it
                self.__Clear_Text_Box()
                self.textBox.insert("end", theCode)

        # go to the latex module and pass the lists. # TODO: insert whether it should be randomised
        print(
            f"The state of the randomise checkbox is {self.__randomiseCheckboxState.get()}")
        __latexCode = latex.Function_Decider(
            self.__objectType, Get_Entry_Box_Contents(), self.__randomiseCheckboxState.get())

        # now that we have the code
        # we can write it to the textbox
        __Write_Text_Box(__latexCode)

        # and copy it to clipboard
        self.__Copy_Text()

    # clear the text box
    def __Clear_Text_Box(self):
        self.textBox.delete(1.0, "end")

    # clear the entry box
    def __Clear_Entry_Boxes(self):
        if self.entryBoxes1:
            for i in self.entryBoxes1:
                i.delete(0, "end")
            for i in self.entryBoxes2:
                i.delete(0, "end")

    # clear the textbox and then clear the entry boxes.
    def __Clear_Everything(self):
        self.__Clear_Text_Box()
        self.__Clear_Entry_Boxes()

    def __Copy_Text(self):
        # clear the clipboard from any junk
        config.win.clipboard_clear()
        # copy to clipboard the textbox content.
        config.win.clipboard_append(self.Get_Text_Box_Contents())
        print(
            f"Successfully copied {self.Get_Text_Box_Contents()} to clipboard!")

    def Create_Buttons(self, latex, clear, copy, randomise):

        self.__currentColumn = 0

        def Create_Randomised_Checkbox(randomise):
            self.__randomiseCheckboxState = tk.IntVar()
            self.__randomiseCheckbox = tk.Checkbutton(
                self.tab, text="Randomise?", width=10, variable=self.__randomiseCheckboxState)
            # if randomise if 0, there is no need to place the button. It is still there but it is hidden.
            if randomise:
                self.__randomiseCheckbox.grid(
                    column=self.__currentColumn, row=self.__currentRow + self.__extraEntryRow, padx=24, sticky="W")
            # set to random immediately if randomise is on.
            if randomise:
                self.__randomiseCheckbox.select()

        def __Create_Latex_Button():
            self.latexButton = ttk.Button(
                self.tab, text="LaTeX", command=self.Create_Latex_Code)
            self.latexButton.grid(
                column=self.__currentColumn, row=self.__currentRow + self.__extraEntryRow, sticky="E")

        def __Create_Clear_Button():
            self.clearButton = ttk.Button(
                self.tab, text="Clear", command=self.__Clear_Everything)
            self.clearButton.grid(column=self.__textBoxColumnLocation,
                                  row=self.__textBoxRowLocation + self.__extraEntryRow + 1, sticky="E")

        def __Create_Copy_Button():
            self.copyButton = ttk.Button(
                self.tab, text="Copy", command=self.__Copy_Text)
            self.copyButton.grid(column=self.__textBoxColumnLocation + 1,
                                 row=self.__textBoxRowLocation + self.__extraEntryRow + 1, sticky="W")

        if latex:
            Create_Randomised_Checkbox(randomise)
            self.__currentColumn = 1
            __Create_Latex_Button()

        if clear:
            __Create_Clear_Button()

        if copy:
            __Create_Copy_Button()

    def Get_Text_Box_Contents(self):
        return self.textBox.get(1.0, "end")
