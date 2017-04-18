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
        node = deepcopy(self)

        # Move the node to predefined postion.
        node.move(relative_position)

        return node


class Node3D(Node2D):
    """ Node in 3D grid.

    Parameters:
    -----------
    coordinate: list of three float
        The location of node in 3D grid canvas.

    zdir: str, optional,
        which direction to use as z ('x', 'y' or 'z') when plotting a 2D set.

    depthshade: bool, optional,
        whether to shade the scatter markers to give the appearance of depth.
        Default is True.

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

    coordinate = dc.Coordinate3D("coordinate")

    def __init__(self, coordinate, **kwargs):
        self.zdir = kwargs.pop("zdir", "z")
        self.depthshade = kwargs.pop("depthshade", True)

        super(Node3D, self).__init__(coordinate, **kwargs)

    def clone(self, relative_position):
        """ Clone a new 3D node to a specific position.

        Parameters:
        -----------
        relative_position: list of three float, optional.
            the position of new cloned node relative to the original node,
            default is [0.0, 0.0, 0.0].
        """
        if relative_position is not None:
            # Check the validity.
            if (len(relative_position) != 3 or
                    not all([isinstance(i, float) for i in relative_position])):
                msg = "relative position must be a sequence with three float number"
                raise ValueError(msg)
        else:
            relative_position = [0.0, 0.0, 0.0]

        # Create a new node.
        node = deepcopy(self)

        # Move the node to predefined postion.
        node.move(relative_position)

        return node

