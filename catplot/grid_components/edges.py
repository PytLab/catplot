#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Module for edge between nodes.
"""

from copy import deepcopy

import numpy as np
from matplotlib.lines import Line2D

from catplot.grid_components.nodes import Node2D, Node3D


class GridEdge(object):
    """ Abstract base class for other edge.
    """
    def __init__(self, node1, node2, **kwargs):
        self.start, self.end = node1.coordinate.copy(), node2.coordinate.copy()

        self.n = kwargs.pop("n", 0)
        self.color = kwargs.pop("color", "#000000")
        self.width = kwargs.pop("width", 1)
        self.style = kwargs.pop("style", "solid")
        self.alpha = kwargs.pop("alpha", 1)
        self.zorder = kwargs.pop("zorder", 0)

class Edge2D(GridEdge):
    """ Edge in 2D grid between 2D nodes.

    Parameters:
    -----------
    node1, node2: Node2D object, nodes at both ends of the edges.

    n: int, optional,
        extra point number in edge line between nodes, default is 0
        (only include two points of the endpoints).

    alpha: float (0.0 transparent through 1.0 opaque).

    color: str, optional, color for the edge, default is "#000000" (black).

    width: int, optional, edge width, default is 1.

    zorder: int, optional, default is 0
        The zorder for the artist. Artists with lower zorder values are drawn first.
    """
    def __init__(self, node1, node2, **kwargs):
        for node in [node1, node2]:
            if not isinstance(node, Node2D):
                raise ValueError("node must be a Node2D object")

        super(Edge2D, self).__init__(node1, node2, **kwargs)

        # Set same color with start node if no color in kwargs
        if "color" not in kwargs:
            self.color = node1.color

    @property
    def x(self):
        """ x values for edge data.
        """
        return np.linspace(self.start[0],
                           self.end[0],
                           num=self.n+2)

    @property
    def y(self):
        """ y values for edge data.
        """
        return np.linspace(self.start[1], self.end[1], self.n+2)


    def line2d(self):
        """ Get the corresponding Line2D object for the edge.
        """
        return Line2D(self.x, self.y,
                      linewidth=self.width,
                      color=self.color,
                      linestyle=self.style,
                      alpha=self.alpha,
                      zorder=self.zorder)

    def move(self, move_vector):
        """ Move the edge to a new position.
        """
        if not isinstance(move_vector, np.ndarray):
            move_vector = np.array(move_vector)

        # Just move the endpoints.
        self.start += move_vector
        self.end += move_vector

        return self

    def clone(self, relative_position=None):
        """ Clone a new 2D edge to a specific position.

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

        # Clone a new edge.
        edge = deepcopy(self)

        # Move the edge to a new position.
        edge.move(relative_position)

        return edge


class Arrow2D(Edge2D):
    """ Arrow edge in 2D grid between 2D nodes.

    Parameters:
    -----------
    node1, node2: Node2D object, nodes at both ends of the edges.

    color: str, optional, color for the edge, default is "#000000" (black).

    head_width: float, total width of the full arrow head, default is 0.03.

    head_length: float, length of arrow head, default is 0.06.

    shape: str, optional, ['full', 'left', 'right'], default is 'full'.

    zorder: int, optional, default is 0
        The zorder for the artist. Artists with lower zorder values are drawn first.
    """
    def __init__(self, node1, node2, **kwargs):
        super(Arrow2D, self).__init__(node1, node2, **kwargs)

        self.head_width = kwargs.pop("head_width", 0.03)
        self.head_length = kwargs.pop("head_width", 0.06)
        self.shape = kwargs.pop("shape", "full")
        self.edgecolor = kwargs.pop("edgecolor", self.color)

    @property
    def dx(self):
        return (self.end - self.start)[0]

    @property
    def dy(self):
        return (self.end - self.start)[1]


class Edge3D(Edge2D):
    """ Edge in 3D grid between 3D nodes.

    Parameters:
    -----------
    node1, node2: Node3D object, nodes at both ends of the edges.

    zdir: which direction to use as z (‘x’, ‘y’ or ‘z’) when plotting a 2D set.

    n: int, optional,
        extra point number in edge line between nodes, default is 0
        (only include two points of the endpoints).

    alpha: float (0.0 transparent through 1.0 opaque).

    color: str, optional, color for the edge, default is "#000000" (black).

    width: int, optional, edge width, default is 1.

    zorder: int, optional, default is 0
        The zorder for the artist. Artists with lower zorder values are drawn first.
    """
    def __init__(self, node1, node2, **kwargs):
        for node in [node1, node2]:
            if not isinstance(node, Node3D):
                raise ValueError("node must be a Node3D object")

        super(Edge2D, self).__init__(node1, node2, **kwargs)

        # Set the same color with the start node if no color in kwargs.
        if "color" not in kwargs:
            self.color = node1.color

        # Extra attributes for Line3D.
        self.zdir = kwargs.pop("zdir", "z")

    @property
    def z(self):
        """ z values for edge data.
        """
        return np.linspace(self.start[2], self.end[2], self.n+2)

    def clone(self, relative_position=None):
        """ Clone a new 3D edge to a specific position.

        Parameters:
        -----------
        relative_position: list of two float, optional.
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

        # Clone a new edge.
        edge = deepcopy(self)

        # Move the edge to a new position.
        edge.move(relative_position)

        return edge

