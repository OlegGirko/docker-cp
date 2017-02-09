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
      return StdioSource(sys.stdin.buffer, bufsize)

  @classmethod
  def create_destination(cls, pathname, bufsize=DEFAULT_BUFSIZE):
    """
    Create destination object to write unprocessed tar archive to stdout.
    @param pathname path name of destination object to create
    @param bufsize size of input buffer in bytes
    @return sys.stdout if pathname is "-", None otherwise
    """
    if pathname == "-":
      return StdioDestination(bufsize)

class StdioSource(object):
  """
  Source object for reading tar archive from stdin.
  """

  def __init__(self, buffer, bufsize):
    """
    Construct source object for reading tar archive to stdout.
    @param buffer stdin buffer to read raw data from
    @param bufsize size of output buffer in bytes
    """
    self.buffer = buffer
    self.bufsize = bufsize

  def read(self, nbytes):
    """
    Read data from the buffer.
    """
    return self.buffer.read(nbytes)

  def __iter__(self):
    """
    Iterate through self, reading no more than self.bufsize bytes.
    @return generator iterator yielding chinks of data read
    """
    while True:
      data = self.read(self.bufsize)
      if len(data) == 0:
        break
      yield data

class StdioDestination(Destination):
  """
  Destination object for writing unprocessed tar archive to stdout.
  """

  def __init__(self, bufsize):
    """
    Construct destination object for writing unprocessed tar archive to stdout.
    @param bufsize size of input buffer in bytes
    """
    self.bufsize = bufsize

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
