#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Test case for 3D supercell.
"""

import unittest

from catplot.grid_components.nodes import Node3D
from catplot.grid_components.edges import Edge3D
from catplot.grid_components.supercell import SuperCell3D


class SuperCell3DTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = True

    def test_construction_and_query(self):
        """ Test we can construct SuperCell3D correctly.
        """
        node1 = Node3D([1.0, 1.0, 1.0], color="#595959", width=1)
        node2 = Node3D([0.5, 0.5, 0.5], color="#595959", width=1)
        edge = Edge3D(node1, node2, n=10)
        supercell = SuperCell3D([node1, node2], [edge])

    def test_move(self):
        """ Test the edge can be moved correctly.
        """
        node1 = Node3D([1.0, 1.0, 1.0], color="#595959", width=1)
        node2 = Node3D([0.5, 0.5, 0.5], color="#595959", width=1)
        edge = Edge3D(node1, node2, n=10)
        supercell = SuperCell3D([node1, node2], [edge])

        supercell.move([0.5, 0.5, 0.5])

        self.assertListEqual(node1.coordinate.tolist(), [1.5, 1.5, 1.5])
        self.assertListEqual(node2.coordinate.tolist(), [1.0, 1.0, 1.0])

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
        self.assertListEqual(edge.z.tolist(), ref_x)

    def test_clone(self):
        """ Make sure we can clone a new supercell.
        """
        node1 = Node3D([1.0, 1.0, 1.0], color="#595959", width=1)
        node2 = Node3D([0.5, 0.5, 0.5], color="#595959", width=1)
        edge = Edge3D(node1, node2, n=10)
        supercell = SuperCell3D([node1, node2], [edge])

        supercell_clone = supercell.clone([0.5, 0.5, 0.5])

        self.assertListEqual(supercell_clone.nodes[0].coordinate.tolist(),
                             [1.5, 1.5, 1.5])
        self.assertListEqual(supercell_clone.nodes[1].coordinate.tolist(),
                             [1.0, 1.0, 1.0])

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

        self.assertListEqual(supercell_clone.edges[0].x.tolist(), ref_x)
        self.assertListEqual(supercell_clone.edges[0].y.tolist(), ref_x)
        self.assertListEqual(supercell_clone.edges[0].z.tolist(), ref_x)

    def test_add(self):
        node1 = Node3D([1.0, 1.0, 1.0], color="#595959", width=1)
        node2 = Node3D([0.5, 0.5, 0.5], color="#595959", width=1)
        edge = Edge3D(node1, node2, n=10)
        s1 = SuperCell3D([node1, node2], [edge])
        s2 = SuperCell3D([node1, node2], [edge])

        s = s1 + s2

        self.assertListEqual(s.nodes, [node1, node2, node1, node2])
        self.assertListEqual(s.edges, [edge, edge])

if "__main__" == __name__: 
    suite = unittest.TestLoader().loadTestsFromTestCase(SuperCell3DTest)
    unittest.TextTestRunner(verbosity=2).run(suite) 

