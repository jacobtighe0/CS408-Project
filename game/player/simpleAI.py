import math
from random import randint
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

    def setGame(self, game):
        self.game = game

    def raising(self, raising = None):
        """
        Function for getting random input
        :returns: TODO

        """
        print(self.money, self.debt)
        #return randint(1, self.money - self.debt) if self.money > self.debt else 0.0 
        return randint(1, 1 + int((self.money - self.debt)/3)) if self.money > self.debt else 0.0 

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
        
    def options(self):
        options = { 0: self.quit,
                    1: self.checkBet ,
                    2: self.callBet , 
                    3: self.raiseBet , 
                    4: self.foldBet , 
                    5: self.allin,
                    }
            
        while True:
            chance = 0 # AI's chance of winning (initially 0)
            if self.game is not None:

                loops = 1000 # Number of simulations
                mcts = MCTS(self)
                i = 0
                while i<loops:
                    mcts.selection()
                    i+=1
                chance = (mcts.root.wins/loops)*100 # AI's chance of winning

                print("AI chance of winning:") # --- FOR TESTING ONLY ---
                print(chance)

            if self.bet == -1:
                if chance < 20:
                    action = 4
                else:
                    action = 5
            else:
                if chance < 10:
                    action = 4
                elif chance < 50:
                    if (self.checkBet() == False):
                        action = 2
                    else:
                        action = 1
                elif chance < 90:
                    if self.prevAction == 3: # Stops AI from raising infinitely
                        if (self.checkBet() == False):
                            action = 2
                        else:
                            action = 1
                    else:
                        action = 3
                else:
                    action = 5
                
            choosed = options[action]()
            self.prevAction = action
            if choosed:
                return choosed
            else:
                continue
    
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

class Node:

    def __init__(self, state):
        self.parent = None
        self.children = []
        self.visits = 0
        self.value = 0
        self.wins = 0
        self.state = state

class MCTS:
    
    def __init__(self, AI):
        self.root = Node(copy.deepcopy(AI.game))
        self.AIName = AI.name
        self.game = AI.game

    def selection(self):
        if self.root.children == []:
            self.expand(self.root)
        else:
            highest_value_node = Node(None)
            for node in self.root.children:
                if node.visits == 0:
                    node.value = float('inf')
                else:
                    C = math.sqrt(2)
                    node.value = node.value / node.visits + C * math.sqrt(math.log(node.parent.visits + 1) / node.visits) 
                if node.value > highest_value_node.value:
                    highest_value_node = node
            self.expand(highest_value_node)
    
    def expand(self, node):
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
        simGame = copy.deepcopy(node.state)

        simGame.dealer.cardControl.shuffle()
        while len(simGame.dealer.cardControl.tableCards) < 5:
            simGame.dealer.cardControl.drawTable()

        winners = simGame.dealer.chooseWinner(simGame.players)
        x = [winner.name for winner in winners]
        if x[0] == self.AIName:
            self.backpropagate(node, 1)
        else:
            self.backpropagate(node, 0)

    def backpropagate(self, node, result):
        node.visits += 1
        node.wins += result
        if node.parent is not None:
            self.backpropagate(node.parent, result)

        
