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

.. image:: https://img.shields.io/badge/pypi-v2.0.0-blue.svg
    :target: https://pypi.python.org/pypi/catplot/
    :alt: versions

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
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

.. code-block:: python

    In [1]: from catplot import interpolate

    In [2]: x1, y1, _ = interpolate.get_potential_energy_points([0.0, 1.3, 0.7])

    In [3]: x2, y2, _ = interpolate.get_potential_energy_points([0.0, 1.0, 0.5])

You can plot it with visualization tools:

.. code-block:: python

    In [4]: import matplotlib.pyplot as plt

    In [5]: plt.plot(x1, y1)
    Out[5]: [<matplotlib.lines.Line2D at 0x1159a29e8>]

    In [6]: plt.plot(x2, y2)
    Out[6]: [<matplotlib.lines.Line2D at 0x1159c5240>]

    In [7]: plt.show()

Result:

.. image:: https://github.com/PytLab/catplot/blob/master/pic/interactive.png


.. _老版README: https://github.com/PytLab/catplot/blob/master/README_old.md


Important update log
--------------------

.. csv-table::
    :header: "Date", "Version", "Description"

    "2017-04-07", "2.0.0", "兼容Python3 & 使用quadratic和spline结合的插值算法使绘制更通用"
    "2015-10-02", "1.0.0", "使用新的quadratic interpolation算法"
    "2015-08-28", "0.1.1", "新增半峰宽设置"

