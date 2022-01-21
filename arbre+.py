import random  
# for demo test

from BPlusTree import BPlusTree

def main():
    bplustree = BPlusTree()

    random_list = []
    for i in range(20):
        random.seed(i)
        # Générer un Nombre au hasard entre 1 à 50.
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
    main()