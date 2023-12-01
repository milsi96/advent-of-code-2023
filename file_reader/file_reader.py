
class FileReader:

  def get_lines(self, file_name: str) -> list:
    """Reads a file and returns the lines as list."""
    lines = []
    with open(file_name) as f:
      lines = [line.rstrip() for line in f.readlines()]
    return lines