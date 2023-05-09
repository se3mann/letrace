from gi.repository import Gtk, GObject, Gio
from terminal import Terminal


class Str(GObject.GObject):
    value: str

    def __init__(self, value):
        GObject.GObject.__init__(self)
        self.value = value

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value
        self.emit('changed')


class TraceUtils:
    kernel_methods = Gio.ListStore.new(Str)
    user_methods = Gio.ListStore.new(Str)
    test_list = Gio.ListStore.new(Str)

    def __init__(self):
        pass

    @classmethod
    def get_kernel_methods(cls):
        cmd = "sudo bpftrace -l | grep -E '^kprobe' | cut -d ':' -f 2"
        output = Terminal.run_simple_command(cmd)
        for line in output.splitlines():
            cls.kernel_methods.append(Str(line.strip()))

    """
    @classmethod
    def get_user_methods(cls):
        cmd = "sudo bpftrace -l | grep -E '^uprobe' | cut -d ':' -f 2"
        output = Terminal.run_simple_command(cmd)
        for line in output.splitlines():
            cls.kernel_methods.append(Str(line.strip()))
    """

