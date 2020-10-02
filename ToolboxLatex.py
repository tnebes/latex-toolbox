import random

# =================
# Function decider
# =================

# we need to figure out which object called us
# according to that, we need to figure out what we need to do with the data
# once we do that we MUST return the data back to the function that called us
# that function will then write to the text box and copy the contents of the textbox to the clipboard.


def Function_Decider(objectType, contents, randomise):
    # set the state of the function and whether it can continue
    if type(contents) is tuple:
        contents1, contents2 = contents
        print(f"Got the tuple! It is now {contents1} and {contents2}.")
    elif type(contents) is list:
        contents1 = contents
        print(f"Got the list! It is now {contents1}.")
    else:
        print(f"Function_Decider() has nothing to work with.")
        return "Illegal input.\nCheck your entries and try again."

    # 0 - MCQ
    # 1 - UnknownWords
    # 2 - UnknownWordsBox
    # 3 - InsertWordsBox

    if objectType == 0 and len(contents1) > 3:

        # the first in the list is the question
        _MCQAnswers = contents1
        _MCQuestion = ""

        if randomise == 1:
            _MCQuestion = _MCQAnswers.pop(0)
            random.shuffle(_MCQAnswers)

        # if there are 3 answers, it's \vquestionthree{}
        # randomise is here because otherwise the list would become longer. Randomise provides an useful integer with which i can make this work. woo.
        if len(_MCQAnswers) == 4 - randomise:
            latexCode = "\\vquestionthree"
            if randomise == 1:
                latexCode += Wrap_Curly(_MCQuestion)
            latexCode += Create_Bracketed_Latex_Code(_MCQAnswers)
            print(f"Script has created {latexCode}.")

        # if there are 4 answers, it's \vquestion{}
        elif len(_MCQAnswers) == 5 - randomise:
            latexCode = "\\vquestion"
            if randomise == 1:
                latexCode += Wrap_Curly(_MCQuestion)
            latexCode += Create_Bracketed_Latex_Code(_MCQAnswers)
            print(f"Script has created {latexCode}.")

        # return to object

        return latexCode

    elif objectType == 1 and len(contents1) > 0 and len(contents2) > 0:
        _unknownLexemes = contents1
        _unknownExplanations = contents2

        if randomise == 1:
            random.shuffle(_unknownLexemes)
            random.shuffle(_unknownExplanations)

        latexCode = "\\unknownwords{\n"
        for i in _unknownLexemes:
            latexCode += f"\item {i}\n"
        latexCode += "}\n{\n"
        for i in _unknownExplanations:
            latexCode += f"\item {i}\n"
        latexCode += "}"

        return latexCode

    elif objectType == 2 and len(contents1) > 0 and len(contents2) > 0:
        _unknownLexemes = contents1
        _unknownExplanations = contents2

        latexCode = "\\unknownWordBox{%\n"
        for i in range(len(_unknownLexemes)):
            latexCode += "\\circledwhite{" + str(i + 1) + "}" + "{\\bfseries " + _unknownLexemes[i] + "} - " + _unknownExplanations[i] + "\n"
        latexCode += "}"

        return latexCode
        

    elif objectType == 3 and len(contents1) > 0:
        _wordsToBeInserted = contents1
        if randomise == 1:
            random.shuffle(_wordsToBeInserted)
        latexCode = "\\wordbox{%\n|"
        for i in _wordsToBeInserted:
            latexCode += f" {i} |\n"
        latexCode += "}%"

        return latexCode

# =================
# Utility functions
# =================

# wrap code around curly braces


def Wrap_Curly(snippet):
    return "{" + snippet + "}"


def Create_Bracketed_Latex_Code(aList):
    theString = ""
    for i in aList:
        theString += Wrap_Curly(i)
    return theString
