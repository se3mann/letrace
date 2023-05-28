from gi.repository import Gtk
from trace_controller import TraceController, TraceControllerFactory
from sidebar import TraceSideBar
from trace_utils import TraceUtils
from graph import GraphArea

@Gtk.Template(filename="ui/window.ui")
class MainWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'MainWindow'

    paned = Gtk.Template.Child()
    start_button = Gtk.Template.Child()
    open_button = Gtk.Template.Child()
    trace_sidebar = Gtk.Template.Child()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trace_controller = TraceControllerFactory.get_instance()
        self.trace_running = False

    @Gtk.Template.Callback()
    def on_open_button_clicked(self, *args):
        # Create a new file selection dialog, using the "open" mode
        # and keep a reference to it
        self.native = Gtk.FileChooserNative(
            title="Open File",
            transient_for=self,
            action=Gtk.FileChooserAction.OPEN,
            accept_label="_Open",
            cancel_label="_Cancel",
        )

        # Create a filter for binary executable files
        executable_filter = Gtk.FileFilter()
        executable_filter.set_name("Binary executable files")
        executable_filter.add_mime_type("application/x-executable")

        # Add the filter to the file chooser dialog
        self.native.add_filter(executable_filter)

        self.native.connect("response", self.on_open_response)
        # Present the dialog to the user
        self.native.show()

    def on_open_response(self, dialog, response):
        # If the user selected a file...
        if response == Gtk.ResponseType.ACCEPT:
            # ... retrieve the location from the dialog and open it
            file = dialog.get_file()
            file_path = file.get_path()
            self.trace_sidebar.set_user_methods(file_path)
        self._native = None

    @Gtk.Template.Callback()
    def on_start_button_clicked(self, *args):
        if not self.trace_running:
            selected_method = self.trace_sidebar.get_selected_method()
            selected_file = self.trace_sidebar.get_selected_file()
            if selected_method is None:
                return
            self.trace_controller.start_trace(selected_method, selected_file)
            self.trace_running = True
            self.start_button.set_label("Stop")
        else:
            self.trace_controller.stop_trace()
            self.trace_running = False
            self.start_button.set_label("Start")
