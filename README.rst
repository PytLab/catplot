=======
catplot
=======

.. image:: https://travis-ci.org/PytLab/catplot.svg?branch=master
    :target: https://travis-ci.org/PytLab/catplot
    :alt: Build Status

.. image:: https://landscape.io/github/PytLab/catplot/master/landscape.svg?style=flat
   :target: https://landscape.io/github/PytLab/catplot/master
   :alt: Code Health

.. image:: https://codecov.io/gh/PytLab/catplot/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/PytLab/catplot

.. image:: https://img.shields.io/badge/python-3.5, 2.7-green.svg
    :target: https://www.python.org/downloads/release/python-351/
    :alt: platform

.. image:: https://img.shields.io/badge/pypi-v1.3.3-blue.svg
    :target: https://pypi.python.org/pypi/catplot/
    :alt: versions


Introduction
------------

**CatPlot** is a Python Library for Energy Profile and Abstract Grid(2D/3D) plotting.

Installation
------------

1. Via pip (recommend)::

    pip install catplot

2. From source::

    python setup.py install


See `examples <https://github.com/PytLab/catplot/tree/master/examples>`_ for more details(Continuously updated).


Energy Profile Plotting
-----------------------

**CatPlot** can plot energy profile using interpolation algorithm.

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

.. image:: https://github.com/PytLab/catplot/blob/master/pic/energy_profile.png


2D Grid Plotting
----------------

You can use **CatPlot** to plot abstract lattice grid, see  `example <https://github.com/PytLab/catplot/tree/master/examples/grid_2d_examples/expand_supercell.ipynb>`_ for details.

Result:

.. image:: https://github.com/PytLab/catplot/blob/master/pic/grid_2d.png


3D Grid Plotting
----------------

Now **CatPlot** can plot abstract 3D lattice grid, see `example <https://github.com/PytLab/catplot/tree/master/examples/grid_3d_examples/expand_3d_supercell.ipynb>`_ for plot details.

Result:

.. image:: https://github.com/PytLab/catplot/blob/master/pic/grid_3d.png

Code Structure
--------------

::

    ├── LICENSE                         # License file
    ├── MANIFEST.in                     # Define the list of files to include in the distribution
    ├── README.rst                      # This file
    ├── catplot                         # Main catplot pacakge
    │   ├── __init__.py
    │   ├── canvas.py                   # 2D & 3D base canvas
    │   ├── chem_parser.py              # Chemical expression parser
    │   ├── descriptors.py              # Python descriptors
    │   ├── ep_components               # Energy profile components
    │   │   ├── __init__.py
    │   │   ├── ep_canvas.py            # Energy profile canvas
    │   │   ├── ep_chain.py             # Energy profile chain
    │   │   ├── ep_lines.py             # Energy profiles line
    │   ├── grid_components             # Grid plotting components
    │   │   ├── __init__.py
    │   │   ├── edges.py                # Edge in grid graph
    │   │   ├── grid_canvas.py          # Grid canvas
    │   │   ├── nodes.py                # Node in grid graph
    │   │   ├── planes.py               # Plane in 3D canvas
    │   │   ├── supercell.py            # Supercell in a grid
    │   ├── interpolate.py              # Interpolation algorithms implementation
    ├── examples                        # Jupyter Notebook examples
    │   ├── energy_profile_examples
    │   ├── grid_2d_examples
    │   └── grid_3d_examples
    ├── pic
    ├── requirements.txt                # Python dependencies
    ├── scripts                         # Plotting script
    │   └── multiplot
    ├── setup.cfg
    ├── setup.py                        # Python setup script
    └── tests                           # Unit test
        ├── arrow_2d_test.py
        ├── catplot_test.py
        ├── edge_2d_test.py
        ├── edge_3d_test.py
        ├── elementary_line_test.py
        ├── ep_canvas_test.py
        ├── ep_chain_test.py
        ├── grid_2d_canvas_test.py
        ├── grid_3d_canvas_test.py
        ├── node_2d_test.py
        ├── node_3d_test.py
        ├── plane_3d_test.py
        ├── supercell_2d_test.py
        ├── supercell_3d_test.py

Important update log
--------------------

.. csv-table::
    :header: "Date", "Version", "Description"

    "2017-04-23", "1.2.0", "Add 3D grid plotting"
    "2017-04-17", "1.1.0", "Add 2D grid plotting"
    "2017-04-10", "1.0.0", "A brand new CatPlot"
    "2015-08-03", "0.0.1", "Intial Version"

