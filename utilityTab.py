import tkinter as tk
from tkinter import ttk
import ToolboxConfig as config

class UtilityTab():

    def __init__(self):
        self.__TAB_NAME = "Utility functions"
        self.__utilityTab = ttk.Frame(config.tabControl)
        config.tabControl.add(self.__utilityTab, text=self.__TAB_NAME)

    def create_grade_calculator(self):
        # create the frame
        self.__gradeCalculatorFrame = ttk.LabelFrame(self.__utilityTab, text="Grade Calculator")

        # place the frame
        self.__gradeCalculatorFrame.grid(column=0, row=0, columnspan=3)

        # add description for the frame
        self.__gradeCalculatorDescriptionText = "Use this widget to determine score for grading."
        self.__gradeCalculatorDescription = ttk.Label(self.__gradeCalculatorFrame, text=self.__gradeCalculatorDescriptionText)

        # place the description within the frame
        self.__gradeCalculatorDescription.pack(side=tk.TOP, fill=tk.X, expand=1, anchor=tk.CENTER)

        # add a frame

        # add label frame
        self.__labelFrame = ttk.Frame(self.__gradeCalculatorFrame)
        self.__labelFrame.pack()

        # place it within the previous frame

        self.__frameTop = ttk.Frame(self.__gradeCalculatorFrame)
        self.__frameTop.pack()


        # also add labels

        self.__minScoreLabel = tk.Label(self.__labelFrame, text="Min. score %", width=16)
        self.__minScoreLabel.pack(side=tk.LEFT, fill=tk.BOTH, expand=1, anchor=tk.CENTER)

        self.__totalScoreLabel = tk.Label(self.__labelFrame, text="Total score", width=16)
        self.__totalScoreLabel.pack(side=tk.LEFT, fill=tk.BOTH, expand=1, anchor=tk.CENTER)

        self.__minScoreEntryContent = tk.StringVar()
        self.__minScoreEntry = ttk.Entry(self.__frameTop, textvariable=self.__minScoreEntryContent)
        self.__minScoreEntry.pack(side=tk.LEFT, padx=6)

        self.__totalScoreEntryContent = tk.StringVar()
        self.__totalScoreEntry = ttk.Entry(self.__frameTop,textvariable=self.__totalScoreEntryContent)
        self.__totalScoreEntry.pack(side=tk.LEFT, padx=6)

        # separate them to make them look nicer
        ttk.Separator(self.__gradeCalculatorFrame, orient="horizontal").pack(fill=tk.X, pady=6)


        # declare some variables that i will need
        # the grade label
        self.__gradeLabelContent = ["F", "D", "C", "B", "A"]
        # just in case i will make a list of the grade labels
        self.gradeLabels = []

        # declare the lists
        self.scoreLabelsContent = []
        # and this one just in case
        self.__scoreLabels = []

        # add a frame for the labels

        self.__scoringFrame = ttk.Frame(self.__gradeCalculatorFrame)
        self.__scoringFrame.pack()

        def create_grade_labels():

            # now in a for loop
            for grade in self.__gradeLabelContent:

                # initialise a counter
                self.__counter = self.__gradeLabelContent.index(grade)

                # add a frame
                self._theFrame = ttk.Frame(self.__scoringFrame)
                self._theFrame.pack(side=tk.TOP)

                # within each frame, add two labels
                # first label contains the grade
                self._theGradeLabel = tk.Label(self._theFrame, text=self.__gradeLabelContent[self.__counter], width=16)

                # don't forget to pack it
                self._theGradeLabel.pack(side=tk.LEFT, fill=tk.X)

                # add it to the list
                self.gradeLabels.append(self._theGradeLabel)


                # the second grade contains the score
                # initialise the variable that will contain the string
                self._theScoreLabelContent = tk.StringVar()
                self._theScoreLabelContent.set("test")

                # create the label and set the text to the variable above
                self._theScoreLabel = tk.Label(self._theFrame, textvariable=self._theScoreLabelContent, width=16)

                # add the contents of the label to the list
                self.scoreLabelsContent.append(self._theScoreLabelContent)
                # add the label to the list
                self.__scoreLabels.append(self._theScoreLabel)

                # pack the label
                self._theScoreLabel.pack(side=tk.LEFT, fill=tk.X)

                # we need the second label because it will be edited later
        
        create_grade_labels()

        def calculate_grades():
            # get the values from the entry boxes
            self.__minPercentage = int(self.__minScoreEntryContent.get())
            self.__maxScore = int(self.__totalScoreEntryContent.get())

            # with how much do we have to work
            self.__calculablePercentage = 100 - self.__minPercentage

            # what is the step?
            self.__percentageStep = self.__calculablePercentage/4
            
            # setting everything up
            self.__gradePercentages = [self.__minPercentage]
            self.__scores = []
            self.__fPercent = self.__minPercentage / 100
            self.__scores.append(round(self.__maxScore * self.__fPercent))
            # print(self.__scores)

            # let's calculate the percentages
            self.__tempPercent = self.__minPercentage
            while max(self.__gradePercentages) < 100:
                self.__tempPercent += self.__percentageStep
                self.__gradePercentages.append(self.__tempPercent)
            # print(self.__gradePercentages)

            # let's calculate the scores for various grades according to the results of the above list
            self.__tempScore = self.__scores[0]
            self.__counter = 1 # counters now start from 1!
            while max(self.__scores) < self.__maxScore:
                self.__currentScore = round(self.__maxScore * (self.__gradePercentages[self.__counter] / 100))
                self.__scores.append(self.__currentScore)
                self.__counter += 1
            # print(self.__scores)

            write_to_labels(self.__gradePercentages, self.__scores)

        def write_to_labels(percentages, scores):
            self.__tempCounter = 0
            for labelContent in self.scoreLabelsContent:
                 
                self.__whatToWrite = "<" + str(percentages[self.__tempCounter]) + "%: <" + str(scores[self.__tempCounter])
                labelContent.set(self.__whatToWrite)
                self.__tempCounter += 1

        def create_calculate_button():
            _gradeCalculateButton = ttk.Button(self.__gradeCalculatorFrame, text="Calculate!", command=calculate_grades)
            _gradeCalculateButton.pack(side=tk.BOTTOM)

        # add another separator to make things look nice

        ttk.Separator(self.__gradeCalculatorFrame, orient="horizontal").pack(fill=tk.X, pady=6)

        # create the button that will call the calculation function

        create_calculate_button()






