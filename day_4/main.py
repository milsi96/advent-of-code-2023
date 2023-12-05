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


class Day4Solver(FileReader):
    def solve_first_problem(self, file_name: str) -> int:
        lines = self.get_lines(file_name)
        cards: list[Card] = []
        for line in lines:
            logger.info(f'Reading line: {line}')
            cards.append(self.parse_card(line))
            logger.debug(str(cards[-1]))

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
        self.get_lines(file_name)


if __name__ == '__main__':
    Day4Solver().solve_first_problem("day_4/input_1.txt")
    # Day4Solver().solve_second_problem("day_4/input_2.txt")
