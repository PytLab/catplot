#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Module for grid plotting canvas.
"""

from collections import namedtuple

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from catplot.canvas import Canvas
from catplot.grid_components.nodes import Node2D, Node3D
from catplot.grid_components.edges import Edge2D, Arrow2D, Edge3D
from catplot.grid_components.supercell import SuperCell2D, SuperCell3D


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
        self.arrows = []
        self.supercells = []

    def add_supercell(self, supercell):
        """ Add a supercell to 2D grid canvas.
        """
        if not isinstance(supercell, SuperCell2D):
            raise ValueError("supercell must be a SuperCell2D object")

        self.supercells.append(supercell)
        self.nodes.extend(supercell.nodes)
        self.edges.extend(supercell.edges)
        self.arrows.extend(supercell.arrows)

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

        if isinstance(edge, Arrow2D):
            self.arrows.append(edge)
        else:
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
        if not self.edges:
            return []
        else:
            x = np.concatenate([edge.x for edge in self.edges])
            y = np.concatenate([edge.y for edge in self.edges])
            return np.array(list(zip(x, y)))

    @property
    def arrow_colors(self):
        """ Colors for all arrows.
        """
        return [arrow.color for arrow in self.arrows]

    @property
    def arrow_coordinates(self):
        """ Coordinates for all arrows.
        """
        if not self.arrows:
            return []
        else:
            x = np.concatenate([arrow.x for arrow in self.arrows])
            y = np.concatenate([arrow.y for arrow in self.arrows])
            return np.array(list(zip(x, y)))

    def _get_data_limits(self):
        """ Private helper function to get the limits of data.
        """
        node_x = self.node_coordinates[:, 0] if self.nodes else []
        edge_x = self.edge_coordinates[:, 0] if self.edges else []
        arrow_x = self.arrow_coordinates[:, 0] if self.arrows else []
        x = np.concatenate([node_x, edge_x, arrow_x])
        max_x, min_x = np.max(x), np.min(x)

        node_y = self.node_coordinates[:, 1] if self.nodes else []
        edge_y = self.edge_coordinates[:, 1] if self.edges else []
        arrow_y = self.arrow_coordinates[:, 1] if self.arrows else []
        y = np.concatenate([node_y, edge_y, arrow_y])
        max_y, min_y = np.max(y), np.min(y)

        return self._limits(max_x, min_x, max_y, min_y)

    def draw(self):
        """ Draw all nodes, edges and arrows on canvas.
        """
        if not any([self.nodes, self.edges, self.arrows]):
            self._logger.warning("Attempted to draw in an empty canvas")
            return

        # Add edges to canvas.
        for edge in self.edges:
            self.axes.add_line(edge.line2d())

        for arrow in self.arrows:
            self.axes.arrow(*arrow.start, dx=arrow.dx, dy=arrow.dy,
                            length_includes_head=True,
                            head_width=arrow.head_width,
                            head_length=arrow.head_length,
                            shape=arrow.shape,
                            alpha=arrow.alpha,
                            linewidth=arrow.width,
                            color=arrow.color,
                            linestyle=arrow.style,
                            zorder=arrow.zorder)

        # Add nodes to canvas one by one.
        for node in self.nodes:
            self.axes.scatter(*node.coordinate,
                              color=node.color,
                              edgecolors=node.edgecolor,
                              marker=node.style,
                              alpha=node.alpha,
                              s=node.size,
                              linewidth=node.line_width,
                              linestyle=node.line_style,
                              zorder=node.zorder)

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
        self.arrows = []
        self.supercells = []


class Grid3DCanvas(Grid2DCanvas):
    """ Canvas for 3D grid plotting.
    """
    def __init__(self, **kwargs):
        # NOTE: here we call the method in Canvas NOT Grid2DCanvas.
        super(Grid2DCanvas, self).__init__(**kwargs)

        # Create a figure.
        self.figure = plt.figure(figsize=self.figsize,
                                 dpi=self.dpi)

        # Add an axes to figure.
        self.axes = self.figure.add_subplot(111, projection="3d",
                                            facecolor=self.facecolor)

        self.axes.set_aspect("equal")

        # Attributes for 3D canvas.
        self.nodes = []
        self.edges = []
        self.supercells = []
        self.arrows = []  # Just a placeholder here.

    def _limits(self, max_x, min_x, max_y, min_y, max_z, min_z):
        """ Override parent's function to get 3D data limits.

        Parameters:
        -----------
        max_x: float, the maximum of x values.
        min_x: float, the minimum of x values.
        max_y: float, the maximum of y values.
        min_y: float, the minimum of y values.
        max_z: float, the maximum of z values.
        min_z: float, the minimum of z values.
        """
        scale_x = max_x - min_x
        scale_y = max_y - min_y
        scale_z = max_z - min_z

        # Define a namedtuple to be returned.
        Limits = namedtuple("Limits", ["max_x", "min_x", "max_y", "min_y", "max_z", "min_z"])
        limits = [max_x + self.margin_ratio*scale_x,
                  min_x - self.margin_ratio*scale_x,
                  max_y + self.margin_ratio*scale_y,
                  min_y - self.margin_ratio*scale_y,
                  max_z + self.margin_ratio*scale_z,
                  min_z - self.margin_ratio*scale_z]

        return Limits._make(limits)

    def _get_data_limits(self):
        """ Get limits for all data in canvas.
        """
        node_x = self.node_coordinates[:, 0] if self.nodes else []
        edge_x = self.edge_coordinates[:, 0] if self.edges else []
        x = np.concatenate([node_x, edge_x])
        max_x, min_x = np.max(x), np.min(x)

        node_y = self.node_coordinates[:, 1] if self.nodes else []
        edge_y = self.edge_coordinates[:, 1] if self.edges else []
        y = np.concatenate([node_y, edge_y])
        max_y, min_y = np.max(y), np.min(y)

        node_z = self.node_coordinates[:, 2] if self.nodes else []
        edge_z = self.edge_coordinates[:, 2] if self.edges else []
        z = np.concatenate([node_z, edge_z])
        max_z, min_z = np.max(z), np.min(z)

        return self._limits(max_x, min_x, max_y, min_y, max_z, min_z)

    def add_node(self, node):
        """ Add a 3D node to 3D grid canvas.
        """
        if not isinstance(node, Node3D):
            raise ValueError("node must be a Node3D object")

        self.nodes.append(node)

    def add_edge(self, edge):
        """ Add a 3D edge to canvas.
        """
        if not isinstance(edge, Edge3D):
            raise ValueError("edge must be an Edge3D object")

        self.edges.append(edge)

    def add_supercell(self, supercell):
        """ Add a supercell to 3D grid canvas.
        """
        if not isinstance(supercell, SuperCell3D):
            raise ValueError("supercell must be a SuperCell3D object")

        self.supercells.append(supercell)
        self.nodes.extend(supercell.nodes)
        self.edges.extend(supercell.edges)

    @property
    def edge_coordinates(self):
        """ Coordinates for all edges in 3D grid canvas.
        """
        if not self.edges:
            return []
        else:
            x = np.concatenate([edge.x for edge in self.edges])
            y = np.concatenate([edge.y for edge in self.edges])
            z = np.concatenate([edge.z for edge in self.edges])
            return np.array(list(zip(x, y, z)))

    def draw(self):
        """ Draw all nodes and edges on 3D canvas.
        """
        if not any([self.nodes, self.edges]):
            self._logger.warning("Attempted to draw in an empty canvas")
            return

        # Add nodes to canvas one by one.
        for node in self.nodes:
            self.axes.scatter(*node.coordinate,
                              zdir=node.zdir,
                              s=node.size,
                              c=node.color,
                              depthshade=node.depthshade,
                              edgecolor=node.edgecolor,
                              marker=node.style,
                              alpha=node.alpha,
                              linewidth=node.line_width,
                              zorder=node.zorder)

        # Add edges to canvas.
        for edge in self.edges:
            self.axes.plot(edge.x, edge.y, edge.z,
                           zdir=edge.zdir,
                           linewidth=edge.width,
                           color=edge.color,
                           linestyle=edge.style,
                           alpha=edge.alpha,
                           zorder=edge.zorder)

        # Set axes limits.
        limits = self._get_data_limits()
        self.axes.set_xlim(limits.min_x, limits.max_x)
        self.axes.set_ylim(limits.min_y, limits.max_y)
        self.axes.set_zlim(limits.min_z, limits.max_z)

    def clear(self):
        """ Clear 3D axes.
        """
        self.axes.clear()

    def deep_clear(self):
        """ Clear all components in canvas.
        """
        self.clear()
        self.nodes = []
        self.edges = []
        self.arrows = []
        self.supercells = []

    def redraw(self):
        """ Clear the canvas and draw all components agian.
        """
        self.clear()
        self.draw()

