import unittest
from custom_logger.custom_logger import CustomLogger

from day_7.main import CardType, Day7Solver, Hand

logger = CustomLogger(__name__).get_logger()


class TestDay7Solver(unittest.TestCase):
    def test_can_solve_first_problem(self):
        result = Day7Solver().solve_first_problem('tests/resources/test_day_7.txt')
        self.assertEqual(result, 6440)

    def test_can_solve_second_problem(self):
        result = Day7Solver().solve_second_problem('tests/resources/test_day_7.txt')

        self.assertEqual(result, 5905)

    def test_returns_correct_type(self):
        hand1 = Hand('AAAAA', 1)
        hand2 = Hand('AA8AA', 2)
        hand3 = Hand('23332', 3)
        hand4 = Hand('TTT98', 4)
        hand5 = Hand('23432', 5)
        hand6 = Hand('A23A4', 6)
        hand7 = Hand('23456', 7)

        self.assertEqual(hand1.type, CardType.FIVE_OF_A_KIND)
        self.assertEqual(hand2.type, CardType.FOUR_OF_A_KIND)
        self.assertEqual(hand3.type, CardType.FULL_HOUSE)
        self.assertEqual(hand4.type, CardType.THREE_OF_A_KIND)
        self.assertEqual(hand5.type, CardType.TWO_PAIR)
        self.assertEqual(hand6.type, CardType.ONE_PAIR)
        self.assertEqual(hand7.type, CardType.HIGH_CARD)

    def test_returns_correct_card_with_joker(self):
        hand1 = Hand('QJJQ2', 1, joker=True)
        hand2 = Hand('AAJAA', 2, joker=True)
        hand3 = Hand('23J32', 3, joker=True)
        hand4 = Hand('JJJJJ', 4, joker=True)
        hand5 = Hand('JKKJJ', 5, joker=True)

        self.assertEqual(hand1.type, CardType.FOUR_OF_A_KIND)
        self.assertEqual(hand2.type, CardType.FIVE_OF_A_KIND)
        self.assertEqual(hand3.type, CardType.FULL_HOUSE)
        self.assertEqual(hand4.type, CardType.FIVE_OF_A_KIND)
        self.assertEqual(hand5.type, CardType.FIVE_OF_A_KIND)
        logger.debug(hand5.repetitions)

    def test_compare_jokers(self):
        hand1 = Hand('JKKK2', 1, joker=True)
        hand2 = Hand('QQQQ2', 2, joker=True)

        self.assertEqual(Day7Solver().compare(hand1, hand2), -1)
