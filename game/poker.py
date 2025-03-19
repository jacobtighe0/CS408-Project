"""
File: poker.py
Author: dave
Github: https://github.com/davidus27
Description: Game is the main Object implementing all the necessary tools for playing. Game is created in function main()
"""
import ui
import dealer
from player import Player, SimpleAI
from database import get_player_stats

class Game(object):
    """
    Creates players based on inputs on call.
    """
    def __init__(self):
        self.rounds = 1
        self.players = []
        self.dealer = dealer.Dealer()

    def createPlayers(self):
        name = ui.nameQuest()
        player_stats = get_player_stats(name)

        if not player_stats: # If player is new, ask for difficulty and number of players
            print("New player detected!")
            difficulty = ui.diffQuest()
            numPlayers = ui.numQuest()
        else: # If player is not new, just ask for number of players, then print their stats
            numPlayers = ui.numQuest()
            print("")
            print(player_stats)
            print(f"Welcome back, {player_stats[1]}! Wins: {player_stats[2]}, Losses: {player_stats[3]}")
            difficulty = "normal"

        money = 500
        return self.dealer.playerControl.createPlayers(name,numPlayers, money, difficulty)

    def controlDeposit(self):
        """
        checks if there are any differences
        :returns: TODO

        """
        deposit = self.players[0].deposit #reference
        for player in self.players[1:]:
            if player.deposit == deposit:
                continue
            else:
                return False
        return True

    def round(self):
        """
        Goes through all players until every player gave same ammount to the pot
        :returns: TODO

        """
        while True:
            players = self.players[:]
            for index,player in enumerate(players[:]):
                record = player.options()
                index = (index+1) % len(self.players) 
                self.players[index].bet = record[0]
                if record[1] == -1:
                    players.remove(player)
                    if len(players) == 1:
                        break
                else:
                    self.dealer.playerControl.pot += record[1]
            
            self.players = players[:] 
            
            if self.isAllIn():
                break
            elif self.controlDeposit():
                break
            else:
                continue
        return self

    def handValues(self):
        return self.dealer.getHandValues(self.players)
    
    def printSituation(self, table=False):
        """
        Prints out whole situation in the game.
        :returns: TODO

        """
        if type(self.players[0]) == Player:
            ui.info(self.dealer.playerControl.players[0].name, self.dealer.playerControl.players[0].money)
            print("Your cards:")
            ui.cards(self.dealer.playerControl.players[0].hand)
            print()

            for player in self.players:
                if isinstance(player, SimpleAI):
                    player.setGame(self)

            if table:
                print("Community cards:")
                ui.cards(table)
                print()

                hands = self.handValues()
                print("You currently have:")
                ui.printValue(hands[0].handValue)
                print()
                
        return self

    def allCards(self):
        """
        Prints hands of all players
        """
        for player in self.players:
            print(player.name, "")
            ui.cards(player.hand)
        return self

    def showdown(self):
        """
        Ending of the round
        :returns: TODO

        """
        print("Community cards:")
        ui.cards(self.dealer.cardControl.tableCards)
        self.allCards()
        
        winners = self.dealer.chooseWinner(self.players)
        x = [winner.name for winner in winners]
        ui.roundWinners(x)

        for player in self.players:
            if isinstance(player, SimpleAI):
                player.setGame(None)

        for w in winners:
            ui.printValue(w.handValue)
        self.dealer.playerControl.givePot(winners)
        return self

    def startPhase(self, phase):
        """
        Goes through one phase part of easy game
        :returns: TODO

        """
        if len(self.players) != 1:
            print("\n\t\t{}\n".format(phase))
            self.printSituation(self.dealer.cardControl.tableCards)
            self.round()
            self.dealer.cardOnTable(phase)
        
    def isAllIn(self):
        """
        Checking all players if someone is allin or not
        :returns: TODO

        """
        for player in self.players:
            if player.bet == -1:
                return True
        return False



    def eachRound(self):
        """TODO: Docstring for function.

        :returns: TODO

        """
        self.dealer.playerControl.ante(self.rounds)
        #Preflop
        self.startPhase("Preflop")
        if self.isAllIn():
            #allin on flop
            return self.dealer.cardOnTable("All-flop")
        else:
            #Flop
            self.startPhase("Flop")
            
        if self.isAllIn():
            #allin on turn
            return self.dealer.cardOnTable("All-turn")
        else:
            #Turn
            self.startPhase("Turn")

