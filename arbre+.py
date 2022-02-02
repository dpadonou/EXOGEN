
# for demo test

from BPlusTree import BPlusTree
from Leaf import Leaf
from Node import Node
def main():
    bplustree = BPlusTree()

    random_list = bplustree.generateNumber(1)


    print()
    print()
    for i in random_list:
        bplustree[i] = 'test' + str(i)
        #print('Insert ' + str(i))
        
    bplustree.show()

    
    #print(list_element)
    #random.shuffle(random_list)
    #for i in random_list:
        #print('Delete ' + str(i))
       # bplustree.delete(i)
       # bplustree.show()

    
    val = 60
    print()
    print()
    #print(bplustree.root.values[1].values[2].keys)
    #print(len(bplustree.root.keys))
    print()
    cpt, node= bplustree.getNode( bplustree.root, val)
    print(node)
    print(cpt)
    #if val in node.keys:
       # for i in node.parent.keys:
          # print(i)
       
    
  
if __name__ == '__main__':
    main()