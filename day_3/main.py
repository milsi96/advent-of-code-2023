from abc import ABC
import logging
import sys
from file_reader.file_reader import FileReader


logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)


class Point(ABC):
    x: int
    y: int
    value: str


class Number(Point):
    def __init__(self, x: int, y: int, value: str):
        self.x = x
        self.y = y
        self.value = value


class Symbol(Point):
    def __init__(self, x: int, y: int, value: str):
        self.x = x
        self.y = y
        self.value = value


class Schematic:
    numbers: list[Number]
    symbols: list[Symbol]

    def __init__(self, points: list[Point]):
        self.points = points

    def get_value(self, x: int, y: int) -> Number | Symbol:
        for p in self.points:
            if p.x == x and p.y == y:
                return p.value
        logger.error(f'Could not find point at coordinates x {x} and y {y}')
        raise ValueError('Probably x {x} and y {y} are not correct')

    def get_whole_number(self, x: int, y: int) -> int:
        if self.get_value(x, y).isdigit():
            pass


class Day3Solver(FileReader):
    def solve_first_problem(self, file_name: str) -> int:
        schematic = self.get_lines(file_name)
        self.beautiful_print(schematic)

    def beautiful_print(self, schematic: [[]]):
        for sche in schematic:
            logger.info(sche)
