'''
Script to plot no-merged energy profile
'''
import csv

import numpy as np
import matplotlib.pyplot as plt

from catplot.en_profile import plot_single_energy_diagram
from catplot.en_profile import plot_multi_energy_diagram
from catplot.en_profile import add_line_shadow
from catplot.functions import equation2list

# get input data
globs, locs = {}, {}
execfile('input.txt', globs, locs)

if 'rxn_equations' in locs and 'energies' in locs:  # multi rxn
    rxn_equations = locs["rxn_equations"]
    energies = locs["energies"]

    # Check data shape.
    if len(rxn_equations) != len(energies):
        raise ValueError("lengths of rxn_equations and energies are different.")

    for rxn_equation, energy_tuple in zip(rxn_equations, energies):
        equation_list = equation2list(rxn_equation)
        if len(equation_list) != len(energy_tuple):
            raise ValueError("unmatched shape: %s, %s" % (rxn_equation, str(energy_tuple)))

    # Check peak_withs length.
    if 'peak_widths' in locs:
        peak_widths = locs['peak_widths']
        if len(peak_widths) != len(rxn_equations):
            raise ValueError("lengths of peak widths is not matched.")
    else:
        peak_widths = [1.0]*len(rxn_equations)

    # Plot single diagrams.
    for idx, args in enumerate(zip(energies, rxn_equations)):
        fname = str(idx).zfill(2)
        print "Plotting diagram " + fname + "..."
        plot_single_energy_diagram(*args, show_mode='save', fname=fname)
        print "Ok."

    # Plot multi-diagram.
    print "Plotting multi-diagram..."
    fig, x_total, y_total = plot_multi_energy_diagram(rxn_equations,
                                                      energies,
                                                      peak_widths=peak_widths,
                                                      show_mode='save')
    print "Ok."

elif 'rxn_equation' in locs and 'energy_tuple' in locs:  # single rxn
    rxn_equation = locs["rxn_equation"]
    energy_tuple = locs["energy_tuple"]

    print "Plotting single-diagram..."
    if 'peak_widths' in locs:
        peak_widths = locs['peak_widths']
        if len(peak_widths) != 1:
            raise ValueError("lengths of peak widths is not matched.")
    else:
        peak_widths = (1.0)
    fig, x_total, y_total = plot_single_energy_diagram(energy_tuple,
                                                       rxn_equation,
                                                       peak_width=peak_widths[0],
                                                       show_mode='save')
    print "Ok."
else:  # no equation and energy tuple
    raise ValueError('No rxn equation and energy tuple is defined.\n' +
                     'Please check you data file...')

# Customize your diagram.
if locs.get('custom'):
    print "Custom plotting..."
    new_fig = plt.figure(figsize=(16, 9))
    # transparent figure
    if locs.get("transparent"):
        new_fig.patch.set_alpha(0)

    ax = new_fig.add_subplot(111)

    # transparent axe
    if locs.get("transparent"):
        ax.patch.set_alpha(0)

    # remove xticks
    ax.set_xticks([])
    ax.set_xmargin(0.03)

    # set attributes of y-axis
    if 'ylim' in locs:
        ymin, ymax = locs['ylim']
        ax.set_ylim(ymin, ymax)
        if 'n_yticks' in locs:  # must set ylim befor setting n_yticks
            ax.set_yticks(np.linspace(ymin, ymax, locs['n_yticks']))
    if 'yticklabels' in locs:
        ax.set_yticklabels(locs['yticklabels'])
    ax.set_ymargin(0.1)

    # add line shadow
    shadow_depth = locs.get("shadow_depth", 7)
    shadow_color = locs.get("shadow_color", "#595959")
    offset_coeff = locs.get("offset_coeff", 9.0)
    add_line_shadow(ax, x_total, y_total, depth=shadow_depth,
                    color=shadow_color, line_width=5.4,
                    offset_coeff=offset_coeff)

    if 'color' not in locs:
        print "No custom color. \nUse default color: black."
        color = '#000000'
    else:
        color = locs['color']
    ax.plot(x_total, y_total, linewidth=5.4, color=color)

    display_mode = locs.get("display_mode", "save")
    if display_mode == "interactive":
        new_fig.show()
    elif display_mode == "save":
        new_fig.savefig('./energy_profile/energy_profile.png', dpi=500)
    else:
        raise ValueError('Unrecognized show mode parameter : %s.', display_mode)
    print 'Ok.'

    # write plot data to csv file
    print "writing data file..."
    with open('./energy_profile/data.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(['X', 'Y'])
        x_col = x_total.reshape(-1, 1)
        y_col = y_total.reshape(-1, 1)
        writer.writerows(np.append(x_col, y_col, axis=1))
    print 'ok'

