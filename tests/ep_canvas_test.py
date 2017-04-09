#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Test case for Energy Profle Canvas.
"""

import unittest

from catplot.ep_components.ep_canvas import EPCanvas


class EPCanvasTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = True

    def test_construction_and_query(self):
        """ Test we can construct ElementaryLine object correctly.
        """
        canvas = EPCanvas(margin_ratio=0.2)

        self.assertEqual(canvas.margin_ratio, 0.2)
        self.assertListEqual(canvas.lines, [])
        self.assertListEqual(canvas.shadow_lines, [])
        self.assertTrue(canvas.figure)
        self.assertTrue(canvas.axes)

        # Check invalid reaction equation.
        self.assertRaises(ValueError, EPCanvas, margin_ratio=-0.1)

if "__main__" == __name__: 
    suite = unittest.TestLoader().loadTestsFromTestCase(EPCanvasTest)
    unittest.TextTestRunner(verbosity=2).run(suite) 

