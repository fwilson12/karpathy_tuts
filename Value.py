from graphviz_helpers import render_graph

# float wrapper w/ history
class Value:

    def __init__(self, data, children=(), op='', label=''):
        self.data = data
        self.grad = 0.0
        self.children = set(children)
        self.op = op
        self.label = label

    def __repr__(self):
        return f"Value(label={self.label}, data={self.data:.4f})"

    def __add__(self, other):
        return Value(self.data + other.data, (self, other), '+')

    def __mul__(self, other):
        return Value(self.data * other.data, (self, other), '*')


import collections

def backprop(node):

    # w respect to itself 
    node.grad = 1.0

    # network graph
    kids = collections.deque()
    kids.append(node)
    
    while kids:
        # get current parent
        parent = kids.popleft() 
        h = .0001
        for child in parent.children:
            # then dParent/dChild = 1
            if parent.op == '+':
                child.grad = 1.0 * parent.grad

            # then find slope w/ respect to child
            elif parent.op == '*':
                # temporarily wiggle child's data to calculate f(child + h) - f(child) / h
                child.data += h
                # calculate f(child + h) by recalculating parent's value, probably inefficient though 
                parentF = 1
                for child in parent.children:
                    parentF *= child.data
                # RoC as a result of nudging child
                dP_dc = (parentF - parent.data)/h
                # by chain rule 
                child.grad = dP_dc * parent.grad
                # restore original value
                child.data -= h

            kids.append(child)
            






    
