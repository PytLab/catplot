#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Module for elementary energy profile line chain.
"""


class EPLineChain(object):
    """ Chain for multiple elementary energy profile lines joined together.
    """
    def __init__(self, elementary_lines):
        self.elementary_lines = elementary_lines

        # Expand all elementary lines.
        self.expand(self.elementary_lines)

    def __check_elementary_lines(self, lines):
        for line in lines:
            if not isinstance(line, ElementaryLine):
                msg = "Entry in elementary line list must be ElementaryLine obejct."
                raise ValueError(msg)

    @staticmethod
    def expand(elementary_lines):
        """ Expand all elementary lines by translation operations.
            _
            _   ->  _ _ _
            _   ->

        """
        for idx, line in enumerate(elementary_lines):
            if idx == 0:
                continue

            # Translate current line.
            prev_line = elementary_lines[idx-1]
            trans_x, trans_y = prev_line.eigen_points.E
            line.translate(trans_x, "x").translate(trans_y, "y")

