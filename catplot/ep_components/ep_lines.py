#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Module for line object in energy profile.
"""

import csv
from collections import namedtuple

from matplotlib.lines import Line2D
from matplotlib import transforms
import numpy as np

import catplot.ep_components.descriptors as dc
from catplot.interpolate import get_potential_energy_points


class EPLine(object):
    """ Base class for lines in energy profile providing some general attributes.

    Parameters:
    -----------
    x: 1-D array or list, x values of points.
    y: 1-D array or list, y values of points.

    line_width: float, optional
        line width, default is 3.
    color: str, optional,
        color code of the line, default is #000000 (black).
    shadow_color: str, optional
        color code of the shadow lines, default is #595959.
    shadow_depth: int, optional
        shadow depth of the line, default is 0, no shadow.
    """
    def __init__(self, x, y, **kwargs):
        self.x = x
        self.y = y

        self.color = kwargs.pop("color", "#000000")
        self.shadow_color = kwargs.pop("shadow_color", "#595959")
        self.shadow_depth = kwargs.pop("shadow_depth", 0)
        self.line_width = kwargs.pop("line_width", 3)

    def translate(self, distance, direction="x"):
        """ Translate all points in line.

        Parameters:
        -----------
        distance: float, translation distance.
        direction: str, translation direction ("x", "y").

        Example:
        --------
        >>> line.translate(-1.0, direction="y")

        """
        if direction == "x":
            self.x += distance
        elif direction == "y":
            self.y += distance
        else:
            raise ValueError("Invalide direction {}".format(direction))

        # Return line itself for the chain operations.
        return self

    def line2d(self):
        """ Create a corresponding matplotlib.lines.Line2D object.
        """
        return Line2D(self.x, self.y,
                      linewidth=self.line_width,
                      color=self.color)

    def export(self, filename):
        """ Export line data to file.
        """
        with open(filename, "w") as f:
            writer = csv.writer(f)
            for data in zip(self.x, self.y):
                writer.writerow(data)


class ElementaryLine(EPLine):
    """ Energy profile line for an elementary reaction.

    Parameters:
    -----------
    energies: tuple or list,
        energies for states of a elementary reaction.

    n: int, optional
        the point number in each state, default is 100.
    hline_length: float, optioanl
        the length of the horizontal line for the IS and FS.
    peak_width: float, optional
        the width of the peak in energy profile, default is 1.0.
    interp_method: str, optional
        the type of interpolation algorithm("spline", "quadratic")
        default is "spline".
    rxn_equation: str, optional
        elementary reaction equation, default is None.
    line_width: float, optional
        line width, default is 3.
    color: str, optional,
        color code of the line, default is #000000 (black).
    shadow_color: str, optional
        color code of the shadow lines, default is #595959.
    shadow_depth: int, optional
        shadow depth of the line, default is 0, no shadow.
    """
    # Descriptors.

    energies = dc.ElementaryEnergies("energies")
    rxn_equation = dc.ElementaryReaction("rxn_equation")
    interp_method = dc.InterpolationMethod("interp_method")

    def __init__(self, energies, **kwargs):
        self.energies = self._get_relative_energies(energies)

        # Attributes for basic line.
        self.n = kwargs.pop("n", 100)
        self.hline_length = kwargs.pop("hline_length", 1.0)
        self.peak_width = kwargs.pop("peak_width", 1.0)
        self.interp_method = kwargs.pop("interp_method", "spline")
        self.rxn_equation = kwargs.pop("rxn_equation", None)

        # Get x and y lists for the given energies.
        x, y = get_potential_energy_points(self.energies,
                                           n=self.n,
                                           hline_length=self.hline_length,
                                           peak_width=self.peak_width,
                                           kind=self.interp_method)
        super(ElementaryLine, self).__init__(x, y, **kwargs)

    def _get_relative_energies(self, energies):
        """ Translate the energy tuple to origin.
        """
        reference = energies[0]
        return (np.array(energies) - reference).tolist()

    @property
    def scale_x(self):
        """ The scale of x values.
        """
        max_x = np.max(self.x)
        min_x = np.min(self.x)

        return max_x - min_x

    @property
    def scale_y(self):
        """ The scale of y values.
        """
        max_y = np.max(self.y)
        min_y = np.min(self.y)

        return  max_y - min_y

    @property
    def eigen_points(self):
        r""" Get the important points for an elementary profile line.

             _ C                                C__E
            / \                                 /D
           /   \_ E    or without barrier      /
        A_/    D                            A_/
           B                                   B

        Get coordinates of points A, B, C, D, E.
        """
        # Coordinate for point A.
        ca = (self.x[0], self.y[0])

        # B
        cb = (ca[0] + self.hline_length, ca[1])

        # D
        cd = (cb[0] + self.peak_width, cb[1] + self.energies[-1])

        # C, the peak.
        if len(self.energies) == 3:
            y = np.max(self.y)
            idx = self.y.tolist().index(y)
            x = self.x[idx]
            cc = (x, y)
            has_barrier = True
        else:
            cc = cd
            has_barrier = False

        # E
        ce = (cd[0] + self.hline_length, cd[1])

        # Define a namedtuple for eigen points here.
        EigenPts = namedtuple("EigenPts", ["has_barrier", "A", "B", "C", "D", "E"])

        return EigenPts._make([has_barrier, ca, cb, cc, cd, ce])

