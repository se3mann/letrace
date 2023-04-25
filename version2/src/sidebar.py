from gi.repository import Gtk

@Gtk.Template(filename="sidebar.ui")
class TraceSideBar(Gtk.Box):
    __gtype_name__ = 'TraceSideBar'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)