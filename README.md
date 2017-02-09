# Implementation of `docker cp` command in Python.

This is a simple Python library and utility to copy files or directories
between running Docker containers and local file system.

## Requirements

 - Python 3.4+
 - `docker` (former `docker_py`) Python module 2.0+

## Installation

```sh
git clone https://github.com/OlegGirko/docker-cp.git
cd docker-cp
python3 setup.py install --user
```

## Library usage

```python
from docker_cp import create_source, create_destination

# Allowed strings for src_path and dst_path:
# - -- stdin for source, stdout for destination
# CONTAINER:PATHNAME -- file or directory inside container
# PATHNAME -- file or directory inside local filesystem
src_path = ...
dst_path = ...

source = create_source(src_path)
destination = create_destination(dst_path)
destination.run(source)
```

## Command line usage

    docker-cp [-h] [-v] [-B BUFSIZE] SOURCE DESTINATION

    optional arguments:
      -h, --help            show this help message and exit
      -v, --verbose         verbose output
      -B BUFSIZE, --bufsize BUFSIZE
                            I/O buffer size
      SOURCE can be the following:
        "-" Read tar archive from stdin
        CONTAINERNAME:PATHNAME file or directory inside the container to copy
        PATHNAME local file or directory to copy
      DESTINATION can be the following:
        "-" Write tar archive to stdout
        CONTAINERNAME:PATHNAME directory inside the container to copy files to
        PATHNAME directory to copy files to

## Author

Oleg Girko

## License

GPLv3+
