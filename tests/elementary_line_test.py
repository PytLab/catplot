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

        # Check invalid reaction equation.
        self.assertRaises(ValueError, ElementaryLine, [0.0, 1.2, 0.7],
                          rxn_equation="A + B -> C")

        # Check invalid interpolation algorithm.
        self.assertRaises(ValueError, ElementaryLine, [0.0, 1.2, 0.7],
                          interp_method="abc")

        # Check invalid energy tuple.
        self.assertRaises(ValueError, ElementaryLine, [0.0, 1.2, 1.5])

    def test_translate(self):
        """ Make sure all points in line can be translated correctly.
        """
        line = ElementaryLine([0.0, 1.2, 0.7], n=2)

        line.translate(0.5, "x")
        ref_x = [0.5, 1.5, 1.5, 2.5, 2.5, 3.5]
        self.assertListEqual(line.x.tolist(), ref_x)

        line.translate(-0.5, "y")
        ref_y = [-0.5, -0.5, -0.5,
                 0.19999999999999996,
                 0.19999999999999996,
                 0.19999999999999996]
        self.assertListEqual(line.y.tolist(), ref_y)

if "__main__" == __name__: 
    suite = unittest.TestLoader().loadTestsFromTestCase(ElementaryLineTest)
    unittest.TextTestRunner(verbosity=2).run(suite) 

