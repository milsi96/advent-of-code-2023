import logging
import sys
import re
from file_reader.file_reader import FileReader


logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)


class Card:
    id: int
    numbers: list[int]
    winning_numbers: list[int]

    def __init__(self, id: int, numbers: list[int], winning_numbers: list[int]):
        self.id = id
        self.numbers = numbers
        self.winning_numbers = winning_numbers

    @property
    def card_value(cls) -> int:
        matches = 0
        for num in cls.numbers:
            if num in cls.winning_numbers:
                matches = matches + 1

        if matches == 1:
            return 1
        elif matches == 0:
            return 0
        return pow(2, matches - 1)

    def __str__(self):
        return f'Card {self.id}: {self.winning_numbers} | {self.numbers};'

    @property
    def wins(cls) -> int:
        matches = 0
        for num in cls.numbers:
            if num in cls.winning_numbers:
                matches = matches + 1
        return matches


class CardPile:
    cards: dict[int, Card] = {}

    def __init__(self, cards: list[Card]):
        for card in cards:
            logger.info(f'Inserting card {card}')
            self.cards[card.id] = card

    @property
    def total_scratchpads(cls) -> int:
        total = 0
        for index in cls.cards.keys():
            total = total + cls.get_card_wins(index)
        return total + len(cls.cards.keys())

    def get_card_wins(self, index: int, statistics: dict[int, int] = {}) -> int:
        if self.cards.get(index).wins == 0:
            statistics[index] = 0
            return 0

        if index in statistics.keys():
            return statistics.get(index)

        LOWER_LIMIT = index + 1
        UPPER_LIMIT = index + self.cards.get(index).wins + 1

        current_total = UPPER_LIMIT - LOWER_LIMIT
        logger.debug(f'Won {current_total} scratchpads for id {index} for now')
        for target in range(LOWER_LIMIT, UPPER_LIMIT):
            current_total = current_total + self.get_card_wins(target, statistics)

        statistics[index] = current_total

        logger.debug(statistics)

        return statistics[index]


class Day4Solver(FileReader):
    def solve_first_problem(self, file_name: str) -> int:
        lines = self.get_lines(file_name)
        cards: list[Card] = []
        for line in lines:
            logger.info(f'Reading line: {line}')
            cards.append(self.parse_card(line))

        final_value = sum([card.card_value for card in cards])
        logger.info(f'Cards are worth {final_value}')
        return final_value

    def parse_card(self, line: str) -> Card:
        pattern = r'Card\s+(\d+)'
        card_id: int = int(re.findall(pattern=pattern, string=line.split(':')[0])[0])
        line_without_id: str = line.split(':')[1].strip()
        winning_numbers: list[int] = [
            int(num.strip())
            for num in line_without_id.split('|')[0].strip().split(' ')
            if num != ''
        ]
        numbers: list[int] = [
            int(num.strip())
            for num in line_without_id.split('|')[1].strip().split(' ')
            if num != ''
        ]

        logger.info(f'Card {card_id}')
        logger.info(f'Winning numbers: {winning_numbers}')
        logger.info(f'Numbers in card: {numbers}')

        return Card(card_id, numbers, winning_numbers)

    def solve_second_problem(self, file_name: str) -> int:
        lines = FileReader().get_lines('day_4/input_1.txt')
        cards = [self.parse_card(line) for line in lines]
        pile = CardPile(cards)

        logger.info(f'Total scratchcards: {pile.total_scratchpads}')


if __name__ == '__main__':
    Day4Solver().solve_first_problem("day_4/input_1.txt")
    Day4Solver().solve_second_problem("day_4/input_2.txt")
