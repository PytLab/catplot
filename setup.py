#!/usr/bin/env python

from setuptools import setup, find_packages
from catplot import __version__ as version

maintainer = 'Shao-Zheng-Jiang'
maintainer_email = 'shaozhengjiang@gmail.com'
author = maintainer
author_email = maintainer_email
description = "A Python Library for Energy Profile and 2D/3D Lattice Grid Plotting"

install_requires = [
    'numpy>=1.12.1',
    'scipy>=0.19.0',
    'matplotlib>=2.0.0',
]

license = 'LICENSE'
long_description = """
=======
catplot
=======

.. image:: https://travis-ci.org/PytLab/catplot.svg?branch=master
    :target: https://travis-ci.org/PytLab/catplot
    :alt: Build Status

.. image:: https://img.shields.io/badge/python-3.5-green.svg
    :target: https://www.python.org/downloads/release/python-351/
    :alt: platform

.. image:: https://img.shields.io/badge/python-2.7-green.svg
    :target: https://www.python.org/downloads/release/python-2710
    :alt: platform

.. image:: https://img.shields.io/badge/pypi-v1.2.7-blue.svg
    :target: https://pypi.python.org/pypi/catplot/
    :alt: versions

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://raw.githubusercontent.com/PytLab/catplot/master/LICENSE


Introduction
------------

**CatPlot** is a Python Library for Energy Profile and Abstract Grid(2D/3D) plotting.

Installation
------------

1. Via pip (recommend)::

    pip install catplot

2. From source::

    python setup.py install
"""
name = 'catplot'
packages = [
    'catplot',
]
platforms = ['linux', 'windows', 'macos']
url = 'https://github.com/PytLab/catplot'
download_url = 'https://github.com/PytLab/catplot/releases'

classifiers = [
    'Development Status :: 3 - Alpha',
    'Topic :: Utilities',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
]

setup(author=author,
      author_email=author_email,
      description=description,
      license=license,
      long_description=long_description,
      install_requires=install_requires,
      maintainer=maintainer,
      name=name,
      packages=find_packages(),
      platforms=platforms,
      url=url,
      download_url=download_url,
      version=version)

