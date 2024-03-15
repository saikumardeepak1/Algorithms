class BTreeNode:
    def __init__(self, t, leaf=False):
        self.t = t  # Minimum degree (defines the range for number of keys)
        self.keys = []  # An array of keys
        self.children = []  # An array of child pointers
        self.leaf = leaf  # Is true when node is leaf. Otherwise false

class BTree:
    def __init__(self, t):
        self.root = BTreeNode(t, True)
        self.t = t

    # Function to traverse the tree
    def traverse(self):
        if self.root:
            self._traverse(self.root)

    def _traverse(self, node):
        for i in range(len(node.keys)):
            if not node.leaf:
                self._traverse(node.children[i])
            print(node.keys[i], end=" ")
        if not node.leaf:
            self._traverse(node.children[len(node.keys)])

    # Function to search key in this tree
    def search(self, k):
        return self._search(self.root, k)

    def _search(self, node, k):
        i = 0
        while i < len(node.keys) and k > node.keys[i]:
            i += 1
        if i < len(node.keys) and node.keys[i] == k:
            return node
        if node.leaf:
            return None
        return self._search(node.children[i], k)

    # The main function that inserts a new key in this B-Tree
    def insert(self, k):
        root = self.root
        if len(root.keys) == 2 * self.t - 1:
            # If root is full, then tree grows in height
            s = BTreeNode(self.t, False)
            self.root = s
            s.children.insert(0, root)  # Former root becomes child of new root
            self._split_child(s, 0)  # Split the old root and move 1 key to the new root
            self._insert_non_full(s, k)  # New root has two children now. Insert new key
        else:
            self._insert_non_full(root, k)

    # A utility function to insert a new key in this node
    def _insert_non_full(self, node, k):
        i = len(node.keys) - 1
        if node.leaf:
            # If this is a leaf node
            node.keys.append(0)
            while i >= 0 and node.keys[i] > k:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = k
        else:
            # If this node is not leaf
            while i >= 0 and node.keys[i] > k:
                i -= 1
            if len(node.children[i + 1].keys) == 2 * self.t - 1:
                self._split_child(node, i + 1)
                if k > node.keys[i + 1]:
                    i += 1
            self._insert_non_full(node.children[i + 1], k)

    # A utility function to split the child y of this node
    def _split_child(self, node, i):
        t = self.t
        y = node.children[i]
        z = BTreeNode(t, y.leaf)
        z.keys = y.keys[t: (2 * t) - 1]
        y.keys = y.keys[0: t - 1]
        if not y.leaf:
            z.children = y.children[t: 2 * t]
            y.children = y.children[0: t]
        node.children.insert(i + 1, z)
        node.keys.insert(i, y.keys[t - 1])

# Example usage
b = BTree(3)  # A B-Tree with minimum degree 3
values = [10, 20, 5, 6, 12, 30, 7, 17]
for v in values:
    b.insert(v)

print("Traversal of the constructed B-tree is:")
b.traverse()
print("\nSearching for a value in the B-tree:")
node = b.search(6)
if node:
    print("Found")
else:
    print("Not Found")
