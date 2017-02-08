#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import sys

description = """Copy files from/to running Docker container."""

setup(
  name='docker_cp',
  version='0.0.1',
  description="Copy files from/to running Docker container",
  long_description=description,
  keywords='docker, tar, file',
  author='Oleg Girko',
  author_email='ol@infoserver.lv',
  url='https://github.com/OlegGirko/docker-cp',
  license='GPLv3+',
  packages=['docker_cp'],
  entry_points={'console_scripts': ['docker-cp = docker_cp:main']},
  install_requires=['setuptools', 'docker >= 2.0.0'],
  setup_requires=['setuptools', 'docker >= 2.0.0'],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Topic :: Software Development :: Build Tools',
    'Topic :: System :: Software Distribution',
  ]
)
