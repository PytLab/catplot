'''
    Script to plot no-merged energy profile
'''
import sys
import csv

from catplot.en_profile import *
from catplot.functions import equation2list

#get input data
globs, locs = {}, {}
execfile('input.txt', globs, locs)

if 'rxn_equations' in locs and 'energy_tuples' in locs:  # multi rxn
    # check data shape
    if len(locs['rxn_equations']) != len(locs['energy_tuples']):
        raise ValueError("lengths of rxn_equations and energy_tuples " +
                         "are different.")
    for rxn_equation, energy_tuple in \
            zip(locs['rxn_equations'], locs['energy_tuples']):
        equation_list = equation2list(rxn_equation)
        if len(equation_list) != len(energy_tuple):
            raise ValueError("unmatched shape: %s, %s" %
                             (rxn_equation, str(energy_tuple)))
    # check peak_withs length
    if 'peak_widths' in locs:
        peak_widths = locs['peak_widths']
        if len(locs['peak_widths']) != len(locs['rxn_equations']):
            raise ValueError("lengths of peak widths is not matched.")
    else:
        peak_widths = tuple([1.0]*len(locs['rxn_equations']))

    #plot single diagrams
    for idx, args in enumerate(zip(locs['energy_tuples'], locs['rxn_equations'])):
        fname = str(idx).zfill(2)
        print "Plotting diagram " + fname + "..."
        plot_single_energy_diagram(*args, show_mode='save', fname=fname)
        print "Ok."

    #plot multi-diagram
    print "Plotting multi-diagram..."
    fig, x_total, y_total = \
        plot_multi_energy_diagram(locs['rxn_equations'], locs['energy_tuples'],
                                  peak_widths=peak_widths, show_mode='save')
    print "Ok."

elif 'rxn_equation' in locs and 'energy_tuple' in locs:  # single rxn
    print "Plotting single-diagram..."
    if 'peak_widths' in locs:
        peak_widths = locs['peak_widths']
        if len(peak_widths) != 1:
            raise ValueError("lengths of peak widths is not matched.")
    else:
        peak_widths = (1.0)
    fig, x_total, y_total = \
        plot_single_energy_diagram(locs['energy_tuple'], locs['rxn_equation'],
                                   peak_width=peak_widths[0],
                                   show_mode='save')
    print "Ok."
else:  # no equation and energy tuple
    raise ValueError('No rxn equation and energy tuple is defined.\n' +
                     'Please check you data file...')

#customize your diagram
if locs.get('custom'):
    print "Custom plotting..."
    new_fig = plt.figure(figsize=(16, 9))
    # transparent figure
    if len(sys.argv) > 2 and sys.argv[2] == '--trans':
        new_fig.patch.set_alpha(0)

    ax = new_fig.add_subplot(111)
    # transparent axe
    if len(sys.argv) > 2 and sys.argv[2] == '--trans':
        ax.patch.set_alpha(0)
    #remove xticks
    ax.set_xticks([])
    ax.set_xmargin(0.03)

    #set attributes of y-axis
    if 'ylim' in locs:
        ymin, ymax = locs['ylim']
        ax.set_ylim(ymin, ymax)
        if 'n_yticks' in locs:  # must set ylim befor setting n_yticks
            ax.set_yticks(np.linspace(ymin, ymax, locs['n_yticks']))
    if 'yticklabels' in locs:
        ax.set_yticklabels(locs['yticklabels'])
    ax.set_ymargin(0.1)

    #add line shadow
    shadow_depth = locs['shadow_depth'] if 'shadow_depth' in locs else 7
    shadow_color = locs['shadow_color'] if 'shadow_color' in locs else '#595959'
    offset_coeff = locs['offset_coeff'] if 'offset_coeff' in locs else 9.0
    add_line_shadow(ax, x_total, y_total, depth=shadow_depth,
                    color=shadow_color, line_width=5.4,
                    offset_coeff=offset_coeff)

    if 'color' not in locs:
        print "No custom color. \nUse default color: black."
        color = '#000000'
    else:
        color = locs['color']
    ax.plot(x_total, y_total, linewidth=5.4, color=color)
    if sys.argv[1] == '--show':
        new_fig.show()
    elif sys.argv[1] == '--save':
        new_fig.savefig('./energy_profile/energy_profile.png', dpi=500)
    else:
        raise ValueError('Unrecognized show mode parameter : %s.', sys.argv[1])
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
