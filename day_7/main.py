from custom_logger.custom_logger import CustomLogger
from file_reader.file_reader import FileReader
from enum import Enum
from functools import cmp_to_key


logger = CustomLogger(__name__).get_logger()


class CardType(Enum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1


class Hand:
    bid: int
    cards: list[str] = []
    joker: bool

    def __init__(self, cards: list[str], bid: int, joker: bool = False):
        if len(cards) != 5:
            error = f'Cards in hand must be five, got {cards}'
            logger.error(error)
            raise ValueError(error)
        if bid < 0:
            error = f'Bid value must be positive, got {bid}'
            logger.error(error)
            raise ValueError(error)

        self.bid = bid
        self.cards = cards
        self.joker = joker

        logger.info(f'Created hand {self}')

    def __str__(self) -> str:
        return f'Hand [{",".join(self.cards)}] with bid value {self.bid}'

    @property
    def repetitions(cls) -> dict[str, int]:
        repetitions: dict[str, int] = {}
        for card in cls.cards:
            repetitions[card] = 1 + repetitions.get(card, 0)

        if not cls.joker:
            return repetitions
        else:
            if 'J' not in repetitions.keys():
                return repetitions
            elif 'J' in repetitions.keys() and len(repetitions.keys()) == 1:
                return repetitions
            else:
                jokers = repetitions.pop('J')
                highest_card = max(repetitions, key=repetitions.get)
                repetitions[highest_card] = repetitions[highest_card] + jokers
                return repetitions

    @property
    def type(cls) -> CardType:
        if len(cls.repetitions.keys()) == 1:
            return CardType.FIVE_OF_A_KIND
        elif len(cls.repetitions.keys()) == 5:
            return CardType.HIGH_CARD
        elif len(cls.repetitions.keys()) == 4:
            return CardType.ONE_PAIR
        elif len(cls.repetitions.keys()) == 2:
            if 4 in cls.repetitions.values():
                return CardType.FOUR_OF_A_KIND
            elif 3 in cls.repetitions.values():
                return CardType.FULL_HOUSE
        elif len(cls.repetitions.keys()) == 3:
            if 3 in cls.repetitions.values():
                return CardType.THREE_OF_A_KIND
            elif 2 in cls.repetitions.values():
                return CardType.TWO_PAIR


class Day7Solver(FileReader):
    def solve_first_problem(self, file_name: str) -> int:
        lines = self.get_lines(file_name)
        hands: list[Hand] = []
        for line in lines:
            hands.append(self.parse_line(line))

        hands_sorted = sorted(hands, key=cmp_to_key(self.compare))
        total_winnings = 0
        for i in range(len(hands_sorted)):
            total_winnings = total_winnings + (hands_sorted[i].bid * (i + 1))

        logger.info(f'Total winnings are {total_winnings}')
        return total_winnings

    def compare(self, hand1: Hand, hand2: Hand, joker: bool = False) -> int:
        logger.debug(
            f'Comparing {hand1} with type {hand1.type.name} '
            f'and {hand2} with type {hand2.type.name}'
        )
        if hand1.type.value > hand2.type.value:
            logger.debug(f'Found {hand1.type.name} > {hand2.type.name}')
            return 1
        elif hand1.type.value < hand2.type.value:
            logger.debug(f'Found {hand1.type.name} < {hand2.type.name}')
            return -1
        else:
            for i in range(len(hand1.cards)):
                if self.get_card_value(hand1.cards[i], joker) > self.get_card_value(
                    hand2.cards[i], joker
                ):
                    logger.debug(f'Found {hand1.cards[i]} > {hand2.cards[i]}')
                    return 1
                elif self.get_card_value(hand1.cards[i], joker) < self.get_card_value(
                    hand2.cards[i], joker
                ):
                    logger.debug(f'Found {hand1.cards[i]} < {hand2.cards[i]}')
                    return -1
                else:
                    continue
            return 0

    def compare_with_joker(self, hand1: Hand, hand2: Hand) -> int:
        return self.compare(hand1, hand2, joker=True)

    def parse_line(self, line: str, joker: bool = False) -> Hand:
        cards = list(line.split(' ')[0])
        bid = int(line.split(' ')[1])
        return Hand(cards, bid, joker)

    def solve_second_problem(self, file_name: str) -> int:
        lines = self.get_lines(file_name)
        hands: list[Hand] = []
        for line in lines:
            hands.append(self.parse_line(line, joker=True))

        hands_sorted = sorted(hands, key=cmp_to_key(self.compare_with_joker))
        total_winnings = 0
        for i in range(len(hands_sorted)):
            total_winnings = total_winnings + (hands_sorted[i].bid * (i + 1))

        logger.info(f'Total winnings are {total_winnings}')
        return total_winnings

    def get_card_value(self, card: str, joker: bool = False) -> int:
        values: list[str, int] = {
            'A': 14,
            'K': 13,
            'Q': 12,
            'J': 11,
            'T': 10,
        }

        if card in values.keys():
            if joker and card == 'J':
                return 1
            return values.get(card)
        elif card.isdigit():
            return int(card)
        else:
            error = f'The card value {card} is not supported'
            logger.error(error)
            raise ValueError(error)


if __name__ == '__main__':
    Day7Solver().solve_first_problem("day_7/input.txt")
    Day7Solver().solve_second_problem("day_7/input.txt")
