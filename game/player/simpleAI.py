import math
from random import random, randint
import player.player
import player.simpleAI
import copy
import database as db
from ai.mcts import MCTS

class SimpleAI(player.Player):

    # Initializes the SimpleAI with a name and initial money
    def __init__(self, name = "AI_", money = 500.0):
        self.name = name
        self.money = money
        self.handValue = 0.0
        self.hand = []
        self.deposit = 0.0
        self.bet = 0.0
        self.game = None # Records current game being played
        self.prevAction = None # Records previous action to prevent infinite loops
        self.hand_strength = 0.0
        self.bluff_chance = 0.2

    def setGame(self, game):
        self.game = game

    def raising(self, raising = None):
        """
        :returns: The amount of money the AI should raise by
        """
        return int((self.money - self.debt) * self.bet_size()) if self.money > self.debt else 0.0
    
    def bet_size(self):
        """
        Calculates how much the AI should bet
        
        :returns: a percent
        """
        if self.hand_strength < 0.25:
            return 0.07 + (random() * 0.05)  # (7% to 12%) - Weak hand
        elif self.hand_strength < 0.6:
            return 0.2 + ((self.hand_strength - 0.3) * 0.3)  # (20% to 26%) - Okay hand
        elif self.hand_strength < 0.8:
            return 0.3 + ((self.hand_strength - 0.5) * 0.4)  # (30% to 38%) - Good hand
        else:
            return 0.4 + ((self.hand_strength - 0.75) * 0.6)  # (40% to 85%) - Strong hand

    def checkBet(self):
        """
        Checks only if difference between deposit and bet is zero
        
        :returns: True/False based on if you can check or not
        """
        if self.debt:
            return False
        else:
            print("{} checks.\n".format(self.name))
            return (self.bet,0)
        
    def calculate_ev(self):
        """
        Calculates the expected value (EV) for calling and raising.

        :returns: Expected values for calling and raising.
        """

        # EV calculation for calling
        call_cost = self.bet - self.deposit
        ev_call = (self.hand_strength * (self.bet + self.deposit)) - ((1 - self.hand_strength) * call_cost)

        # EV calculation for raising
        raise_amount = self.raising()
        if raise_amount > 0:
            bet_after_raising = self.bet + raise_amount
            ev_raise = (self.hand_strength * bet_after_raising) - ((1 - self.hand_strength) * raise_amount)
        else:
            ev_raise = float('-inf') # Raising is not an option

        return ev_call, ev_raise
    
    def player_model(self):
        """
        Allows AI to adapt to player's playstyle
        """
        player_name = self.game.dealer.playerControl.players[0].name
        player_stats = db.get_player_stats(player_name)

        # For each action; calculates how often the player makes that action
        player_actions = {"checks": player_stats[4] / player_stats[9], # No of checks / No of total actions
                          "calls": player_stats[5] / player_stats[9],
                          "raises": player_stats[6] / player_stats[9],
                          "folds": player_stats[7] / player_stats[9],
                          "all_ins": player_stats[8] / player_stats[9],
                          }
        
        # If player checks a lot, bluff more
        if player_actions["checks"] > 0.5:
            self.bluff_chance = min(self.bluff_chance * 1.2, 0.75)
            self.hand_strength = min(self.hand_strength * 1.1, 1.0)

        # If player calls a lot, bluff less
        if player_actions["calls"] > 0.4:
            self.bluff_chance = min(self.bluff_chance * 0.5, 0.75)
            self.hand_strength = min(self.hand_strength * 0.9, 1.0)

        # If player raises a lot, bluff less. Else, bluff more
        if player_actions["raises"] > 0.15:
            self.bluff_chance = min(self.bluff_chance * 0.5, 0.75)
            self.hand_strength = min(self.hand_strength * 0.8, 1.0)
        elif player_actions["raises"] < 0.1:
            self.bluff_chance = min(self.bluff_chance * 2, 0.75)
            self.hand_strength = min(self.hand_strength * 1.2, 1.0)

        # If player folds a lot, bluff more
        if player_actions["folds"] > 0.2:
            self.bluff_chance = min(self.bluff_chance * 2, 0.75)
        
        # If player goes all-in a lot, bluff less. Else, bluff more
        if player_actions["all_ins"] > 0.1:
            self.bluff_chance = min(self.bluff_chance * 0.5, 0.75)
            self.hand_strength = min(self.hand_strength * 0.85, 1.0)
        elif player_actions["all_ins"] < 0.05:
            self.bluff_chance = min(self.bluff_chance * 1.5, 0.75)
    
    def should_bluff(self):
        """
        AI decides whether to bluff or not
        """
        if random() < self.bluff_chance:
            self.hand_strength = self.hand_strength + ((1.0 - self.hand_strength) / 3)

    def options(self):
        # All the options available to each player
        options = { 0: self.quit,
                    1: self.checkBet ,
                    2: self.callBet , 
                    3: self.raiseBet , 
                    4: self.foldBet , 
                    5: self.allin,
                    }
        # Print statement to tell the human player that the AI is currently "thinking"
        print(f"Waiting on {self.name}...")

        while True:
            if self.game is not None:

                player_name = self.game.dealer.playerControl.players[0].name
                player_stats = db.get_player_stats(player_name)
                player_elo = player_stats[10]

                loops = 5000 # Number of simulations
                mcts = MCTS(self) # Instance of MCTS class
                i = 0
                while i<loops:
                    mcts.run() # Run MCTS simulation
                    i+=1
                self.hand_strength = (mcts.root.wins/loops) # AI's chance of winning
                self.bluff_chance = 0.2 # Resets bluff chance

                if player_elo >= 100: # Medium difficulty
                    self.player_model()
                if player_elo >= 200: # Hard difficulty
                    self.should_bluff()

                ev_call, ev_raise = self.calculate_ev()
                
            if ev_call > ev_raise and ev_call > 0:
                action = 2 # Call
            elif ev_raise > ev_call and ev_raise > 0:
                action = 3 # Raise
            else:
                if self.checkBet():
                    action = 1 # Check
                else:
                    action = 4 # Fold
                
            choosed = options[action]() # Chosen action
            self.prevAction = action
            if choosed:
                return choosed
            else:
                continue

        
