#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Module for line object in energy profile.
"""

class EPLine(object):
    """ Base class for lines in energy profile.
    """
    def __init__(self, x, y, **kwargs):
        self.x = x
        self.y = y

        self.color = kwargs.pop("color", "#000000")
        self.shadow_color = kwargs.pop("shadow_color", "#595959")

