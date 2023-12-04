import unittest
import logging
import sys

from file_reader.file_reader import FileReader

logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.INFO)
logger.addHandler(stream_handler)


class TestReadFile(unittest.TestCase):
    def test_returns_correct_lines(self):
        result = FileReader().get_lines("tests/resources/test_file_reader.txt")
        logger.debug(result)
        expected_result = ['this', 'is a', 'test']
        self.assertEqual(result, expected_result)

    def test_cannot_read_file(self):
        with self.assertRaises(FileNotFoundError):
            FileReader().get_lines("tests/resources/dfghdfgh.txt")
