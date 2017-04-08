""" Script to plot merged energy profile
"""

import csv

import numpy as np
import matplotlib.pyplot as plt

from catplot.plotutil import plot_multi_energy_diagram, add_line_shadow
from catplot.functions import verify_multi_shape, verify_attrlen

globs, locs = {}, {}
execfile('input.txt', globs, locs)  # get input data

# Check the shape of input data.
multi_rxn_equations = locs['multi_rxn_equations']
multi_energies = locs['multi_energies']
verify_multi_shape(multi_rxn_equations, multi_energies)

if 'peak_widths' in locs:
    set_peak_widths = True
    peak_widths = locs['peak_widths']

    # Check peak_widths length.
    for widths, energy_tuples in zip(peak_widths, multi_energies):
        if len(widths) != len(energy_tuples):
            raise ValueError("lengths of peak widths is not matched.")

# Number of lines to be drawn.
nlines = len(multi_rxn_equations)

# Get initial points offset on y axis.
if 'init_y_offsets' in locs:
    init_y_offsets = locs['init_y_offsets']
    verify_attrlen(init_y_offsets, nlines)
else:
    init_y_offsets = [0.0]*nlines

points_list = []
print "Plotting single multi-energy profile..."

# Zip data.
zipped_data = zip(multi_rxn_equations, multi_energies, init_y_offsets)

for idx, (rxn_equations, energy_tuples, init_y_offset) in enumerate(zipped_data):
    fname = 'multi_energy_diagram_' + str(idx).zfill(2)
    print "Plotting diagram " + fname + "..."

    if set_peak_widths:
        fig, x_total, y_total = plot_multi_energy_diagram(rxn_equations,
                                                          energy_tuples,
                                                          init_y_offset=init_y_offset,
                                                          peak_widths=peak_widths[idx],
                                                          n=10000, show_mode='save',
                                                          fname=fname)
    else:
        fig, x_total, y_total = plot_multi_energy_diagram(rxn_equations,
                                                          energy_tuples,
                                                          init_y_offset=init_y_offset,
                                                          n=10000, show_mode='save',
                                                          fname=fname)
    print "Ok."
    points_list.append((x_total, y_total))

# Merge lines
print 'Merge diagrams...'
new_fig = plt.figure(figsize=(16, 9))

# transparent figure
if locs.get("transparent"):
    new_fig.patch.set_alpha(0)

ax = new_fig.add_subplot(111)

# transparent axe
if locs.get("transparent"):
    ax.patch.set_alpha(0)

# Remove xticks.
ax.set_xticks([])
ax.set_xmargin(0.03)

# Set attributes of y-axis.
ax.set_ymargin(0.03)

if 'ylim' in locs:
    ymin, ymax = locs['ylim']
    ax.set_ylim(ymin, ymax)
    if 'n_yticks' in locs:  # must set ylim befor setting n_yticks
        n_yticks = locs['n_yticks']
        ax.set_yticks(np.linspace(ymin, ymax, n_yticks))

if 'yticklabels' in locs:
    yticklabels = locs['yticklabels']
    ax.set_yticklabels(yticklabels)

# Colors setting.
if 'colors' in locs:
    colors = locs['colors']
    verify_attrlen(colors, nlines)
elif nlines <= 6:
    colors = ['#A52A2A', '#000000', '#36648B', '#FF7256', '#008B8B', '#7A378B']
else:
    raise ValueError('Line color is undefined.')

# Shadow attrs setting.
shadow_depth = locs.get("shadow_depth", 7)
shadow_color = locs.get("shadow_color", "#595959")
offset_coeff = locs.get("offset_coeff", 9.0)

# Line attr setting
line_width = locs.get("line_width", 4.5)

for color, points in zip(colors, points_list):
    add_line_shadow(ax, *points, depth=shadow_depth, color=shadow_color,
                    line_width=3, offset_coeff=offset_coeff)
    ax.plot(*points, linewidth=line_width, color=color)

display_mode = locs.get("display_mode", "save")

if display_mode == "interactive":
    new_fig.show()
elif display_mode == "save":
    new_fig.savefig('./energy_profile/merged_energy_profile.png', dpi=500)
else:
    raise ValueError("Invalide display mode: {}".format(display_mode))

print 'Ok.'

# write data to csv file
print 'writting data files...'
header = ['X', 'Y']
for idx, (x_total, y_total) in enumerate(points_list):
    x_col = x_total.reshape(-1, 1)
    y_col = y_total.reshape(-1, 1)
    rows = np.append(x_col, y_col, axis=1)
    with open('./energy_profile/data'+str(idx)+'.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
print 'Ok.'

