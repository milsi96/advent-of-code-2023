import unittest

from custom_logger.custom_logger import CustomLogger
from day_13.main import Day13Solver, Line, Note, Pattern, Point
from file_reader.file_reader import FileReader

logger = CustomLogger(__name__).get_logger()


class TestDay13Solver(unittest.TestCase):
    def test_can_solve_first_problem(self):
        Day13Solver().solve_first_problem('tests/resources/test_day_13.txt')

    @unittest.skip('tbd')
    def test_can_solve_second_problem(self):
        Day13Solver().solve_second_problem('tests/resources/test_day_13.txt')

    def test_column_reflection_is_correct(self) -> None:
        lines = FileReader().get_lines('tests/resources/test_day_13.txt')
        logger.debug(lines)

        notes: list[Note] = []
        temp_note: list[Line] = []
        for line in lines:
            if line == '':
                notes.append(Note(temp_note))
                temp_note = []
                continue
            temp_note.append(Day13Solver().parse_line(line))
        notes.append(Note(temp_note))

        logger.debug(notes[0].total_column_above_reflection)

    def test_points_are_equal(self) -> None:
        point1 = Point(1, 2, Pattern.ROCK)
        point2 = Point(1, 2, Pattern.ASH)
        self.assertFalse(point1 == point2)

        point3 = Point(1, 2, Pattern.ASH)
        point4 = Point(1, 2, Pattern.ASH)
        self.assertTrue(point3 == point4)

    def test_line_are_equal(self) -> None:
        point1 = Point(4, 2, Pattern.ASH)
        point2 = Point(1, 2, Pattern.ASH)
        line1 = Line([], [point1, point2])

        point3 = Point(7, 2, Pattern.ASH)
        point4 = Point(1, 2, Pattern.ASH)
        line2 = Line([], [point3, point4])

        self.assertTrue(line1 == line2)
