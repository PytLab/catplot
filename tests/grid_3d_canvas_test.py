#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Test case for 3D grid canvas.
"""

import unittest

from matplotlib.collections import PathCollection

from catplot.grid_components.grid_canvas import Grid3DCanvas
from catplot.grid_components.nodes import Node3D


class Grid3DCanvasTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = True

    def test_construction_and_query(self):
        """ Test the 2D grid canvas can be constructed corretly.
        """
        canvas = Grid3DCanvas()

        self.assertListEqual(canvas.nodes, [])
        self.assertListEqual(canvas.edges, [])

    def test_add_node(self):
        """ Make sure we can add node to canvas correctly.
        """
        canvas = Grid3DCanvas()

        n1 = Node3D([0.5, 0.5, 0.5])
        n2 = Node3D([1.0, 1.0, 1.0])
        canvas.add_node(n1)
        canvas.add_node(n2)

        # Check nodes in canvas.
        self.assertTrue(canvas.nodes)
        for node in canvas.nodes:
            self.assertTrue(isinstance(node, Node3D))

        # Check colors.
        for c in canvas.node_edgecolors:
            self.assertEqual(c, "#000000")

        for c in canvas.node_colors:
            self.assertEqual(c, "#000000")

        # Check cooridnates.
        ref_coordinates = [[0.5, 0.5, 0.5], [1.0, 1.0, 1.0]]
        self.assertListEqual(ref_coordinates, canvas.node_coordinates.tolist())

    def test_draw(self):
        """ Make sure we can draw in grid canvas without exception raised.
        """
        canvas = Grid3DCanvas()

        n1 = Node3D([0.5, 0.5, 0.5])
        n2 = Node3D([1.0, 1.0, 1.0])
        canvas.add_node(n1)
        canvas.add_node(n2)

        canvas.draw()

if "__main__" == __name__: 
    suite = unittest.TestLoader().loadTestsFromTestCase(Grid3DCanvasTest)
    unittest.TextTestRunner(verbosity=2).run(suite) 

