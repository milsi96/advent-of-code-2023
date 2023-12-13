from enum import StrEnum
from typing import Optional
import numpy as np
from custom_logger.custom_logger import CustomLogger
from solver.solver import Solver


logger = CustomLogger(__name__).get_logger()


class Pattern(StrEnum):
    ASH = '.'
    ROCK = '#'

    def __str__(self) -> str:
        return self.value


class Point:
    row: int
    column: int
    value: Pattern

    def __init__(self, row: int, column: int, value: Pattern):
        if row < 0 or column < 0:
            error = (
                f'Row and column must be positive, got row {row} and column {column}'
            )
            logger.error(error)
            raise ValueError(error)
        self.row = row
        self.column = column
        self.value = value

    @property
    def is_ash(cls) -> bool:
        return cls.value == Pattern.ASH

    @property
    def is_rock(cls) -> bool:
        return not cls.is_ash

    def __str__(self) -> str:
        return f'({self.row}, {self.column}): {str(self.value)}'

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Point):
            return False
        return self.value == __value.value


class Line:
    rocks: list[Point]
    ashes: list[Point]

    def __init__(self, rocks: list[Point], ashes: list[Point]) -> None:
        self.rocks = rocks
        self.ashes = ashes

    def __str__(self) -> str:
        for i in range(len(self.rocks + self.ashes)):
            pass
        return "Rocks: {}, Ashes: {}".format(
            ', '.join([str(rock) for rock in self.rocks]),
            ''.join([str(ash) for ash in self.ashes]),
        )

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Line):
            return False
        return self.rocks == __value.rocks and self.ashes == __value.ashes


class Note:
    lines: list[Line]

    def __init__(self, lines: list[Line]) -> None:
        self.lines = lines

    def __str__(self) -> str:
        return ', '.join([str(line) for line in self.lines])

    @property
    def total_column_above_reflection(cls) -> int:
        result = 0
        horizontal_reflection = cls._horizontal_reflection_index(cls.lines)
        vertical_reflection = cls._vertical_reflection_index(cls.lines)
        if horizontal_reflection is not None:
            result += 100 * (horizontal_reflection + 1)
        if vertical_reflection is not None:
            result += vertical_reflection + 1
        return result

    def _horizontal_reflection_index(self, lines: list[Line]) -> Optional[int]:
        for row in range(len(lines)):
            if row + 1 == len(lines) - 1:
                break
            if lines[row] == lines[row + 1]:
                index = 0
                correct = True
                while row - index >= 0 and row + 1 + index < len(lines):
                    if lines[row - index] != lines[row + 1 + index]:
                        correct = False
                        break
                    index += 1
                if correct:
                    return row
        return None

    def _vertical_reflection_index(self, lines: list[Line]) -> Optional[int]:
        transposed_lines = np.array(lines).transpose()

        logger.debug(', '.join(str(line) for line in transposed_lines.tolist()))

        return self._horizontal_reflection_index(transposed_lines.tolist())


class Day13Solver(Solver):
    def solve_first_problem(self, file_name: str) -> int:
        lines = self.get_lines(file_name)
        logger.debug(lines)

        notes: list[Note] = []
        temp_note: list[Line] = []
        for line in lines:
            if line == '':
                notes.append(Note(temp_note))
                temp_note = []
                continue
            temp_note.append(self.parse_line(line))
        notes.append(Note(temp_note))

        logger.debug('\n'.join([str(note) for note in notes]))

        return 0

    def parse_line(self, line: str) -> Line:
        ashes: list[Point] = []
        rocks: list[Point] = []

        # TODO: need to parse a matrix of lines not only one line
        for row in range(len(line)):
            for column in range(len([ch for ch in line[row]])):
                logger.debug(line[row])
                if line[row][column] == Pattern.ROCK.value:
                    rocks.append(Point(row, column, Pattern.ROCK))
                elif line[row][column] == Pattern.ASH.value:
                    ashes.append(Point(row, column, Pattern.ASH))
                else:
                    continue
        logger.debug('\n')

        return Line(rocks, ashes)

    def solve_second_problem(self, file_name: str) -> int:
        return 0


if __name__ == '__main__':
    Day13Solver().solve_first_problem("day_13/input.txt")
    Day13Solver().solve_second_problem("day_13/input.txt")
