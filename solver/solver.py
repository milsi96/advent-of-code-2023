from abc import ABC, abstractmethod
from file_reader.file_reader import FileReader


class Solver(FileReader, ABC):
    @abstractmethod
    def solve_first_problem(self, file_name: str) -> int:
        pass

    @abstractmethod
    def solve_second_problem(self, file_name: str) -> int:
        pass
