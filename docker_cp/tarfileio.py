from .io import IOFactory, Destination, DEFAULT_BUFSIZE
import tarfile
from threading import Thread
from queue import Queue
import os

class TarFileIOFactory(IOFactory):
  """
  Class for creating source for creating tar archive from local file/directory
  and destination for extracting tar archive to local directory.
  """

  @classmethod
  def create_source(cls, pathname, bufsize=DEFAULT_BUFSIZE):
    """
    Create source object for creating tar archive from local file/directory.
    @param pathname path name of file or directory to archive
    @param bufsize size of output buffer in bytes
    """
    return TarFileSource(pathname, bufsize)

  @classmethod
  def create_destination(cls, pathname, bufsize=DEFAULT_BUFSIZE):
    """
    Create destination object to extract tar archive to local directory.
    @param pathname path name of directory where to extract archive
    @param bufsize size of input buffer in bytes
    @return destination object that extracts archive to given directory
    """
    return TarFileDestination(pathname, bufsize)

class TarFileSource(object):
  """
  Source object for creating tar archive of given file or directory.
  Source objects are supposed to be passive and be read be destination
  using source's read() method.
  Unfortunately, TarFile class doesn't want to be passive,
  insisting on writing to specified fileobj.
  Hence, we have to make this source passive by running tar creation
  in a separate thread, writing to a queue,
  and reading from this queue only in read() method in main thread.
  """

  def __init__(self, pathname, bufsize):
    """
    Initialise passive source for creating tar archive from local files.
    Create worker thread and start it.
    @param pathname path name of file or directory to create tar archive from
    @param buf size output buffer size
    """
    self.pathname = pathname
    self.bufsize = bufsize
    self.queue = Queue()
    self.thread = Thread(target=self.run)
    self.thread.start()

  def run(self):
    """
    Function to be run in worker thread.
    Opens TarFile for writing, passes self object to it as fileobj,
    adds specified pathname to tar archive.
    """
    try:
      with tarfile.open(fileobj=self, mode="w|", bufsize=self.bufsize) as tf:
        tf.add(self.pathname, arcname=os.path.basename(self.pathname))
      self.queue.put(b'')
    except Exception as e:
      self.queue.put(e)

  def write(self, data):
    """
    Write data to the queue.
    This method is used by TarFile for writing to fileobj
    @param data data to be written
    """
    self.queue.put(data)

  def read(self, nbytes):
    """
    Read data from the queue.
    """
    data = self.queue.get()
    if type(data) is not bytes:
      self.thread.join()
      raise data
    if data == b'':
      self.thread.join()
    return data

class TarFileDestination(Destination):
  """
  Destination object for extracting tar archive to given directory.
  """

  def __init__(self, pathname, *args, **kwargs):
    """
    Construct destination for extracting tar archive to a directory.
    @param pathname path name of destination where to extract data
    """
    self.pathname = pathname
    super(TarFileDestination, self).__init__(pathname, *args, **kwargs)

  def run(self, source):
    """
    Read data from source and extract to directory specified by self.pathname.
    @param source file-like object to read tar archive data from
    """
    with tarfile.open(fileobj=source, mode="r|", bufsize=self.bufsize) as tf:
      tf.extractall(self.pathname)
