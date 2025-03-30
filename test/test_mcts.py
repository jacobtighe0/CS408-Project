import unittest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'game'))
from game.player.simpleAI import SimpleAI
from game.ai.mcts import MCTS

class TestMCTS(unittest.TestCase):

    def setUp(self):
        self.ai = SimpleAI()
        self.ai.game = MagicMock()
        self.ai.game.dealer = MagicMock()
        self.ai.game.dealer.playerControl = MagicMock()
        self.ai.game.dealer.playerControl.players = [MagicMock(name="player1")]
        self.ai.game.dealer.playerControl.players[0].name = "player1"
        self.ai.name = "player1"
        self.ai.game.dealer.chooseWinner = MagicMock(return_value=[self.ai.game.dealer.playerControl.players[0]])

    # Test to show that MCTS functions correctly, and adjusts the AI's hand strength
    def test_mcts(self):
        self.ai.hand = [("Ace", "Spades"), ("Ace", "Clubs")]
        self.ai.game.dealer.cardControl.tableCards = [(10, "Hearts"),("King", "Spades"),("Ace", "Diamonds"),(3, "Clubs"),("Queen", "Hearts")]
        self.ai.hand_strength = 0.0
        initial_hand_strength = self.ai.hand_strength

        mcts = MCTS(self.ai)
        i = 0
        loops = 100
        while i<loops:
            mcts.run()
            i+=1

        self.ai.hand_strength = (mcts.root.wins/loops) # AI's chance of winning
        self.assertGreater(self.ai.hand_strength, initial_hand_strength)
