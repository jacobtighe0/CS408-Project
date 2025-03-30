import unittest
from unittest.mock import patch, MagicMock
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
    
    # Test to check if bluff is triggered when random value is below bluff chance
    @patch('game.player.simpleAI.random')
    def test_should_bluff_trigger(self, mock_random):
        self.ai.bluff_chance = 0.2
        self.ai.hand_strength = 0
        mock_random.return_value = 0.1
        initial_hand_strength = self.ai.hand_strength
        self.ai.should_bluff()
        self.assertGreater(self.ai.hand_strength, initial_hand_strength)

    # Test to check if bluff is not triggered when random value is above bluff chance
    @patch('game.player.simpleAI.random')
    def test_should_not_bluff(self, mock_random):
        self.ai.bluff_chance = 0.2
        self.ai.hand_strength = 0
        mock_random.return_value = 0.3
        initial_hand_strength = self.ai.hand_strength
        self.ai.should_bluff()
        self.assertEqual(self.ai.hand_strength, initial_hand_strength)

    # Test for bluff when hand strength is low and bluff chance is high
    @patch('game.player.simpleAI.random')
    def test_should_bluff_high_chance_with_low_hand_strength(self, mock_random):
        self.ai.bluff_chance = 0.9
        self.ai.hand_strength = 0
        mock_random.return_value = 0.1
        initial_hand_strength = self.ai.hand_strength
        self.ai.should_bluff()
        self.assertGreater(self.ai.hand_strength, initial_hand_strength)

    # Test for bluff when bluff chance is zero
    @patch('game.player.simpleAI.random')
    def test_bluff_chance_zero(self, mock_random):
        self.ai.bluff_chance = 0.0
        self.ai.hand_strength = 0.4
        mock_random.return_value = 0.1
        initial_hand_strength = self.ai.hand_strength
        self.ai.should_bluff()
        self.assertEqual(self.ai.hand_strength, initial_hand_strength)

    # Test when bluff chance equals hand strength, should bluff if random is below chance
    @patch('game.player.simpleAI.random')
    def test_should_bluff_when_hand_strength_equals_bluff_chance(self, mock_random):
        self.ai.bluff_chance = 0.5
        self.ai.hand_strength = 0.5
        mock_random.return_value = 0.4
        initial_hand_strength = self.ai.hand_strength
        self.ai.should_bluff()
        self.assertGreater(self.ai.hand_strength, initial_hand_strength)
    
if __name__ == '__main__':
    unittest.main()
