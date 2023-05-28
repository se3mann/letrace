from gi.repository import Gtk
from trace_controller import TraceController, TraceControllerFactory

@Gtk.Template(filename="ui/grapharea.ui")
class GraphArea(Gtk.Box):
    __gtype_name__ = 'GraphArea'
    def __init__(self):
        Gtk.Box.__init__(self)
        self.trace_controller = TraceControllerFactory.get_instance()



