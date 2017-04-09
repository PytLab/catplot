#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple

import matplotlib.pyplot as plt
from matplotlib import transforms
from matplotlib.lines import Line2D
import numpy as np

import catplot.ep_components.descriptors as dc
from catplot.ep_components.ep_lines import EPLine


class EPCanvas(object):
    """ Energy profile canvas.

    Parameters:
    -----------
    margin_ratio: float, optional, default is 0.1
        control the white space between energy profile line and axes.

    """
    margin_ratio = dc.MarginRatio("margin_ratio")

    def __init__(self, **kwargs):
        self.margin_ratio = kwargs.pop("margin_ratio", 0.1)

        self.figure = plt.figure()
        self.axes = self.figure.add_subplot(111)

        # Energy profile lines.
        self.lines = []
        self.shadow_lines = []

    def add_lines(self, ep_lines):
        """ Add energy profile lines to canvas.
        """
        # Check lines before adding.
        for line in ep_lines:
            if not isinstance(line, EPLine):
                raise ValueError("line in ep_lines must be instance of EPLine")

        self.lines.extend(ep_lines)

    def _render_ep_lines(self):
        """ Render energy profile lines in canvas.
        """
        for line in self.lines:
            for idx in range(line.shadow_depth):
                identity_trans = transforms.IdentityTransform()
                offset = transforms.ScaledTranslation(idx, -idx, identity_trans)
                shadow_trans = self.axes.transData + offset

                # Create matplotlib Line2D.
                alpha = (line.shadow_depth-idx)/2.0/line.shadow_depth
                shadow_line = Line2D(line.x, line.y,
                                     linewidth=line.line_width,
                                     color=line.shadow_color,
                                     transform=shadow_trans,
                                     alpha=alpha)
                self.shadow_lines.append(shadow_line)

    def _get_data_limits(self):
        """ Private helper function to get the limits of data.
        """
        # Merge all data in energy profile lines.
        all_x = np.concatenate([l.x for l in self.lines])
        all_y = np.concatenate([l.y for l in self.lines])

        max_x = np.max(all_x)
        min_x = np.min(all_x)
        scale_x = max_x - min_x

        max_y = np.max(all_y)
        min_y = np.min(all_y)
        scale_y = max_y - min_y

        # Define a namedtuple to be returned.
        Limit = namedtuple("Limit", ["max_x", "min_x", "max_y", "min_y"])
        limits = [max_x + self.margin_ratio*scale_x,
                  min_x - self.margin_ratio*scale_x,
                  max_y + self.margin_ratio*scale_y,
                  min_x - self.margin_ratio*scale_y]

        return Limit._make(limits)


    def draw(self):
        """ Draw all lines to canvas.
        """
        # Draw energy profile lines.
        for line in self.lines:
            self.axes.add_line(line.line2d())

        # Render energy profile lines.
        self._render_ep_lines()

        # Draw shadows.
        for shadow_line in self.shadow_lines:
            self.axes.add_line(shadow_line)

        # Set axes limits.
        limits = self._get_data_limits()
        self.axes.set_xlim(limits.min_x, limits.max_x)
        self.axes.set_ylim(limits.min_y, limits.max_y)

