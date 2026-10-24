from graphviz_helpers import draw_dot

class Value:

    def __init__(self, data, children=(), op='', label=''):
        self.data = data
        self.children = set(children)
        self.op = op
        self.label = label

    def __repr__(self):
        return f"Value(label={self.label}, data={self.data:.4f})"

    def __add__(self, other):
        return Value(self.data + other.data, (self, other), '+')

    def __mul__(self, other):
        return Value(self.data * other.data, (self, other), '*')


a = Value(2.0, label='a')
b = Value(-19.1, label='b')
c = Value(13.5, label='c')
e = a * b; e.label = 'e'
d = e + c; d.label='d'

print(d)
draw_dot(d).render('graph', view=True)


    