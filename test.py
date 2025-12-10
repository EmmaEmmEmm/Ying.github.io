# Full implementation of HW4 polynomial linked-list operations

import re

class Node:
    def __init__(self, c, exp):
        self.coefficient = float(c)
        self.exponential = int(exp)
        self.next = None

    def getCoefficient(self):
        return self.coefficient

    def getExponential(self):
        return self.exponential

    def getNext(self):
        return self.next

    def setData(self, c, exp):
        self.coefficient = float(c)
        self.exponential = int(exp)

    def setCoefficient(self, c):
        self.coefficient = float(c)

    def setExponential(self, exp):
        self.exponential = int(exp)

    def setNext(self, newnext):
        self.next = newnext


class Poly_List:
    def __init__(self):
        self.head = None
        self.tail = None

    def isEmpty(self):
        return self.head is None

    def size(self):
        count = 0
        cur = self.head
        while cur:
            count += 1
            cur = cur.next
        return count

    def isHead(self, node):
        return node == self.head

    def isTail(self, node):
        return node == self.tail

    def getHead(self):
        return self.head

    def getTail(self):
        return self.tail

    def setHead(self, node):
        self.head = node

    def setTail(self, node):
        self.tail = node

    def polyDegree(self):
        if self.isEmpty():
            return -1
        return self.head.exponential

    def insertAfter(self, p, c, exp):
        newNode = Node(c, exp)
        newNode.next = p.next
        p.next = newNode
        if p == self.tail:
            self.tail = newNode

    def insertAtHead(self, c, exp):
        newNode = Node(c, exp)
        newNode.next = self.head
        self.head = newNode
        if self.tail is None:
            self.tail = newNode

    def insertAtTail(self, c, exp):
        newNode = Node(c, exp)
        if self.tail:
            self.tail.next = newNode
            self.tail = newNode
        else:
            self.head = self.tail = newNode

    def deleteAtHead(self):
        if self.head:
            self.head = self.head.next
            if self.head is None:
                self.tail = None

    def paddingPoly(self):
        if self.isEmpty():
            return
        cur = self.head
        while cur.next:
            if cur.exponential - 1 != cur.next.exponential:
                self.insertAfter(cur, 0, cur.exponential - 1)
            cur = cur.next

    def timeConst_liftDegree(self, m, d):
        cur = self.head
        while cur:
            cur.coefficient *= m
            cur.exponential += d
            cur = cur.next

    def copy(self):
        newList = Poly_List()
        cur = self.head
        while cur:
            newList.insertAtTail(cur.coefficient, cur.exponential)
            cur = cur.next
        return newList

    def printPoly_List(self):
        cur = self.head
        while cur:
            print(f"({cur.coefficient}, {cur.exponential}) -> ", end="")
            cur = cur.next
        print("None")

    def printPolynomial(self):
        if self.isEmpty():
            print("0")
            return
        cur = self.head
        out = ""
        while cur:
            c = cur.coefficient
            e = cur.exponential
            if c >= 0 and cur != self.head:
                out += "+"
            if e == 0:
                out += f"{c}"
            elif e == 1:
                out += f"{c}x"
            else:
                out += f"{c}x^{e}"
            cur = cur.next
        print(out)


def read_lines():
    with open("inFile.txt", "r") as f:
        return [line.strip() for line in f.readlines()]


def read_string(s):
    poly = Poly_List()
    # terms like +3x^2 -x +4
    terms = re.findall(r"[+-]?\d*x\^\d+|[+-]?\d*x|[+-]?\d+", s)

    for t in terms:
        if 'x' not in t:
            c = float(t)
            exp = 0
        else:
            # coefficient
            c = re.findall(r"[+-]?\d*", t)[0]
            if c in ('', '+', '-'):
                c = c + '1' if c != '' else '1'
            c = float(c)
            # exponent
            if '^' in t:
                exp = int(t.split('^')[1])
            else:
                exp = 1
        poly.insertAtTail(c, exp)

    return poly


# === Operations ===
def add(p1, p2):
    r = Poly_List()
    a = p1.copy().head
    b = p2.copy().head

    while a and b:
        if a.exponential == b.exponential:
            r.insertAtTail(a.coefficient + b.coefficient, a.exponential)
            a = a.next
            b = b.next
        elif a.exponential > b.exponential:
            r.insertAtTail(a.coefficient, a.exponential)
            a = a.next
        else:
            r.insertAtTail(b.coefficient, b.exponential)
            b = b.next

    while a:
        r.insertAtTail(a.coefficient, a.exponential)
        a = a.next
    while b:
        r.insertAtTail(b.coefficient, b.exponential)
        b = b.next

    return r, None


def substract(p1, p2):
    r = Poly_List()
    a = p1.copy().head
    b = p2.copy().head

    while a and b:
        if a.exponential == b.exponential:
            r.insertAtTail(a.coefficient - b.coefficient, a.exponential)
            a = a.next
            b = b.next
        elif a.exponential > b.exponential:
            r.insertAtTail(a.coefficient, a.exponential)
            a = a.next
        else:
            r.insertAtTail(-b.coefficient, b.exponential)
            b = b.next

    while a:
        r.insertAtTail(a.coefficient, a.exponential)
        a = a.next
    while b:
        r.insertAtTail(-b.coefficient, b.exponential)
        b = b.next

    return r, None


def multiply(p1, p2):
    r = Poly_List()
    a = p1.head

    while a:
        curPoly = Poly_List()
        b = p2.head
        while b:
            curPoly.insertAtTail(a.coefficient * b.coefficient, a.exponential + b.exponential)
            b = b.next
        r, _ = add(r, curPoly)
        a = a.next

    return r, None


def divide(p1, p2):
    dividend = p1.copy()
    divisor = p2.copy()
    quotient = Poly_List()

    while (not dividend.isEmpty()) and dividend.polyDegree() >= divisor.polyDegree():
        leadA = dividend.getHead()
        leadB = divisor.getHead()

        c = leadA.coefficient / leadB.coefficient
        exp = leadA.exponential - leadB.exponential

        quotient.insertAtTail(c, exp)

        temp = divisor.copy()
        temp.timeConst_liftDegree(c, exp)

        dividend, _ = substract(dividend, temp)
        while dividend.head and dividend.head.coefficient == 0:
            dividend.deleteAtHead()

    return quotient, dividend


def operation_selection(operation, poly1, poly2):
    switcher = {
        1: add,
        2: substract,
        3: multiply,
        4: divide,
    }
    func = switcher.get(operation, lambda: "nothing")
    return func(poly1, poly2)


def poly_operation():
    strings = read_lines()
    operation = int(strings[0])
    poly1 = read_string(strings[1])
    poly2 = read_string(strings[2])

    r1, r2 = operation_selection(operation, poly1, poly2)

    if operation == 4:
        print("The quotient is:", end="")
        r1.printPolynomial()
        print("The remainder is:", end="")
        r2.printPolynomial()
    else:
        print("The result is:", end="")
        r1.printPolynomial()
if __name__ == "__main__":
    poly_operation()