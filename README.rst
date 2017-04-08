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

.. image:: https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square
    :target: https://raw.githubusercontent.com/PytLab/catplot/master/LICENSE


Introduction
------------
CatPlot is a Python library for plotting energy profile using interpolation algrithm.

Installation
------------
1. Via pip (recommend)::

   pip install catplot

2. From source::

   python setup.py install

Example
-------

Get points in energy profile for a reaction:

.. code_block:: python

    >>> from catplot import interpolate
    >>> x, y, _ = interpolate.get_potential_energy_points([0.0, 1.3, 0.7])

You can plot it with visualization tools:

.. code_block:: python
    >>> import matplotlib.pyplot as plt
    >>> plt.plot(x, y)
    >>> plt.show()

Result:

.. image:: https://github.com/PytLab/catplot/blob/dev/pic/interactive.png

