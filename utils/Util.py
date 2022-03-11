import os
import random
from typing import List


def generate_number(fix_seed, max_elem):
    random.seed(fix_seed)
    list_element: List[int] = []
    while len(list_element) < max_elem:
        nbr = random.randint(1, max_elem)
        if nbr not in list_element:
            list_element.append(nbr)
    return list_element


def ask_vals(text):
    val = input(text + ": ")
    ok = False
    while not ok:
        try:
            int_val = int(val)
            ok = True
        except ValueError:
            val = input(text + ": ")
        else:
            return int_val


def generate_image():
    os.system('cmd /c "python ./export/btree.py ./export/graph.yml | dot -Tsvg > ./export/graph.svg"')


def askOption():
    input("Mettre l'élément médian dans le fils gauche (O/N) ? default (O): ")
