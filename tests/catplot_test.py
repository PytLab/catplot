#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Module for all test in catplot.
"""

import unittest

from ep_chain_test import EPChainTest
from ep_canvas_test import EPCanvasTest
from elementary_line_test import ElementaryLineTest

def suite():
    test_suite = unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(EPChainTest),
        unittest.TestLoader().loadTestsFromTestCase(EPCanvasTest),
        unittest.TestLoader().loadTestsFromTestCase(ElementaryLineTest),
    ])

    return test_suite

if "__main__" == __name__:
    result = unittest.TextTestRunner(verbosity=2).run(suite())

    if result.errors or result.failures:
        raise ValueError("Get errors and failures")

