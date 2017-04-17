#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Module for super cell.
"""

import numpy as np

import catplot.descriptors as dc


class SuperCell(object):
    """ Supercell for a lattice grid.
    """

    cell_vectors = dc.Basis2D("cell_vectors")

    def __init__(self, nodes, edges, cell_vectors=None):
        self.nodes = nodes
        self.edges = edges

        if cell_vectors is None:
            self.cell_vectors = np.array([[1.0, 0.0],
                                          [0.0, 1.0]])
        else:
            self.cell_vectors = np.array(cell_vectors)

        # Change all coordinates in nodes and edges to Cartisan coordinates.
        for node in self.nodes:
            node.coordinate = np.dot(self.cell_vectors, node.coordinate)

        for edge in self.edges:
            edge.start = np.dot(self.cell_vectors, edge.start)
            edge.end = np.dot(self.cell_vectors, edge.end)

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

        return SuperCell(new_nodes, new_edges)

