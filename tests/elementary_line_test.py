#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Test case for ElementaryLine.
"""

import unittest

from catplot.ep_components.ep_lines import ElementaryLine


class ElementaryLineTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = True

    def test_construction_and_query(self):
        """ Test we can construct ElementaryLine object correctly.
        """
        line = ElementaryLine([0.0, 1.2, 0.7], n=2)

        ret_x = line.x.tolist()
        ref_x = [0.0, 1.0, 1.0, 2.0, 2.0, 3.0]
        self.assertListEqual(ret_x, ref_x)

        ret_y = line.y.tolist()
        ref_y = [0.0, 0.0, -3.4426554548552387e-18, 0.7, 0.7, 0.7]
        self.assertListEqual(ret_y, ref_y)

        self.assertIsNone(line.rxn_equation)
        self.assertEqual(line.color, "#000000")
        self.assertEqual(line.shadow_color, "#595959")
        self.assertEqual(line.shadow_depth, 7)
        self.assertEqual(line.hline_length, 1.0)
        self.assertEqual(line.interp_method, "spline")
        self.assertEqual(line.n, 2)
        self.assertEqual(line.peak_width, 1.0)

if "__main__" == __name__: 
    suite = unittest.TestLoader().loadTestsFromTestCase(ElementaryLineTest)
    unittest.TextTestRunner(verbosity=2).run(suite) 

