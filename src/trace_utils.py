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
        output, error = Terminal.run_simple_command(cmd)
        if error:
            print(error)
        else:
            for line in output.splitlines():
                cls.kernel_methods.append(Str(line.strip()))

    @classmethod
    def get_user_methods(cls, file):
        cmd = f"objdump -t {file}"
        output, error = Terminal.run_simple_command(cmd)
        if error:
            print(error)
        else:
            lines = output.splitlines()
            for i, line in enumerate(lines):
                if "SYMBOL TABLE:" in line and "no" in lines[i+1].split()[0]:
                    print("No symbols found")
                    break
                if ".text" in line:
                    cls.user_methods.append(Str(line.split()[-1]))



