#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Test case for 2D grid canvas.
"""

import unittest

from matplotlib.collections import PathCollection

from catplot.grid_components.grid_canvas import Grid2DCanvas


class Grid2DCanvasTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = True

    def test_construction_and_query(self):
        """ Test the 2D grid canvas can be constructed corretly.
        """
        canvas = Grid2DCanvas()

        self.assertListEqual(canvas.nodes, [])
        self.assertListEqual(canvas.edges, [])
        self.assertTrue(isinstance(canvas.collection, PathCollection))

if "__main__" == __name__: 
    suite = unittest.TestLoader().loadTestsFromTestCase(Grid2DCanvasTest)
    unittest.TextTestRunner(verbosity=2).run(suite) 

