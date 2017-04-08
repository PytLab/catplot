# -*- coding:utf-8 -*-
#static functions
import re

from catplot.chem_parser import RxnEquation


#functions for general energy profile
def get_relative_energy_tuple(energy_tuple):
    """ Set is energy as 0, other energies are relative.
    """
    energy_list = list(energy_tuple)
    reference_energy = energy_list[0]
    for i in xrange(len(energy_list)):
        energy_list[i] = energy_list[i] - reference_energy
    return tuple(energy_list)


# functions for merged energy profile
def verify_multi_shape(multi_rxn_equations, multi_energy_tuples):
    """ Verify the legitimacy of input data.
    """
    for rxn_equations, energy_tuples in zip(multi_rxn_equations, multi_energy_tuples):
        if len(rxn_equations) != len(energy_tuples):
            raise ValueError('Unmatched shape.\nCheck your input data please.')

        for rxn_equation, energy_tuple in zip(rxn_equations, energy_tuples):
            rxn_list = RxnEquation(rxn_equation).tolist()
            if len(rxn_list) != len(energy_tuple):
                raise ValueError("unmatched shape: {}, {}".format(rxn_equation, energy_tuple))
    return


def verify_attrlen(attr, n):
    """ Verify length of iterable attr.
    """
    if hasattr(attr, '__getitem__'):  # if iterable
        if len(attr) != n:
            raise ValueError('length of %s is not equal to %d' % (str(attr), n))
    else:
        raise ValueError('%s is not iterable!' % str(attr))

