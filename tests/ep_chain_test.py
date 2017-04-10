#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Test case for ElementaryLine.
"""

import unittest

from catplot.ep_components.ep_lines import ElementaryLine
from catplot.ep_components.ep_chain import EPChain


class EPChainTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = True

    def test_construction_and_query(self):
        """ Test we can construct EPChain object correctly.
        """
        l1 = ElementaryLine([0.0, 1.2, 0.7])
        l2 = ElementaryLine([0.0, 1.0, 0.5])
        l = EPChain([l1, l2])

        # Now the l2 should be translated.
        self.assertTupleEqual(l2.eigen_points.A, (3.0, 0.69999999999999996))

    def test_translate(self):
        """ Make sure all lines in chain can be translated correctly.
        """
        l1 = ElementaryLine([0.0, 1.2, 0.6])
        l2 = ElementaryLine([0.0, 1.0, 0.8])
        chain = EPChain([l1, l2])

        chain.translate(1.0, "x").translate(1.0, "y")

        self.assertTupleEqual(l1.eigen_points.A, (1.0, 1.0))
        self.assertTupleEqual(l2.eigen_points.A, (4.0, 1.6000000000000001))

    def test_append(self):
        """ Make sure the elementary line can be appended properly.
        """
        l1 = ElementaryLine([0.0, 1.2, 0.7])
        l2 = ElementaryLine([0.0, 1.0, 0.5])
        l = EPChain([l1])

        l.append(l2)

        # Check the l2 should be translated.
        self.assertTupleEqual(l2.eigen_points.A, (3.0, 0.69999999999999996))

        # Appending a repeated line will raise an exception.
        self.assertRaises(ValueError, l.append, l2)

    def test_membership(self):
        """ Test the `in` operator.
        """
        l1 = ElementaryLine([0.0, 1.2, 0.7])
        l2 = ElementaryLine([0.0, 1.0, 0.5])
        chain = EPChain([l1])

        self.assertTrue(l1 in chain)
        self.assertFalse(l2 in chain)

    def test_iterable(self):
        """ Make sure the chain is iterable.
        """
        l1 = ElementaryLine([0.0, 1.2, 0.7])
        l2 = ElementaryLine([0.0, 1.0, 0.5])
        chain = EPChain([l1, l2])

        for l in chain:
            self.assertTrue(isinstance(l, ElementaryLine))

if "__main__" == __name__: 
    suite = unittest.TestLoader().loadTestsFromTestCase(EPChainTest)
    unittest.TextTestRunner(verbosity=2).run(suite) 

