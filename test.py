import random
from typing import List

import numpy as np


class Operation(object):
    def __init__(self, op_type, trans_number, var=None):
        self.op_type = op_type
        self.trans_number = trans_number
        self.var = var

    def show(self):
        name = self.op_type + str(self.trans_number) + "(" + str(
            self.var) + ")" if self.op_type != 'c' else self.op_type + str(self.trans_number)
        return name


class History:
    def __init__(self, nb_op, nb_var, nb_trans, serializable=False, type_histoire="SAC"):
        self.trans_nb = nb_trans
        self.operations: List[Operation] = []
        self.__generate__(nb_op, nb_var, nb_trans, serializable, type_histoire)

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
                d_r,_,__ =self.dirty_read()
                d_w,_,__ = self.dirty_write()
                if type_histoire == "S":
                    
                    if d_r or d_w:
                        self.operations.pop()
                    else :
                       i += 1  
                elif type_histoire == "R":
                    if d_w:
                        self.operations.pop()
                    else :
                       i += 1
                else:
                    i += 1
        # print("Story generated")
        return self.operations

    def reorganise(self):
        print(end="\n")
        # print("Start reorganizer")
        doneTrans = []

        while len(doneTrans) < self.trans_nb:
            c_index = next((ope_index for ope_index, ope in enumerate(self.operations)
                            if (ope.op_type == "c" and ope.trans_number not in doneTrans)), -1)

            # for ___o in self.operations:
            #     print(___o.show(), end=" ")
            # print(c_index)

            if c_index != -1:
                current_transaction = self.operations[c_index].trans_number
                doneTrans.append(current_transaction)

                last_op_index = next(inde for inde in range(len(self.operations) - 1, -1, -1)
                                     if self.operations[inde].trans_number == current_transaction)

                if last_op_index > c_index:
                    self.operations[last_op_index], self.operations[c_index] = self.operations[c_index], \
                                                                               self.operations[last_op_index]

    def check_conflict(self):
        # conflict_list = []
        mat = np.zeros((self.trans_nb, self.trans_nb))
        for ind, elem in enumerate(self.operations):
            if elem.op_type != "c":
                __op = elem
                for j in range(ind + 1, len(self.operations)):
                    __op__ = self.operations[j]
                    if __op.var == __op__.var:
                        if __op.trans_number != __op__.trans_number:
                            if __op.op_type == "w" or __op__.op_type == "w":
                                # conflict_list.append((__op, ind, __op__, j))
                                mat[__op.trans_number - 1][__op__.trans_number - 1] = 1
        # print("Conflicts checked")
        return mat
        # return conflict_list, mat

    def exist_path(self, matrice_adj, u, v):
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
                    # print("Path checked")
                    return True
        # print("Path checked")
        return False

    # def estCycle(self, matrice_adj):
    #     n = len(matrice_adj)
    #     for index in range(n):
    #         if self.exist_path(matrice_adj, index, index):
    #             return True
    #         return False

    def estCycle(self, matriceAdj):
        n = len(matriceAdj)
        compte_cycle = 0

        for i in range(n):
            if self.exist_path(matriceAdj, i, i):
                compte_cycle += 1

        if compte_cycle > n - 1:
            print("Histoire cyclique.")
            return True

        print("Histoire acyclique")
        return False
    
    
    def dirty_read(self):
            
        for i, op in enumerate(self.operations):
            if op.op_type == 'w':
                num = op.trans_number
                for j in range(i+1,len(self.operations)):
                    if self.operations[j].op_type == 'r' and  op.var == self.operations[j].var and num != self.operations[j].trans_number :
                        return True, num, self.operations[j].trans_number
        return False, None, None
    
    def dirty_write(self):
        for i, op in enumerate(self.operations):
            if  op.op_type == 'w'  :
                num = op.trans_number
                for j in range(i+1,len(self.operations)):
                    if self.operations[j].op_type == 'w' and  op.var == self.operations[j].var and num != self.operations[j].trans_number:
                        return True, num, self.operations[j].trans_number
        return False, None, None

    def valid_lecture(self, first_trans, second_trans):
        print("first_trans:",first_trans)
        print("second_trans:",second_trans)
        
        first_index = [x for x in range(len(self.operations)) if self.operations[x].op_type == 'c'and self.operations[x].trans_number == first_trans]
        #first_index = next(x for x, o in enumerate(self.operations) if( o.op_type == "c" and o.trans_number == first_trans))
        print("first_index:",first_index)
        second_index =  [x for x in range(len(self.operations)) if self.operations[x].op_type == 'c'and self.operations[x].trans_number == second_trans]
        #second_index = next(x for x, o in enumerate(self.operations) if (o.op_type == "c" and o.trans_number == second_trans))
        print("second_index:",second_index)

        if first_index[0] < second_index[0]: #lecture validée avant ecriture
            return True
        return False


    def __generate__(self, nb_op, nb_var, nb_trans, serialize=False, type_histoire="SAC"):
        s = 0
        while s < nb_trans:
            self.generate_hist(nb_op, nb_var, nb_trans,type_histoire)
            s = sum(1 for x in self.operations if x.op_type == "c")

        self.reorganise()
        if serialize:
            while self.estCycle(self.check_conflict()):
                s = 0
                while s < nb_trans:
                    self.generate_hist(nb_op, nb_var, nb_trans,type_histoire)
                    s = sum(1 for x in self.operations if x.op_type == "c")
                
                self.reorganise()
         
        if type_histoire == 'R':
            d_r,w,r =self.dirty_read()
            if d_r and not self.valid_lecture(r,w) :
                self.__generate__(nb_op, nb_var, nb_trans, serialize=False, type_histoire="R")
    # def generate_serealizable_history(self, hist):
    #     self.generate_hist(nb_op, nb_var, nb_trans)
    #     self.reorganise()
    #     # matrice_adj = self.check_conflict()
    #
    #     while self.estCycle(self.check_conflict()):
    #         self.generate_hist(nb_op, nb_var, nb_trans)
    #         self.reorganise()
    #         matrice_adj = self.check_conflict()


if __name__ == '__main__':
    
    hist = History(20, 3, 3, True, 'R')
    for operation in hist.operations:
        print(operation.show(), end=" ")

    # print()
    # print()
    # matriceAdj = hist.check_conflict()
    # print(matriceAdj)
    #
    # if hist.estCycle(matriceAdj):
    #     print("le graphe contient un cycle")
    # else:
    #     print("le graphe est acyclique")

    # for i, o in enumerate(conf):
    #     print(', '.join((x.show() if type(x) is Operation else str(x)) for x in o))
