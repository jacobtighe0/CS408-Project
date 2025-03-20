import copy
import math

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