from .io import IOFactory, Destination, DEFAULT_BUFSIZE
import docker
import re

class DockerIOFactory(IOFactory):
  """
  Class for creating source for creating tar archive from file or directory
  inside Docker container
  and destination for extracting tar archive inside Docker container.
  """

  pathname_pattern = re.compile(r'^([A-Za-z0-9_-]+):(.*)$')

  @classmethod
  def create_source(cls, pathname, bufsize=DEFAULT_BUFSIZE):
    """
    Create source object for creating tar srchive from file or directort
    inside Docker container.
    @param pathname path name of file or directory to archive
    @param bufsize size of output buffer in bytes
    @return source object that creates tar archive from Docker container
    """
    m = cls.pathname_pattern.fullmatch(pathname)
    if m is not None:
      client = docker.from_env()
      container = client.containers.get(m.group(1))
      res = container.get_archive(m.group(2))
      return res[0]

  @classmethod
  def create_destination(cls, pathname, bufsize=DEFAULT_BUFSIZE):
    """
    Create destination object for extracting tar archive
    inside Docker container.
    @param pathname path name of directory where to extract archive
    @param bufsize size of input buffer in bytes
    @return destination object that extracts archive to given directory
    """
    m = cls.pathname_pattern.fullmatch(pathname)
    if m is not None:
      return DockerDestination(m.group(1), m.group(2))

class DockerDestination(Destination):
  """
  Destination object for extracting tar archive inside Docker container.
  """

  def __init__(self, containername, pathname):
    """
    Construct destination for extracting tar archive inside Docker container.
    @param containername name of the container where to extract archive
    @param pathname path name inside container where to extract archive
    """
    self.containername = containername
    self.pathname = pathname

  def run(self, source):
    """
    Read data from source and extract to directory specified by self.pathname
    inside container with name specified by self.containername.
    @param source file-like object to read tar archive data from
    """
    client = docker.from_env()
    container = client.containers.get(self.containername)
    container.put_archive(self.pathname, source)
