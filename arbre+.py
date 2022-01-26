# for demo test

from BPlusTree import BPlusTree


def main():
    bplustree = BPlusTree()

    input("")
    random_list = bplustree.generateNumber(1, 30)

    for i in random_list:
        bplustree[i] = 'test' + str(i)
        print('Insert ' + str(i))
        bplustree.show()

    # print(list_element)
    # random.shuffle(random_list)
    # for i in random_list:
    # print('Delete ' + str(i))
    # bplustree.delete(i)
    # bplustree.show()


if __name__ == '__main__':
    main()
