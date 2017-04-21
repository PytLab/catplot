#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Test case for Arrow2D.
"""

import unittest

from catplot.grid_components.nodes import Node2D
from catplot.grid_components.edges import Arrow2D


class Arrow2DTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = True

    def test_construction_and_query(self):
        """ Test we can construct 2D arrow correctly.
        """
        node1 = Node2D([1.0, 1.0], color="#595959", width=1)
        node2 = Node2D([0.5, 0.5], color="#595959", width=1)
        arrow = Arrow2D(node1, node2)

        ref_x = [1.0, 0.5]
        self.assertListEqual(arrow.x.tolist(), ref_x)
        self.assertListEqual(arrow.y.tolist(), ref_x)

        # Check other attributes.
        self.assertEqual(arrow.color, "#595959")
        self.assertEqual(arrow.edgecolor, "#595959")
        self.assertEqual(arrow.dx, -0.5)
        self.assertEqual(arrow.dy, -0.5)
        self.assertEqual(arrow.alpha, 1)
        self.assertListEqual(arrow.start.tolist(), [1.0, 1.0])
        self.assertListEqual(arrow.end.tolist(), [0.5, 0.5])
        self.assertEqual(arrow.head_length, 0.06)
        self.assertEqual(arrow.head_width, 0.03)
        self.assertEqual(arrow.shape, "full")
        self.assertEqual(arrow.style, "solid")
        self.assertEqual(arrow.width, 1)
        self.assertEqual(arrow.zorder, 0)

    def test_move(self):
        """ Test the arrow can be moved correctly.
        """
        node1 = Node2D([1.0, 1.0], color="#595959", width=1)
        node2 = Node2D([0.5, 0.5], color="#595959", width=1)
        arrow = Arrow2D(node1, node2)

        arrow.move([0.5, 0.5])

        ref_x = [1.5, 1.0]

        self.assertListEqual(arrow.x.tolist(), ref_x)
        self.assertListEqual(arrow.y.tolist(), ref_x)

        # The delta x and y should be unchanged.
        self.assertEqual(arrow.dx, -0.5)
        self.assertEqual(arrow.dy, -0.5)

if "__main__" == __name__: 
    suite = unittest.TestLoader().loadTestsFromTestCase(Arrow2DTest)
    unittest.TextTestRunner(verbosity=2).run(suite) 

