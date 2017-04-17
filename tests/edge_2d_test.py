#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Test case for Edge2D.
"""

import unittest

from catplot.grid_components.nodes import Node2D
from catplot.grid_components.edges import Edge2D


class Edge2DTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = True

    def test_construction_and_query(self):
        """ Test we can construct Grid2DNode correctly.
        """
        node1 = Node2D([1.0, 1.0], color="#595959", width=1)
        node2 = Node2D([0.5, 0.5], color="#595959", width=1)
        edge = Edge2D(node1, node2, n=10)

        ref_x = [1.0,
                 0.9545454545454546,
                 0.9090909090909091,
                 0.8636363636363636,
                 0.8181818181818181,
                 0.7727272727272727,
                 0.7272727272727273,
                 0.6818181818181819,
                 0.6363636363636364,
                 0.5909090909090908,
                 0.5454545454545454,
                 0.5]
        self.assertListEqual(edge.x.tolist(), ref_x)
        self.assertListEqual(edge.y.tolist(), ref_x)

    def test_move(self):
        """ Test the edge can be moved correctly.
        """
        node1 = Node2D([1.0, 1.0], color="#595959", width=1)
        node2 = Node2D([0.5, 0.5], color="#595959", width=1)
        edge = Edge2D(node1, node2, n=10)

        edge.move([0.5, 0.5])

        self.assertListEqual(node1.coordinate.tolist(), [1.5, 1.5])
        self.assertListEqual(node2.coordinate.tolist(), [1.0, 1.0])

        ref_x = [1.5,
                 1.4545454545454546,
                 1.4090909090909092,
                 1.3636363636363638,
                 1.3181818181818181,
                 1.2727272727272727,
                 1.2272727272727273,
                 1.1818181818181819,
                 1.1363636363636362,
                 1.0909090909090908,
                 1.0454545454545454,
                 1.0]

        self.assertListEqual(edge.x.tolist(), ref_x)
        self.assertListEqual(edge.y.tolist(), ref_x)

if "__main__" == __name__: 
    suite = unittest.TestLoader().loadTestsFromTestCase(Edge2DTest)
    unittest.TextTestRunner(verbosity=2).run(suite) 

