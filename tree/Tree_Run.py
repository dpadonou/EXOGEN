from Tree import Tree

from history.Operation import Operation
from utils.Util import ask_vals
from utils.Util import generate_image
from utils.Util import generate_number
from utils.Util import swap_elmts
from utils.Util import random_choice
from utils.Util import display


def main():
    # tree = Tree()
    #
    # seedVal = ask_vals("Facteur de génération")
    # maxNbr = ask_vals("Nombre d'éléments")
    # random_list = generate_number(seedVal, maxNbr)
    #
    # print("=================================== Generated values =====================================")
    # print(random_list)
    # input()
    # print("================================== Generating B+ tree ====================================")
    #
    # for i in random_list:
    #     tree[i] = 'test' + str(i)
    # graph = open('../export/graph.txt', 'w')
    # tree.show(file=graph)
    # graph.close()
    #
    # print()
    # print()
    # graph_yml = open('../export/graph.yml', 'w')
    # tree.show_yaml(file=graph_yml)
    # graph_yml.close()
    #
    # generate_image()

    # List = [23, 65, 19, 90, 23, 65, 19, 90]
    op_list = [Operation('r', 1, 'x'), Operation('w', 1, 'y'), Operation('r', 2, 'y'), Operation('c', 1, None), Operation('c', 2, None), Operation('W', 2, 'x')]

    # i1, i2 = random_choice(List)
    # print(i1, i2)
    #
    # print(List)
    # print(swap_elmts(List, i1, i2))

    print(display(op_list))


if __name__ == '__main__':
    main()
