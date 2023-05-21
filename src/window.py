from gi.repository import Gtk, Gio
from sidebar import TraceSideBar

@Gtk.Template(filename="ui/window.ui")
class MainWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'MainWindow'

    paned = Gtk.Template.Child()
    start_button = Gtk.Template.Child()
    open_button = Gtk.Template.Child()
    trace_sidebar = Gtk.Template.Child()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @Gtk.Template.Callback()
    def on_open_button_clicked(self, *args):
        # Create a new file selection dialog, using the "open" mode
        # and keep a reference to it
        self._native = Gtk.FileChooserNative(
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
        self._native.add_filter(executable_filter)

        self._native.connect("response", self.on_open_response)
        # Present the dialog to the user
        self._native.show()

    def on_open_response(self, dialog, response):
        # If the user selected a file...
        if response == Gtk.ResponseType.ACCEPT:
            # ... retrieve the location from the dialog and open it
            file = dialog.get_file()
            file_path = file.get_path()
            print(file_path)
            self.trace_sidebar.set_user_list_on_thread(file_path)
        self._native = None

    @Gtk.Template.Callback()
    def on_start_button_clicked(self, *args):
        print("Start button clicked")
