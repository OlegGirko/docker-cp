from abc import ABCMeta, abstractmethod

DEFAULT_BUFSIZE = 10240

class IOFactory(metaclass=ABCMeta):
  """
  Abstract factory class for creating source and destination.
  Source is file-like object that contains tar archive data.
  It must provide read(nbytes) method that reads specified number of bytes.
  Also, it must be iterable, yielding some portion of data on each iteration.
  Source is passive, its read() method is called by Destination's run() method.
  Destination is object that has run(source) method that reads tar archive
  from source by either using its read() method or iterating over it,
  and extracts files into destination specified by its pathname.
  """

  @classmethod
  @abstractmethod
  def create_source(cls, pathname, bufsize=DEFAULT_BUFSIZE):
    """
    Create file-like object corresponding to given pathname.
    This object must have read(nbytes) method.
    @param pathname path name of file-like object to create
    @param bufsize size of output buffer in bytes
    @return file-like object if pathname is valid, None otherwise
    """
    return

  @classmethod
  @abstractmethod
  def create_destination(cls, pathname, bufsize=DEFAULT_BUFSIZE):
    """
    Create destination object corresponding to given pathname.
    This object must have run(source) method that reads tar archive
    from source until there are no data in source and extracts to
    specified pathname.
    No more than self.bufsize bytes is read each time read() method
    is called on source object.
    @param pathname path name of destination where to extract data
    @param bufsize size of input buffer in bytes
    @return destination object if pathname is valid, None otherwise
    """
    return

class Destination(metaclass=ABCMeta):
  """
  Abstract class for Destination object.
  """

  @abstractmethod
  def run(self, source):
    """
    Read data from source and extract to destination.
    @param source file-like object to read tar archive data from
    """
    return
