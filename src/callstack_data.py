import networkx as nx
import re


def delete_offset(line):
    pattern = re.compile(r'(\w+)\+\d+')
    match = pattern.match(line)

    if match:
        function_name = match.group(1)
        return function_name
    else:
        return line


class CallGraph:
    def __init__(self):
        self.nx_graph = nx.DiGraph()

    def parse_from_list(self, stack_list):
        prev_node = None
        for line in stack_list:
            node = delete_offset(line)
            node_is_new = True
            if self.nx_graph.has_node(node):
                node_is_new = False
            node = node

            if node_is_new:
                self.nx_graph.add_node(node, count=1, traced=False, label=node)
            else:
                self.nx_graph.nodes[node]['count'] += 1

            # when prev_node is not None, it's not the first node
            # check if the edge already exists, if not, add a new edge
            # else, update the edge weight
            if prev_node is not None:
                if not self.nx_graph.has_edge(node, prev_node):
                    self.nx_graph.add_edge(node, prev_node, weight=1)
                else:
                    self.nx_graph.edges[node, prev_node]['weight'] += 1

            prev_node = node

    def print_graph(self):
        for node, attributes in self.nx_graph.nodes(data=True):
            print(f"Node {node}: {attributes}")

    def print_edges(self):
        for edge, attributes in self.nx_graph.edges(data=True):
            print(f"Edge {edge}: {attributes}")

    def parse(self, stack_list):
        traced_node = delete_offset(stack_list[0])
        self.parse_from_list(stack_list)
        self.nx_graph.nodes[traced_node]['traced'] = True

    def clear(self):
        self.nx_graph.clear()

    def get_nx_graph(self):
        return self.nx_graph


