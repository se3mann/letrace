from gi.repository import GObject, Gio
import shlex

from terminal import Terminal


# Gtk wrapper class for sidebar list view items
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
    # Gtk ListStore for kernel and user methods, data layer
    kernel_methods = Gio.ListStore.new(Str)
    user_methods = Gio.ListStore.new(Str)

    def __init__(self):
        pass

    # Get the methods from kernel
    @classmethod
    def get_kernel_methods(cls):
        cmd = "sudo bpftrace -l | grep -E '^kprobe' | cut -d ':' -f 2"
        output, error = Terminal.run_simple_command(cmd)
        if error:
            print(error)
        else:
            for line in output.splitlines():
                cls.kernel_methods.append(Str(line.strip()))

    # Get the methods from user file
    @classmethod
    def get_user_methods(cls, file):
        cmd = f"objdump -t {file}"
        output, error = Terminal.run_simple_command(cmd)
        # When objdump does not recognize file format,
        # it prints to stderr
        if error:
            print(error)
        else:
            lines = output.splitlines()
            for i, line in enumerate(lines):
                # If no symbols in file, the output looks like:
                # SYMBOL TABLE:\n no symbols, otherwise the next lines
                # containing the symbols as a table
                if "SYMBOL TABLE:" in line and "no" in lines[i+1].split()[0]:
                    print("No symbols found")
                    break
                # We can use symbols marked with text
                if ".text" in line:
                    cls.user_methods.append(Str(line.split()[-1]))

    @classmethod
    def get_start_trace_command(cls, function, file=None):
        if file is None:
            command = f"sudo bpftrace -e 'kprobe:{function} {{ printf(\"%s\\n\", kstack()); }}'"
            cmd = shlex.split(command)
            return cmd
        else:
            return f"sudo bpftrace -e 'uprobe:{file}:{function} {{ printf(\"%s\\n\", ustack()); }}'"
