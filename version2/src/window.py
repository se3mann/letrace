from gi.repository import Gtk
from sidebar import TraceSideBar

@Gtk.Template(filename="window.ui")
class MainWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'MainWindow'

    paned = Gtk.Template.Child()
    start_button = Gtk.Template.Child()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
