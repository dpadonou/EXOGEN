
from Node import fusions
from Node import splits
from Node import Node
class Leaf(Node):
    def __init__(self, parent=None, prev_node=None, next_node=None):
        """
        Créer une nouvelle feuille
        :type prev_node: Leaf (Noeud gauche)
        :type next_node: Leaf (Noeud droite)
        """
        super(Leaf, self).__init__(parent)
        self.next: Leaf = next_node
        if next_node is not None:
            next_node.prev = self
        self.prev: Leaf = prev_node
        if prev_node is not None:
            prev_node.next = self

    def __getitem__(self, item):
        return self.values[self.keys.index(item)]

    def __setitem__(self, key, value):
        i = self.index(key)
        if key not in self.keys:
            self.keys[i:i] = [key]
            self.values[i:i] = [value]
        else:
            self.values[i - 1] = value

    def split(self):
        global splits
        splits += 1

        left = Leaf(self.parent, self.prev, self)
        mid = len(self.keys) // 2

        left.keys = self.keys[:mid+1]
        left.values = self.values[:mid+1]

        self.keys: list = self.keys[mid+1:]
        self.values: list = self.values[mid+1:]
        #print("splits-Leaf:", splits)

        
        # Lorsque le nœud feuille est divisé, définissez la clé parent à la clé la plus à gauche du nœud enfant droit.
        return left.keys[-1], [left, self]

    def __delitem__(self, key):
        i = self.keys.index(key)
        del self.keys[i]
        del self.values[i]

    def show(self):
        #if(key in self.keys):
        print(self.keys, self.next, self.prev)
        #print(self.keys, self.next, self.prev)
        
        
    def fusion(self):
        global fusions
        fusions += 1

        if self.next is not None and self.next.parent == self.parent:
            self.next.keys[0:0] = self.keys
            self.next.values[0:0] = self.values
        else:
            self.prev.keys += self.keys
            self.prev.values += self.values

        if self.next is not None:
            self.next.prev = self.prev
        if self.prev is not None:
            self.prev.next = self.next

    def borrow_key(self, minimum: int):
        index = self.parent.index(self.keys[0])
        if index < len(self.parent.keys) and len(self.next.keys) > minimum:
            self.keys += [self.next.keys.pop(0)]
            self.values += [self.next.values.pop(0)]
            self.parent.keys[index] = self.next.keys[0]
            return True
        elif index != 0 and len(self.prev.keys) > minimum:
            self.keys[0:0] = [self.prev.keys.pop()]
            self.values[0:0] = [self.prev.values.pop()]
            self.parent.keys[index - 1] = self.keys[0]
            return True

        return False