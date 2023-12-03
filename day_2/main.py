import logging
import sys
from typing import Any
from file_reader.file_reader import FileReader
import re


logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.INFO)
logger.addHandler(stream_handler)

class Game:
  id: int
  cubes: dict[str, int]

  def __init__(self, id: int, cubes: dict[str, int]):
    self.id = id       
    self.cubes = cubes


class Day2Solver(FileReader):

  RED_TARGET = 12
  GREEN_TARGET = 13
  BLUE_TARGET = 14
  
  def solve_first_problem(self, file_name: str) -> int:
    """Returns the sum of games' IDs tha could have been played."""
    lines = [line.replace(' ', '') for line in FileReader().get_lines(file_name)]
    games: list[Game] = []
    for line in lines:
      games.append(self._parse_line(line))
    
    sum = 0
    for game in games:
      logger.info(f'Current game: {game.cubes}')
      if game.cubes.get('red', 0) <= self.RED_TARGET and game.cubes.get('green', 0) <= self.GREEN_TARGET and game.cubes.get('blue', 0) <= self.BLUE_TARGET:
        sum = sum + game.id
    logger.info(f'Got this sum: {sum}')

    return sum
  
  def solve_second_problem(self, file_name: str) -> int:
    """Returns the sum of the power of games' IDs"""
    lines = [line.replace(' ', '') for line in FileReader().get_lines(file_name)]
    games: list[Game] = []
    for line in lines:
      games.append(self._parse_line(line))

    sum = 0
    for game in games:
      logger.info(f'Current game: {game.cubes}')
      power = 1
      for _, quantity in game.cubes.items():
        power = power * quantity
      sum = sum + power
    logger.info(f'Got this sum: {sum}')

    return sum

  def _parse_line(self, line: str) -> Game:
    game_id = self._get_game_id(line)
    logger.debug(f'Game id = {game_id}')
    cubes = self._get_total_cubes(line.split(':')[1])
    logger.info(f'Got this total {cubes} for game {game_id}')
    return Game(game_id, cubes)


  def _get_total_cubes(self, line: str) -> dict[str, int]:
    total = {}
    for set_str in line.split(';'):
      set_dict = self._get_set(set_str)
      logger.debug(f'Got this set {set_str}')
      for color, quantity in set_dict.items():
        total[color] = max(total.get(color, quantity), quantity)
    logger.debug(f'Got this total {total}')
    return total

  
  def _get_set(self, set_str: str) -> dict[str, int]:
    result = {}
    for cubes in set_str.split(','):
      logger.debug(f'This is the cube set: {cubes}')
      cube_pattern = r'(\d+)(blue|green|red)'
      color = re.match(cube_pattern, cubes).group(2)
      quantity = re.match(cube_pattern, cubes).group(1)
      result[color] = int(quantity)
      logger.debug(f'This is the result: {result}')
    return result



  def _get_game_id(self, line: str) -> int:
    game_pattern: str = r'Game(\d+)'
    first_part = line.split(':')[0]
    return int(re.match(game_pattern, first_part).group(1))


if __name__ == '__main__':
  Day2Solver().solve_first_problem("day_2/input_1.txt")
  Day2Solver().solve_second_problem("day_2/input_1.txt")
