import random
from typing import List

import numpy as np

from history.Operation import Operation


class Story:
    def __init__(self, nb_op, nb_var, nb_trans, serializable=False, type_histoire="SAC"):
        self.trans_nb = nb_trans
        self.op_nb = nb_op
        self.var_nb = nb_var
        self.operations: List[Operation] = []
        self.__generate__(nb_op, nb_var, nb_trans, serializable, type_histoire)

    # """
    #
    # Getters and setters
    #
    # """
    #
    # # function to get value of nb_trans
    # def get_trans_nb(self):
    #     return self.trans_nb
    #
    # # function to set value of nb_trans
    # def set_trans_nb(self, trans_nb):
    #     self.trans_nb = trans_nb
    #
    # # function to delete trans_nb attribute
    # def del_trans_nb(self):
    #     del self.trans_nb
    #
    # trans_nb = property(get_trans_nb, set_trans_nb, del_trans_nb)
    #
    # # function to get value of nb_var
    # def get_nb_var(self):
    #     return self.nb_var
    #
    # # function to set value of nb_var
    # def set_nb_var(self, nb_var):
    #     self.nb_var = nb_var
    #
    # # function to delete nb_var attribute
    # def del_nb_var(self):
    #     del self.nb_var
    #
    # nb_var = property(get_nb_var, set_nb_var, del_nb_var)
    #
    # # function to get value of nb_op
    # def get_nb_op(self):
    #     return self.nb_op
    #
    # # function to set value of nb_op
    # def set_nb_op(self, nb_op):
    #     self.nb_op = nb_op
    #
    # # function to delete nb_op attribute
    # def del_nb_op(self):
    #     del self.nb_op
    #
    # nb_op = property(get_nb_op, set_nb_op, del_nb_op)
    #
    # """
    #
    #     End getters and setters
    #
    # """

    def clear_story(self):
        self.operations.clear()

    def create_story(self, ops=None):
        if ops is None:
            ops = []
            self.trans_nb = 0
            self.op_nb = 0
            self.var_nb = 0
        # trans_ = list(dict.fromkeys([ope.trans_number for ope_index, ope in enumerate(ops)]))
        # vars_ = list(dict.fromkeys([ope.var for ope_index, ope in enumerate(ops) if ope.var is not None]))
        self.operations = ops
        self.op_nb = len(ops)
        self.var_nb = len(list(dict.fromkeys([ope.var for ope_index, ope in enumerate(ops) if ope.var is not None])))
        self.trans_nb = len(list(dict.fromkeys([ope.trans_number for ope_index, ope in enumerate(ops)])))

    def generate_hist(self, nb_op, nb_var, nb_trans, type_histoire):
        self.operations.clear()

        variables = ["x", "y", "z", "t", "u", "v"]
        variable = variables[:nb_var]
        trans = []
        for _ in range(nb_trans):
            trans.append('c')
        trans.append('r')
        trans.append('w')

        i = 1
        while i <= nb_op:
            choice_op = random.choice(trans)
            choice_var = random.choice(variable)
            ri = random.randint(1, nb_trans)
            cpt = 0
            if choice_op == 'c':
                for j in self.operations:
                    if j.op_type == 'c' and j.trans_number == ri:
                        cpt += 1
                if cpt == 0:
                    if any(ri == _.trans_number for _ in self.operations):
                        self.operations.append(Operation(choice_op, ri))
                        i += 1
            else:
                self.operations.append(Operation(choice_op, ri, choice_var))
                d_r, _, __ = self.dirty_read()
                d_w, _, __ = self.dirty_write()
                if type_histoire == "S":

                    if d_r or d_w:
                        self.operations.pop()
                    else:
                        i += 1
                elif type_histoire == "R":
                    if d_w:
                        self.operations.pop()
                    else:
                        i += 1
                else:
                    i += 1
        return self.operations

    def reorganise(self):
        print(end="\n")
        doneTrans = []

        while len(doneTrans) < self.trans_nb:
            c_index = next((ope_index for ope_index, ope in enumerate(self.operations)
                            if (ope.op_type == "c" and ope.trans_number not in doneTrans)), -1)

            if c_index != -1:
                current_transaction = self.operations[c_index].trans_number
                doneTrans.append(current_transaction)

                last_op_index = next(inde for inde in range(len(self.operations) - 1, -1, -1)
                                     if self.operations[inde].trans_number == current_transaction)

                if last_op_index > c_index:
                    self.operations[last_op_index], self.operations[c_index] = self.operations[c_index], self.operations[last_op_index]

    def check_conflict(self):
        mat = np.zeros((self.trans_nb, self.trans_nb))
        for ind, elem in enumerate(self.operations):
            if elem.op_type != "c":
                __op = elem
                for j in range(ind + 1, len(self.operations)):
                    __op__ = self.operations[j]
                    if __op.var == __op__.var:
                        if __op.trans_number != __op__.trans_number:
                            if __op.op_type == "w" or __op__.op_type == "w":
                                mat[__op.trans_number - 1][__op__.trans_number - 1] = 1
        return mat

    @staticmethod
    def exist_path(matrice_adj, u, v):
        n = len(matrice_adj)  # nombre de sommets
        file = []
        visites = [False] * n
        file.append(u)
        while file:
            courant = file.pop(0)
            visites[courant] = True
            for t in range(n):
                if matrice_adj[courant][t] > 0 and not visites[t]:
                    file.append(t)
                    visites[t] = True
                elif matrice_adj[courant][t] > 0 and t == v:
                    return True
        return False

    def estCycle(self, matriceAdj):
        n = len(matriceAdj)
        compte_cycle = 0

        for i in range(n):
            if self.exist_path(matriceAdj, i, i):
                compte_cycle += 1

        if compte_cycle > n - 1:
            return True

        return False

    def dirty_read(self):
        for i, op in enumerate(self.operations):
            if op.op_type == 'w':
                num = op.trans_number
                for j in range(i + 1, len(self.operations)):
                    if self.operations[j].op_type == 'r' and op.var == self.operations[j].var and num != \
                            self.operations[j].trans_number:
                        return True, num, self.operations[j].trans_number
        return False, None, None

    def dirty_write(self):
        for i, op in enumerate(self.operations):
            if op.op_type == 'w':
                num = op.trans_number
                for j in range(i + 1, len(self.operations)):
                    if self.operations[j].op_type == 'w' and op.var == self.operations[j].var and num != \
                            self.operations[j].trans_number:
                        return True, num, self.operations[j].trans_number
        return False, None, None

    def valid_lecture(self, first_trans, second_trans):
        first_index = [x for x in range(len(self.operations)) if
                       self.operations[x].op_type == 'c' and self.operations[x].trans_number == first_trans]
        second_index = [x for x in range(len(self.operations)) if
                        self.operations[x].op_type == 'c' and self.operations[x].trans_number == second_trans]
        if first_index < second_index:  # lecture validée avant ecriture.
            return True
        return False

    def __generate__(self, nb_op, nb_var, nb_trans, serialize, type_histoire):
        s = 0
        while s < nb_trans:
            self.generate_hist(nb_op, nb_var, nb_trans, type_histoire)
            s = sum(1 for x in self.operations if x.op_type == "c")

        self.reorganise()
        if serialize:
            while self.estCycle(self.check_conflict()):
                s = 0
                while s < nb_trans:
                    self.generate_hist(nb_op, nb_var, nb_trans, type_histoire)
                    s = sum(1 for x in self.operations if x.op_type == "c")
                self.reorganise()
                if type_histoire == 'R':
                    d_r, w, r = self.dirty_read()
                    if d_r and not self.valid_lecture(r, w):
                        self.__generate__(nb_op, nb_var, nb_trans, serialize, type_histoire)

    def is_serializable(self):
        return not self.estCycle(self.check_conflict())
