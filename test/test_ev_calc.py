import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'game'))
from game.player.simpleAI import SimpleAI

class TestEVCalc(unittest.TestCase):
    
    def setUp(self):
        self.ai = SimpleAI()
        self.ai.hand_strength = 0.7
        self.ai.bet = 100
        self.ai.deposit = 50

    def test_ev_call(self):
        call_cost = self.ai.bet - self.ai.deposit
        expected_ev_call = (self.ai.hand_strength * (self.ai.bet + self.ai.deposit)) - ((1 - self.ai.hand_strength) * call_cost)
        actual_ev_call, _ = self.ai.calculate_ev()
        self.assertEqual(expected_ev_call, actual_ev_call)

    def test_ev_raise(self):
        self.ai.raising = lambda: 50
        raise_amount = self.ai.raising()
        bet_after_raising = self.ai.bet + raise_amount
        expected_ev_raise = (self.ai.hand_strength * bet_after_raising) - ((1 - self.ai.hand_strength) * raise_amount)
        _, actual_ev_raise = self.ai.calculate_ev()
        self.assertEqual(expected_ev_raise, actual_ev_raise)

    def test_ev_raise_no_raise(self):
        self.ai.raising = lambda: 0
        _, actual_ev_raise = self.ai.calculate_ev()
        self.assertEqual(actual_ev_raise, float('-inf'))

    def test_ev_call_with_zero_hand_strength(self):
        self.ai.hand_strength = 0.0
        call_cost = self.ai.bet - self.ai.deposit
        expected_ev_call = (self.ai.hand_strength * (self.ai.bet + self.ai.deposit)) - ((1 - self.ai.hand_strength) * call_cost)
        actual_ev_call, _ = self.ai.calculate_ev()
        self.assertEqual(expected_ev_call, actual_ev_call)

    def test_ev_call_with_full_hand_strength(self):
        self.ai.hand_strength = 1.0
        call_cost = self.ai.bet - self.ai.deposit
        expected_ev_call = (self.ai.hand_strength * (self.ai.bet + self.ai.deposit)) - ((1 - self.ai.hand_strength) * call_cost)
        actual_ev_call, _ = self.ai.calculate_ev()
        self.assertEqual(expected_ev_call, actual_ev_call)

    def test_ev_call_no_bet(self):
        self.ai.bet = 0.0
        call_cost = self.ai.bet - self.ai.deposit
        expected_ev_call = (self.ai.hand_strength * (self.ai.bet + self.ai.deposit)) - ((1 - self.ai.hand_strength) * call_cost)
        actual_ev_call, _ = self.ai.calculate_ev()
        self.assertEqual(expected_ev_call, actual_ev_call)

    def test_ev_call_high_bet(self):
        self.ai.bet = 1000.0
        call_cost = self.ai.bet - self.ai.deposit
        expected_ev_call = (self.ai.hand_strength * (self.ai.bet + self.ai.deposit)) - ((1 - self.ai.hand_strength) * call_cost)
        actual_ev_call, _ = self.ai.calculate_ev()
        self.assertEqual(expected_ev_call, actual_ev_call)

    def test_ev_call_zero_deposit(self):
        self.ai.deposit = 0.0
        call_cost = self.ai.bet - self.ai.deposit
        expected_ev_call = (self.ai.hand_strength * (self.ai.bet + self.ai.deposit)) - ((1 - self.ai.hand_strength) * call_cost)
        actual_ev_call, _ = self.ai.calculate_ev()
        self.assertEqual(expected_ev_call, actual_ev_call)

    def test_ev_call_negative_hand_strength(self):
        self.ai.hand_strength = -0.5
        call_cost = self.ai.bet - self.ai.deposit
        expected_ev_call = (self.ai.hand_strength * (self.ai.bet + self.ai.deposit)) - ((1 - self.ai.hand_strength) * call_cost)
        actual_ev_call, _ = self.ai.calculate_ev()
        self.assertEqual(expected_ev_call, actual_ev_call)

    def test_ev_call_full_strength_no_bet(self):
        self.ai.hand_strength = 1.0
        self.ai.bet = 0.0
        call_cost = self.ai.bet - self.ai.deposit
        expected_ev_call = (self.ai.hand_strength * (self.ai.bet + self.ai.deposit)) - ((1 - self.ai.hand_strength) * call_cost)
        actual_ev_call, _ = self.ai.calculate_ev()
        self.assertEqual(expected_ev_call, actual_ev_call)

    def test_ev_raise_large_bet(self):
        self.ai.bet = 1000.0
        self.ai.raising = lambda: 500.0
        raise_amount = self.ai.raising()
        bet_after_raising = self.ai.bet + raise_amount
        expected_ev_raise = (self.ai.hand_strength * bet_after_raising) - ((1 - self.ai.hand_strength) * raise_amount)
        _, actual_ev_raise = self.ai.calculate_ev()
        self.assertEqual(expected_ev_raise, actual_ev_raise)

    def test_ev_raise_low_hand_strength(self):
        self.ai.hand_strength = 0.2
        self.ai.raising = lambda: 50.0
        raise_amount = self.ai.raising()
        bet_after_raising = self.ai.bet + raise_amount
        expected_ev_raise = (self.ai.hand_strength * bet_after_raising) - ((1 - self.ai.hand_strength) * raise_amount)
        _, actual_ev_raise = self.ai.calculate_ev()
        self.assertEqual(expected_ev_raise, actual_ev_raise)

    def test_ev_raise_large_raise(self):
        self.ai.raising = lambda: 1000.0
        raise_amount = self.ai.raising()
        bet_after_raising = self.ai.bet + raise_amount
        expected_ev_raise = (self.ai.hand_strength * bet_after_raising) - ((1 - self.ai.hand_strength) * raise_amount)
        _, actual_ev_raise = self.ai.calculate_ev()
        self.assertEqual(expected_ev_raise, actual_ev_raise)

    def test_ev_call_equal_ev_raise(self):
        self.ai.hand_strength = 0.5
        self.ai.bet = 100.0
        self.ai.deposit = 50.0
        self.ai.raising = lambda: 50.0
        expected_ev_call = (self.ai.hand_strength * (self.ai.bet + self.ai.deposit)) - ((1 - self.ai.hand_strength) * (self.ai.bet - self.ai.deposit))
        expected_ev_raise = (self.ai.hand_strength * (self.ai.bet + self.ai.raising())) - ((1 - self.ai.hand_strength) * self.ai.raising())
        actual_ev_call, actual_ev_raise = self.ai.calculate_ev()
        self.assertEqual(expected_ev_call, actual_ev_call)
        self.assertEqual(expected_ev_raise, actual_ev_raise)

    def test_ev_raise_small_raise(self):
        self.ai.raising = lambda: 10.0
        raise_amount = self.ai.raising()
        bet_after_raising = self.ai.bet + raise_amount
        expected_ev_raise = (self.ai.hand_strength * bet_after_raising) - ((1 - self.ai.hand_strength) * raise_amount)
        _, actual_ev_raise = self.ai.calculate_ev()
        self.assertEqual(expected_ev_raise, actual_ev_raise)
