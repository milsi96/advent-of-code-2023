from custom_logger.custom_logger import CustomLogger
from solver.solver import Solver

logger = CustomLogger(__name__).get_logger()


class History:
    numbers: list[int]

    def __init__(self, numbers: list[int]):
        self.numbers = numbers

    @property
    def next_value(cls) -> int:
        differences: list[float] = []
        for i in range(len(cls.numbers) - 1, 0, -1):
            differences.append(cls.numbers[i] - cls.numbers[i - 1])

        differences = differences[::-1]

        if all(diff == differences[0] for diff in differences):
            return cls.numbers[-1] + differences[0]

        return cls.numbers[-1] + History(differences).next_value

    @property
    def previous_value(cls) -> int:
        differences: list[float] = []
        for i in range(len(cls.numbers) - 1, 0, -1):
            differences.append(cls.numbers[i] - cls.numbers[i - 1])

        differences = differences[::-1]

        if all(diff == differences[0] for diff in differences):
            logger.debug(f'The previous value in {cls.numbers[0] - differences[0]}')
            return cls.numbers[0] - differences[0]

        return cls.numbers[0] - History(differences).previous_value

    def __str__(self) -> str:
        return f'History: {self.numbers}'


class Day9Solver(Solver):
    def solve_first_problem(self, file_name: str) -> int:
        lines = self.get_lines(file_name)
        histories: list[History] = []

        for line in lines:
            logger.debug(line)
            histories.append(History([float(num) for num in line.split(' ')]))

        logger.info(f'{", ".join([str(history) for history in histories])}')

        values_sum = 0
        for history in histories:
            logger.debug(history)
            next_value = history.next_value
            logger.debug(next_value)
            values_sum += history.next_value

        logger.info(f'The sum of all next values is {int(values_sum)}')
        return values_sum

    def solve_second_problem(self, file_name: str) -> int:
        lines = self.get_lines(file_name)
        histories: list[History] = []

        for line in lines:
            logger.debug(line)
            histories.append(History([float(num) for num in line.split(' ')]))

        values_sum = 0
        for history in histories:
            previous_value = history.previous_value
            logger.debug(f'{history} -> {previous_value}')
            values_sum += history.previous_value

        logger.info(f'The sum of all next values is {int(values_sum)}')
        return values_sum


if __name__ == '__main__':
    Day9Solver().solve_first_problem("day_9/input.txt")
    Day9Solver().solve_second_problem("day_9/input.txt")
