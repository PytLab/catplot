#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Module for super cell.
"""

import numpy as np

import catplot.descriptors as dc


class SuperCell(object):
    """ Abstract base class for supercell.
    """
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges

        # Change all coordinates in nodes and edges to Cartisan coordinates.
        for node in self.nodes:
            node.coordinate = np.dot(self.cell_vectors, node.coordinate)

        for edge in self.edges:
            edge.start = np.dot(self.cell_vectors, edge.start)
            edge.end = np.dot(self.cell_vectors, edge.end)

    def __add__(self, other):
        """ Redefine add operator to change the default behaviour.
        """
        if not np.array_equal(self.cell_vectors, other.cell_vectors):
            raise ValueError("Can't add two supercell with different cell vectors")
        nodes = self.nodes + other.nodes
        edges = self.edges + other.edges

        return self.__class__(nodes, edges, self.cell_vectors)


class SuperCell2D(SuperCell):
    """ Supercell for a lattice grid.
    """

    cell_vectors = dc.Basis2D("cell_vectors")

    def __init__(self, nodes, edges, cell_vectors=None):
        if cell_vectors is None:
            self.cell_vectors = np.array([[1.0, 0.0],
                                          [0.0, 1.0]])
        else:
            self.cell_vectors = np.array(cell_vectors)

        super(SuperCell2D, self).__init__(nodes, edges)

    def move(self, move_vector):
        """ Move the super cell along the move vector.
        """
        # Move nodes.
        for node in self.nodes:
            node.move(move_vector)

        # Move edges.
        for edge in self.edges:
            edge.move(move_vector)

        return self

    def clone(self, relative_position):
        """ Clone a new 2D supercell to a specific position.

        Parameters:
        -----------
        relative_position: list of two float, optional.
            the position of new cloned node relative to the original node,
            default is [0.0, 0.0].
        """
        new_nodes = [node.clone(relative_position) for node in self.nodes]
        new_edges = [edge.clone(relative_position) for edge in self.edges]

        return SuperCell2D(new_nodes, new_edges)

