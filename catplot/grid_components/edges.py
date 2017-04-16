#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Module for edge between nodes.
"""

import numpy as np
from scipy.interpolate import interp1d
from matplotlib.lines import Line2D

from catplot.grid_components.nodes import Node2D


class GridEdge(object):
    """ Abstract base class for other edge.
    """
    def __init__(self, node1, node2, **kwargs):
        self.node1, self.node2 = node1, node2

        self.n = kwargs.pop("n", 0)
        self.color = kwargs.pop("color", "#000000")
        self.line_width = kwargs.pop("line_width", 1)

class Edge2D(GridEdge):
    """ Edge in 2D grid between 2D nodes.

    Parameters:
    -----------
    node1, node2: Node2D object, nodes at both ends of the edges.

    n: int, optional,
        extra point number in edge line between nodes, default is 0
        (only include two points of the endpoints).

    color: str, optional, color for the edge, default is "#000000" (black).

    line_width: int, optional, edge width, default is 1.
    """
    def __init__(self, node1, node2, **kwargs):
        for node in [node1, node2]:
            if not isinstance(node, Node2D):
                raise ValueError("node must be a Node2D object")

        super(Edge2D, self).__init__(node1, node2, **kwargs)

    @property
    def x(self):
        """ x values for edge data.
        """
        return np.linspace(self.node1.coordinate[0],
                           self.node2.coordinate[0],
                           num=self.n+2)

    @property
    def y(self):
        """ y values for edge data.
        """
        # Interpolate linearly n values between two nodes.
        x = [self.node1.coordinate[0], self.node2.coordinate[0]]
        y = [self.node1.coordinate[1], self.node2.coordinate[1]]
        interp_func = interp1d(x, y, kind="linear")

        return np.array([interp_func(x) for x in self.x])

    def line2d(self):
        """ Get the corresponding Line2D object for the edge.
        """
        return Line2D(self.x, self.y, linewidth=self.line_width, color=self.color)

