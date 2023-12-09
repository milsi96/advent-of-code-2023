from file_reader.file_reader import FileReader
import logging
import sys
import re

logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)


class Day1Solver(FileReader):
    def solve_first_problem(self, file_name: str) -> int:
        """
        Given a file, it returns the sum of the first and
        last digits found in each line.
        """
        lines = self.get_lines(file_name)
        logger.debug(f'Read these lines: {lines}')

        numbers = []
        for line in lines:
            only_digits = self._get_all_digits(line)
            logger.debug(f'Found these digits: {only_digits}')
            numbers.append(self._compose_number(only_digits))
        logger.debug(f'Got this numbers: {numbers}')
        result = sum([int(number) for number in numbers])
        logger.info(f'The sum of the numbers is {result}')

        return result

    def _get_all_digits(self, line: str) -> list[int]:
        return [int(char) for char in line if char.isdigit()]

    def _compose_number(self, number_sequence: list[int]) -> int:
        return int(f'{number_sequence[0]}{number_sequence[-1]}')

    def solve_second_problem(self, file_name: str) -> int:
        """
        Given a file name, it returns the sum of the numbers as words
        found in each line.
        """

        lines = self.get_lines(file_name)
        logger.debug(f'Read these lines: {lines}')

        numbers = []
        for line in lines:
            final_number = self._get_final_number(line)
            logger.debug(f'Found {final_number} from {line}')
            numbers.append(final_number)
        logger.debug(f'Got this numbers: {numbers}')
        result = sum([int(number) for number in numbers])
        logger.info(f'The sum of the numbers is {result}')

        return result

    def _get_final_number(self, line: str) -> str:
        """
        Given a line, it finds the first occurrence of a number as word
        and returns the number found and the rest of the line.
        """

        NUMBERS = {
            'one': '1',
            'two': '2',
            'three': '3',
            'four': '4',
            'five': '5',
            'six': '6',
            'seven': '7',
            'eight': '8',
            'nine': '9',
        }

        number_pattern = 'one|two|three|four|five|six|seven|eight|nine'
        pattern = r'(\d|' + number_pattern + r')'
        logger.debug(f'Pattern is: {pattern}')
        first_number: str = re.findall(pattern, line)[0]
        logger.debug(f"First number is: {first_number}")

        inverse_pattern = r'(\d|' + number_pattern[::-1] + r')'
        logger.debug(f'Inverse pattern: {inverse_pattern}')
        logger.debug(f'Inverse line: {line[::-1]}')

        second_number: list[str] = re.findall(inverse_pattern, line[::-1])[0][::-1]
        logger.debug(f"Second number is: {second_number}")

        result = str(NUMBERS.get(first_number, first_number)) + str(
            NUMBERS.get(second_number, second_number)
        )
        return result


if __name__ == '__main__':
    Day1Solver().solve_first_problem("day_1/input_1.txt")
    Day1Solver().solve_second_problem("day_1/input_2.txt")
