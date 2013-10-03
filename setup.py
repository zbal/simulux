#!/usr/bin/env python
import os
import sys
import shutil

sys.path.insert(0, os.path.abspath('lib'))
from simulinux import __version__, __author__
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='simulux',
    version=__version__,
    description='Simulator for linux',
    url = 'https://github.com/zbal/simulux',
    author=__author__,
    author_email='vincent.viallet@gmail.com',
    license='MIT',
    package_dir={ 'simulux': 'lib/simulux' },
    packages=[
       'simulux'
    ]
)