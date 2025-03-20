#!/usr/bin/env python3

import poker
from database import initialise_db, update_player_wins, get_player_stats
from os import system
def main():
    """ 
    Work to create game
    """
    system('cls')
    game = poker.Game()
    initialise_db()
    print("")
    print("Let's play Texas Hold'em!\n")
    allPlayers = game.createPlayers()
    while True:
        #The simple game functioning:
        #Players bets on preflop (before the release of firt three cards)
        #First three cards are released
        #Another beting
        #Turn-fourth card release
        #Another bets
        #River-final card
        #Last beting
        #Showdown-cards are showed (if any players are left)
        print("\n\n\tRound #", game.rounds, end="\n\n") 
        game.players = list(allPlayers)
        player = game.players[0]
        game.dealer.gameOn()
        game.dealer.giveCards()
        game.eachRound()
        #Showdown
        print("\n\t\tShowdown\n")
        game.showdown()
        game.dealer.endGame()
        if len(game.dealer.playerControl.players) == 1:
            print("")
            print("Final winner is:", game.dealer.playerControl.players[0].name)
            print("Money: ", int(game.dealer.playerControl.players[0].money))
            print("")
            win = False
            if game.dealer.playerControl.players[0].name == player.name:
                win = True
            update_player_wins(player.name, win)
            break
        input("Press Enter to continue.")        
        
        game.rounds += 1
        

if __name__ == "__main__":
    main()

