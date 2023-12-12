from enum import StrEnum
from functools import lru_cache
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
        for new_arrangement in Arrangement.next_arrangement(cls.spring_conditions):
            if cls.is_valid(new_arrangement, cls.damaged_springs_groups):
                valid_arrangements += 1
        return valid_arrangements

    @property
    def valid_arrangements_unfolded(cls) -> int:
        match cls.spring_conditions[-1]:
            case Condition.DAMAGED:
                return pow(cls.valid_arrangements, 5)
            case Condition.OPERATIONAL:
                return cls._case_operational()
            case Condition.UNKNOWN:
                return cls._case_unknown()

    @lru_cache
    def _case_unknown(self) -> int:
        valid_arrangements_unfolded = 0
        new_spring_conditions = self.spring_conditions.copy()
        addition = [Condition.UNKNOWN] + new_spring_conditions
        new_spring_conditions.extend(addition + addition + addition + addition)

        logger.debug(''.join([str(cond) for cond in new_spring_conditions]))

        for new_arrangement in Arrangement.next_arrangement(new_spring_conditions):
            logger.debug(
                "New arrangement: {}".format(
                    ''.join([str(cond) for cond in new_spring_conditions])
                )
            )
            if self.is_valid(new_arrangement, self.damaged_springs_groups):
                valid_arrangements_unfolded += 1

        logger.debug(f'Total unfolded is {valid_arrangements_unfolded}')
        return valid_arrangements_unfolded

    def _case_operational(self) -> int:
        valid_arrangements_unfolded = 0
        new_spring_conditions = self.spring_conditions.copy()
        new_spring_conditions.insert(0, Condition.UNKNOWN)

        for new_arrangement in Arrangement.next_arrangement(new_spring_conditions):
            if self.is_valid(new_arrangement, self.damaged_springs_groups):
                valid_arrangements_unfolded += 1

        logger.debug(f'Total unfolded is {valid_arrangements_unfolded}')
        return pow(valid_arrangements_unfolded, 4) * self.valid_arrangements

    @staticmethod
    def next_arrangement(spring_conditions: list[Condition]) -> Generator:
        possible_conditions = [Condition.DAMAGED, Condition.OPERATIONAL]
        unknown_springs_indexes: list[int] = []
        for i in range(len(spring_conditions)):
            if spring_conditions[i] == Condition.UNKNOWN:
                unknown_springs_indexes.append(i)

        condition_combinations = list(
            itertools.product(possible_conditions, repeat=len(unknown_springs_indexes))
        )
        for comb in condition_combinations:
            index = 0
            temp_conditions = spring_conditions.copy()
            for i in unknown_springs_indexes:
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
        if any([cond == Condition.UNKNOWN for cond in spring_conditions]):
            return False
        if sum([cond == Condition.DAMAGED for cond in spring_conditions]) != sum(
            damaged_springs_groups
        ):
            return False

        temp_groups = damaged_springs_groups.copy()
        i = 0
        while i < len(spring_conditions):
            if spring_conditions[i] == '#':
                try:
                    items_number = temp_groups.pop(0)
                    damaged = [
                        cond == Condition.DAMAGED
                        for cond in spring_conditions[i : i + items_number]
                    ]
                    if not all(damaged):
                        return False
                    if i > 0 and spring_conditions[i - 1] != '.':
                        return False
                    if (
                        i + items_number <= len(spring_conditions) - 1
                        and spring_conditions[i + items_number] != '.'
                    ):
                        return False

                    i += items_number
                except IndexError as e:
                    logger.error(e)
                    raise e
            i += 1

        logger.info(
            'This arrangement {0} with groups {1} is valid'.format(
                "".join([str(cond) for cond in spring_conditions]),
                damaged_springs_groups,
            )
        )
        return True


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

        total_arrangements = sum([arr.valid_arrangements for arr in arrangements])
        logger.info(f'The total of valid arrangements is {total_arrangements}')

        return total_arrangements

    def get_first_unknown_spring(self, springs: list[str]) -> int:
        for i in range(len(springs)):
            if springs[i] == '?':
                return i
        return -1

    def solve_second_problem(self, file_name: str) -> int:
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

        total_arrangements = sum(
            [arr.valid_arrangements_unfolded for arr in arrangements]
        )
        logger.info(f'The total of valid arrangements is {total_arrangements}')

        return total_arrangements


if __name__ == '__main__':
    Day12Solver().solve_first_problem("day_12/input.txt")
    Day12Solver().solve_second_problem("day_12/input.txt")
