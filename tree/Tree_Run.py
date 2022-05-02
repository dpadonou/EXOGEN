from Tree import Tree
from utils.Util import ask_vals
from utils.Util import generate_image
from utils.Util import generate_number


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
    graph = open('../export/graph.txt', 'w')
    tree.show(file=graph)
    graph.close()

    print()
    print()
    graph_yml = open('../export/graph.yml', 'w')
    tree.show_yaml(file=graph_yml)
    graph_yml.close()

    generate_image()


if __name__ == '__main__':
    main()
