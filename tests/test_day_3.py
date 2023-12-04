import unittest
import logging
import sys

from day_3.main import Day3Solver, Point, Schematic

logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)


class TestDay3Solver(unittest.TestCase):
    def test_can_solve_first_problem(self):
        result = Day3Solver().solve_first_problem('tests/resources/test_day_3_1.txt')
        self.assertEqual(result, 4361)

    def test_can_solve_second_problem(self):
        result = Day3Solver().solve_second_problem('tests/resources/test_day_3_1.txt')
        self.assertEqual(result, 467835)

    def test_point_is_correctly_initialized(self):
        point = Point(4, 5, '#')
        self.assertEqual(point.row, 4)
        self.assertEqual(point.column, 5)
        self.assertEqual(point.value, '#')

        with self.assertRaises(ValueError):
            Point(-1, 5, '#')

    def test_point_is_recognized_as_digit_or_symbol(self):
        point = Point(2, 4, '5')
        self.assertEqual(point.is_number, True)

        point = Point(6, 1, '#')
        self.assertEqual(point.is_symbol, True)

        point = Point(6, 0, '#')
        self.assertEqual(point.is_number, False)

    def test_schematic_is_built_correctly(self):
        point1 = Point(2, 4, '5')
        point2 = Point(6, 1, '#')
        point3 = Point(6, 0, '#')

        schematic = Schematic([point1, point2, point3])

        self.assertEqual(schematic.numbers, [point1])
        self.assertEqual(schematic.symbols, [point2, point3])

    def test_near_numbers_are_found(self):
        point1 = Point(3, 6, '#')
        point2 = Point(2, 6, '6')
        point3 = Point(2, 7, '3')
        point4 = Point(2, 5, '+')
        point5 = Point(3, 6, '#')

        schematic = Schematic([point1, point2, point3, point4, point5])
        near_numbers = schematic.get_near_numbers(3, 6)

        self.assertEqual(near_numbers, [point2, point3])

    def test_get_whole_number(self):
        point1 = Point(3, 6, '#')
        point2 = Point(2, 6, '6')
        point3 = Point(2, 7, '3')
        point4 = Point(2, 8, '3')
        point5 = Point(3, 6, '#')

        schematic = Schematic([point1, point2, point3, point4, point5])
        numbers = schematic.get_whole_number(2, 7)
        logger.info(f'number converted: {schematic.convert_to_number(numbers)}')
        self.assertEqual(numbers, [point2, point3, point4])

    def test_convert_to_number(self):
        point1 = Point(4, 0, '6')
        point2 = Point(4, 1, '1')
        point3 = Point(4, 2, '7')
        point4 = Point(4, 3, '+')

        schematic = Schematic([point1, point2, point3, point4])
        numbers = schematic.get_near_numbers(4, 3)
        logger.info(f'Number found: {";".join([str(num) for num in numbers])}')
        self.assertEqual(numbers, [point3])

        whole_number = schematic.get_whole_number(numbers[0].row, numbers[0].column)
        final_number = schematic.convert_to_number(whole_number)
        self.assertEqual(final_number, 617)
