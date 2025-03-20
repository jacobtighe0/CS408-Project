"""
File: questions.py
Author: dave
Github: https://github.com/davidus27
Description: The CLI of the game on terminal. Collects input from the player and sends it to the main game logic (poker.py)
"""
   
def nameQuest():
    """
    Asks about name of the player
    :returns: entered username
    """
    while True:
        x = input("Enter your username: ")
        if x:
            return x
        print("Please enter a valid username.")

def diffQuest():
    """
    Asks about difficulty of game
    :returns: difficulty
    """
    inputList = ["easy", "normal", "hard"]
    while True:
        x = input("Choose difficulty (easy/normal/hard): ").lower()
        if x in inputList:
            return x
        print("Please enter a valid difficulty.")    

def info(name, money):
    """
    Printout basic info about player

    :returns: 

    """
    print("Name: {}".format(name))
    print("Balance: {}".format(money))

def raising(minimum, maximum):
    """
    Decorator
    Asks the player how much will he raise the pot
    :returns: TODO

    """
    #return raised if raised == type(int) and raised >= minimal and raised <= maximum else False
    return int(input("How much do you want to raise [{0}-{1}]: ".format(maximum, minimum)))

def numQuest():
    """
    Decorator
    Asks about number of players
    :returns: numPlayers 

    """
    while True:
        x = input("How many players do you want to play with? (1-9): ")
        try:
            numPlayers = int(x)
            if 1 <= numPlayers <= 9:
                return numPlayers
        except ValueError:
            pass
        print("Please enter a number between 1 and 9.")


 

