from .io import IOFactory, Destination, DEFAULT_BUFSIZE
import sys

class StdioIOFactory(IOFactory):
  """
  Class for creating source for reading from stdin
  and destination for writing to stdout.
  """

  @classmethod
  def create_source(cls, pathname, bufsize=DEFAULT_BUFSIZE):
    """
    Create source object for reading tar archive from stdin.
    @param pathname path name of file-like object to create
    @param bufsize size of output buffer in bytes
    @return sys.stdin if pathname is "-", None otherwise
    """
    if pathname == "-":
      return sys.stdin.buffer

  @classmethod
  def create_destination(cls, pathname, bufsize=DEFAULT_BUFSIZE):
    """
    Create destination object to write unprocessed tar archive to stdout.
    @param pathname path name of destination object to create
    @param bufsize size of input buffer in bytes
    @return sys.stdout if pathname is "-", None otherwise
    """
    if pathname == "-":
      return StdioDestination(pathname, bufsize)

class StdioDestination(Destination):
  """
  Destination object for writing unprocessed tar archive to stdout.
  """

  def run(self, source):
    """
    Read data from source and extract to destination.
    @param source file-like object to read tar archive data from
    """
    while True:
      data = source.read(self.bufsize)
      if len(data) == 0:
        break
      sys.stdout.buffer.write(data)
