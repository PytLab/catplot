# -*- coding:utf-8 -*-
'''
Module to plot energy profile.
'''

import threading
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
from matplotlib.patches import Ellipse

from catplot.interpolate import get_potential_energy_points
from catplot.functions import get_relative_energy_tuple
from catplot.chem_parser import RxnEquation


class ShadowThread(threading.Thread):
    "Sub-class of Thread class to create threads to plot shadows."
    def __init__(self, func, args):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args

    def run(self):
        self.func(*self.args)


class NoteThread(threading.Thread):
    "Sub-class of Thread class to add notes to line."
    def __init__(self, func, args):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args

    def run(self):
        self.func(*self.args)



def add_line_shadow(ax, x, y, depth, color, line_width=3, offset_coeff=1.0):
    "Add shadow to line in axes 'ax' by changing attribute of the object"
    # {{{
    def add_single_shadow(ax, x, y, order, depth, color, line_width):
        offset = transforms.ScaledTranslation(offset_coeff*order,
                                              -offset_coeff*order,
                                              transforms.IdentityTransform())
        shadow_trans = ax.transData + offset
        ax.plot(x, y, linewidth=line_width, color=color,
                transform=shadow_trans,
                alpha=(depth-order)/2.0/depth)
        return

    threads = []
    for i in range(depth):  # gather thread objects
        t = ShadowThread(add_single_shadow, (ax, x, y, i, depth,
                                             color, line_width))
        threads.append(t)

    for i in range(depth):
        threads[i].start()

    for i in range(depth):
        threads[i].join()

    return ax.lines
    # }}}


def plot_single_energy_diagram(*args, **kwargs):
    """
    Draw a potential energy diagram of a elementary reaction equation
    and save it.
    Return the Figure object.

    Parameters
    ----------
    energies : tuple of float, essential
        energy data for profile plotting.
        e.g. (0.0, 1.2, 0.7)

    rxn_equation : str, essential
        reaction equation string according to rules in setup file.
        e.g. 'HCOOH_g + 2*_s <-> HCOO-H_s + *_s -> HCOO_s + H_s'.

    hline_length : int, optional
        Length of each subsection(x_i, x_f), defualt to be 1.0.

    line_color : str, optional
        Color code of the line. Default to be '#000000'/'black'.

    has_shadow : Bool
        Whether to add shadow effect to the main line.
        Default to be False.

    fmt : str, optional
        The output format : ['pdf'|'jpeg'|'png'|'raw'|'pgf'|'ps'|'svg']
        Default to be 'jpeg'

    show_mode : str, 'show' or 'save'
        'show' : show the figure in a interactive way.
        'save' : save the figure automatically.

    peak_width : float, 1.0(default)
        peak width if TS exists.

    Other parameters
    ----------------
    kwargs :
        'fname' : str, optional
        'offset_coeff' : float, default to be 1.0
            shadow offset coefficient.

    Examples
    --------
    >>> plot_single_energy_diagram((0.0, 1.2, 0.6),
                                   'COO_s -> CO2_g + *_s',
                                   has_shadow=True,
                                   fname='pytlab')
    >>> <matplotlib.figure.Figure at 0x5659f30>
    """
    # {{{
    ###############  args setting before plotting  ################

    # Get arguments.
    if len(args) != 2:
        raise ValueError("Need at least 2 args: energies, rxn_equation.")
    energies, rxn_equation = args

    # Get keyword arguments.
    n = kwargs.pop("n", 100)
    hline_length = kwargs.pop("hline_length", 1.0)
    line_color = kwargs.pop("line_color", "#000000")
    has_shadow = kwargs.pop("has_shadow", True)
    fmt = kwargs.pop("fmt", "png")
    show_mode = kwargs.pop("show_mode", "show")
    peak_width = kwargs.pop("peak_width", 1.0)

    #####################  args setting END  #######################

    rxn_list = RxnEquation(rxn_equation).tolist()
    energies = get_relative_energy_tuple(energies)

    # energy info
    rxn_energy = round(energies[-1] - energies[0], 2)
    if len(energies) == 3:
        act_energy = round(energies[1] - energies[0], 2)

    # get x, y array
    x, y, _ = get_potential_energy_points(energies, n=n,
                                          hline_length=hline_length,
                                          peak_width=peak_width)

    # get maximum and minimum values of x and y axis
    y_min, y_max = np.min(y), np.max(y)
    x_max = 3.7*hline_length

    # scale of y
    y_scale = abs(y_max - y_min)

    ###################      start Artist Mode!      #######################

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111)
    ax.set_ylim(y_min - y_scale/5, y_max + y_scale/5)
    ax.set_xlim(-hline_length/3, x_max)
    ax.set_xlabel('Reaction Coordinate')
    ax.set_ylabel('Free Energy(eV)')
    ax.set_title(r'$\bf{'+RxnEquation(rxn_equation).texen()+r'}$',
                 fontdict={'fontsize': 13,
                           'weight': 1000,
                           'verticalalignment': 'bottom'})

    # add shadow
    if has_shadow:
        add_line_shadow(ax, x, y, depth=8, color='#595959')

    # main line
    ax.plot(x, y, color=line_color, linewidth=3)

    # energy latex string
    if 'act_energy' in dir():
        act_energy_latex = r'$\bf{G_{a} = ' + str(act_energy) + r' eV}$'
    rxn_energy_latex = r'$\bf{\Delta G = ' + str(rxn_energy) + r' eV}$'

    #######################   annotates   #######################

    # add species annotation

    # get annotate coordiantes
    note_offset = y_scale/40
    param_list = []

    # initial state
    note_x_i = hline_length/10
    note_y_i = energies[0] + note_offset
    note_str_i = r'$\bf{' + rxn_list[0].texen() + r'}$'
    param_list.append((note_x_i, note_y_i, note_str_i))

    # final state
    note_x_f = hline_length/10 + hline_length + peak_width
    note_y_f = energies[-1] + note_offset
    note_str_f = r'$\bf{' + rxn_list[-1].texen() + r'}$'
    param_list.append((note_x_f, note_y_f, note_str_f))

    if len(energies) == 3:
        # transition state
        note_y_b = np.max(y) + note_offset  # equal to energies[1]
        idx = np.argmax(y)
        note_x_b = x[idx] - hline_length/4
        #####################
        barrier_x = x[idx]  # x value of TS point
        #####################
        note_str_b = r'$\bf' + rxn_list[1].texen() + r'}$'
        param_list.append((note_x_b, note_y_b, note_str_b))

    # add annotates
    for idx, param_tuple in enumerate(param_list):
        if idx == 2:
            ax.text(*param_tuple, fontdict={'fontsize': 13,
                                            'color': '#CD5555'})
        else:
            ax.text(*param_tuple, fontdict={'fontsize': 13,
                                            'color': '#1874CD'})

    #########################################
    #                                       #
    #  inflection points coordinates:       #
    #    (hline_length, energies[0])        #
    #    (barrier_x, np.max(y))             #
    #    (2*hline_length, energies[-1])     #
    #                                       #
    #########################################

    # energy change annotation

    # initial state horizontal line
    hori_x_i = np.linspace(hline_length,
                           peak_width + 2*hline_length, 50)
    hori_y_i = np.linspace(energies[0], energies[0], 50)

    ax.plot(hori_x_i, hori_y_i, color=line_color, linewidth=1,
            linestyle='dashed')

    el = Ellipse((2, -1), 0.5, 0.5)

    if len(energies) == 3:  # for reaction with barrier
        # arrow between barrier
        ax.annotate('', xy=(barrier_x, energies[0]), xycoords='data',
                    xytext=(barrier_x, np.max(y)), textcoords='data',
                    arrowprops=dict(arrowstyle="<->"))
        # text annotations of barrier
        ax.annotate(act_energy_latex,
                    xy=(barrier_x, np.max(y)/2), xycoords='data',
                    xytext=(-150, 30), textcoords='offset points',
                    size=13, color='#B22222',
                    arrowprops=dict(arrowstyle="simple",
                                    fc="0.6", ec="none",
                                    patchB=el,
                                    connectionstyle="arc3,rad=0.2"),
                    )

    # arrow between reaction energy
    ax.annotate('', xy=(hline_length*3/2 + peak_width, energies[-1]),
                xycoords='data',
                xytext=(hline_length*3/2 + peak_width, energies[0]),
                textcoords='data',
                arrowprops=dict(arrowstyle="<->"))

    # text annotations of reaction energy
    ax.annotate(rxn_energy_latex,
                xy=(hline_length*3/2 + peak_width, (energies[-1]+energies[0])/2),
                xycoords='data',
                xytext=(50, 30), textcoords='offset points',
                size=13, color='#8E388E',
                arrowprops=dict(arrowstyle="simple",
                                fc="0.6", ec="none",
                                patchB=el,
                                connectionstyle="arc3,rad=-0.2"))

          ##############      annotates end      ################
     #################      Artist Mode End !      #######################

    # remove xticks
    ax.set_xticks([])

    # save the figure object

    # creat path
    if not os.path.exists("./energy_profile"):
        os.mkdir("./energy_profile")

    # filename
    if 'fname' in kwargs:
        fname = kwargs['fname'] + '.' + fmt
    else:
        fname = 'elementary_energy_diagram.' + fmt
    fullname = "./energy_profile/" + fname

    if show_mode == 'save':
        if 'dpi' in kwargs:
            fig.savefig(fullname, dpi=kwargs['dpi'])
        fig.savefig(fullname)
    elif show_mode == 'show':
        plt.show()
    else:
        raise ValueError('Unrecognized show mode parameter : ' + show_mode)

    return fig, x, y
    # }}}


def plot_multi_energy_diagram(*args, **kwargs):
    """
    Draw a potential energy diagram of a series of
    elementary reaction equation and save or show it.
    Return the Figure object.

    Parameters
    ----------
    args:

    rxn_equations_list : list
        a list containing a series of reaction equation string
        according to rules in setup file.
        e.g. ['HCOOH_g + 2*_s <-> HCOO-H_s + *_s -> HCOO_s + H_s',
              'HCOO_s + *_s <-> H-COO_s + *_s -> COO_s + H_s',
              'COO_s -> CO2_g + *_s',
              '2H_s <-> H-H_s + *_s -> H2_g + 2*_s'].
    energies : list of tuples
        e.g. [
                 (0.0, 1.0, 0.5),
                 (3.0, 4.7, 0.7),
                 (0.0, 4.0),
                 (3.0, 4.7, 0.7),
             ]

    hline_length : int, optional
        Length of each subsection(x_i, x_f), defualt to be 1.0.

    line_color : str, optional
        Color code of the line. Default to be '#000000'/'black'.

    init_y_offset : float, optional
        Initial offset value on y axis.

    has_shadow : Bool
        Whether to add shadow effect to the main line.
        Default to be True.

    show_note : bool
        Whether to show species note on the main line.
        Default to be True.

    show_aux_line: bool
        Whether to show auxiliary lines on the main line.
        Default to be Ture.

    show_arrow : bool
        Whether to show annotation arrow.
        Default to be True.

    fmt : str, optional
        The output format : ['pdf'|'jpeg'|'png'|'raw'|'pgf'|'ps'|'svg']
        Default to be 'jpeg'

    show_mode : str, 'show' or 'save'
        'show' : show the figure in a interactive way.
        'save' : save the figure automatically.

    peak_widths : tuple of floats, (1.0, ...)(default)
        peak widths if TS exists.

    Other parameters
    ----------------
    kwargs :
        'fname' : str, optional
        'dpi' : int, default to be 80
        'offset_coeff' : float, default to be 1.0
            shadow offset coefficient.

    Examples
    --------

    """
    # {{{

    ###############  args setting before plotting  ################

    # Get arguments.
    if len(args) != 2:
        raise ValueError("Need at least 2 args: rxn_equations_list, energies_tuple.")
    rxn_equations_list, energies_tuple = args

    # Get keyword arguements.
    if 'peak_widths' in kwargs:
        peak_widths = kwargs['peak_widths']
        if len(peak_widths) != len(rxn_equations_list):
            raise ValueError('number of peak widths and ' +
                             'number of rxn equations are not matched.')
    else:  # set to (1.0, 1.0, ...)
        peak_widths = tuple([1.0]*len(rxn_equations_list))

    n = kwargs.pop("n", 100)
    hline_length = kwargs.pop("hline_length", 1.0)
    line_color = kwargs.pop("line_color", "#000000")
    has_shadow = kwargs.pop("has_shadow", True)
    fmt = kwargs.pop("fmt", "png")
    init_y_offset = kwargs.pop("init_y_offset", 0.0)
    show_note = kwargs.pop("show_note", True)
    show_aux_line = kwargs.pop("show_aux_line", True)
    show_arrow = kwargs.pop("show_arrow", True)
    show_mode = kwargs.pop("show_mode", "show")

    #####################  args setting END  #######################

    # convert rxn_equation_list(str) to elementary_rxns_list alike list
    rxns_list = [RxnEquation(rxn_equation).tolist() for rxn_equation in rxn_equations_list]

    x_offset, y_offset = 0.0, init_y_offset
    total_x, total_y = [], []
    piece_points = []  # collectors

    for idx, (rxn_equation, peak_width) in enumerate(zip(rxn_equations_list, peak_widths)):
        energies = get_relative_energy_tuple(energies_tuple[idx])
        x, y, x2 = get_potential_energy_points(energies=energies, n=n,
                                               hline_length=hline_length,
                                               peak_width=peak_widths[idx])
        x_scale = 2*hline_length + peak_width

        # get total y
        offseted_y = y + y_offset
        total_y.extend(offseted_y.tolist())

        # get total x
        offseted_x = x + x_offset
        total_x.extend(offseted_x.tolist())

        #######   collect values for adding annotations   #######

        # there are 3 points in each part
        p1 = (2*hline_length+offseted_x[0], offseted_y[0])
        p3 = (offseted_x[-1], offseted_y[-1])

        if len(energies) == 3:
            p2 = (2*hline_length + x2 + offseted_x[0],  # x2 is the x value of barrier
                  energies[1] + y_offset)
            piece_points.append((p1, p2, p3))
        elif len(energies) == 2:
            piece_points.append((p1, p3))

        ################   Collection End   ################

        # update offset value for next loop
        x_offset += x_scale
        y_offset = offseted_y[-1]

    # Add extral line

    # add head horizontal line
    head_extral_x = np.linspace(0.0, hline_length, n).tolist()
    offseted_total_x = (np.array(total_x)+hline_length).tolist()
    head_extral_y = [total_y[0]]*n
    total_x = head_extral_x + offseted_total_x
    total_y = head_extral_y + total_y

    # add the last horizontal line
    tail_extral_x = np.linspace(total_x[-1],
                                total_x[-1]+hline_length,
                                n).tolist()
    tail_extral_y = [total_y[-1]]*n
    total_x += tail_extral_x
    total_y += tail_extral_y
    total_x, total_y = np.array(total_x), np.array(total_y)

    # get extreme values of x and y
    y_min, y_max = np.min(total_y), np.max(total_y)
    x_min, x_max = total_x[0], total_x[-1]
    y_scale = y_max-y_min

    ###################      start Artist Mode!      ######################

    multi = len(rxn_equations_list)/2.2
    fig = plt.figure(figsize=(multi*10, multi*5))
    #fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_ylim(y_min - y_scale/10, y_max + y_scale/10)
    ax.set_xlim(x_min-hline_length, x_max+hline_length)
    ax.set_title('Energy Profile',
                 fontdict={
                     'fontsize': 15,
                     'weight': 100,
                     'verticalalignment': 'bottom'
                     })
    ax.set_xlabel('Reaction Coordinate')
    ax.set_ylabel('Free Energy(eV)')

    # add shadow
    if has_shadow:
        add_line_shadow(ax, total_x, total_y, depth=8,
                        color='#595959')

    # main line
    ax.plot(total_x, total_y, color=line_color, linewidth=3)

    # get state string list as notes
    state_str_list = []
    for rxn_list in rxns_list:
        t = tuple([state_obj.texen() for state_obj in rxn_list[:-1]])
        state_str_list.append(t)

    ####################     Main loop to add notes     ###################
    # This is the main loop to add extral info to main line
    # For each single loop, we get 3 or 2 points(tuple) for each elementary rxn
    # and the first 2 or 1 latex reaction state string(involved in list)

    def add_state_note(pts, tex_states):
        "function to add notes to a state"
        start_point, end_point = pts[0], pts[-1]

        # add horizontal lines and vertical arrowa
        if show_aux_line:
            # plot horizontal lines
            hori_x = np.linspace(start_point[0], end_point[0]+2*hline_length, 50)
            hori_y = np.linspace(start_point[-1], start_point[-1], 50)
            ax.plot(hori_x, hori_y, color=line_color, linewidth=1, linestyle='dashed')

            # plot vertical arrows
            if len(pts) == 3:
                mid_point = pts[1]
                #plot activation energy arrow
                ax.annotate('', xy=(mid_point[0], mid_point[-1]),
                            xycoords='data',
                            xytext=(mid_point[0], start_point[-1]),
                            textcoords='data',
                            arrowprops=dict(arrowstyle="<->"))

            # plot reaction energy arrow
            ax.annotate('', xy=(end_point[0]+hline_length, end_point[-1]),
                        xycoords='data',
                        xytext=(end_point[0]+hline_length, start_point[-1]),
                        textcoords='data',
                        arrowprops=dict(arrowstyle="<->"))

        if show_note:
            # add species notes
            if len(pts) == 3:  # those who have TS
                for state_idx, (pt, tex_state) in enumerate(zip(pts, tex_states)):
                    if state_idx == 0:  # for initial or final state
                        note_x = pt[0] - 1.8*hline_length
                        note_y = pt[-1] + y_scale/50
                        ax.text(note_x, note_y, r'$\bf{'+tex_state+r'}$',
                                fontdict={'fontsize': 13, 'color': '#1874CD'})

                    if state_idx == 1:  # for transition state
                        note_x = pt[0] - hline_length/2
                        note_y = pt[-1] + y_scale/50
                        ax.text(note_x, note_y, r'$\bf{'+tex_state+r'}$',
                                fontdict={'fontsize': 13, 'color': '#CD5555'})
            # no TS.
            if len(pts) == 2:
                pt, tex_state = pts[0], tex_states[0]
                note_x = pt[0] - 1.8*hline_length
                note_y = pt[-1] + y_scale/50
                ax.text(note_x, note_y, r'$\bf{'+tex_state+r'}$',
                        fontdict={'fontsize': 13, 'color': '#1874CD'})

        if show_arrow:
            # add energy annotations
            el = Ellipse((2, -1), 0.5, 0.5)
            # annotation between IS and FS
            rxn_energy = round(end_point[-1] - start_point[-1], 2)
            rxn_energy_latex = r'$\bf{\Delta G = ' + str(rxn_energy) + r' eV}$'
            ax.annotate(rxn_energy_latex,
                        xy=(end_point[0]+hline_length, (start_point[-1]+end_point[-1])/2),
                        xycoords='data',
                        xytext=(-70, 30), textcoords='offset points',
                        size=13, color='#8E388E',
                        arrowprops=dict(arrowstyle="simple",
                                        fc="0.6", ec="none",
                                        patchB=el,
                                        connectionstyle="arc3,rad=0.2"))
            if len(pts) == 3:
                # annotation between TS and IS
                act_energy = round((mid_point[-1] - start_point[-1]), 2)
                act_energy_latex = r'$\bf{G_{a} = '+str(act_energy)+r' eV}$'
                ax.annotate(act_energy_latex,
                            xy=(mid_point[0], (mid_point[1]+start_point[1])/2),
                            xycoords='data', xytext=(30, 20),
                            textcoords='offset points',
                            size=13, color='#B22222',
                            arrowprops=dict(arrowstyle="simple",
                                            fc="0.6", ec="none",
                                            patchB=el,
                                            connectionstyle="arc3,rad=-0.2"))

    #########    Main Loop END    ########

    # use multiple thread to add notes
    note_threads = []
    nstates = len(state_str_list)

    for pts, tex_states in zip(piece_points, state_str_list):
        thrd = NoteThread(add_state_note, (pts, tex_states))
        note_threads.append(thrd)

    for i in range(nstates):
        note_threads[i].start()

    for i in range(nstates):
        note_threads[i].join()

    #add species note at last section
    if show_note:
        pt = pts[-1]
        tex_state = rxns_list[-1][-1].texen()
        ax.text(pt[0]+0.2*hline_length, pt[-1]+y_scale/50,
                r'$\bf{'+tex_state+r'}$',
                fontdict={'fontsize': 13, 'color': '#1874CD'})

    # remove xticks
    ax.set_xticks([])

#####################   Artist Mode End   #####################

    # creat path
    if not os.path.exists("./energy_profile"):
        os.mkdir("./energy_profile")

    # filename
    if 'fname' in kwargs:
        fname = kwargs['fname'] + '.' + fmt
    else:
        fname = 'multi_energy_diagram.' + fmt
    fullname = "./energy_profile/" + fname

    if show_mode == 'show':
        fig.show()
    elif show_mode == 'save':
        if 'dpi' in kwargs:
            fig.savefig(fullname, dpi=kwargs['dpi'])
        fig.savefig(fullname)
    else:
        raise ValueError('Unrecognized show mode parameter : ' + show_mode)

    return fig, total_x, total_y
    # }}}

