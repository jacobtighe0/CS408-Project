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
    #print("Name: {}".format(name))
    print("Your balance: {}".format(int(money)))

def raising(minimum, maximum):
    """
    Decorator
    Asks the player how much will he raise the pot
    :returns: TODO

    """
    while True:
        try:
            user_input = int(input("How much do you want to raise? (between {0} and {1}): ".format(minimum, int(maximum))))
            if user_input < minimum or user_input > maximum:
                print("Please enter a number between {0} and {1}.".format(minimum, int(maximum)))
            else:
                return user_input
        except ValueError:
            print("Please enter a valid integer.")

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

def newPlayerInfo():
    """
    Prints out information for new players
    """
    print("\nNew player detected!")
    print("\nDifficulty levels:")
    print("- Easy (0-99): AI makes predictable moves.")
    print("- Medium (100-199): AI adapts to its opponent.")
    print("- Hard (200+): AI starts bluffing.")
    print("\nYou will start on easy.")
    print("Increase your score by winning!")
    input("\nPress Enter to play. ")     

def stats(name, wins, losses, elo, difficulty):
    """
    Prints out player stats
    """
    print(f"Player: {name}\nWins: {wins}\nLosses: {losses}\nScore: {elo} ({difficulty})")



 

