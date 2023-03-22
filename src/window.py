
from gi.repository import Gtk, Gio

@Gtk.Template(resource_path='/org/gnome/Example/window.ui')
class LetraceWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'LetraceWindow'

    label = Gtk.Template.Child()
    open_button = Gtk.Template.Child()


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        open_action = Gio.SimpleAction(name="open")
        open_action.connect("activate", self.open_file_dialog)
        self.add_action(open_action)

    def open_file_dialog(self, action, parameter):
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

        # Connect the "response" signal of the file selection dialog;
        # this signal is emitted when the user selects a file, or when
        # they cancel the operation
        self._native.connect("response", self.on_open_response)
        # Present the dialog to the user
        self._native.show()

    def on_open_response(self, dialog, response):
        # If the user selected a file...
        if response == Gtk.ResponseType.ACCEPT:
            # ... retrieve the location from the dialog and open it
            file = dialog.get_file()
            self.label.set_label(f"Selected file: {file}")
        # Release the reference on the file selection dialog now that we
        # do not need it any more
        self._native = None

    def trace_file(self, file):
        # we want to get the bpftrace list this file's functions
        pass
