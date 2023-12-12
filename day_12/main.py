from enum import StrEnum
import itertools
from typing import Generator, Optional
from custom_logger.custom_logger import CustomLogger
from solver.solver import Solver


logger = CustomLogger(__name__).get_logger()


class Condition(StrEnum):
    OPERATIONAL = '.'
    DAMAGED = '#'
    UNKNOWN = '?'

    @staticmethod
    def from_str(condition) -> 'Condition':
        match condition:
            case '?':
                return Condition.UNKNOWN
            case '#':
                return Condition.DAMAGED
            case '.':
                return Condition.OPERATIONAL
            case _:
                error = f'This condition is not implemented, got {condition}'
                logger.error(error)
                raise NotImplementedError(error)

    def __str__(self) -> str:
        return self.value


class Arrangement:
    spring_conditions: list[Condition]
    damaged_springs_groups: list[int]
    _damaged_springs_indexes: Optional[list[int]] = None
    _unknown_springs_indexes: Optional[list[int]] = None
    _operational_springs_indexes: Optional[list[int]] = None

    def __init__(
        self, spring_conditions: list[Condition], damaged_springs_groups: list[int]
    ):
        self.spring_conditions = spring_conditions
        self.damaged_springs_groups = damaged_springs_groups

    def __str__(self) -> str:
        result = f'{"".join([str(cond) for cond in self.spring_conditions])} '
        result += f'{",".join([str(num) for num in self.damaged_springs_groups])}'
        return result

    @property
    def valid_arrangements(cls) -> int:
        valid_arrangements = 0
        for new_arrangement in cls.next_arrangement():
            logger.debug(
                f'New arrangement: {"".join(str(arr) for arr in new_arrangement)}'
            )
            if cls.is_valid(new_arrangement, cls.damaged_springs_groups):
                valid_arrangements += 1
        return valid_arrangements

    def next_arrangement(self) -> Generator:
        possible_conditions = [Condition.DAMAGED, Condition.OPERATIONAL]
        condition_combinations = list(
            itertools.product(
                possible_conditions, repeat=len(self.unknown_springs_indexes)
            )
        )
        for comb in condition_combinations:
            index = 0
            temp_conditions = self.spring_conditions.copy()
            for i in self.unknown_springs_indexes:
                temp_conditions[i] = comb[index]
                index += 1
            yield temp_conditions

    @property
    def damaged_springs_indexes(cls) -> list[int]:
        if cls._damaged_springs_indexes is not None:
            return cls._damaged_springs_indexes

        result: list[int] = []
        for i in range(len(cls.spring_conditions)):
            if cls.spring_conditions[i] == Condition.DAMAGED:
                result.append(i)

        cls._damaged_springs_indexes = result
        return cls._damaged_springs_indexes

    @property
    def operational_springs_indexes(cls) -> list[int]:
        if cls._operational_springs_indexes is not None:
            return cls._operational_springs_indexes

        result: list[int] = []
        for i in range(len(cls.spring_conditions)):
            if cls.spring_conditions[i] == Condition.OPERATIONAL:
                result.append(i)

        cls._operational_springs_indexes = result
        return cls._operational_springs_indexes

    @property
    def unknown_springs_indexes(cls) -> list[int]:
        if cls._unknown_springs_indexes is not None:
            return cls._unknown_springs_indexes

        result: list[int] = []
        for i in range(len(cls.spring_conditions)):
            if cls.spring_conditions[i] == Condition.UNKNOWN:
                result.append(i)

        cls._unknown_springs_indexes = result
        return cls._unknown_springs_indexes

    @staticmethod
    def is_valid(
        spring_conditions: list[Condition], damaged_springs_groups: list[int]
    ) -> bool:
        return False


class Day12Solver(Solver):
    def solve_first_problem(self, file_name: str) -> int:
        lines = self.get_lines(file_name)
        arrangements: list[Arrangement] = []

        for line in lines:
            conditions = [cond for cond in line.split(' ')[0]]
            arrangements.append(
                Arrangement(
                    [Condition.from_str(cond) for cond in conditions],
                    [int(num) for num in line.split(' ')[1].split(',')],
                )
            )

        logger.debug(f'First arrangement: {arrangements[4]}')

        return 0

    def get_first_unknown_spring(self, springs: list[str]) -> int:
        for i in range(len(springs)):
            if springs[i] == '?':
                return i
        return -1

    def solve_second_problem(self, file_name: str) -> int:
        self.get_lines(file_name)

        return 0


if __name__ == '__main__':
    Day12Solver().solve_first_problem("day_12/input.txt")
    Day12Solver().solve_second_problem("day_12/input.txt")
