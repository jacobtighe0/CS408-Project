import unittest
from unittest.mock import patch, MagicMock
import random
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'game'))
from game.player.simpleAI import SimpleAI

class TestBluff(unittest.TestCase):

    def setUp(self):
        self.ai = SimpleAI()
        self.ai.game = MagicMock()
        self.ai.game.dealer = MagicMock()
        self.ai.game.dealer.playerControl = MagicMock()
        self.ai.game.dealer.playerControl.players = [MagicMock(name='player1')]
        self.ai.game.dealer.playerControl.players[0].name = "Player1"
    
    @patch('game.player.simpleAI.random')
    def test_should_bluff_trigger(self, mock_random):
        self.ai.bluff_chance = 0.2
        self.ai.hand_strength = 0
        mock_random.return_value = 0.1
        initial_hand_strength = self.ai.hand_strength
        self.ai.should_bluff()
        self.assertGreater(self.ai.hand_strength, initial_hand_strength)

    @patch('game.player.simpleAI.random')
    def test_should_not_bluff(self, mock_random):
        self.ai.bluff_chance = 0.2
        self.ai.hand_strength = 0
        mock_random.return_value = 0.3
        initial_hand_strength = self.ai.hand_strength
        self.ai.should_bluff()
        self.assertEqual(self.ai.hand_strength, initial_hand_strength)

    @patch('game.player.simpleAI.random')
    def test_should_bluff_with_hand_strength(self, mock_random):
        self.ai.bluff_chance = 0.5
        self.ai.hand_strength = 0.4
        mock_random.return_value = 0.2
        initial_hand_strength = self.ai.hand_strength
        self.ai.should_bluff()
        self.assertGreater(self.ai.hand_strength, initial_hand_strength)

    @patch('game.player.simpleAI.random')
    def test_bluff_chance_zero(self, mock_random):
        self.ai.bluff_chance = 0.0
        self.ai.hand_strength = 0.4
        mock_random.return_value = 0.1
        initial_hand_strength = self.ai.hand_strength
        self.ai.should_bluff()
        self.assertEqual(self.ai.hand_strength, initial_hand_strength)

    @patch('game.player.simpleAI.random')
    def test_bluff_chance_one(self, mock_random):
        self.ai.bluff_chance = 1.0
        self.ai.hand_strength = 0.4
        mock_random.return_value = 0.1
        initial_hand_strength = self.ai.hand_strength
        self.ai.should_bluff()
        self.assertGreater(self.ai.hand_strength, initial_hand_strength)

    @patch('game.player.simpleAI.random')
    def test_should_bluff_high_chance_with_low_hand_strength(self, mock_random):
        self.ai.bluff_chance = 0.9
        self.ai.hand_strength = 0
        mock_random.return_value = 0.1
        initial_hand_strength = self.ai.hand_strength
        self.ai.should_bluff()
        self.assertGreater(self.ai.hand_strength, initial_hand_strength)

    @patch('game.player.simpleAI.random')
    def test_should_not_bluff_high_hand_strength_with_low_chance(self, mock_random):
        self.ai.bluff_chance = 0.1
        self.ai.hand_strength = 0.9
        mock_random.return_value = 0.2
        initial_hand_strength = self.ai.hand_strength
        self.ai.should_bluff()
        self.assertEqual(self.ai.hand_strength, initial_hand_strength)

    @patch('game.player.simpleAI.random')
    def test_should_bluff_when_hand_strength_equals_bluff_chance(self, mock_random):
        self.ai.bluff_chance = 0.5
        self.ai.hand_strength = 0.5
        mock_random.return_value = 0.4
        initial_hand_strength = self.ai.hand_strength
        self.ai.should_bluff()
        self.assertGreater(self.ai.hand_strength, initial_hand_strength)

    @patch('game.player.simpleAI.random')
    def test_should_bluff_when_random_equals_bluff_chance(self, mock_random):
        self.ai.bluff_chance = 0.5
        self.ai.hand_strength = 0.4
        mock_random.return_value = 0.5
        initial_hand_strength = self.ai.hand_strength
        self.ai.should_bluff()
        self.assertGreaterEqual(self.ai.hand_strength, initial_hand_strength)

    @patch('game.player.simpleAI.random')
    def test_should_not_bluff_when_bluff_chance_zero_and_random_greater_than_zero(self, mock_random):
        self.ai.bluff_chance = 0.0
        self.ai.hand_strength = 0.4
        mock_random.return_value = 0.5
        initial_hand_strength = self.ai.hand_strength
        self.ai.should_bluff()
        self.assertEqual(self.ai.hand_strength, initial_hand_strength)





if __name__ == '__main__':
    unittest.main()
