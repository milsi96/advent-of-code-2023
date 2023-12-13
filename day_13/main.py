from custom_logger.custom_logger import CustomLogger
from solver.solver import Solver


logger = CustomLogger(__name__).get_logger()


class Day13Solver(Solver):
    def solve_first_problem(self, file_name: str) -> int:
        return 0

    def solve_second_problem(self, file_name: str) -> int:
        return 0


if __name__ == '__main__':
    Day13Solver().solve_first_problem("day_13/input.txt")
    Day13Solver().solve_second_problem("day_13/input.txt")
