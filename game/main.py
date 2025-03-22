#!/usr/bin/env python3

import poker
from database import initialise_db, update_player_wins, write_game_results, write_player_stats
from os import system
def main():
    """ 
    Work to create game
    """
    system('cls')
    initialise_db()
    while True:
        game = poker.Game()
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
                elo = -15
                if game.dealer.playerControl.players[0].name == player.name:
                    win = True
                    elo = 25
                update_player_wins(player.name, win, elo)
                write_player_stats("player_stats.txt")
                write_game_results("game_results.txt")
                break
            input("Press Enter to continue.")        
            
            game.rounds += 1

        while True:
            play_again = input("Do you want to play again? (y/n): ").strip().lower()
            if play_again == 'y':
                break  # Continue the game if 'y' is entered
            elif play_again == 'n':
                print("\nGoodbye!\n")
                return  # Exit the game if 'n' is entered
            else:
                print("Invalid input. Please enter 'y' for yes or 'n' for no.")

if __name__ == "__main__":
    main()

