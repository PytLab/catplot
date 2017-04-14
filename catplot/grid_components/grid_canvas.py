#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Module for grid plotting canvas.
"""

from catplot.canvas import Canvas


class Grid2DCanvas(Canvas):
    """ Canvas for 2D grid plotting.
    """
    def __init__(self, **kwargs):
        super(Grid2DCanvas, self).__init__(**kwargs)

