from gi.repository import Gtk, GLib
from trace_controller import TraceController, TraceControllerFactory
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk4agg import FigureCanvasGTK4Agg as FigureCanvas
import networkx as nx

@Gtk.Template(filename="ui/grapharea.ui")
class GraphArea(Gtk.Box):
    __gtype_name__ = 'GraphArea'
    def __init__(self):
        Gtk.Box.__init__(self)
        self.trace_controller = TraceControllerFactory.get_instance()
        self.call_graph = self.trace_controller.call_graph.get_nx_graph()
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.append(self.canvas)
        self.ax = self.figure.add_subplot(111)
        self.interval = 1000

        # GLib.timeout_add(self.interval, self.update)
        self.show()

    def update(self):
        self.ax.clear()
        pos = nx.spring_layout(self.call_graph)
        nx.draw_networkx(self.call_graph, pos, ax=self.ax, with_labels=True, arrows=True)
        self.canvas.draw()

    def draw_graph(self):
        self.ax.clear()
        pos = nx.spring_layout(self.call_graph)
        node_colors = ['red' if self.call_graph.nodes[node].get('traced') else 'blue' for node in self.call_graph.nodes()]
        nx.draw_networkx(self.call_graph, pos, node_color=node_colors, ax=self.ax, with_labels=True, arrows=True)
        # nx.draw_networkx_labels(nx_graph, pos, labels, font_size=10, font_color='black', verticalalignment='center')
        # nx.draw_networkx_labels(nx_graph, pos, ax=self.ax, font_size=8, font_color='w')
        self.canvas.draw()