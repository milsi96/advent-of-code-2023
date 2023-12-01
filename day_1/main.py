
from file_reader.file_reader import FileReader
import logging, sys

logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)

class Day1Solver(FileReader):
  
  def solve_first_problem(self, file_name: str) -> int:
    lines = self.get_lines(file_name)
    logger.debug(f'Read these lines: {lines}')

    numbers = []
    for line in lines:
      only_digits = [char for char in line if char.isdigit()]
      logger.debug(f'Found these digits: {only_digits}')
      numbers.append(f'{only_digits[0]}{only_digits[-1]}')
    logger.info(f'Got this numbers: {numbers}')
    result = sum([int(number) for number in numbers])
    logger.info(f'The sum of the numbers is {result}')

    return result



if __name__ == '__main__':
  Day1Solver().solve_first_problem("day_1/input.txt")
