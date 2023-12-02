

import logging
import sys
from file_reader.file_reader import FileReader


logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)

class Day2Solver(FileReader):
