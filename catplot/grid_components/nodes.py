#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Module for node definition in grid.
"""

from copy import deepcopy

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

    zorder: float, set the zorder for the artist, default is 0.

    """

    # NOTE: The grid may contains a huge number of nodes,
    # so we define __slots__ for saving memery.
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
        self.zorder = kwargs.pop("zorder", 0)


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

    def move(self, move_vector):
        """ Move the node on grid along the move vector.

        Parameters:
        -----------
        move_vector: list of float, the vector along which the node moves.
        """
        if not isinstance(move_vector, np.ndarray):
            move_vector = np.array(move_vector)
        # Move it.
        self.coordinate += move_vector

        # For chain operations.
        return self

    def clone(self, relative_position=None):
        """ Clone a new 2D node to a specific position.

        Parameters:
        -----------
        relative_position: list of two float, optional.
            the position of new cloned node relative to the original node,
            default is [0.0, 0.0].
        """
        if relative_position is not None:
            # Check the validity.
            if (len(relative_position) != 2 or
                    not all([isinstance(i, float) for i in relative_position])):
                msg = "relative position must be a sequence with two float number"
                raise ValueError(msg)
        else:
            relative_position = [0.0, 0.0]

        # Create a new node.
#        node = Node2D(self.coordinate,
#                      color=self.color,
#                      size=self.size,
#                      style=self.style,
#                      alpha=self.alpha,
#                      line_width=self.line_width,
#                      edgecolor=self.edgecolor)
        node = deepcopy(self)

        # Move the node to predefined postion.
        node.move(relative_position)

        return node

