#!/usr/bin/env python
import os
import sys
import shutil
from glob import glob

sys.path.insert(0, os.path.abspath('lib'))
from simulux import __version__, __author__, __author_email__
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from simulux.constants import DIST_DEFAULTS_PATH
data_files = []
data_files.append((DIST_DEFAULTS_PATH, glob('./defaults/*')))

setup(
    name='simulux',
    version=__version__,
    description='Simulator for linux',
    url = 'https://github.com/zbal/simulux',
    author=__author__,
    author_email=__author_email__,
    license='MIT',
    package_dir={ 'simulux': 'lib/simulux' },
    packages=[
       'simulux'
    ],
    data_files=data_files
)
