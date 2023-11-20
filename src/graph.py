from gi.repository import Gtk, GLib
from trace_controller import TraceController, TraceControllerFactory
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk4agg import FigureCanvasGTK4Agg as FigureCanvas
from matplotlib.backends.backend_gtk4 import NavigationToolbar2GTK4 as NavigationToolbar
import networkx as nx


class NodeInfoDialog(Gtk.Window):
    def __init__(self, node, attributes):
        Gtk.Dialog.__init__(self, title=f"Node {node} Information")

        self.set_default_size(200, 150)
        self.label = Gtk.Label()
        info_text = ""
        for key, value in attributes.items():
            info_text += f"{key}: {value}\n"
        self.label.set_text(info_text)
        self.set_child(self.label)
        self.show()


@Gtk.Template(filename="ui/grapharea.ui")
class GraphArea(Gtk.Box):
    __gtype_name__ = 'GraphArea'

    def __init__(self):
        Gtk.Box.__init__(self)
        self.trace_controller = TraceControllerFactory.get_instance()
        self.call_graph = self.trace_controller.call_graph.get_nx_graph()


        # set up figure and canvas
        self.figure = Figure(facecolor='lightskyblue')
        self.figure.tight_layout()
        self.figure.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)

        self.canvas = FigureCanvas(self.figure)
        self.canvas.set_hexpand(True)
        self.canvas.set_vexpand(True)
        self.append(self.canvas)
        self.ax = self.figure.add_subplot()
        self.show()

        # Add NavigationToolbar
        self.toolbar = NavigationToolbar(self.canvas)
        self.append(self.toolbar)

    def draw_graph(self):
        self.ax.clear()
        self.pos = nx.nx_agraph.graphviz_layout(self.call_graph, prog="dot")
        node_colors = ['red' if self.call_graph.nodes[node].get('traced') else 'blue' for node in self.call_graph.nodes()]
        nx.draw_networkx(self.call_graph, self.pos, node_color=node_colors, ax=self.ax, with_labels=False, arrows=True, alpha=0.5)
        nx.draw_networkx_labels(self.call_graph, self.pos, font_color='black', font_size=8, font_weight='bold', ax=self.ax)
        self.canvas.mpl_connect('button_press_event', self.on_canvas_click)
        self.canvas.draw()

    def get_clicked_node(self, x, y):
        for node, (node_x, node_y) in self.pos.items():
            distance = ((x - node_x) ** 2 + (y - node_y) ** 2) ** 0.5
            if distance < 15:
                return node
        return None
    def on_canvas_click(self, event):
        if not self.toolbar.mode and event.button == 1:
            # Handle node click only if the toolbar is not active and left mouse button is pressed
            x, y = event.xdata, event.ydata

            clicked_node = self.get_clicked_node(x, y)

            if clicked_node is not None:
                node_attributes = self.call_graph.nodes[clicked_node]
                dialog = NodeInfoDialog(clicked_node, node_attributes)

