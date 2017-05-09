#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Test case for 2D grid canvas.
"""

import unittest

import matplotlib.pyplot as plt

from catplot.grid_components.grid_canvas import Grid2DCanvas, Grid3DCanvas
from catplot.grid_components.nodes import Node2D


class Grid2DCanvasTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = True

    def test_construction_and_query(self):
        """ Test the 2D grid canvas can be constructed corretly.
        """
        canvas = Grid2DCanvas()

        self.assertListEqual(canvas.nodes, [])
        self.assertListEqual(canvas.edges, [])

        plt.close(canvas.figure)

    def test_add_node(self):
        """ Make sure we can add node to canvas correctly.
        """
        canvas = Grid2DCanvas()

        n1 = Node2D([0.5, 0.5])
        n2 = Node2D([1.0, 1.0])
        canvas.add_node(n1)
        canvas.add_node(n2)

        # Check nodes in canvas.
        self.assertTrue(canvas.nodes)
        for node in canvas.nodes:
            self.assertTrue(isinstance(node, Node2D))

        # Check colors.
        for c in canvas.node_edgecolors:
            self.assertEqual(c, "#000000")

        for c in canvas.node_colors:
            self.assertEqual(c, "#000000")

        # Check cooridnates.
        ref_coordinates = [[0.5, 0.5], [1.0, 1.0]]
        self.assertListEqual(ref_coordinates, canvas.node_coordinates.tolist())

        plt.close(canvas.figure)

    def test_remove(self):
        """ Make sure we can remove a component correctly.
        """
        canvas = Grid2DCanvas()

        n1 = Node2D([0.5, 0.5])
        n2 = Node2D([1.0, 1.0])
        canvas.add_node(n1)
        canvas.add_node(n2)
        self.assertTrue(n1 in canvas.nodes)

        canvas.remove(n1)
        self.assertFalse(n1 in canvas.nodes)

    def test_draw(self):
        """ Make sure we can draw in grid canvas without exception raised.
        """
        canvas = Grid2DCanvas()

        n1 = Node2D([0.5, 0.5])
        n2 = Node2D([1.0, 1.0])
        canvas.add_node(n1)
        canvas.add_node(n2)

        canvas.draw()

        plt.close(canvas.figure)

    def test_to3d(self):
        """ Make sure we can map all components in 2D canvas to 3D canvas.
        """
        canvas2d = Grid2DCanvas()

        n1 = Node2D([0.5, 0.5])
        n2 = Node2D([1.0, 1.0])
        canvas2d.add_node(n1)
        canvas2d.add_node(n2)

        canvas3d = Grid3DCanvas()
        canvas2d.to3d(canvas3d)

        self.assertListEqual(canvas3d.nodes[0].coordinate.tolist(), [0.5, 0.5, 0.0])
        self.assertListEqual(canvas3d.nodes[1].coordinate.tolist(), [1.0, 1.0, 0.0])


if "__main__" == __name__: 
    suite = unittest.TestLoader().loadTestsFromTestCase(Grid2DCanvasTest)
    unittest.TextTestRunner(verbosity=2).run(suite) 

