from operator import index
import random
from typing import List

import numpy as np


class Operation(object):
    def __init__(self, op_type, trans_number, var=None):
        self.op_type = op_type
        self.trans_number = trans_number
        self.var = var

    def show(self):
        name = self.op_type + str(self.trans_number) + "(" + str(self.var) + ")" if self.op_type != 'c' else self.op_type + str(self.trans_number)
        return name


class History:
    def __init__(self, nb_op, nb_var, nb_trans):
        self.trans_nb = nb_trans
        self.operations: List[Operation] = []
        self.generate_hist(nb_op, nb_var, nb_trans)

    def generate_hist(self, nb_op, nb_var, nb_trans):
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
                i += 1

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
        conflict_list = []
        a = np.zeros((self.trans_nb,self.trans_nb))
        for ind, elem in enumerate(self.operations):
            if elem.op_type != "c":
                __op = elem
                for j in range(ind + 1, len(self.operations)):
                    __op__ = self.operations[j]
                    if __op.var == __op__.var:
                        if __op.trans_number != __op__.trans_number:
                            if __op.op_type == "w" or __op__.op_type == "w":
                                conflict_list.append((__op, ind, __op__, j))
                                a[__op.trans_number-1][__op__.trans_number-1]=1
        return a

    def exist_chemin(self,matriceAdj, u, v):
        n = len(matriceAdj) # nombre de sommets
        file = []
        visites = [False] * n
        file.append(u)
        while file:
            courant = file.pop(0)
            visites[courant] = True
            for i in range(n):
                if matriceAdj[courant][i] > 0 and visites[i] == False:
                    file.append(i)
                    visites[i] = True
                elif matriceAdj[courant][i] > 0 and i == v:
                    return True
        return False

    def estCycle(self,matriceAdj):
        n = len(matriceAdj)
        
        compte_cycle=0
        for i in range(n):
            if self.exist_chemin(matriceAdj, i, i) == True:
                compte_cycle+=1
            
        if compte_cycle > n-1:
            return True
        
        return False
    
    def dirty_read(self,first_trans, second_trans):
        
        for i, op in enumerate(self.operations):
            if op.op_type == 'w' and op.trans_number == first_trans:
                for j in range(i+1,len(self.operations)):
                    if self.operations[j].op_type == 'r' and  op.var == self.operations[j].var and self.operations[j].trans_number == second_trans:
                        return True, first_trans, second_trans
        return False,first_trans, second_trans
    
    
    def dirty_write(self,first_trans, second_trans):
        for i, op in enumerate(self.operations):
            if  op.op_type == 'w' and op.trans_number == first_trans:
                for j in range(i+1,len(self.operations)):
                    if self.operations[j].op_type == 'w' and  op.var == self.operations[j].var and self.operations[j].trans_number == second_trans:
                        return True, first_trans, second_trans 
        return False,first_trans, second_trans
    
    def valid_lecture(self, first_trans, second_trans):
        first_index = [x for x in range(len(self.operations)) if self.operations[x].op_type == 'c'and self.operations[x].trans_number == first_trans]
        second_index =  [x for x in range(len(self.operations)) if self.operations[x].op_type == 'c'and self.operations[x].trans_number == second_trans]
        if first_index > second_index: #lecture validée avant ecriture
            return True
        return False
        
if __name__ == '__main__':
    hist = History(20, 3, 3)
    hist.reorganise()
    
    for operation in hist.operations:
        print(operation.show(), end=" ")

    print()
    print()
    matriceAdj = hist.check_conflict()
    print(matriceAdj)
    if hist.estCycle(matriceAdj) == True:
        print("le graphe contient un cycle")
    else:
        print("le graphe est acyclique")

    
    for i in range(1,4):
        for j in range(1,4):
            if i != j :
                ok  = hist.dirty_read(i,j)
                print('dirty read',ok)
                print('####################################################')
                write = hist.dirty_write(i,j)
                print('ecriture sale',write)
                print('####################################################')
   
        
    
   
    #for i, o in enumerate(conf):
      #  print(', '.join((x.show() if type(x) is Operation else str(x)) for x in o))
