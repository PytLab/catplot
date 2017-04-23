#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from collections import namedtuple

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.spines import Spine

import catplot.descriptors as dc
from catplot.grid_components.edges import GridEdge, Arrow2D
from catplot.grid_components.nodes import GridNode


class Canvas(object):
    """ Canvas abstract base class.

    Parameters:
    -----------
    margin_ratio: float, optional, default is 0.1
        control the white space between energy profile line and axes.

    figsize : tuple of integers, optional, default: None
        width, height in inches. If not provided, defaults to rc figure.figsize.

    dpi : integer, optional, default: None
        resolution of the figure. If not provided, defaults to rc figure.dpi.

    facecolor : str, optional
        the background color. If not provided, defaults to rc figure.facecolor

    edgecolor : str, optional
        the border color. If not provided, defaults to rc figure.edgecolor

    x_ticks : float list
        set the x ticks with a list of ticks.

    y_ticks : float list
        set the y ticks with a list of ticks.

    """
    margin_ratio = dc.MarginRatio("margin_ratio")

    def __init__(self, **kwargs):
        self.margin_ratio = kwargs.pop("margin_ratio", 0.1)
        self.figsize = kwargs.pop("figsize", None)
        self.dpi = kwargs.pop("dpi", None)
        self.facecolor = kwargs.pop("facecolor", None)
        self.edgecolor = kwargs.pop("edgecolor", None)
        self.x_ticks = kwargs.pop("x_ticks", None)
        self.y_ticks = kwargs.pop("y_ticks", None)

        # Create a figure.
        self.figure = plt.figure(figsize=self.figsize,
                                 dpi=self.dpi)

        # Add an axes to figure.
        # NOTE: here we use the canvas facecolor as the axes facecolor.
        self.axes = self.figure.add_subplot(111, facecolor=self.facecolor)

        # Change the spine color of axes.
        if self.edgecolor:
            for child in self.axes.get_children():
                if isinstance(child, Spine):
                    child.set_color(self.edgecolor)

        # Set axe ticks.
        if self.x_ticks is not None:
            self.axes.set_xticks(self.x_ticks)
        if self.y_ticks is not None:
            self.axes.set_yticks(self.y_ticks)

        # Set logger.
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(logging.INFO)

        # Set console handler.
        formatter = logging.Formatter("%(name)s   %(levelname)-8s %(message)s")
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        handler.setFormatter(formatter)

        # Add handler to logger.
        self._logger.addHandler(handler)

    def _limits(self, max_x, min_x, max_y, min_y):
        """ Private helper function to get data limits.

        Parameters:
        -----------
        max_x: float, the maximum of x values.
        min_x: float, the minimum of x values.
        max_y: float, the maximum of y values.
        min_y: float, the minimum of y values.
        """
        scale_x = max_x - min_x
        scale_y = max_y - min_y

        # Define a namedtuple to be returned.
        Limits = namedtuple("Limits", ["max_x", "min_x", "max_y", "min_y"])
        limits = [max_x + self.margin_ratio*scale_x,
                  min_x - self.margin_ratio*scale_x,
                  max_y + self.margin_ratio*scale_y,
                  min_y - self.margin_ratio*scale_y]

        return Limits._make(limits)

    @property
    def current_zorder(self):
        """ The max zorder in current canvas.
        """
        components = self.nodes + self.edges + self.arrows
        current_zorder = np.max([comp.zorder for comp in components])
        return current_zorder

    def _remove_component(self, component):
        """ Private helper function to remove a single components in canvas.
        """
        # Check the component type and remove.
        if isinstance(component, Arrow2D):
            self.arrows.remove(component)
        elif isinstance(component, GridEdge):
            self.edges.remove(component)
        elif isinstance(component, GridNode):
            self.nodes.remove(component)
        else:
            raise ValueError("component {} is not in canvas".format(component))

    def remove(self, *components):
        """ Remove components in canvas.
        """
        for comp in components:
            self._remove_component(comp)

