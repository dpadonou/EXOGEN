
# for demo test

from BPlusTree import BPlusTree
from Leaf import Leaf
from Node import Node
def main():
    bplustree = BPlusTree()

    random_list = bplustree.generateNumber(2)


    print()
    print()
    for i in random_list:
        bplustree[i] = str(i)
        #print('Insert ' + str(i))
        
    bplustree.show()
    graph_yml = open('graph.yml', 'w')
    bplustree.show_yaml(file=graph_yml)
    graph_yml.close()

    
    #print(list_element)
    #random.shuffle(random_list)
    #for i in random_list:
        #print('Delete ' + str(i))
       # bplustree.delete(i)
       # bplustree.show()

    
    val = 22
    print()
    print()
    #print(bplustree.root.values[1].values[2].keys)
    #print(len(bplustree.root.keys))
    print()
    cpt,node= bplustree.search( val)
    if node == None:
        cpt=0
    ok, cpteur, leaves = bplustree.search_range(8,16)
    print(node)
    print(cpt)
    print()
    for leaf in leaves:
        print(leaf.keys)
    
    #print(cpt)
    #if val in node.keys:
       # for i in node.parent.keys:
          # print(i)
       
    
  
if __name__ == '__main__':
    main()