'''
    Data for energy profile plotting.
'''

#elementary reaction equations
multi_rxn_equations = [
    [
        'CO2 + * -> CO2*',
        'CO2* <-> CO-O_* -> CO*',
        'CO* <-> C-O* -> C*',
    ],

    [
        'CO2 + * -> CO2*',
        'CO2* <-> CO-O_* -> CO*',
        'CO* + H* <-> CO-H* -> COH*',
        'COH* <-> CH-O* -> CH*',
    ],
]

#relative energies
multi_energy_tuples = [
    # IS,  TS,  FS
    #--------------
    [
        (0.0, -0.34),
        (-0.34, -0.08, -1.28),
        (-1.28, 1.49, -0.45),
    ],

    [
        (0.0, -0.34),
        (-0.34, -0.08, -1.28),
        (-1.28, -0.26, -0.66),
        (-0.66, 0.98, -0.89),
    ],
]

#line colors
colors = ['#A52A2A', '#000000']  # '#A52A2A', '#000000', '#36648B', '#FF7256', '#008B8B', '#7A378B'

#shadow attrs
shadow_depth = 7
shadow_color = '#595959'
offset_coeff = 8.0

#line attrs
line_width = 4.5

#initial y offset
init_y_offsets = [0.0, -0.39]

#y axis attrs
ylim = (-2.0, 2.0)  # (min, max)
n_yticks = 9  # ticks number on y axis
#yticklabels = ['-0.5', '', '-0.25', '', '0.0', '', '0.25', '', '0.5']  # tick labels on y axis
