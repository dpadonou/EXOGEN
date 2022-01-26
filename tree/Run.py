# for demo test

from Tree import Tree
from util.Util import askVals
from util.Util import generateNumber


def main():
    tree = Tree()

    seedVal = askVals("Facteur de génération")
    maxNbr = askVals("Nombre d'éléments")

    print("================================== Generating B+ tree ====================================")

    random_list = generateNumber(seedVal, maxNbr)

    for i in random_list:
        tree[i] = 'test' + str(i)
        print('Insert ' + str(i))
        tree.show()

    # print(list_element)
    # random.shuffle(random_list)
    # for i in random_list:
    # print('Delete ' + str(i))
    # bplustree.delete(i)
    # bplustree.show()


if __name__ == '__main__':
    main()
