import unittest
import logging
import sys

from day_4.main import Card, CardPile, Day4Solver
from file_reader.file_reader import FileReader

logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)


class TestDay4Solver(unittest.TestCase):
    def test_can_solve_first_problem(self):
        result = Day4Solver().solve_first_problem('tests/resources/test_day_4_1.txt')
        self.assertEqual(result, 13)

    def test_can_solve_second_problem(self):
        result = Day4Solver().solve_second_problem('tests/resources/test_day_4_1.txt')
        self.assertEqual(result, 467835)

    def test_card_value_is_correct(self):
        card1: Card = Day4Solver().parse_card(
            'Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53'
        )
        self.assertEqual(card1.card_value, 8)

        card2 = Day4Solver().parse_card(
            'Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83'
        )
        self.assertEqual(card2.card_value, 1)

        card3 = Day4Solver().parse_card(
            'Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11'
        )
        self.assertEqual(card3.card_value, 0)

    def test_won_correct_number_of_cards(self):
        card1: Card = Day4Solver().parse_card(
            'Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53'
        )
        self.assertEqual(card1.matching_numbers, 4)
        self.assertEqual(Day4Solver().get_winning_cards(card1), [2, 3, 4, 5])

    def test_get_total(self):
        lines = FileReader().get_lines('tests/resources/test_day_4_1.txt')
        cards = [Day4Solver().parse_card(line) for line in lines]
        pile = CardPile(cards)

        self.assertEqual(pile.get_total, 30)

    def test_get_card_wins(self):
        lines = FileReader().get_lines('tests/resources/test_day_4_1.txt')
        cards = [Day4Solver().parse_card(line) for line in lines]
        pile = CardPile(cards)

        total_scratchpads = pile.total_scratchpads
        self.assertEqual(total_scratchpads, 30)
