# -*- coding:utf-8 -*-
'''
    处理化学方程式化学式等的模块.
'''
import re


class RxnEquation(object):
    """
    Class to create reaction equation object.
    """
    def __init__(self, rxn_equation):
        self.rxn_equation = rxn_equation

    def __repr__(self):
        return self.rxn_equation

    def __str__(self):
        return self.__repr__()

    def tolist(self):
        "Convert rxn_equation string to rxn_list(chem_state objects)."
        states_regex = re.compile(r'([^\<\>]*)(?:\<?\-\>)' +
                                  r'(?:([^\<\>]*)(?:\<?\-\>))?([^\<\>]*)')
        m = states_regex.search(self.rxn_equation)
        state_list = []
        for idx in range(1, 4):
            if m.group(idx):
                chem_state_obj = ChemState(m.group(idx).strip())
                state_list.append(chem_state_obj)

        return state_list

    def texen(self):
        state_list = self.tolist()
        tex_list = [state_obj.texen() for state_obj in state_list]

        if len(tex_list) == 3:
            tex_str = tex_list[0] + r' \leftrightarrow ' + tex_list[1] + \
                      r' \rightarrow ' + tex_list[-1]
        elif len(tex_list) == 2:
            tex_str = tex_list[0] + r' \rightarrow ' + tex_list[-1]

        return tex_str


class ChemState(object):
    """
    Class to generate chemical state object.
    """
    def __init__(self, chem_state):
        self.chem_state = chem_state
        self.sp_list = [sp.strip() for sp in chem_state.split('+')]

    def texen(self):
        "Get tex string."
        first_sp = ChemFormula(self.sp_list[0])
        tex_str = first_sp.texen()
        for sp in self.sp_list[1:]:
            tex_str += r' + ' + ChemFormula(sp).texen()

        return tex_str

    def __repr__(self):
        return self.chem_state

    def __str__(self):
        return self.__repr__()


class ChemFormulaError(Exception):
    "Exception raised for errors in the chemical formula."
    pass


class ChemFormula(object):
    """
    Class to generate chemical formula object.
    """
    def __init__(self, formula):
        self.formula = formula
        self.formula_regex = re.compile(r'(\d*)([\w\*]*)_(\d*)([a-z\*]+)')
        self.sp_regex = re.compile(r'([a-zA-Z\*])(\d*)')

        self.stoich, self.species, self.nsite, self.site =\
            self.split()

    def __repr__(self):
        return self.formula

    def __str__(self):
        return self.__repr__()

    def split(self):
        """
        Split whole formual to
        stoichiometry, species name, site number, site name.
        """
        m = self.formula_regex.search(self.formula)
        if not m:
            raise ChemFormulaError('Unexpected chemical formula: %s' %
                                   self.formula)
        else:
            stoich = int(m.group(1)) if m.group(1) else 1
            species = m.group(2)
            site = m.group(4)
            nsite = int(m.group(3)) if m.group(3) else 1
            return stoich, species, nsite, site

    def split_species(self):
        return self.sp_regex.findall(self.species)

    def texen(self):
        "Return tex format formula."
        tex_str = r''
        tex_str += str(self.stoich) if self.stoich != 1 else ''
        splited_tuples = self.split_species()
        for element, n in splited_tuples:
            if n:
                tex_str += element + r'_{' + n + r'}'
            else:
                tex_str += element
        tex_str += r'(' + self.site + r')'

        return tex_str

    def __add__(self, formula_inst):
        chem_state = self.formula + ' + ' + formula_inst.formula
        return ChemState(chem_state)
