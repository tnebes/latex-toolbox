# import urllib3
import requests
import webbrowser
import FileWriter as FileWriter
import ToolboxConfig as config
import suffixDestroyer as suffix
from bs4 import BeautifulSoup

# TODO: make it so that it collects all the difficulties and makes the value a list containing all difficulties.


# is it going to spit out the most difficult or least difficult CEFR?
CHOOSE_HIGHEST_DIFFICULTY = False

# where is our dictionary

# define the CEFR levels

# where can we find the levels?

STATIC_WEBPAGE = "https://dictionary.cambridge.org/dictionary/english/"

# what is the search term that is asked of us?

def Find_Word_Difficulty(searchTerm):

    # where is the dictionary
    OFFLINE_DICTIONARY = FileWriter.Read_From_Dictionary()
    # print(f"Successfully loaded dictionary. It contains {OFFLINE_DICTIONARY}.")

    # resetting the lookup bool
    __lookup = False

    # how can we isolate the CEFR levels?

    # when the analyser starts
    # print(f"Starting analyser.\n ================== \n Dictionary contains {len(OFFLINE_DICTIONARY)} entries.\n")

    def __Isolate_Word_Difficulty(searchTermList):

        __difficultyList = []

        # for each i find ">
        for i in searchTermList:
            # print(searchTermList)
            # print(f"\n{i}")
            # print(type(i))
            # we need to turn this into a string.
            i = str(i)
            __startPosition = i.find('>')

            if __startPosition == -1 or __startPosition == None:
                print("Something went wrong while isolating word difficulty.")
                break

            # if true, append to list
            # get the two characters after it

            __difficultyList.append(
                i[__startPosition + 1: __startPosition + 3])


        return __difficultyList

    # how many levels can we find?
    def Check_How_Many_Levels():
        if len(possibleWordDifficulties) > 1:
            print(
                f"Multiple difficulty levels detected. \"{searchTerm}\" has {len(possibleWordDifficulties)} difficulty levels.\
                \n {possibleWordDifficulties}")
        # if it only has one
        elif len(possibleWordDifficulties) == 1:
            print(
                f"Difficulty level detected for \"{searchTerm}\". It is {possibleWordDifficulties}.")
        else:
            print(f"No difficulty levels detected for \"{searchTerm}\".")

    def Choose_Difficulty_Level():
        # get the list
        __difficultyList = []

        if CHOOSE_HIGHEST_DIFFICULTY == True:
            __WhereToLook = -1
        else:
            __WhereToLook = 0

        # convert entries into the ones provided by dictionary
        for i in possibleWordDifficulties:
            __difficultyList.append(config.CEFR_LEVELS.get(i))

        # sort by largest
        __difficultyList.sort()
       
        # convert back to dictionary key
        for i in config.CEFR_LEVELS:
            
            # if the selected difficulty level equals one of the dictionary entries
            try:
                if __difficultyList[__WhereToLook] == config.CEFR_LEVELS.get(i):
                    # assign the string to that list
                    for __currentlySelectedCEFRLevel, __currentlySelectedCEFRLevelInt in config.CEFR_LEVELS.items():
                        if __difficultyList[__WhereToLook] == __currentlySelectedCEFRLevelInt:
                            __difficultyList[__WhereToLook] = __currentlySelectedCEFRLevel
                            break
            except IndexError:
                break

        if __difficultyList[__WhereToLook] is int:
            print(
                f"Something went wrong. CEFR level could not be found for \"{__difficultyList[0]}\".")
            pass
        else:
            print(f"Difficulty of \"{searchTerm}\" is: {__difficultyList[__WhereToLook]}.")

        return __difficultyList[__WhereToLook]

        # return it

    # if the list is not empty
    if searchTerm:
        searchTerm = searchTerm.lower()

        if searchTerm in OFFLINE_DICTIONARY:
            # we got them ladies and gentlemen
            __lookup = True
            # get the difficulty from the dictionary
            wordDifficulty = OFFLINE_DICTIONARY.get(searchTerm)
            print(f"Found \"{searchTerm}\" in offline dictionary.\tDifficulty: {wordDifficulty}\n")

        else:
            print(f"\"{searchTerm}\" not found in offline dictionary. Looking up online...")
            # get the HTML
            rawHTML = requests.get(
                STATIC_WEBPAGE + searchTerm, headers={'User-Agent': 'Mozilla/5.0'})

            # soupify it
            betterHTML = BeautifulSoup(rawHTML.content, 'html.parser')

            # find the CSS tag we need
            possibleWordDifficulties = betterHTML.select('.epp-xref.dxref')

            # isolate what interests us
            possibleWordDifficulties = __Isolate_Word_Difficulty(
                possibleWordDifficulties)

            # call the function to check how difficult the word is
            Check_How_Many_Levels()

            # get the desired difficulty level as stated by CHOOSE_HIGHEST_DIFFICULTY
            try:
                wordDifficulty = Choose_Difficulty_Level()
            except IndexError:
                print(f"No online difficulties for \"{searchTerm}\".")
                wordDifficulty = False
                FileWriter.Write_To_File(searchTerm, False)
                # return wordDifficulty

            # if wordDifficulty is returned as false, remove certain suffixes and return those to the offline dictionary

        if not wordDifficulty:
            print(f"\nFinding \"{searchTerm}\" by removing suffixes...")
            wordDifficulty = suffix.if_ending(searchTerm)
            

                

    # GTFO if empty.

    else:
        print("Invalid input.")
        return False

    # write to the file
    if __lookup == False:
        FileWriter.Write_To_File(searchTerm, wordDifficulty)

        # return the word difficulty to main?

    return wordDifficulty
    
