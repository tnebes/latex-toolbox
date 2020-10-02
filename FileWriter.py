import os
import json


# where is the file
FILE_NAME = "wordDifficulties.txt"
FILE_DIRECTORY = "./WordDictionary/"

# where is your daddy and what does he do
FILE_DIRECTORY_NAME = FILE_DIRECTORY + FILE_NAME

# DEBUG
__dictionary = {}

def Write_Dictionary_To_File(dictionary):
    with open(FILE_DIRECTORY_NAME, "w") as theFile:
        theFile.write((json.dumps(dictionary)))

def Read_From_Dictionary():
    with open(FILE_DIRECTORY_NAME, "r") as theFile:
        return json.load(theFile)

def Write_To_File(word, difficulty):
    __dictionary = Read_From_Dictionary()
    __dictionary.update({word : difficulty})
    print(f"Added \"{word}\" : {difficulty} to dictionary.\n")
    Write_Dictionary_To_File(__dictionary)
    __dictionary = {}


try:
    with open(FILE_DIRECTORY_NAME, "r") as theFile:
        theFile.close()
except FileNotFoundError:
    try:
        os.mkdir(FILE_DIRECTORY)
    except FileExistsError:
        pass
    with open(FILE_DIRECTORY_NAME, "w") as theFile:  
        Write_Dictionary_To_File(__dictionary)
    theFile.close()
try:
    Read_From_Dictionary()
except:
    Write_Dictionary_To_File(__dictionary)


