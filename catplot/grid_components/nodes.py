#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Module for node definition in grid.
"""

from copy import deepcopy

import numpy as np

from catplot.grid_components import extract_plane
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
    #__slots__ = {"coordinate", "color", "size", "style", "alpha",
    #             "line_width", "line_style", "edgecolor", "zorder"}

    def __init__(self, coordinate, **kwargs):
        self.coordinate = np.array(coordinate)

        # Keyword arguments.
        self.color = kwargs.pop("color", "#000000")
        self.size = kwargs.pop("size", 400)
        self.style = kwargs.pop("style", "o")
        self.alpha = kwargs.pop("alpha", 1.0)
        self.line_width = kwargs.pop("line_width", 0)
        self.line_style = kwargs.pop("line_style", "solid")
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

    def clone(self, relative_position=None, **kwargs):
        """ Clone a new 2D node to a specific position.

        Parameters:
        -----------
        relative_position: list of two float, optional.
            the position of new cloned node relative to the original node,
            default is [0.0, 0.0].

        The kwargs are Node2D properties
        """
        if relative_position is not None:
            # Check the validity.
            if (len(relative_position) != 2 or
                    not all([isinstance(i, (int, float)) for i in relative_position])):
                msg = "relative position must be a sequence with two float number"
                raise ValueError(msg)
        else:
            relative_position = [0.0, 0.0]

        # Create a new node.
        node = deepcopy(self)

        # Move the node to predefined postion.
        node.move(relative_position)

        # Update node attributes.
        for k, v in kwargs.items():
            setattr(node, k, v)

        return node

    @extract_plane
    def to3d(self, **kwargs):
        """ Map the 2D node to 3D space.

        Parameters:
        -----------
        plane: str, the plane to which the node is mapped to.
            The value could be 'xy', 'xz' or 'yz', default is 'xy'.

        zdir: str, optional,
            which direction to use as z ('x', 'y' or 'z') when plotting a 2D set.

        depthshade: bool, optional,
            whether to shade the scatter markers to give the appearance of depth.
            Default is True.
        """
        # Map the coordinate.
        plane = kwargs.pop("plane")

        if plane == "xy":
            coordinate3d = np.insert(self.coordinate, 2, 0.0)
        elif plane == "xz":
            coordinate3d = np.insert(self.coordinate, 1, 0.0)
        elif plane == "yz":
            coordinate3d = np.insert(self.coordinate, 0, 0.0)
        else:
            raise ValueError("Invalid plane name '{}'".format(plane))

        node3d = Node3D(coordinate3d, color=self.color, size=self.size,
                        style=self.style, alpha=self.alpha,
                        line_width=self.line_width, line_style=self.line_style,
                        edgecolor=self.edgecolor, zorder=self.zorder, **kwargs)

        return node3d


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

    @staticmethod
    @extract_plane
    def from2d(node2d, **kwargs):
        """ Construct a 3D node from a 2D node.
        """
        if not isinstance(node2d, Node2D):
            raise ValueError("node2d must be an object of Node2D")

        return node2d.to3d(**kwargs)

    def clone(self, relative_position, **kwargs):
        """ Clone a new 3D node to a specific position.

        Parameters:
        -----------
        relative_position: list of three float, optional.
            the position of new cloned node relative to the original node,
            default is [0.0, 0.0, 0.0].

        The kwargs are Node3D properties.
        """
        if relative_position is not None:
            # Check the validity.
            if (len(relative_position) != 3 or
                    not all([isinstance(i, (int, float)) for i in relative_position])):
                msg = "relative position must be a sequence with three float number"
                raise ValueError(msg)
        else:
            relative_position = [0.0, 0.0, 0.0]

        # Create a new node.
        node = deepcopy(self)

        # Move the node to predefined postion.
        node.move(relative_position)

        # Update node attribtues.
        for k, v in kwargs.items():
            setattr(node, k, v)

        return node

