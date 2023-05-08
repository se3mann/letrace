import sys
import gi
import threading
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Gio

from window import MainWindow
from trace_utils import TraceUtils


class LeTraceApp(Gtk.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_action('quit', self.quit, ['<primary>q'])

        #load kernel methods at app startup at different thread
        self.load_linux_kernels()

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = MainWindow(application=self)
        win.present()

    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)

    def load_linux_kernels(self):
        thread = threading.Thread(target=TraceUtils.get_kernel_methods)
        thread.start()


if __name__ == "__main__":
    app = LeTraceApp()
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)
