# for demo test

from Tree import Tree
from utils.Util import askVals
from utils.Util import generateNumber


def main():
    tree = Tree()

    seedVal = askVals("Facteur de génération")
    maxNbr = askVals("Nombre d'éléments")
    random_list = generateNumber(seedVal, maxNbr)

    print("=================================== Generated values =====================================")
    print(random_list)
    input()

    print("================================== Generating B+ tree ====================================")

    for i in random_list:
        tree[i] = 'test' + str(i)
        #print('Insert ' + str(i))
    tree.show()

    # print(bplustree.root.values[1].values[2].keys)
    # print(len(bplustree.root.keys))

    # print()
    # cpt, node = tree.search(45)
    # print(node)
    # print(cpt)

    print()
    ok, cpt, leaves = tree.search_range(12, 37)
    print(ok)
    print(cpt)
    for leaf in leaves:
        print(leaf.keys)

    # print(list_element)
    # random.shuffle(random_list)
    # for i in random_list:
    # print('Delete ' + str(i))
    # bplustree.delete(i)
    # bplustree.show()


if __name__ == '__main__':
    main()
