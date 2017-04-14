#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Test case for Grid2DNode.
"""

import unittest

from catplot.grid_components.nodes import Node2D


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

if "__main__" == __name__: 
    suite = unittest.TestLoader().loadTestsFromTestCase(Node2DTest)
    unittest.TextTestRunner(verbosity=2).run(suite) 

