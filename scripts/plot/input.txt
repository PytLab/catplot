'''
    Data for energy profile plotting.
'''

#for a number of rxn equations
#COMMENT THEM OUT if not a number of rxn equations

#elementary reaction equations
rxn_equations = [
    'HCOOH_g + 2*_s <-> HCOO-H_s + *_s -> HCOO_s + H_s',
    'HCOO_s + *_s <-> H-COO_s + *_s -> COO_s + H_s',
    'COO_s -> CO2_g + *_s',
    '2H_s <-> H-H_s + *_s -> H2_g + 2*_s'
]

#relative energies
energy_tuples = [
    # IS,  TS,  FS
    #--------------
    (0.0, 1.0, 0.5),
    (3.0, 4.7, 0.7),
    (0.0, 4.0),
    (3.0, 4.7, 0.7),
]


#for a single rxn equation.
#COMMENT THEM OUT if not single rxn equation
'''
rxn_equation = 'HCOOH_g + 2*_s <-> HCOO-H_s + *_s -> HCOO_s + H_s'

#relative energies
energy_tuple = (0.0, 0.33, -0.26)
'''

#custom plotting attrs setting

custom = True  # True or False. if False, no custom diagram is plotted.

#y axis attrs
#ylim = (-0.75, 0.5)  # (min, max)
#n_yticks = 11  # ticks number on y axis
#yticklabels = ['-0.5', '', '-0.25', '', '0.0', '', '0.25', '', '0.5']  # tick labels on y axis

color = '#585858'  # line color

#shadow attrs
shadow_depth = 7
shadow_color = '#595959'
offset_coeff = 8.0
