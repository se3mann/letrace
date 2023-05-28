from threading import Thread, Event
from contextlib import redirect_stdout
from queue import Empty, Queue
from subprocess import Popen, PIPE

from trace_utils import TraceUtils

# Special Queue class with a write and flush method
# which can be used to write text streams into
class WritableQueue(Queue):
    def write(self, s):
        self.put(s)

    def flush(self):
        pass

class TraceThread(Thread):
    def __init__(self, function, file = None):
        super().__init__()
        self.queue = WritableQueue()
        self.cmd = TraceUtils.get_start_trace_command(function, file)
        self.daemon = True
        self.process = None
        self.tracing_enabled = False

    def run(self):
        print(self.cmd)
        print("Starting trace")
        self.tracing_enabled = True
        self.process = Popen(self.cmd, shell=False, stdout=PIPE, stderr=PIPE)
        while self.tracing_enabled:
            line = self.process.stdout.readline().decode('utf-8')
            self.queue.put(line)
        self.queue.put("\n")

    def get_output(self):
        try:
            return self.queue.get_nowait().strip(' ')
        except Empty:
            return None

    def print_line(self):
        print(self.queue.get_nowait())

    def stop_trace(self):
        self.tracing_enabled = False
        if self.process is not None:
            pid = self.process.pid
            if self.process.poll() is None:
                print("Sending CTRL+C to bpftrace...")
                kill_process = Popen(["pkexec", "kill", "-2", str(pid)])
                print("Bpftrace stopped")