import collections
import copy

from Story import Story
from Operation import Operation


def main():
    op_list = [Operation('r', 1, 'x'), Operation('w', 1, 'y'), Operation('r', 2, 'y'), Operation('c', 1, None),
               Operation('c', 2, None), Operation('W', 2, 'x')]

    copy_list = op_list.copy()
    print('op_list:', op_list)
    print()
    print('copy_list:', copy_list)

    op_list.pop()
    print()
    print()
    print('op_list:', op_list)
    print()
    print('copy_list:', copy_list)
    print()
    print(collections.Counter(op_list) == collections.Counter(copy_list))

    # hist = Story(8, 2, 2, False, 'SAC')
    # for operation in hist.operations:
    #     print(operation.show(), end=" ")
    #
    # hist.clear_story()
    # print("\n", end="\n")
    # print("Cleared story lenght: ", len(hist.operations))
    #
    # hist = Story(20, 3, 3, False, 'SAC')
    # op_list = [Operation('r', 1, 'x'), Operation('w', 1, 'y'), Operation('r', 2, 'y'), Operation('c', 1, None), Operation('W', 2, 'x'), Operation('c', 2, None)]
    # hist.create_story(op_list)
    # print(hist.check_conflict())
    # op_list = [Operation('r', 1, 'x'), Operation('w', 2, 'y'), Operation('r', 1, 'y'), Operation('w', 1, 'x'), Operation('c', 1, None), Operation('r', 2, 'x'), Operation('W', 2, 'x'), Operation('c', 2, None)]
    # hist.create_story(op_list)
    #
    # for operation in hist.operations:
    #     print(operation.show(), end=" ")
    #
    # print("\n", end="\n")
    # print("Refulled story lenght: ", len(hist.operations))
    # print("Refulled story vars: ", hist.var_nb)
    # print("Refulled story trans: ", hist.trans_nb)

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


if __name__ == '__main__':
    main()
