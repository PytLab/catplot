#!/usr/bin/env python
# -*- coding: utf-8 -*-

from copy import deepcopy

import numpy as np


class Plane3D(object):
    """ Plane in 3D canvas.

    Parameters:
    -----------
    x: 1-d array, the range of the plane along "x" axis
       (it's a generalized x, it depends on the axis value).

    y: 1-d array, the range of the plane along "y" axis.
       (it's a generalized y, it depends on the axis value).

    z: 1-d array, the range of the plane along "z" axis.
       (it's a generalized z, it depends on the axis value).

    axis: the axis vertical to the plane, default value is "z".
        if axis is 'z', the x would be x axis, the y would be y axis.
        if axis is 'x', the x would be y axis, the y would be z axis.
        if axis is 'y', the x would be x axis, the y would be z axis.

    color: str, color of the plane face.

    edgecolor: str, color of plane edges.

    shade: bool, whether to shade the facecolor, default is False.

    alpha: float, transparent of the plane, default is 1.0.
    """
    def __init__(self, x, y, z, axis="z", **kwargs):
        # Force to float for coordinates operations.
        x = [float(i) for i in x]
        y = [float(i) for i in y]
        z = float(z)

        # Broadcast data.
        x, y = np.meshgrid(x, y)
        z = np.ones(x.shape)*z

        # Assignment correctly.
        if axis == "x":
            self.y, self.z, self.x  = x, y, z
        elif axis == "y":
            self.x, self.z, self.y = x, y, z
        elif axis == "z":
            self.x, self.y, self.z = x, y, z

        self.color = kwargs.pop("color", None)
        self.edgecolor = kwargs.pop("edgecolor", None)
        self.shade = kwargs.pop("shade", False)
        self.alpha = kwargs.pop("alpha", 1.0)

    def move(self, move_vector):
        """ Move the plane along the move vector.

        Parameters:
        -----------
        move_vector: list of float, the vector along which the node moves.
        """
        if ((len(move_vector) != 3) or
                not all([isinstance(i, (int, float)) for i in move_vector])):
            msg = "move vector must be a sequence with three numbers"
            raise ValueError(msg)

        dx, dy, dz = move_vector
        self.x += dx
        self.y += dy
        self.z += dz

        # For chain operations.
        return self

    def clone(self, relative_position=None):
        """ Clone a new plane to a specific position.

        Parameters:
        -----------
        relative_position: list of three float, optional.
            the position of new cloned node relative to the original node,
            default is [0.0, 0.0, 0.0].
        """
        if relative_position is None:
            relative_position = [0.0, 0.0, 0.0]

        # Create a new plane and move.
        plane = deepcopy(self)
        plane.move(relative_position)

        return plane

