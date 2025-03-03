import math
from random import random, randint
import player.player
import player.simpleAI
import copy

class SimpleAI(player.Player):

    def __init__(self, name = "simpleAI", money = 500.0):
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
        Function for getting random input
        :returns: TODO

        """
        print(self.money, self.debt)
        return int((self.money - self.debt) * self.bet_size()) if self.money > self.debt else 0.0
    
    def bet_size(self):
        
        if self.hand_strength > .75:
            return .75
        elif self.hand_strength > .50:
            return .50
        else:
            return .25

    def checkBet(self):
        """
        Checks only if difference between deposit and bet is zero
        
        :returns: True/False based on if you can check or not
        """
        if self.debt:
            return False
        else:
            print("{} check".format(self.name))
            return (self.bet,0)
        
    def calculate_ev(self): # Calculates expected values
        raise_amount = self.raising()
        call_cost = self.bet - self.deposit
        after_raise = self.bet + raise_amount

        ev_call = (self.hand_strength * (self.bet + self.deposit)) - ((1 - self.hand_strength) * call_cost)
        ev_raise = (self.hand_strength * after_raise) - ((1 - self.hand_strength) * raise_amount)

        return ev_call, ev_raise
    
    def should_bluff(self):
        if random() < self.bluff_chance:
                print("(BLUFFING) - prev hand strength:", self.hand_strength) # --- FOR TESTING ONLY ---
                self.hand_strength = min(self.hand_strength * 1.5, 1.0) # Makes sure hand_strength doesn't exceed 1.0
    
    def options(self):
        options = { 0: self.quit,
                    1: self.checkBet ,
                    2: self.callBet , 
                    3: self.raiseBet , 
                    4: self.foldBet , 
                    5: self.allin,
                    }
            
        while True:
            if self.game is not None:

                loops = 5000 # Number of simulations
                mcts = MCTS(self)
                i = 0
                while i<loops:
                    mcts.run()
                    i+=1

                self.hand_strength = (mcts.root.wins/loops) # AI's chance of winning
                self.should_bluff() # Decides if AI should bluff
                ev_call, ev_raise = self.calculate_ev()

                print("\033[93mAI chance of winning: " + str(self.hand_strength) + "\033[0m") # --- FOR TESTING ONLY ---
                print("call: ", ev_call, "raise: ", ev_raise) # --- FOR TESTING ONLY ---

            if ev_call > ev_raise and ev_call > 0:
                action = 2
            elif ev_raise > ev_call and ev_raise > 0:
                action = 3
            else:
                if self.checkBet():
                    action = 1
                else:
                    action = 4

            '''
            if self.bet == -1:
                if chance < .20:
                    action = 4
                else:
                    action = 5
            else:
                if chance < .10:
                    action = 4
                elif chance < .50:
                    if (self.checkBet() == False):
                        action = 2
                    else:
                        action = 1
                elif chance < .90:
                    if self.prevAction == 3: # Stops AI from raising infinitely
                        if (self.checkBet() == False):
                            action = 2
                        else:
                            action = 1
                    else:
                        action = 3
                else:
                    action = 5
            '''
                
            choosed = options[action]()
            self.prevAction = action
            if choosed:
                return choosed
            else:
                continue
    
    '''
    def simulateGame(self):
        import copy
        simGame = copy.deepcopy(self.game)

        player = simGame.dealer.playerControl.players[0] # Non-AI player
        for c in player.hand:
            simGame.dealer.cardControl.deck.append(c) # Adds player's cards back to deck
        player.hand = []

        simGame.players = simGame.dealer.playerControl.players # Makes sure simGame.players is up-to-date

        simGame.dealer.cardControl.shuffle()
        simGame.dealer.cardControl.dealCard([player])
        simGame.dealer.cardControl.dealCard([player])

        while len(simGame.dealer.cardControl.tableCards) < 5:
            simGame.dealer.cardControl.drawTable()

        winners = simGame.dealer.chooseWinner(simGame.players)
        x = [winner.name for winner in winners]
        if x[0] == self.name:
            return 1
        else:
            return 0
    '''
    
class Node:

    def __init__(self, state):
        self.parent = None
        self.children = []
        self.visits = 0
        self.value = 0
        self.wins = 0
        self.state = state
        self.terminal = False

class MCTS:
    
    def __init__(self, AI):
        self.root = Node(copy.deepcopy(AI.game))
        self.AIName = AI.name
        self.game = AI.game

    def run(self):
        self.randomizeCards() # Randomizes cards for non-AI player
        selected_node = self.selection(self.root, self.root)
        self.expand(selected_node)
    
    def selection(self, node, highest_value_node):
        if node.terminal == False:
            if node.children != []:
                for child in node.children:
                    temp = self.selection(child, highest_value_node)
                    if temp.value > highest_value_node.value:
                        highest_value_node = temp

            if node.visits == 0:
                node.value = float('inf')
            else:
                C = math.sqrt(2)
                parent_visits = node.parent.visits if node.parent else 1
                node.value = node.wins / node.visits + C * math.sqrt(math.log(parent_visits) / node.visits)

            if node.value > highest_value_node.value:
                highest_value_node = node
        return highest_value_node

    def expand(self, node):
        if node.terminal == False:
            new_node = Node(copy.deepcopy(node.state))
            new_node.parent = node

            new_node.state.dealer.cardControl.shuffle()

            if len(new_node.state.dealer.cardControl.tableCards) < 5:
                if len(new_node.state.dealer.cardControl.tableCards) == 0:
                    new_node.state.dealer.cardControl.drawTable()
                    new_node.state.dealer.cardControl.drawTable()
                    new_node.state.dealer.cardControl.drawTable()
                else:
                    new_node.state.dealer.cardControl.drawTable()

            node.children.append(new_node)

            self.simulate(new_node)

    def simulate(self, node):
        node.state.dealer.cardControl.shuffle()
        while len(node.state.dealer.cardControl.tableCards) < 5:
            node.state.dealer.cardControl.drawTable()

        winners = node.state.dealer.chooseWinner(node.state.players)
        x = [winner.name for winner in winners]
        node.terminal = True
        if x[0] == self.AIName:
            self.backpropagate(node, 1)
        else:
            self.backpropagate(node, 0)

    def backpropagate(self, node, result):
        node.visits += 1
        node.wins += result
        if node.parent is not None:
            self.backpropagate(node.parent, result)
        
    def randomizeCards(self):
        for player in self.root.state.dealer.playerControl.players:
            if player.name != self.AIName:
                for c in player.hand:
                    self.root.state.dealer.cardControl.deck.append(c) # Adds player's cards back to deck
                player.hand = []
                self.root.state.players = self.root.state.dealer.playerControl.players # Keeps it up-to-date
                self.root.state.dealer.cardControl.shuffle()
                self.root.state.dealer.cardControl.dealCard([player])
                self.root.state.dealer.cardControl.dealCard([player])

        
