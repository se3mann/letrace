from terminal import Terminal


class TraceUtils:
    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def get_kernel_methods():
        kernel_methods = []
        cmd = "sudo bpftrace -l | grep -E '^kprobe' | cut -d ':' -f 2"
        output = Terminal.run_simple_command(cmd)
        for line in output.splitlines():
            kernel_methods.append(line.strip())

        return kernel_methods
