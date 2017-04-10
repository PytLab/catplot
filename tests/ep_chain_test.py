#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Test case for ElementaryLine.
"""

import unittest

from catplot.ep_components.ep_lines import ElementaryLine
from catplot.ep_components.ep_chain import EPLineChain


class EPLineChainTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = True

    def test_construction_and_query(self):
        """ Test we can construct EPLineChain object correctly.
        """
        l1 = ElementaryLine([0.0, 1.2, 0.7])
        l2 = ElementaryLine([0.0, 1.0, 0.5])
        l = EPLineChain([l1, l2])

        # Now the l2 should be translated.
        self.assertTupleEqual(l2.eigen_points.A, (3.0, 0.69999999999999996))

if "__main__" == __name__: 
    suite = unittest.TestLoader().loadTestsFromTestCase(EPLineChainTest)
    unittest.TextTestRunner(verbosity=2).run(suite) 

