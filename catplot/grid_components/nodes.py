#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Module for node definition in grid.
"""

import numpy as np

import catplot.descriptors as dc


class GridNode(object):
    """ Abstract base class for other node.

    Parameters:
    -----------
    coordinate: array_like, shape (n, )
        The location of node in grid canvas.

    color: str, optional, default is "#000000"
        Facecolor of node.

    size: scalar, optional
        size in points^2, default is 400.

    style: MarkerStyle, optional, default is 'o'.

    alpha: scalar, optional, default is 1
        The alpha blending value, between 0 (transparent) and 1 (opaque)

    line_width: scalar or array_like, optional, default is 0.

    edgecolor: str, optional, default is the color of face.

    """

    __slots__ = {"coordinate", "color", "size", "style", "alpha",
                 "line_width", "edgecolor"}

    def __init__(self, coordinate, **kwargs):
        self.coordinate = np.array(coordinate)

        # Keyword arguments.
        self.color = kwargs.pop("color", "#000000")
        self.size = kwargs.pop("size", 400)
        self.style = kwargs.pop("style", "o")
        self.alpha = kwargs.pop("alpha", 1.0)
        self.line_width = kwargs.pop("line_width", 0)
        self.edgecolor = kwargs.pop("edgecolor", self.color)


class Node2D(GridNode):
    """ Node in 2D grid.

    Parameters:
    -----------
    coordinate: list of two float
        The location of node in grid canvas.

    color: str, optional, default is "#000000"
        Facecolor of node.

    size: scalar, optional
        size in points^2, default is 400.

    style: MarkerStyle, optional, default is 'o'.

    alpha: scalar, optional, default is 1
        The alpha blending value, between 0 (transparent) and 1 (opaque)

    line_width: scalar or array_like, optional, default is 0.

    edgecolor: str, optional, default is the color of face.
    """

    coordinate = dc.Coordinate2D("coordinate")

    def __init__(self, coordinate, **kwargs):
        super(Node2D, self).__init__(coordinate, **kwargs)

