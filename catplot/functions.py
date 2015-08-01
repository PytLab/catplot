# -*- coding:utf-8 -*-
#static functions
import re


#functions for general energy profile
def get_relative_energy_tuple(energy_tuple):
    "Set is energy as 0, other energies are relative."
    energy_list = list(energy_tuple)
    reference_energy = energy_list[0]
    for i in xrange(len(energy_list)):
        energy_list[i] = energy_list[i] - reference_energy
    return tuple(energy_list)


def equation2list(rxn_equation):
    "Convert rxn_equation string to rxn_list."
    states_regex = re.compile(r'([^\<\>]*)(?:\<?\-\>)' +
                              r'(?:([^\<\>]*)(?:\<?\-\>))?([^\<\>]*)')
    m = states_regex.search(rxn_equation)
    rxn_list = []
    for idx in range(1, 4):
        if m.group(idx):
            rxn_list.append(m.group(idx))

    return rxn_list


#functions for merged energy profile
def verify_multi_shape(multi_rxn_equations, multi_energy_tuples):
    "Verify the legitimacy of input data."
    for rxn_equations, energy_tuples in \
            zip(multi_rxn_equations, multi_energy_tuples):
        if len(rxn_equations) != len(energy_tuples):
            raise ValueError('Unmatched shape.\n' +
                             'Check your input data please.')
        for rxn_equation, energy_tuple in zip(rxn_equations, energy_tuples):
            rxn_list = equation2list(rxn_equation)
            if len(rxn_list) != len(energy_tuple):
                raise ValueError("unmatched shape: %s, %s" %
                                 (rxn_equation, str(energy_tuple)))
    return


def verify_attrlen(attr, n):
    "Verify length of iterable attr."
    if hasattr(attr, '__getitem__'):  # if iterable
        if len(attr) != n:
            raise ValueError('length of %s is not equal to %d' %
                             (str(attr), n))
    else:
        raise ValueError('%s is not iterable!' % str(attr))
