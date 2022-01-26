import random


def generateNumber(fix_seed, max_elem):
    random.seed(fix_seed)
    list_element = []
    while len(list_element) < max_elem:
        nbr = random.randint(1, max_elem)
        if nbr not in list_element:
            list_element.append(nbr)
    return list_element


def askVals(text):
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
