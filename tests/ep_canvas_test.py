#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Test case for Energy Profle Canvas.
"""

import unittest

from catplot.ep_components.ep_canvas import EPCanvas
from catplot.ep_components.ep_lines import ElementaryLine
from catplot.ep_components.ep_chain import EPChain


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

    def test_draw(self):
        """ Make sure the lines can be added without exceptions.
        """
        canvas = EPCanvas()
        line = ElementaryLine([0.0, 1.3, 0.8])
        canvas.add_lines([line])
        canvas.draw()

    def test_add_species_annotations(self):
        """ Make sure the species annotations can be added without exceptions.
        """
        canvas = EPCanvas()
        line = ElementaryLine([0.0, 1.3, 0.8],
                              rxn_equation="CO_b + O_b <-> CO-O_2b -> CO2_g + 2*_b")
        canvas.add_lines([line])
        canvas.add_species_annotations(line)

    def test_add_horizontal_auxiliary_line(self):
        """ Make sure the horizontal line can be added without exceptions.
        """
        canvas = EPCanvas()
        line = ElementaryLine([0.0, 1.3, 0.8])
        canvas.add_lines([line])
        canvas.add_horizontal_auxiliary_line(line)

    def test_add_vertical_auxiliary_line(self):
        """ Make sure the vertical line can be added without exceptions.
        """
        canvas = EPCanvas()
        line = ElementaryLine([0.0, 1.3, 0.8])
        canvas.add_lines([line])
        canvas.add_vertical_auxiliary_lines(line)

    def test_add_chain(self):
        """ Test energy profile chain can be added correctly to canvas.
        """
        canvas = EPCanvas()

        self.assertFalse(canvas.lines)
        self.assertFalse(canvas.chains)

        l1 = ElementaryLine([0.0, 1.2, 0.6])
        l2 = ElementaryLine([0.0, 1.0, 0.8])
        chain = EPChain([l1, l2])
        canvas.add_chain(chain)

        self.assertEqual(len(canvas.lines), 2)
        for l in canvas.lines:
            self.assertTrue(isinstance(l, ElementaryLine))

        self.assertEqual(len(canvas.chains), 1)
        self.assertTrue(isinstance(canvas.chains[0], EPChain))

if "__main__" == __name__: 
    suite = unittest.TestLoader().loadTestsFromTestCase(EPCanvasTest)
    unittest.TextTestRunner(verbosity=2).run(suite) 

