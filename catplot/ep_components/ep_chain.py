#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Module for elementary energy profile line chain.
"""

import csv

import numpy as np


class EPChain(object):
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

    @property
    def x(self):
        """ All x values for lines in chain.
        """
        return np.concatenate([line.x for line in self.elementary_lines])

    @property
    def y(self):
        """ All y values for lines in chain.
        """
        return np.concatenate([line.y for line in self.elementary_lines])

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

    def translate(self, distance, direction="x"):
        """ Translate all elementary lines in the chain.

        Parameters:
        -----------
        distance: float, translation distance.
        direction: str, translation direction ("x", "y").
        """
        for line in self.elementary_lines:
            line.translate(distance, direction)

        return self

    def append(self, elementary_line):
        """ Append a elementary energy profile line to chain.
        """
        if elementary_line in self:
            msg = "Can't append a line in chain, try to append a copy of it."
            raise ValueError(msg)

        trans_x, trans_y = self.elementary_lines[-1].eigen_points.E
        elementary_line.translate(trans_x, "x").translate(trans_y, "y")
        self.elementary_lines.append(elementary_line)

    @property
    def scale_x(self):
        """ The scale of x values.
        """
        max_x = self.elementary_lines[-1].eigen_points.E[0]
        min_x = self.elementary_lines[-0].eigen_points.A[0]

        return max_x - min_x

    def export(self, filename):
        """ Export line data to file.
        """
        with open(filename, "w") as f:
            writer = csv.writer(f)
            for data in zip(self.x, self.y):
                writer.writerow(data)

    # -------------------------------------------------------------------------
    # Magic method to change default behaviours.
    # -------------------------------------------------------------------------

    def __contains__(self, item):
        """ Membership test operators.
        """
        return item in self.elementary_lines

    def __iter__(self):
        """ Make the chain iterable.
        """
        return iter(self.elementary_lines)

