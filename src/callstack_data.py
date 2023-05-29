import graph_tool.all as gt
import networkx as nx


class CallGraph:
    def __init__(self):
        self.graph = gt.Graph(directed=True)
        self.labels = self.graph.new_vertex_property("string")
        self.weights = self.graph.new_edge_property("int")
        self.count = self.graph.new_vertex_property("int")
        self.traced = self.graph.new_vertex_property("bool")
        self.nx_graph = nx.DiGraph()

    def parse_from_list(self, stack_list):
        prev_vertex = None
        for node in stack_list:
            vertex = None
            # breaks when the vertex is found
            for v in self.graph.vertices():
                if self.labels[v] == node:
                    vertex = v
                    break

            # if vertex is None, it's a new node, else
            # update the existing node count
            if vertex is None:
                vertex = self.graph.add_vertex()
                self.labels[vertex] = node
                self.count[vertex] = 1
                self.traced[vertex] = False
            else:
                self.count[vertex] += 1

            # when prev_vertex is not None, it's not the first node
            # check if the edge already exists, if not, add a new edge
            # else, update the edge weight
            if prev_vertex is not None:
                edge = None
                # breaks when the edge is found
                for e in self.graph.edges():
                    if e.source() == prev_vertex and e.target() == vertex:
                        edge = e
                        break

                if edge is None:
                    edge = self.graph.add_edge(vertex, prev_vertex)
                    self.weights[edge] = 1
                else:
                    self.weights[edge] += 1

            prev_vertex = vertex

    def print_graph(self):
        for v in self.graph.vertices():
            line = f"{self.labels[v]}: {self.count[v]}"
            print(line)

    def print_edges(self):
        for e in self.graph.edges():
            line = f"{self.labels[e.source()]} ----> {self.labels[e.target()]}: {self.weights[e]}"
            print(line)

    def parse(self, stack_list):
        traced_vertex = stack_list[0]
        self.parse_from_list(stack_list)
        for v in self.graph.vertices():
            if self.labels[v] == traced_vertex:
                self.traced[v] = True
                break

    def clear(self):
        self.graph.clear()
        self.labels = self.graph.new_vertex_property("string")
        self.weights = self.graph.new_edge_property("int")
        self.count = self.graph.new_vertex_property("int")
        self.traced = self.graph.new_vertex_property("bool")

    def convert_to_nx(self):
        self.nx_graph = nx.DiGraph()
        for v in self.graph.vertices():
            self.nx_graph.add_node(self.labels[v], count=self.count[v], traced=self.traced[v])
        for e in self.graph.edges():
            self.nx_graph.add_edge(self.labels[e.source()], self.labels[e.target()], weight=self.weights[e])
        return self.nx_graph
