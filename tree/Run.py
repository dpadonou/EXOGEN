# for demo test

from Tree import Tree
from utils.Util import ask_vals
from utils.Util import generate_number
from utils.Util import generate_image


def main():
    tree = Tree()

    seedVal = ask_vals("Facteur de génération")
    maxNbr = ask_vals("Nombre d'éléments")
    random_list = generate_number(seedVal, maxNbr)

    print("=================================== Generated values =====================================")
    print(random_list)
    input()

    print("================================== Generating B+ tree ====================================")

    for i in random_list:
        tree[i] = 'test' + str(i)
        # print('Insert ' + str(operation))
    graph = open('../export/graph.txt', 'w')
    tree.show()
    graph.close()

    print()
    print()
    graph_yml = open('../export/graph.yml', 'w')
    tree.show_yaml(file=graph_yml)
    graph_yml.close()

    generate_image()

    # print(bplustree.root.values[1].values[2].keys)
    # print(len(bplustree.root.keys))

    # print()
    # node = tree.find(5)
    # print(node.keys)
    # cpt, leaves = tree.search(5)
    # print(leaves)

    # print()
    # ok, cpt, leaves = tree.search_range(12, 27)
    # print(ok)
    # print(cpt)
    # for leaf in leaves:
    #     print(leaf.keys)

    # print(list_element)
    # random.shuffle(random_list)
    # for operation in random_list:
    # print('Delete ' + str(operation))
    # bplustree.delete(operation)
    # bplustree.show()


if __name__ == '__main__':
    main()
