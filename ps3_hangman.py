# Hangman game
# Idea : MIT
# Implementation / Author : Kunst, finished on 25.09.2016

# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)

import random
import string
import time

WORDLIST_FILENAME = "words.txt"

def loadWords():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def chooseWord(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code
# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = loadWords()


def isWordGuessed(secretWord, lettersGuessed):
    '''
    secretWord: string, the word the user is guessing
    lettersGuessed: list, what letters have been guessed so far
    returns: boolean, True if all the letters of secretWord are 
    in lettersGuessed; False otherwise
    '''
    def is_empty(any_structure):
        '''
        input: Any structured data type
        If the data structure is empty, "returns" True.  
        Else, "returns" False.
        '''
        if any_structure: # if it's != 0, so differs from empty
            return False # it is false that the structure's empty
        else:
            return True
        
    # Transform each iterable into a set so we can use
    # set operations on unique letters from two words
    
    return is_empty( set(secretWord) - set(lettersGuessed) )
    # obtain the set of letters that are in secretWord 
    # but are not in lettersGuessed and see if it's void,
    # that meaning we can return True. Else, return False.


def getGuessedWord(secretWord, lettersGuessed):
    '''
    secretWord: string, the word the user is guessing
    lettersGuessed: list, what letters have been guessed so far
    returns: string, comprised of letters and underscores that
    represents what letters in secretWord have been guessed so far.
    '''
    
    # The set of letters that are in secretWord but 
    # are not in lettersGuessed :
    omitted = set(secretWord) - set(lettersGuessed)
    
    """ Set and loop Method nr. 1 :
    guessedWord = "" # an empty string to be appended to
    
    # Iterate over every letter of the secretWord and check:
    for letter in secretWord:
        if letter in omitted: # if it was not discovered ...
            guessedWord += "_" + " "
        else: # or if it was discovered ...
            guessedWord += letter + " "
            
    return guessedWord
    """
    
    # Make a dict : every key which is the Unicode ordinal(int)
    # of evey char in the omitted set, is bound to "_" .
    # Using that translation table we now translate the "complete"
    # string, replacing using the translation method. We get
    # a new string ...
    currentWord = secretWord.translate({ord(x) : '_' for x in omitted})
    
    # We return that string but joining whitespace between
    # the characters composing it :
    return " ".join(currentWord)


def delayedPrint (string):
    '''
    input: any string
    returns: None, constructs & prints simultaneously the string given
    with a small but visible delay
    '''
    for letter in string:
        time.sleep(0.1)
        print(letter, end="", flush=True)



"""
    'Main()' hangman() FUNCTION DEFINITION : 
"""

def hangman(secretWord):
    '''
    secretWord: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many 
      letters the secretWord contains.

    * Ask the user to supply one guess (i.e. letter) per round.

    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computers word.

    * After each round, you should also display to the user the 
      partially guessed word so far, as well as letters that the 
      user has not yet guessed.

    Only if the guess is wrong, one remaining guess is subtracted from
    the total number of guesses(tries) remaining !
    '''
      
    print("\nWelcome to the game Hangman !")
    initialString = "I am thinking of a word that is {} letters long." \
            .format(len(secretWord))
    delayedPrint(initialString)
    print("\n-------------\n") 
            
    """
    numTries: int, how many TRIES you have LEFT
    lettersGuessed: LIST OF strings, contains only the GOOD GUESSES so far;
                    used as an argument to the function isWordGuessed(...)
    availableLetters: LIST OF strings, contains all the LETTERS you have
                       NOT TRIED so far ...
    """
    # At the begining :
    numTries = 8 # we give you 8 tries
    lettersGuessed = [] # you haven't got any good guesses so far
    availableLetters = list(string.ascii_lowercase) # you haven't tried to guess any
    
    while numTries and not isWordGuessed(secretWord, lettersGuessed) : 
    # while numTries is !=0 and not true that the word is guessed:
        
        time.sleep(3)
        print( "You have {} guesses left".format(numTries) )
        # prints available letters list-style but it looks better ...
        print( "Available Letters:", availableLetters) 
        
        guess = input("Please guess a letter, or the whole word: ").lower()
        
        # Check if you entered something else than a letter:
        if not guess.isalpha():
            print("You have to enter only letters !")
            continue # re-enter loop from the top ...
        # Than check if you tried to guess the whole word:
        if len(guess) > 1:
            if guess == secretWord:
                lettersGuessed = sorted(list(secretWord))
                print("Good guess:", getGuessedWord(secretWord, lettersGuessed))
            else: # wrong guess
                # Decrease number of tries :
                numTries -= 1
                print( "Oops! That is not my word:", \
                    getGuessedWord(secretWord, lettersGuessed) )
                
        # Than ... you only inputed a letter:
        elif guess in availableLetters:
            # Remove guessed letter from availableLetters
            availableLetters.remove(guess)
            if guess in secretWord:
                # Append letter to the lettersGuessed list
                lettersGuessed.append(guess)
                print("Good guess:", getGuessedWord(secretWord, lettersGuessed))
            else: # wrong guess
                # Decrease number of tries :
                numTries -= 1
                print( "Oops! That letter is not in my word:", \
                    getGuessedWord(secretWord, lettersGuessed) )
                    
        else: # you guessed something previously guessed, so we don't penalize :
            print( "Oops! You've already guessed that letter:", \
                    getGuessedWord(secretWord, lettersGuessed) )
                    
        print("------------\n")
        
    # The loop ends, the game is over so check if you win or loose:
    finalString = ""
    if isWordGuessed(secretWord, lettersGuessed):
        finalString = "Congratulations, you won!"
    else:
        finalString = "Sorry, you ran out of guesses. The word was {}." \
            .format(secretWord) 
    delayedPrint(finalString)
            


"""
    'Main()' CALLs SECTION : 
"""

secretWord = chooseWord(wordlist).lower()

hangman(secretWord)
