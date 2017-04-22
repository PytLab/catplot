#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Module for all test in catplot.
"""

import unittest

from ep_chain_test import EPChainTest
from ep_canvas_test import EPCanvasTest
from elementary_line_test import ElementaryLineTest
from node_2d_test import Node2DTest
from edge_2d_test import Edge2DTest
from arrow_2d_test import Arrow2DTest
from supercell_2d_test import SuperCell2DTest
from grid_2d_canvas_test import Grid2DCanvasTest
from node_3d_test import Node3DTest
from edge_3d_test import Edge3DTest
from grid_3d_canvas_test import Grid3DCanvasTest
from supercell_3d_test import SuperCell3DTest

def suite():
    test_suite = unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(EPChainTest),
        unittest.TestLoader().loadTestsFromTestCase(EPCanvasTest),
        unittest.TestLoader().loadTestsFromTestCase(ElementaryLineTest),
        unittest.TestLoader().loadTestsFromTestCase(Node2DTest),
        unittest.TestLoader().loadTestsFromTestCase(Edge2DTest),
        unittest.TestLoader().loadTestsFromTestCase(Arrow2DTest),
        unittest.TestLoader().loadTestsFromTestCase(SuperCell2DTest),
        unittest.TestLoader().loadTestsFromTestCase(Grid2DCanvasTest),
        unittest.TestLoader().loadTestsFromTestCase(Node3DTest),
        unittest.TestLoader().loadTestsFromTestCase(Edge3DTest),
        unittest.TestLoader().loadTestsFromTestCase(Grid3DCanvasTest),
        unittest.TestLoader().loadTestsFromTestCase(SuperCell3DTest),
    ])

    return test_suite

if "__main__" == __name__:
    result = unittest.TextTestRunner(verbosity=2).run(suite())

    if result.errors or result.failures:
        raise ValueError("Get errors and failures")

