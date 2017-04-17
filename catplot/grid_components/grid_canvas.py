#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Module for grid plotting canvas.
"""

import numpy as np
import matplotlib.pyplot as plt

from catplot.canvas import Canvas
from catplot.grid_components.nodes import Node2D
from catplot.grid_components.edges import Edge2D


class Grid2DCanvas(Canvas):
    """ Canvas for 2D grid plotting.
    """
    def __init__(self, **kwargs):
        super(Grid2DCanvas, self).__init__(**kwargs)

        # Equalize the scale of x and y axis.
        self.axes.set_aspect("equal")

        # Attributes for 2D grid canvas.
        self.nodes = []
        self.edges = []
        self.supercells = []

    def add_supercell(self, supercell):
        """ Add a supercell to 2D grid canvas.
        """
        self.supercells.append(supercell)
        self.nodes.extend(supercell.nodes)
        self.edges.extend(supercell.edges)

    def add_supercells(self, supercells):
        """ Add multiple supercells to 2D grid canvas.
        """
        for sc in supercells:
            self.add_supercell(sc)

    def add_node(self, node):
        """ Add a node to grid canvas.
        """
        # Check node.
        if not isinstance(node, Node2D):
            raise ValueError("node must be a Node2D object")

        self.nodes.append(node)

    def add_nodes(self, nodes):
        """ Add multiple nodes to canvas.
        """
        for node in nodes:
            self.add_node(node)

    def add_edge(self, edge):
        """ Add a edge to grid canvas.
        """
        if not isinstance(edge, Edge2D):
            raise ValueError("edge must be an Edge2D object")

        self.edges.append(edge)

    def add_edges(self, edges):
        """ Add multiple edges to canvas.
        """
        for edge in self.edges:
            self.add_edge(edges)

    @property
    def node_coordinates(self):
        """ Coordinates for all nodes.
        """
        return np.array([node.coordinate.tolist() for node in self.nodes])

    @property
    def node_edgecolors(self):
        """ Color codes for node edges.
        """
        return [node.edgecolor for node in self.nodes]

    @property
    def node_colors(self):
        """ Colors for all nodes.
        """
        return [node.color for node in self.nodes]

    @property
    def edge_coordinates(self):
        """ Coordiantes for all edges.
        """
        x = np.concatenate([edges.x for edges in self.edges])
        y = np.concatenate([edges.y for edges in self.edges])

        return np.array(list(zip(x, y)))


    def _get_data_limits(self):
        """ Private helper function to get the limits of data.
        """
        node_x = self.node_coordinates[:, 0]
        edge_x = self.edge_coordinates[:, 0]
        x = np.append(node_x, edge_x)
        max_x, min_x = np.max(x), np.min(x)

        node_y = self.node_coordinates[:, 1]
        edge_y = self.edge_coordinates[:, 1]
        y = np.append(node_y, edge_y)
        max_y, min_y = np.max(y), np.min(y)

        return self._limits(max_x, min_x, max_y, min_y)

    def draw(self):
        """ Draw all nodes and edges on canvas.
        """
        if not any([self.nodes, self.edges]):
            self._logger.warning("Attempted to draw in an empty canvas")
            return

        # Add edges to canvas.
        for edge in self.edges:
            self.axes.add_line(edge.line2d())

        # Add nodes to canvas one by one.
        for node in self.nodes:
            self.axes.scatter(*node.coordinate,
                              color=node.color,
                              edgecolors=node.edgecolor,
                              marker=node.style,
                              alpha=node.alpha,
                              s=node.size,
                              zorder=99)

        # Set axes limits.
        limits = self._get_data_limits()
        self.axes.set_xlim(limits.min_x, limits.max_x)
        self.axes.set_ylim(limits.min_y, limits.max_y)

    def redraw(self):
        """ Clear the canvas and draw all components again.
        """
        self.clear()
        self.draw()

    def clear(self):
        """ Clear components drawned in canvas.
        """
        self.axes.clear()

    def deep_clear(self):
        """ Clear all components in canvas.
        """
        self.clear()
        self.nodes = []
        self.edges = []
        self.supercells = []

