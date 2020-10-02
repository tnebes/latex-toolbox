import ToolboxConfig as config
import WebsiteScraper as scraper

SUFFIXES = ["s", "es", "t", "et", "ing", "d", "ed", "r", "er", "st", "est", "ise", "ize", "ly", "ely", "ss", "ess", "ness", "ible", "able", "n", "en", "ion", "ly"]

SUFFIXES.sort(reverse = True, key = lambda i: len(i))

# make a function that returns a word without a suffix
def if_ending(toBeRemovedSuffixWord):
    # set up the lengths
    __wordWithSuffixLength = len(toBeRemovedSuffixWord)

    # if the suffix is anywhere in the word
    # TODO optimise this
    for __currentSuffix in SUFFIXES:
        if __currentSuffix in toBeRemovedSuffixWord:
            __suffixLength = len(__currentSuffix)
            __suffixPosition = __wordWithSuffixLength - __suffixLength

            # check whether it's at the end by subtracting the length of the word by the length of the current suffix
            if toBeRemovedSuffixWord.find(__currentSuffix) == __suffixPosition:
                wordRoot = toBeRemovedSuffixWord[:__suffixPosition]
                # we send the word back to the word finder.
                return scraper.Find_Word_Difficulty(wordRoot)

                
                


