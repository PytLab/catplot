#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Module for interpolation algorithm implementation for energy profile plotting.
"""

from math import sqrt

import numpy as np
from scipy import interpolate


def quadratic_connect_interp(x1, y1, x2, y2):
    # {{{
    """
    Use quadratic interpolation(y = ax^2 + bx + c) to connect points (x1, y1) and (x2, y2).

    ------------------------------

    A = (x1, y1)
    B = (x2, y2)

         B                       B
         _                       _
                                /
                -->            /
    A           -->         A /
    _                       _/

    ------------------------------

    Parameters
    ----------
    x1, y1 : float
        x and y value of the first point.
    x2, y2 : float
        x and y value of the second point.

    Return:
    -------
    Quadratic function object.

    Examples
    --------
    >>> f = m.plotter.quadratic_interp_poly(0.0, 0.0, 2.0, 2.0)
    >>> <function kinetic.plotters.general_plotter.poly_func>

    """
    A = np.matrix([[x1**2, x1, 1],
                   [x2**2, x2, 1],
                   [2*x2, 1, 0]])

    b = np.matrix([[y1], [y2], [0]])
    x = A.I * b
    x.shape = (1, -1)
    a, b, c = x.tolist()[0]

    poly_func = lambda x: a*x**2 + b*x + c

    return poly_func
    # }}}


def quadratic_interp(x1, y1, x3, y3, y2):
    # {{{
    r"""
    Given the y value of the second point and use quadratic function to
    find the x value of second point by solving the equation
         y = m*(x - n)**2

    ------------------------------------

    A = (x1, y1)
    B = (x2, y2) *<x2 will be found>
    C = (x3, y3)
                                    B
    BBBBB                           _
          C                        / \ C
          _        -->            /   \_
    A              -->         A /
    _                          _/

    ------------------------------------

    Parameters:
    -----------
    x1, y1 : float
        x and y value of the first point(A).
    x3, y3 : float
        x and y value of the third point(C).
    y2: float
        the y value of the second point(B).

    Return:
    -------
    (x value of second point, quadratic function object)
    """
    k = (y3 - y2)/(y1 - y2)
    a = k - 1
    b = 2*x3 - 2*k*x1
    c = k*x1**2 - x3**2

    roots = [
        (-b + sqrt(b**2 - 4*a*c)) / (2*a),
        (-b - sqrt(b**2 - 4*a*c)) / (2*a),
    ]
    # get root between x1 and x3
    root = [x for x in roots if min(x1, x3) <= x <= max(x1, x3)]
    if len(root) == 0:
        raise ValueError('No real root.')
    else:
        n = x2 = root[0]
    # y = m*(x - n)**2 + l
    m = (y1 - y2) / ((x1 - x2)**2)
    l = y2
    func = lambda x: m*(x - n)**2 + l

    return x2, func
    # }}}


def spline_interp(x1, y1, x3, y3, y2, x2_ratio=0.5):
    # {{{
    r"""
    Use both quadratic and spline interpolation to interpolate three given points.

    ---------------------------------------

    A = (x1, y1)
    B = (x2, y2) = ( (x1 + x3)*x2_ratio )
    C = (x3, y3)

       B                            B
       _                            _
          C                        / \ C
          _        -->            /   \_
    A              -->         A /
    _                          _/

    --------------------------------------

    Parameters:
    -----------
    x1, y1 : float
        x and y value of the first point(A).
    x3, y3 : float
        x and y value of the third point(C).
    y2: float
        the y value of the second point(B).
    x2_ratio: float (0 ~ 1)
        define the horizontal position of the second point(B),
        x2 = (x1 + x3)*x2_ratio

    Return:
    -------
    (x value of second point, quadratic function object)

    """
    if not 0.0 < x2_ratio < 1.0:
        raise ValueError("Invalide x2 ratio({}) which should be in (0 ~ 1)".format(x2_ratio))

    x2 = (x1 + x3)*x2_ratio

    # Collect all points to be interpolated.
    x, y = [], []

    # Insert temporary point.
    # The first half.
    quad_func = quadratic_connect_interp(x1, y1, x2, y2)
    quad_func = np.frompyfunc(quad_func, 1, 1)
    insert_x1 = np.linspace(x1, x2, 5)
    insert_y1 = quad_func(insert_x1)
    x = np.append(x, insert_x1)
    y = np.append(y, insert_y1)

    # The second half.
    quad_func = quadratic_connect_interp(x3, y3, x2, y2)
    quad_func = np.frompyfunc(quad_func, 1, 1)
    insert_x2 = np.linspace(x2 + 0.1, x3, 5)
    insert_y2 = quad_func(insert_x2)
    x = np.append(x, insert_x2)
    y = np.append(y, insert_y2)

    func = interpolate.UnivariateSpline(x, y, s=0)

    return x2, func
    # }}}


def get_potential_energy_points(energies,
                                n=100,
                                hline_length=1.0,
                                peak_width=1.0,
                                kind="spline"):
    # {{{
    """
    Get all points for a reaction process containing IS, TS, FS.

    Parameters
    ----------
    energies : tuple
        A energy tuple containing (E_IS, E_TS, E_FS).
    n : float, optional
        Number of points interpolated.
    hline_length : int, optional
        Length of the horizontal line for the IS & FS.
    peak_width : float, default to be 1.0
    kind: str, optional
        Specifies the kind of interpolation as a string ('quadratic', 'spline').
        Default is 'spline'.

    Return:
    -------
    (points for x, points for y), two 1-D arrays.
    """
    if kind == "spline":
        interp_func = spline_interp
    elif kind == "quadratic":
        interp_func = quadratic_interp
    else:
        raise ValueError(("Invalide interpolation kind({}) which should be" +
                          "in ('quadiatic', 'spline')").format(kind))

    # Use interpolation method to get barrier point.
    if len(energies) == 3:
        y1, y2, y3 = energies  # E_is, E_ts, E_fs
        # check energy tuple
        if not (y2 > max(y1, y3)):
            raise ValueError('abnormal energy : ' + str(energies))
        # get x2
        x2, f = interp_func(0.0, y1, peak_width, y3, y2)
        init_x_b = np.linspace(0, peak_width, n)
        f_ufunc = np.frompyfunc(f, 1, 1)  # convert to universal function
        y_b = f_ufunc(init_x_b)
        x_b = init_x_b + hline_length     # translation

        # initial state y
        x_i = np.linspace(0, hline_length, n)
        y_i = np.linspace(y1, y1, n)

        # final state y
        x_f = np.linspace(hline_length+peak_width,
                          2*hline_length+peak_width, n)
        y_f = np.linspace(y3, y3, n)
        # Combine all points
        y = np.array(y_i.tolist() + y_b.tolist() + y_f.tolist())
        #x = np.linspace(0, x3 + 2*hline_length, 3*n)
        x = np.array(x_i.tolist() + x_b.tolist() + x_f.tolist())

    if len(energies) == 2:
        #transition state
        energy_list = list(energies)
        if energy_list[0] < energy_list[-1]:
            energy_list.insert(1, energies[-1]+1e-100)
            init_x_b = np.array([0.0, peak_width - 1e-5, peak_width])
        else:
            energy_list.insert(1, energies[0]+1e-100)
            init_x_b = np.array([0.0, 1e-5, peak_width])
        energies = tuple(energy_list)

        init_y_b = np.array(energies)
        f_b = interpolate.interp1d(init_x_b, init_y_b, kind='quadratic')
        x_b = np.linspace(0, peak_width, n)
        y_b = f_b(x_b)
        x_b = x_b + hline_length

        # initial state y
        y_i = np.linspace(energies[0], energies[0], n)
        x_i = np.linspace(0, hline_length, n)

        # final state y
        y_f = np.linspace(energies[-1], energies[-1], n)
        x_f = np.linspace(hline_length + peak_width,
                          2*hline_length + peak_width, n)

        # Combine all points
        y = np.array(y_i.tolist() + y_b.tolist() + y_f.tolist())
        x = np.array(x_i.tolist() + x_b.tolist() + x_f.tolist())
        x2 = 0.0

#    plt.plot(x, y)
#    plt.show()
    return x, y
    # }}}

