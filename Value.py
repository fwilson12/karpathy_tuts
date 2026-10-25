from graphviz_helpers import render_graph
import math


# float wrapper w/ history
class Value:

    def __init__(self, data, children=(), op='', label=''):
        self.data = data
        self.grad = 0.0
        self._backward = lambda: None # empty function (nothing to due for a leaf)
        self.children = set(children)
        self.op = op
        self.label = label

    def __repr__(self):
        return f"Value(label={self.label}, data={self.data:.4f})"

    def __add__(self, other):
        out =  Value(self.data + other.data, (self, other), '+')

        # when the new Value object out calls backward, the self and other objects are baked in as references, and will be updated accordingly 
        def _backward():
            self.grad = 1.0 * out.grad
            other.grad = 1.0 * out.grad

        out._backward = _backward 
        return out

    def __mul__(self, other):
        out = Value(self.data * other.data, (self, other), '*')

        def _backward():
            self.grad = other.data * out.grad
            other.grad = self.data * out.grad

        out._backward = _backward

        return 
    
    def tanh(self):
        x = self.data
        t = (math.exp(2 * x) - 1) / (math.exp(2 * x) + 1)
        out = Value(t, (self), 'tanh')

        def _backward():
            self.grad = (1 - t ** 2) * out.grad

        out._backward = _backward  

        return out 

        # d/dx(tanh(x)) = 1 - tanh(x)^2 
 
    
    def backward(self):

        # create topological map such that the children of each parent node appear before it does
        top = []
        visited = set()
        def build_top(node):
            if node not in visited:
                visited.add(node)
                for child in node.children:
                    build_top(child)
                top.append(node)


        # create topological map w/ respect to caller node, set self.gradient, backprop through top map starting w/ caller
        build_top(self)
        self.grad = 1.0
        for node in reversed(top):
            node._backward()












            






    
