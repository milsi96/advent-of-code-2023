from enum import StrEnum
from typing import Optional
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
        return str(self.value)

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Point):
            return False
        return self.value == __value.value


class Note:
    lines: list[list[Point]]

    def __init__(self, lines: list[list[Point]]) -> None:
        self.lines = lines

    def __str__(self) -> str:
        return ', '.join([str(line) for line in self.lines])

    @property
    def total_column_above_reflection(cls) -> int:
        horizontal_reflection = cls._horizontal_reflection_index(cls.lines)
        vertical_reflection = cls._vertical_reflection_index(cls.lines)

        result = 0
        if horizontal_reflection is not None:
            logger.info(
                f'The horizontal reflection line is at index {horizontal_reflection}'
            )
            result += 100 * (horizontal_reflection + 1)
        if vertical_reflection is not None:
            logger.info(
                f'The vertical reflection line is at index {vertical_reflection}'
            )
            result += vertical_reflection + 1
        return result

    def _horizontal_reflection_index(self, lines: list[list[Point]]) -> Optional[int]:
        for row in range(len(lines)):
            if row + 1 == len(lines):
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

    def _vertical_reflection_index(self, lines: list[list[Point]]) -> Optional[int]:
        lines_copy = lines.copy()
        transposed_lines = [
            [lines_copy[j][i] for j in range(len(lines_copy))]
            for i in range(len(lines_copy[0]))
        ]

        return self._horizontal_reflection_index(transposed_lines)


class Day13Solver(Solver):
    def solve_first_problem(self, file_name: str) -> int:
        lines = self.get_lines(file_name)
        logger.debug(lines)
        notes: list[Note] = []

        temp_note: list[str] = []
        for line in lines:
            if line == '':
                notes.append(self.parse_note(temp_note))
                temp_note = []
                continue
            temp_note.append(line)
        notes.append(self.parse_note(temp_note))

        total = sum([note.total_column_above_reflection for note in notes])
        logger.debug(f'Total sum is {total}')

        return total

    def parse_note(self, lines: list[str]) -> Note:
        points: list[list[Point]] = []

        for row in range(len(lines)):
            temp_points: list[Point] = []
            for column in range(len(lines[row])):
                if lines[row][column] == Pattern.ROCK.value:
                    temp_points.append(Point(row, column, Pattern.ROCK))
                elif lines[row][column] == Pattern.ASH.value:
                    temp_points.append(Point(row, column, Pattern.ASH))
                else:
                    continue
            points.append(temp_points)

        return Note(points)

    def solve_second_problem(self, file_name: str) -> int:
        return 0


if __name__ == '__main__':
    Day13Solver().solve_first_problem("day_13/input.txt")
    # Day13Solver().solve_second_problem("day_13/input.txt")
