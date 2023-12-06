from gi.repository import GObject, Gio
import shlex

from model.terminal import Terminal


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
    kernel_methods = Gio.ListStore.new(Str)
    user_methods = Gio.ListStore.new(Str)
    file = None

    def __init__(self):
        pass

    @classmethod
    def get_kernel_methods(cls):
        cmd = "pkexec bpftrace -l | grep -E '^kprobe' | cut -d ':' -f 2"
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
        # When objdump does not recognize file format,
        # it prints to stderr
        if error:
            print(error)
        else:
            lines = output.splitlines()
            # If no symbols in file, the output looks like:
            # SYMBOL TABLE:\n no symbols, otherwise the next lines
            # containing the symbols as a table
            if "SYMBOL TABLE:" in lines[2] and "no" in lines[3].split()[0]:
                print("No symbols found")
                cls.clear_user_methods()
            else:
                cls.clear_user_methods()
                cls.file = file
                for i, line in enumerate(lines):
                    # The symbols marked with text are the functions
                    # in the source code
                    if ".text" in line:
                        cls.user_methods.append(Str(line.split()[-1]))

    @classmethod
    def get_start_trace_command(cls, function, file=None):
        if file is None:
            command = f"pkexec bpftrace -e \'kprobe:{function} {{ printf(\"%s\\n\", kstack()); }}\'"
            cmd = shlex.split(command)
            return cmd
        else:
            command = f"pkexec bpftrace -e 'uprobe:{file}:{function} {{ printf(\"%s\\n\", ustack()); }}'"
            cmd = shlex.split(command)
            return cmd

    @classmethod
    def clear_kernel_methods(cls):
        cls.kernel_methods.remove_all()

    @classmethod
    def clear_user_methods(cls):
        cls.user_methods.remove_all()
