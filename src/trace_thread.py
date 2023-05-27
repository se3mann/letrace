from threading import Thread
from contextlib import redirect_stdout
from queue import Empty, Queue
from subprocess import Popen

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

    def run(self):
        print(self.cmd)
        print("Starting trace")
        with redirect_stdout(self.queue):
            self.process = Popen(self.cmd, shell=False)
            self.process.wait()

    def get_output(self):
        try:
            return self.queue.get_nowait().strip(' ')
        except Empty:
            return None

    def print_line(self):
        print(self.queue.get_nowait())

    def stop_trace(self):
        if self.process is not None:
            pid = self.process.pid
            if self.process.poll() is None:
                Popen(["pkexec", "kill", "-9", str(pid)])
                self.process.wait()
                self.process = None
