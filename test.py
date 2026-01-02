import re

# =========================
# Node class
# =========================
class Hnode:
    def __init__(self, key, item):
        self.key = key
        self.item = item
        self.parent = None
        self.right = None
        self.left = None

    def getKey(self):
        return self.key

    def getItem(self):
        return self.item

    def getRightChild(self):
        return self.right

    def getLeftChild(self):
        return self.left

    def getParent(self):
        return self.parent

    def hasRightChild(self):
        return self.right is not None

    def hasLeftChild(self):
        return self.left is not None

    def isRoot(self):
        return self.parent is None

    def isLeaf(self):
        return self.left is None and self.right is None

    def isRightChild(self):
        return self.parent and self.parent.right == self

    def isLeftChild(self):
        return self.parent and self.parent.left == self

    def setParent(self, p):
        self.parent = p

    def setKey(self, key):
        self.key = key

    def setItem(self, item):
        self.item = item

    def addRightChild(self, hnode):
        self.right = hnode
        hnode.setParent(self)

    def addLeftChild(self, hnode):
        self.left = hnode
        hnode.setParent(self)


# =========================
# Heap class
# =========================
class Heap:
    def __init__(self):
        self.root = None
        self.last = None
        self.size = 0

    def isEmpty(self):
        return self.size == 0

    def getSize(self):
        return self.size

    def getRoot(self):
        return self.root

    def getLast(self):
        return self.last

    def getHighestPriority(self):
        if self.root is None:
            return None
        return self.root.getKey()

    # -------------------------
    # downwardHeapify
    # -------------------------
    def downwardHeapify(self, current):
        while current.hasLeftChild():
            small = current.getLeftChild()

            if current.hasRightChild() and \
               current.getRightChild().getKey() < small.getKey():
                small = current.getRightChild()

            if small.getKey() < current.getKey():
                current.key, small.key = small.key, current.key
                current.item, small.item = small.item, current.item
                current = small
            else:
                break

    # -------------------------
    # upwardHeapify
    # -------------------------
    def upwardHeapify(self, current):
        while not current.isRoot():
            parent = current.getParent()
            if current.getKey() < parent.getKey():
                current.key, parent.key = parent.key, current.key
                current.item, parent.item = parent.item, current.item
                current = parent
            else:
                break

    # -------------------------
    # removeMin
    # -------------------------
    def removeMin(self):
        if self.isEmpty():
            print("The heap is empty and no entry can be removed")
            return None

        if self.size == 1:
            self.root = None
            self.last = None
            self.size = 0
            return

        # swap root and last
        self.root.key, self.last.key = self.last.key, self.root.key
        self.root.item, self.last.item = self.last.item, self.root.item

        # remove last node
        parent = self.last.getParent()
        if self.last.isLeftChild():
            parent.left = None
        else:
            parent.right = None

        self.size -= 1

        # update last
        bits = list(d2by(self.size))
        bits.reverse()
        cur = self.root
        for b in bits[1:]:
            if b == 0:
                cur = cur.left
            else:
                cur = cur.right
        self.last = cur

        self.downwardHeapify(self.root)

    # -------------------------
    # Insert
    # -------------------------
    def Insert(self, hnode):
        if self.isEmpty():
            self.root = hnode
            self.last = hnode
            self.size = 1
            return

        self.size += 1
        bits = list(d2by(self.size))
        bits.reverse()

        cur = self.root
        for b in bits[1:-1]:
            if b == 0:
                cur = cur.left
            else:
                cur = cur.right

        if bits[-1] == 0:
            cur.addLeftChild(hnode)
        else:
            cur.addRightChild(hnode)

        self.last = hnode
        self.upwardHeapify(hnode)

    # -------------------------
    # printHeapPreOrder
    # -------------------------
    def printHeapPreOrder(self, i):
        if i is None:
            return
        if i.isLeaf():
            print("Leaf [", i.getKey(), i.getItem(), "]")
        else:
            print("Node [", i.getKey(), i.getItem(), "]")
        self.printHeapPreOrder(i.getLeftChild())
        self.printHeapPreOrder(i.getRightChild())


# =========================
# decimal to binary (yield)
# =========================
def d2by(x):
    while x > 0:
        x, r = divmod(x, 2)
        yield r


# =========================
# Main function
# =========================
def HeapwithEntriesInserted():

    h = Heap()

    # ---- read input file ----
    with open("inFile.txt", "r") as f:
        for line in f:
            line = line.strip()
            if line == "":
                continue  # 跳過空白行
            parts = line.split()
            if len(parts) != 2:
                print(f"跳過格式錯誤的行: {line}")
                continue
            key, item = parts
            h.Insert(Hnode(int(key), item))

    print("Heap size=", h.getSize(), "The highest priority is", h.getHighestPriority())
    print("pre-order traversal:")
    h.printHeapPreOrder(h.getRoot())

    print("deleteMin")
    h.removeMin()

    print("deleteMin")
    h.removeMin()

    print("deleteMin")
    h.removeMin()

    print("deleteMin")
    h.removeMin()

    print("deleteMin")
    h.removeMin()

    print("insert 35, resume")
    h.Insert(Hnode(35, "resume"))

    print("insert 15, second")
    h.Insert(Hnode(15, "second"))

    print("insert 20, fourth")
    h.Insert(Hnode(20, "fourth"))

    print("Heap size=", h.getSize(), "The highest priority is", h.getHighestPriority())
    print("pre-order traversal:")
    h.printHeapPreOrder(h.getRoot())

    print("deleteMin")
    h.removeMin()

    print("insert 40, nineth")
    h.Insert(Hnode(40, "nineth"))


HeapwithEntriesInserted()
