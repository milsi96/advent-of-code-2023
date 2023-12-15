from custom_logger.custom_logger import CustomLogger
from solver.solver import Solver


logger = CustomLogger(__name__).get_logger()


class Day15Solver(Solver):
    def solve_first_problem(self, file_name: str) -> int:
        tokens = self.get_lines(file_name)[0].split(',')

        result = 0
        for token in tokens:
            result += self.calculate_hash(token)

        logger.debug(f'The sum of the hash conversion is {result}')
        return result

    def calculate_hash(self, token: str) -> int:
        current_value = 0
        for tk in token:
            current_value += ord(tk)
            current_value *= 17
            current_value %= 256
        return current_value

    def solve_second_problem(self, file_name: str) -> int:
        return 0


if __name__ == '__main__':
    Day15Solver().solve_first_problem("day_15/input.txt")
    Day15Solver().solve_second_problem("day_15/input.txt")
