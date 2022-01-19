import random  # for demo test

from BPlusTree import BPlusTree

def demo():
    bplustree = BPlusTree()
    # random module is imported
    random_list = []
    for i in range(20):
    # Any number can be used in place of '0'.
        random.seed(i)
        # Generated random number will be between 1 to 1000.
        random_list.append(random.randint(1, 50) )
    for i in random_list:
        bplustree[i] = 'test' + str(i)
        print('Insert ' + str(i))
        bplustree.show()

    #random.shuffle(random_list)
    #for i in random_list:
        #print('Delete ' + str(i))
       # bplustree.delete(i)
       # bplustree.show()


if __name__ == '__main__':
    demo()