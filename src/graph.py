from gi.repository import Gtk, GLib
from trace_controller import TraceController, TraceControllerFactory
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk4agg import FigureCanvasGTK4Agg as FigureCanvas
from matplotlib.backends.backend_gtk4 import NavigationToolbar2GTK4 as NavigationToolbar
import networkx as nx
from mpl_interactions import panhandler, zoom_factory


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

        # Connect the button_press_event signal to the callback function for panning
        # self.canvas.mpl_connect('button_press_event', self.on_canvas_press)

        # Connect the scroll_event signal to the callback function for zooming
        # self.canvas.mpl_connect('scroll_event', self.on_canvas_scroll)

    def draw_graph(self):
        self.ax.clear()
        pos = nx.nx_agraph.graphviz_layout(self.call_graph, prog="dot")
        node_colors = ['red' if self.call_graph.nodes[node].get('traced') else 'blue' for node in self.call_graph.nodes()]
        nx.draw_networkx(self.call_graph, pos, node_color=node_colors, ax=self.ax, with_labels=True, arrows=True)
        self.canvas.draw()

"""
    def on_canvas_press(self, event):
        if event.button == 3:  # Right mouse button for panning
            self.press_x = event.x
            self.press_y = event.y

    def on_canvas_scroll(self, event):
        # Zoom using the mouse wheel
        if event.button == 'up':
            self.ax.set_xlim(self.ax.get_xlim()[0] - 0.1, self.ax.get_xlim()[1] + 0.1)
            self.ax.set_ylim(self.ax.get_ylim()[0] - 0.1, self.ax.get_ylim()[1] + 0.1)
        elif event.button == 'down':
            self.ax.set_xlim(self.ax.get_xlim()[0] + 0.1, self.ax.get_xlim()[1] - 0.1)
            self.ax.set_ylim(self.ax.get_ylim()[0] + 0.1, self.ax.get_ylim()[1] - 0.1)

        self.canvas.draw()
"""