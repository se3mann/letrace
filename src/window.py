from gi.repository import Gtk

@Gtk.Template(resource_path='/org/gnome/Example/window.ui')
class LetraceWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'LetraceWindow'

    label = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
