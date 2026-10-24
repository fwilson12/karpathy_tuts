from graphviz import Digraph


def _trace(root):

    nodes, edges = set(), set()
    # recursive helper
    def build(v):
        # v can be a child of two nodes, but only need to add once
        if v not in nodes: 
            nodes.add(v)
            for child in v.children:
                edges.add((child, v))
                build(child)

    build(root)
    return nodes, edges

def draw_dot(root):
    dot = Digraph(format='svg', graph_attr={'rankdir': 'LR'})

    nodes, edges = _trace(root)
    for n in nodes:
        # unique identifier 
        uid = str(id(n))

        # init value node
        dot.node(name=uid, label="{ %s | data %.4f}" % (n.label, n.data), shape="record")
        if n.op:
            # init op node
            dot.node(name=uid + n.op, label=n.op)
            # arrow from op node to parent
            dot.edge(uid + n.op, uid)

    # op connections already done for each parent, connect children to parent's op
    for n1, n2 in edges:
        # arrow from child value to parent op node
        dot.edge(str(id(n1)), str(id(n2)) + n2.op)

    return dot
    
