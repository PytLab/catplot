#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Module for super cell.
"""

from copy import deepcopy

import numpy as np

import catplot.descriptors as dc


class SuperCell(object):
    """ Abstract base class for supercell.
    """
    def __init__(self, nodes, edges, arrows=None):
        self.nodes = nodes
        self.edges = edges
        self.arrows = [] if arrows is None else arrows

        # Change all coordinates in nodes and edges to Cartisan coordinates.
        for node in self.nodes:
            node.coordinate = np.dot(self.cell_vectors.T, node.coordinate)

        for edge in self.edges:
            edge.start = np.dot(self.cell_vectors.T, edge.start)
            edge.end = np.dot(self.cell_vectors.T, edge.end)

        for arrow in self.arrows:
            arrow.start = np.dot(self.cell_vectors.T, arrow.start)
            arrow.end = np.dot(self.cell_vectors.T, arrow.end)

    def __add__(self, other):
        """ Redefine add operator to change the default behaviour.
        """
        if not np.array_equal(self.cell_vectors, other.cell_vectors):
            raise ValueError("Can't add two supercell with different cell vectors")
        nodes = self.nodes + other.nodes
        edges = self.edges + other.edges
        arrows = self.arrows + other.arrows

        # NOTE: here the cell_vectors will not be passed in,
        #       or the coordinate mapping will be done repeatly.
        new_supercell = self.__class__(nodes, edges, arrows)
        new_supercell.cell_vectors = self.cell_vectors

        return new_supercell


class SuperCell2D(SuperCell):
    """ 2D supercell for a lattice grid.

    Parameters:
    -----------
    nodes: Node2D object list, all nodes in supercell.

    edges: Edge2D object list, all edges in supercell.

    arrows: Arrow2D object list, all arrows in supercell, default is [].

    cell_vectors: 2D-like array,
        the basis vectors for the supercell, default is [[1.0, 0.0], [0.0, 1.0]].
    """

    cell_vectors = dc.Basis2D("cell_vectors")

    def __init__(self, nodes, edges, arrows=None, cell_vectors=None):
        if cell_vectors is None:
            self.cell_vectors = np.array([[1.0, 0.0],
                                          [0.0, 1.0]])
        else:
            self.cell_vectors = np.array(cell_vectors)

        super(self.__class__, self).__init__(nodes, edges, arrows)

    def move(self, move_vector):
        """ Move the super cell along the move vector.
        """
        # Move nodes.
        for node in self.nodes:
            node.move(move_vector)

        # Move edges.
        for edge in self.edges:
            edge.move(move_vector)

        # Move arrows.
        for arrow in self.arrows:
            arrow.move(move_vector)

        return self

    def clone(self, relative_position):
        """ Clone a new 2D supercell to a specific position.

        Parameters:
        -----------
        relative_position: list of two float, optional.
            the position of new cloned node relative to the original node,
            default is [0.0, 0.0].
        """
#        new_nodes = [node.clone(relative_position) for node in self.nodes]
#        new_edges = [edge.clone(relative_position) for edge in self.edges]
#        new_arrows = [arrow.clone(relative_position) for arrow in self.arrows]
#
#        new_supercell = self.__class__(new_nodes,
#                                       new_edges,
#                                       new_arrows)
        new_supercell = deepcopy(self)
        new_supercell.move(relative_position)

        return new_supercell

    def expand(self, nx, ny, cell_vectors=None):
        """ Expand the supercell to a lager supercell.

        Parameters:
        -----------
        nx : int, the expansion number along x axis.
        ny : int, the expansion number along y axis.
        cell_vectors: 2x3 array, cell vectors for supercell expansion
            default value is the same as cell vectors of this supercell.
        """

        if cell_vectors is None:
            cell_vectors = self.cell_vectors
        cell_vectors = np.array(cell_vectors)

        # Expand along x axis.
        x_expanded_supercell = self
        for i in range(1, nx):
            move_vector = cell_vectors[0, :]*i
            x_expanded_supercell += self.clone(move_vector)

        # Expand along y axis.
        expanded_supercell = x_expanded_supercell
        for j in range(1, ny):
            move_vector = cell_vectors[1, :]*j
            expanded_supercell += x_expanded_supercell.clone(move_vector)

        return expanded_supercell

    def to3d(self, cell_vectors=None):
        """ Map a 2D supercell to 3D space.
        """
        # Map nodes and edges.
        nodes = [n.to3d() for n in self.nodes]
        edges = [e.to3d() for e in self.edges]

        return SuperCell3D(nodes, edges, cell_vectors=cell_vectors)


class SuperCell3D(SuperCell2D):
    """ 3D supercell in a 3D lattice grid.

    Parameters:
    -----------
    nodes: Node3D object list, all nodes in supercell.

    edges: Edge3D object list, all edges in supercell.

    arrows: (NOT SUPPORT) Arrow3D object list, all arrows in supercell, default is [].

    cell_vectors: 3D-like array,
        the basis vectors for the supercell, default is [[1.0, 0.0, 0.0],
                                                         [0.0, 1.0, 0.0],
                                                         [0.0, 0.0, 1.0]].
    """

    cell_vectors = dc.Basis3D("cell_vectors")

    def __init__(self, nodes, edges, arrows=None, cell_vectors=None):
        if cell_vectors is None:
            self.cell_vectors = np.array([[1.0, 0.0, 0.0],
                                          [0.0, 1.0, 0.0],
                                          [0.0, 0.0, 1.0]])
        else:
            self.cell_vectors = np.array(cell_vectors)

        super(SuperCell2D, self).__init__(nodes, edges, arrows)

    @staticmethod
    def from2d(supercell2d, cell_vectors=None):
        """ Construct 3D supercell from a 2D supercell.
        """
        return supercell2d.to3d(cell_vectors=cell_vectors)

    def expand(self, nx, ny, nz, cell_vectors=None):
        """ Expand the supercell to a larger one in 3D grid.

        Parameters:
        -----------
        nx : int, the expansion number along x axis.
        ny : int, the expansion number along y axis.
        nz : int, the expansion number along z axis.
        cell_vectors: 3x3 array, cell vectors for supercell expansion
            default value is the same as cell vectors of this supercell.
        """
        if cell_vectors is None:
            cell_vectors = self.cell_vectors
        cell_vectors = np.array(cell_vectors)

        # Expand along x axis.
        x_expanded_supercell = self
        for i in range(1, nx):
            move_vector = cell_vectors[0, :]*i
            x_expanded_supercell += self.clone(move_vector)

        # Expand along y axis.
        y_expanded_supercell = x_expanded_supercell
        for j in range(1, ny):
            move_vector = cell_vectors[1, :]*j
            y_expanded_supercell += x_expanded_supercell.clone(move_vector)

        # Expand along z axis.
        expanded_supercell = y_expanded_supercell
        for k in range(1, nz):
            move_vector = cell_vectors[2, :]*k
            expanded_supercell += y_expanded_supercell.clone(move_vector)

        return expanded_supercell

