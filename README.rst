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

.. image:: https://img.shields.io/badge/pypi-v1.0.3-blue.svg
    :target: https://pypi.python.org/pypi/catplot/
    :alt: versions

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://raw.githubusercontent.com/PytLab/catplot/master/LICENSE


Introduction
------------
CatPlot is a Python library for plotting energy profile using interpolation algorithm.

Installation
------------
1. Via pip (recommend)::

    pip install catplot

2. From source::

    python setup.py install

Example
-------

See `examples <https://github.com/PytLab/catplot/tree/master/examples>`_ for more details(Continuously updated).

Plot an energy profile for an elementary reaction.

.. code-block:: python

    >>> from catplot.ep_components.ep_canvas import EPCanvas
    >>> from catplot.ep_components.ep_lines import ElementaryLine

    # Create an energy profile canvas.
    >>> canvas = EPCanvas()

    # Create an energy profile line.
    >>> line = ElementaryLine([0.0, 1.2, 0.8])

    # Add line to canvas.
    >>> canvas.add_line(line)

    # Plot it.
    >>> canvas.draw()
    >>> canvas.figure.show()

Result:

.. image:: https://github.com/PytLab/catplot/blob/master/pic/interactive.png


Important update log
--------------------

.. csv-table::
    :header: "Date", "Version", "Description"

    "2017-04-10", "1.0.0", "A brand new CatPlot"
    "2015-08-03", "0.0.1", "Intial Version"

