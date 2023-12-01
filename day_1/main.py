
from file_reader.file_reader import FileReader
import logging, sys
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
      only_digits = self._get_all_digits(self._replace_numbers(line))
      logger.debug(f'Found these digits: {only_digits}')
      numbers.append(self._compose_number(only_digits))
    logger.debug(f'Got this numbers: {numbers}')
    result = sum([int(number) for number in numbers])
    logger.info(f'The sum of the numbers is {result}')

    return result
  
  
  def _replace_numbers(self, line: str) -> str:
    """
    Given a line, it finds the first occurrence of a number as word
    and returns the number found and the rest of the line.
    """

    NUMBERS = {
      'one': 1,
      'two': 2,
      'three': 3,
      'four': 4,
      'five': 5, 
      'six': 6,
      'seven': 7,
      'eight': 8,
      'nine': 9,
    }

    logger.info(f'Replacing in line: {line}')
    modified_line = line
    for num in NUMBERS.keys():
      modified_line = modified_line.replace(num, str(NUMBERS[num]))
    logger.info(f'Line {line} became {modified_line}')

    return modified_line



if __name__ == '__main__':
  Day1Solver().solve_first_problem("day_1/input_1.txt")
  Day1Solver().solve_second_problem("day_1/input_2.txt")
