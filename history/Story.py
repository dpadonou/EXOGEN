import random
from typing import List

import numpy as np

from history.Operation import Operation


class Story:
    def __init__(self, nb_op, nb_var, nb_trans, serializable = False, type_histoire = "SAC"):
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

    def create_story(self, ops = None):
        if ops is None:
            ops = []
            self.trans_nb = 0
            self.op_nb = 0
            self.var_nb = 0
        # trans_ = elmts(dict.fromkeys([ope.trans_number for ope_index, ope in enumerate(ops)]))
        # vars_ = elmts(dict.fromkeys([ope.var for ope_index, ope in enumerate(ops) if ope.var is not None]))
        self.operations = ops
        self.op_nb = len(ops)
        self.var_nb = len(list(dict.fromkeys([ope.var for ope_index, ope in enumerate(ops) if ope.var is not None])))
        self.trans_nb = len(list(dict.fromkeys([ope.trans_number for ope_index, ope in enumerate(ops)])))

    def generate_hist(self, nb_op, nb_var, nb_trans, type_histoire):
        """la génération d'histoire n'est rien d'autre que de créer plusieur objet operation est les ajouter 
        à la liste d'opération

        Args:
            nb_op (int): Donne le nombre d'opération qu'on veut avoir dans l'histoire générée
            nb_var (int): Donne le nombre de variable sur lesquelles les transactions vont se faire (on peut en avoir 6
            mais pour plus de variable il faudra ajouter des variable dans le tableau de variable en bas)
            nb_trans (int): Donne le nombre de transaction qu'on veut avoir dans l'histoire générée
            type_histoire (string): Des caractères pour designer le type de l'histoire qu'on veut. Par defaut on a 
            <<SAC>> pour sans annulation en cascade, <<S>> pour Stricte et <<NR>> pour non recouvrable 

        Returns:
            List[Operation]: La liste d'operation qu'on a créé 
        """

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
                d_r, _, __ = self.dirty_read(self.operations)
                d_w, _, __ = self.dirty_write(self.operations)
                if type_histoire == "S":

                    if d_r or d_w:
                        self.operations.pop()
                    else:
                        i += 1
                elif type_histoire == "NR":
                    if d_w:
                        self.operations.pop()
                    else:
                        i += 1
                else:
                    i += 1
        return self.operations

    def reorganise(self):
        """Cette fonction permet de réorganiser l'histoire de sorte à ce qu'après le commit relative à une transaction, 
        il n'y ait pas d'opération de cette transaction
        """
        print(end = "\n")
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
                    self.operations[last_op_index], self.operations[c_index] = self.operations[c_index], \
                                                                               self.operations[last_op_index]

    def check_conflict(self, data):
        """Cette fonction permet de vérifier s'il y a un conflit entre les transaction.
        Deux transactions sont en conflits si l'une lis une variable dans laquelle une autre écrit ou inversemment ou encore
        s'il y a deux ecriture par des transactions différentes sur la même variable

        Returns:
            int[][]: Une matrice d'adjascence qui ajoute 1 quand une transaction est en conflit avec une autre et 0 sinon
        """
        # conflict_list = []
        mat = np.zeros((self.trans_nb, self.trans_nb))
        for ind, elem in enumerate(data):
            if elem.op_type != "c":
                __op = elem
                for j in range(ind + 1, len(data)):
                    __op__ = data[j]
                    if __op.var == __op__.var:
                        if __op.trans_number != __op__.trans_number:
                            if __op.op_type == "w" or __op__.op_type == "w":
                                # conflict_list.append((__op, ind, __op__, j))
                                mat[__op.trans_number - 1][__op__.trans_number - 1] = 1
        return mat

    def exist_path(self, matrice_adj, u, v):
        """verifie dans la matrice d'adjascence s'il y a un chémin entre une transaction et une autre 
        par exemple il y a un chemin de la transaction 1 à la 2 si la matrice[1][2]=1 

        Args:
            matrice_adj (int): Est une matrice rempli de 1 et de 0
            u (int): est un numéro de transaction qui represente ici un sommet
            v (int): est un numéro de transaction qui represente ici un sommet

        Returns:
            Boolean: true s'il existe un chémin entre les deux transaction donnée sinon false
        """
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
        """Verifie s'il y a un cycle dans le graphe

        Args:
            matriceAdj (int): Est une matrice rempli de 1 et de 0

        Returns:
            Boolean: true s'il y a un cirle dans le graphe 
        """
        n = len(matriceAdj)
        compte_cycle = 0

        for i in range(n):
            if self.exist_path(matriceAdj, i, i):
                compte_cycle += 1

        if compte_cycle > n - 1:
            return True

        return False

    def dirty_read(self, data):
        """Verifie s'il y a une lecture sale

        Returns:
            Boolean: true s'il existe une lecture sale dans l'histooire false sinon
        """
        for i, op in enumerate(data):
            if op.op_type == 'w':
                num = op.trans_number
                for j in range(i + 1, len(data)):
                    if data[j].op_type == 'r' and op.var == data[j].var and num != data[j].trans_number:
                        return True, num, data[j].trans_number
        return False, None, None

    def dirty_write(self, data):
        """Verifie s'il y a une écriture sale

        Returns:
            Boolean: true s'il existe une écriture sale dans l'histooire false sinon
        """
        for i, op in enumerate(data):
            if op.op_type == 'w':
                num = op.trans_number
                for j in range(i + 1, len(data)):
                    if data[j].op_type == 'w' and op.var == data[j].var and num != data[j].trans_number:
                        return True, num, data[j].trans_number
        return False, None, None

    def verif_dirty_read(self, first_trans, second_trans):
        """Vérifie s'il existe une lecture sale entre les deux transactions en parametre

        Args:
            first_trans (int): numéro de la prémiere transaction celle qui fait l'ecriture
            second_trans (int): numéro de la seconde transaction celle qui fait la lecture sale

        Returns:
            Boolean: true s'il y a une lecture sale entre les deux sinon false
        """
        for op in self.operations:
            if op.op_type == 'w' and op.trans_number == first_trans:
                for j in self.operations:
                    if j.op_type == 'r' and op.var == j.var and second_trans == j.trans_number:
                        return True
        return False

    def valid_lecture(self, first_trans, second_trans):
        """Quand il y a une lecture sale mais pas de écriture sale, on vérifie que la transaction ayant fait la lecture
        sale, soit commitée avant celle ayant fait l'écriture

        Args:
            first_trans (int): numéro de la premiere transaction
            second_trans (int): numéro de la seconde transaction

        Returns:
            Boolean: true si lecture est validée avant écriture 
        """

        first_index = [x for x in range(len(self.operations)) if
                       self.operations[x].op_type == 'c' and self.operations[x].trans_number == first_trans]

        second_index = [x for x in range(len(self.operations)) if
                        self.operations[x].op_type == 'c' and self.operations[x].trans_number == second_trans]

        if first_index[0] < second_index[0]:  # lecture validée avant ecriture
            return True
        return False

    def __generate__(self, nb_op, nb_var, nb_trans, serialize, type_histoire):
        """ cette fonction permet de généré une histoire correcte au sens de ce nous voulons avoir en fonction des parametre 
        définis. l'histoire est régénéré jusqu 'à obtenir ce que l'on veut

        Args:
            nb_op (int): nombre d'operation
            nb_var (int): nombre de variable
            nb_trans (int): nombre de transaction
            serialize (bool, optional): true pour signifier qu'on veut une histoire sérialisable sinon false . Defaults to False.
            type_histoire (str, optional): pour signifier le type d'opération. Defaults to "SAC".
        """
        s = 0
        while s < nb_trans:
            self.generate_hist(nb_op, nb_var, nb_trans, type_histoire)
            s = sum(1 for x in self.operations if x.op_type == "c")

        self.reorganise()
        if serialize:
            while self.estCycle(self.check_conflict(self.operations)):
                s = 0
                while s < nb_trans:
                    self.generate_hist(nb_op, nb_var, nb_trans, type_histoire)
                    s = sum(1 for x in self.operations if x.op_type == "c")

                self.reorganise()

        if type_histoire == 'NR':
            cpt = 0
            cpt_dirty_read = 0
            for i in range(1, nb_trans + 1):

                for j in range(1, nb_trans + 1):

                    if i != j:
                        if self.verif_dirty_read(i, j):
                            cpt_dirty_read += 1
                            if not self.valid_lecture(j, i):
                                cpt += 1

            if cpt != 0 or cpt_dirty_read == 0:
                self.__generate__(nb_op, nb_var, nb_trans, serialize = False, type_histoire = "NR")

    def is_serializable(self):
        return not self.estCycle(self.check_conflict(self.operations))

    def exist_trans(self, i, tableau):

        for j in range(len(tableau)):

            if i.var == tableau[j][1]:

                if i.trans_number != tableau[j][0]:
                    return True
        return False

    def blocked_trans(self, i, attente: List[Operation]):

        # print(attente)
        if attente:
            for j in range(len(attente)):
                if i.trans_number == attente[j].trans_number and attente[j].op_type != "c":
                    return True
        return False

    def pop_element(self, i, tab):
        return list(filter(lambda x: x[0] != i.trans_number, tab))

    def add_in_list(self, i, __verrou, attente, _verrou, solution):
        if __verrou:
            if self.exist_trans(i, __verrou) or self.blocked_trans(i, attente):
                attente.append(i)
            else:
                _verrou.append((i.trans_number, i.var))
                solution.append(i)
        elif _verrou:

            if self.exist_trans(i, _verrou) or self.blocked_trans(i, attente):
                attente.append(i)
            else:
                _verrou.append((i.trans_number, i.var))
                solution.append(i)
        else:
            _verrou.append((i.trans_number, i.var))
            solution.append(i)
        return __verrou, attente, _verrou, solution

    def deplace(self, element, __verrou, solution, _verrou):

        _verrou.append((element.trans_number, element.var))
        solution.append(element)

        return __verrou, solution, _verrou

    def numTransBlock(self, i, tableau):
        for j in range(len(tableau)):

            if i.var == tableau[j][1]:

                if i.trans_number != tableau[j][0]:
                    return True, i.trans_number, tableau[j][0]
        return False, 0, 0

    def inter_bloc(self, trans_bloc):
        for i in range(len(trans_bloc)):
            for j in range(len(trans_bloc)):
                if i != j and trans_bloc[i][0] and trans_bloc[j][0]:
                    if trans_bloc[i][1] == trans_bloc[j][2] and trans_bloc[i][2] == trans_bloc[j][1]:
                        return True
        return False

    def vide_attente(self, __verrou, _attente, _verrou, solution):
        __attente = []
        trans_bloc = []
        __attente = _attente.copy()
        while _attente:

            for i in range(len(_attente)):
                print("type", _attente[i].op_type, "var", _attente[i].var, "num", _attente[i].trans_number)
                if _attente[i].op_type == "r":

                    if __verrou:
                        # print("bloque r")
                        trans_bloc.append(self.numTransBlock(_attente[i], __verrou))
                        if not self.exist_trans(_attente[i], __verrou):
                            __verrou, solution, _verrou = self.deplace(_attente[i], __verrou, solution, _verrou)
                            __attente.remove(_attente[i])
                    else:
                        __verrou, solution, _verrou = self.deplace(_attente[i], __verrou, solution, _verrou)
                        __attente.remove(_attente[i])
                elif _attente[i].op_type == "w":

                    if _verrou:

                        trans_bloc.append(self.numTransBlock(_attente[i], _verrou))
                        if not self.exist_trans(_attente[i], _verrou):
                            _verrou, solution, __verrou = self.deplace(_attente[i], _verrou, solution, __verrou)
                            __attente.remove(_attente[i])
                    else:

                        _verrou, solution, __verrou = self.deplace(_attente[i], _verrou, solution, __verrou)
                        __attente.remove(_attente[i])
                else:

                    if not self.blocked_trans(_attente[i], __attente):
                        solution.append(_attente[i])
                        __verrou = self.pop_element(_attente[i], __verrou)
                        _verrou = self.pop_element(_attente[i], _verrou)
                        __attente.remove(_attente[i])

            if self.inter_bloc(trans_bloc):
                return __verrou, __attente, _verrou, solution

            _attente = __attente.copy()

        return __verrou, __attente, _verrou, solution

    def check_inter_bloc(self, _attente):
        if self.verify_nb_trans_blocked(_attente):
            return True
        return False

    def verify_nb_trans_blocked(self, data: list[Operation]):
        cpt = 0
        for i in data:
            if i.op_type == 'c':
                cpt += 1
        if cpt == self.trans_nb:
            return True
        return False

    def solve_history(self):
        """
        une file d'attente pour les transaction en attentes
        un tableau pour le resultat apres toutes les calculs
        un verrou
        savoir quand il faut verrouiller:
        -le verrou est partagé seulement en lecture
        -si une variable est vérrouillée en lecture toutes ecritures qui suivront sur cette variable seront en attente
        -si une variable est vérrouillée en ecriture alors toutes les autres ecriture sur cette variables seront en attente
        -si une variable est vérrouillée en ecriture alors toutes les autres lecture sur cette variables seront en attente

        """
        solution: List[Operation] = []
        attente: List[Operation] = []
        verrou_lecture = []
        verrou_ecriture = []
        list_attente = []

        for i in range(len(self.operations)):
            if self.operations[i].op_type == "r":
                verrou_ecriture, attente, verrou_lecture, solution = self.add_in_list(self.operations[i],
                                                                                      verrou_ecriture, attente,
                                                                                      verrou_lecture, solution)
            elif self.operations[i].op_type == "w":
                verrou_lecture, attente, verrou_ecriture, solution = self.add_in_list(self.operations[i],
                                                                                      verrou_lecture, attente,
                                                                                      verrou_ecriture, solution)
            else:
                if self.blocked_trans(self.operations[i], attente):
                    attente.append(self.operations[i])

                else:
                    solution.append(self.operations[i])
                    verrou_ecriture = self.pop_element(self.operations[i], verrou_ecriture)
                    verrou_lecture = self.pop_element(self.operations[i], verrou_lecture)
        if self.check_inter_bloc(attente):
            return solution, attente

        verrou_ecriture, list_attente, verrou_lecture, solution = self.vide_attente(verrou_ecriture, attente,
                                                                                    verrou_lecture, solution)
        return solution, list_attente

    def is_strict(self, data: list[Operation]):
        for i, op in enumerate(data):
            if op.op_type == 'w':
                num = op.trans_number
                for j in range(i + 1, len(data)):
                    ok, _num, __num = self.dirty_r_w(op, data[j], num)
                    if ok:
                        if not self.valid_lecture(self, _num, __num):
                            return False
        return True

    def dirty_r_w(self, op: Operation, data: Operation, num):

        if data.op_type != 'c' and op.var == data.var and num != data.trans_number:
            return True, num, data.trans_number
        return False, None, None
