#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os

from setuptools import setup, find_packages
from downmergesubs.downmergesubs import __version__, __author__

py_version = sys.version_info[:2]

if py_version < (2, 6):
    raise Exception('This version of srtmerge needs Python 2.6 or later. ')

if sys.argv[-1] in ("submit", "publish"):
    os.system("python setup.py bdist_egg sdist --format=zip upload")
    sys.exit()

README = """
"""

requires = ['srtmerge']
if py_version < (2, 7):
    requires.append('argparse')

setup(name='downmergesubs',
      version=__version__,
      author=__author__,
      author_email='xecgr@gmail.com',
      packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
      description="downmergesubs (.srt) used to download and merge subs",
      long_description=README,
      url="https://github.com/xecgr/downmergesubs",
      license="LGPL",
      install_requires=requires,
      platforms=["Unix,"],
      keywords="downmergesubs, srt, subtitle",
      test_suite='tests',
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Environment :: Console",
          "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
          "Operating System :: POSIX :: Linux",
          "Programming Language :: Python :: 2",
          "Topic :: Text Processing",
          "Topic :: Utilities"
      ],
      entry_points={
          'console_scripts': [
              'downmergesubs = downmergesubs.cli:main'
          ]},
      )
