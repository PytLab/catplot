#!/usr/bin/env python

from distutils.core import setup
from catplot import __version__ as version

maintainer = 'Shao-Zheng-Jiang'
maintainer_email = 'shaozhengjiang@gmail.com'
author = maintainer
author_email = maintainer_email
description = __doc__

requires = [
    'numpy',
    'scipy',
    'matplotlib',
]

license = 'LICENSE'
long_description = open('README.md').read()
name = 'python-catplot'
packages = [
    'catplot',
]
platforms = ['linux', 'windows']
url = 'https://github.com/PytLab/catplot'
download_url = 'https://github.com/PytLab/catplot/releases'

setup(
    author=author,
    author_email=author_email,
    description=description,
    license=license,
    long_description=long_description,
    maintainer=maintainer,
    name=name,
    packages=packages,
    platforms=platforms,
    url=url,
    download_url=download_url,
    version=version,
    )
