import random
from typing import List

from Leaf import Leaf
from Node import Node
from Node import fusions
from Node import parent_fusions
from Node import parent_splits
from Node import splits


class BPlusTree(object):
    """ Un objet B+ constitué de Noeuds
    Un noeud est automatiquement divisé en deux dès qu'il est rempli (Nombre d'éléments supérieur à maximum). 
    Quand un découpage se produit, on envoie l'élément du milieu vers le haut (dans le noeud parent) pour servir de pivot.

    Returns:
         maximum (int): Le nombre maximum d'éléments que chaque Noeud peut comporter.
    """
    root: Node

    def __init__(self, maximum=4):
        self.root = Leaf()
        self.maximum: int = maximum if maximum > 2 else 2
        self.minimum: int = self.maximum // 2
        self.depth = 0

    """ retrouver une feuille
        Retourne:
        Leaf: la feuille qui comtient la clé (key)
    """

    def find(self, key) -> Leaf:
        node = self.root

        # Parcours l'arbre jusqu'à retrouver la clé.
        while type(node) is not Leaf:
            node = node[key]

        return node

    def __getitem__(self, item):
        return self.find(item)[item]

    def query(self, key):
        """ retourne une valeur pour la clé donnée et rien si la clé n'existe pas"""
        leaf = self.find(key)
        return leaf[key] if key in leaf.keys else None

    def change(self, key, value):
        """change la valeur
        Returns:
         (bool,Leaf): la feuille où se trouve la clé, retourne false si la clé n'existe pas 
        """
        leaf = self.find(key)
        if key not in leaf.keys:
            return False, leaf
        else:
            leaf[key] = value
            return True, leaf

    def __setitem__(self, key, value, leaf=None):
        """Insère une paire clé-valeur après avoir traversé un nœud feuille. Si le noeud feuille est plein, divise
            le nœud de feuille en deux
            """
        if leaf is None:
            leaf = self.find(key)
        leaf[key] = value
        if len(leaf.keys) > self.maximum:
            self.insert_index(*leaf.split())

    def generateNumber(self, fix_seed, max_elem):
        random.seed(fix_seed)
        list_element = []
        while len(list_element) < max_elem:
            nbr = random.randint(1, max_elem)
            if nbr not in list_element:
                list_element.append(nbr)
        return list_element

    def insert(self, key, value):
        """
        Returns:
        (bool,Leaf): la feuille où la clé est insérée. Retourne False si la même clé existe déjà.
        """
        leaf = self.find(key)
        if key in leaf.keys:
            return False, leaf
        else:
            self.__setitem__(key, value, leaf)
            return True, leaf

    def insert_index(self, key, values: List[Node]):
        """Pour un nœud parent et un nœud enfant,
         Insérez les valeurs de l'enfant dans les valeurs du parent."""
        parent = values[1].parent
        if parent is None:
            values[0].parent = values[1].parent = self.root = Node()
            self.depth += 1
            self.root.keys = [key]
            self.root.values = values
            return

        parent[key] = values
        # Si le noeud est plein, diviser le noeud en deux
        if len(parent.keys) > self.maximum:
            self.insert_index(*parent.split())
        # Après division, un noeud feuille est composé d'un noeud interne et de deux noeuds feuilles
        # Une réinsertion dans l'arbre est nécessaire

    def delete(self, key, node: Node = None):
        if node is None:
            node = self.find(key)
        del node[key]

        if len(node.keys) < self.minimum:
            if node == self.root:
                if len(self.root.keys) == 0 and len(self.root.values) > 0:
                    self.root = self.root.values[0]
                    self.root.parent = None
                    self.depth -= 1
                return

            elif not node.borrow_key(self.minimum):
                node.fusion()
                self.delete(key, node.parent)
        # Change the left-most key in node
        # if i == 0:
        #     node = self
        #     while i == 0:
        #         if node.parent is None:
        #             if len(node.keys) > 0 and node.keys[0] == key:
        #                 node.keys[0] = self.keys[0]
        #             return
        #         node = node.parent
        #         i = node.index(key)
        #
        #     node.keys[i - 1] = self.keys[0]

    def show(self, node=None, file=None, _prefix="", _last=True):
        """Afficher les éléments de chaque niveau"""
        if node is None:
            node = self.root
        print(_prefix, "`- " if _last else "|- ", node.keys, sep="", file=file)
        _prefix += "   " if _last else "|  "

        if type(node) is Node:
            # Affiche récursivement les éléments des noeuds enfant (s'ils existent).
            for i, child in enumerate(node.values):
                _last = (i == len(node.values) - 1)
                self.show(child, file, _prefix, _last)

    def output(self):
        return splits, parent_splits, fusions, parent_fusions, self.depth

    def readfile(self, reader):
        i = 0
        for i, line in enumerate(reader):
            s = line.decode().split(maxsplit=1)
            self[s[0]] = s[1]
            if i % 1000 == 0:
                print('Insert ' + str(i) + 'items')
        return i + 1

    def leftmost_leaf(self) -> Leaf:
        node = self.root
        while type(node) is not Leaf:
            node = node.values[0]
        return node
