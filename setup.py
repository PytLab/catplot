#!/usr/bin/env python

from setuptools import setup, find_packages
from catplot import __version__ as version

maintainer = 'Shao-Zheng-Jiang'
maintainer_email = 'shaozhengjiang@gmail.com'
author = maintainer
author_email = maintainer_email
description = "A Python Library for Energy Profile Plotting"

install_requires = [
    'numpy>=1.12.1',
    'scipy>=0.19.0',
    'matplotlib>=2.0.0',
]

license = 'LICENSE'
long_description = open('README.rst').read()
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

