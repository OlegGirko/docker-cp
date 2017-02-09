from .io import DEFAULT_BUFSIZE
from .stdioio import StdioIOFactory
from .dockerio import DockerIOFactory
from .tarfileio import TarFileIOFactory
import sys

IO_FACTORY_CLASSES = [StdioIOFactory, DockerIOFactory, TarFileIOFactory]

def create_source(pathname, bufsize=DEFAULT_BUFSIZE):
  for cls in IO_FACTORY_CLASSES:
    source = cls.create_source(pathname, bufsize)
    if source is not None:
      return source

def create_destination(pathname, bufsize=DEFAULT_BUFSIZE):
  for cls in IO_FACTORY_CLASSES:
    destination = cls.create_destination(pathname, bufsize)
    if destination is not None:
      return destination

def main():
  import argparse
  parser = argparse.ArgumentParser(
    description='Copy files from/to running Docker container',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""\
  source can be the following:
    "-" Read tar archive from stdin
    CONTAINERNAME:PATHNAME file or directory inside the container to copy
    PATHNAME local file or directory to copy
  destination can be the following:
    "-" Write tar archive to stdout
    CONTAINERNAME:PATHNAME directory inside the container to copy files to
    PATHNAME directory to copy files to
  """)
  parser.add_argument('-v', '--verbose', action='store_true',
                      help='verbose output')
  parser.add_argument('-B', '--bufsize', type=int, default=DEFAULT_BUFSIZE,
                      help='I/O buffer size')
  parser.add_argument('source', help='Source file or directory')
  parser.add_argument('destination', help='Destination directory')
  args = parser.parse_args()
  verbose = args.verbose
  bufsize = args.bufsize
  src_path = args.source
  dst_path = args.destination
  if verbose:
    sys.stderr.write("Bufsize = %d\n" % bufsize)
    sys.stderr.write("Source = %s\n" % src_path)
    sys.stderr.write("Destination = %s\n" % dst_path)
  source = create_source(src_path, bufsize)
  destination = create_destination(dst_path, bufsize)
  destination.run(source)

if __name__ == "__main__":
  main()
