#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Test case for Grid2DNode.
"""

import unittest

from catplot.grid_components.nodes import Node2D, Node3D


class Node2DTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = True

    def test_construction_and_query(self):
        """ Test we can construct Grid2DNode correctly.
        """
        node = Node2D([1.0, 1.0], color="#595959", line_width=1)

        self.assertListEqual(node.coordinate.tolist(), [1.0, 1.0])
        self.assertEqual(node.color, "#595959")
        self.assertEqual(node.edgecolor, "#595959")
        self.assertEqual(node.size, 400)
        self.assertEqual(node.style, "o")
        self.assertEqual(node.line_width, 1)

        # Exception is expected when invalid cooridnate passed in.
        self.assertRaises(ValueError, Node2D, [1.0, 1.0, 0.0])

    def test_move(self):
        """ Make sure we can move the node correctly.
        """
        node = Node2D([1.0, 1.0], color="#595959", line_width=1)
        node.move([1.0, 1.0])
        self.assertListEqual(node.coordinate.tolist(), [2.0, 2.0])

        # Check chain operation.
        node.move([-1.0, -1.0,]).move([-1.0, -1.0])
        self.assertListEqual(node.coordinate.tolist(), [0.0, 0.0])

    def test_clone(self):
        """ Make sure we can clone a node correctly.
        """
        node = Node2D([0.5, 0.5], color="#595959", line_width=1)
        node_clone = node.clone(relative_position=[0.5, 0.5])

        self.assertListEqual(node_clone.coordinate.tolist(), [1.0, 1.0])
        self.assertFalse(node is node_clone)

    def test_to3d(self):
        """ Make sure we can convert 2D node to corresponding 3D node.
        """
        node2d = Node2D([0.5, 0.5], color="#595959", line_width=1)
        node3d = node2d.to3d()

        self.assertTrue(isinstance(node3d, Node3D))
        self.assertListEqual(node3d.coordinate.tolist(), [0.5, 0.5, 0.0])
        self.assertEqual(node2d.color, node3d.color)
        self.assertEqual(node2d.line_width, node3d.line_width)

if "__main__" == __name__: 
    suite = unittest.TestLoader().loadTestsFromTestCase(Node2DTest)
    unittest.TextTestRunner(verbosity=2).run(suite) 

