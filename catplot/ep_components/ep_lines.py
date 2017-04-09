#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Module for line object in energy profile.
"""

import catplot.ep_components.descriptors as dc
from catplot.interpolate import get_potential_energy_points


class EPLine(object):
    """ Base class for lines in energy profile.
    """
    def __init__(self, x, y, **kwargs):
        self.x = x
        self.y = y

        self.color = kwargs.pop("color", "#000000")
        self.shadow_color = kwargs.pop("shadow_color", "#595959")
        self.shadow_depth = kwargs.pop("shadow_depth", 7)

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


class ElementaryLine(EPLine):
    """ Energy profile line for an elementary reaction.
    """
    # Descriptors.
    energies = dc.ElementaryEnergies("energies")
    rxn_equation = dc.ElementaryReaction("rxn_equation")
    interp_method = dc.InterpolationMethod("interp_method")

    def __init__(self, energies, **kwargs):
        self.energies = energies

        # Attributes for basic line.
        self.n = kwargs.pop("n", 100)
        self.hline_length = kwargs.pop("hline_length", 1.0)
        self.peak_width = kwargs.pop("peak_width", 1.0)
        self.interp_method = kwargs.pop("interp_method", "spline")
        self.rxn_equation = kwargs.pop("rxn_equation", None)

        # Get x and y lists for the given energies.
        x, y, _ = get_potential_energy_points(self.energies,
                                              n=self.n,
                                              hline_length=self.hline_length,
                                              peak_width=self.peak_width,
                                              kind=self.interp_method)
        super(ElementaryLine, self).__init__(x, y, **kwargs)

