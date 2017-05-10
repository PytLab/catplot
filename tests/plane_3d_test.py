#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Test case for Grid2DNode.
"""

import unittest

from catplot.grid_components.planes import Plane3D


class Plane3DTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = True

    def test_construction_and_query(self):
        """ Test we can construct plane correctly.
        """
        plane = Plane3D([1, 2], [1, 2], 3, color="#595959", edgecolor="#595959")

        self.assertListEqual(plane.x.tolist(), [[1.0, 2.0], [1.0, 2.0]])
        self.assertListEqual(plane.y.tolist(), [[1.0, 1.0], [2.0, 2.0]])
        self.assertListEqual(plane.z.tolist(), [[3.0, 3.0], [3.0, 3.0]])
        self.assertEqual(plane.color, "#595959")
        self.assertEqual(plane.edgecolor, "#595959")
        self.assertFalse(plane.shade)

    def test_move(self):
        """ Make sure we can move the plane correctly.
        """
        plane = Plane3D([1, 2], [1, 2], 3, color="#595959", edgecolor="#595959")
        plane.move([1.0, 1.0, 1.0])
        self.assertListEqual(plane.x.tolist(), [[2.0, 3.0], [2.0, 3.0]])
        self.assertListEqual(plane.y.tolist(), [[2.0, 2.0], [3.0, 3.0]])
        self.assertListEqual(plane.z.tolist(), [[4.0, 4.0], [4.0, 4.0]])

        # Check chain operation.
        plane.move([-1.0, -1.0, -1.0]).move([-1.0, -1.0, -1.0])
        self.assertListEqual(plane.x.tolist(), [[0, 1], [0, 1]])

    def test_clone(self):
        """ Make sure we can clone a plane correctly.
        """
        plane = Plane3D([1, 2], [1, 2], 3, color="#595959", edgecolor="#595959")
        plane_clone = plane.clone(relative_position=[1.0, 1.0, 1.0])

        self.assertListEqual(plane_clone.x.tolist(), [[2, 3], [2, 3]])
        self.assertFalse(plane is plane_clone)

if "__main__" == __name__: 
    suite = unittest.TestLoader().loadTestsFromTestCase(Plane3DTest)
    unittest.TextTestRunner(verbosity=2).run(suite) 

