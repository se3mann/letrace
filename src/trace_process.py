import os
import signal
from threading import Thread, Event
from contextlib import redirect_stdout
from queue import Empty, Queue
from subprocess import Popen

from trace_utils import TraceUtils


class TraceProcess(Thread):
    def __init__(self, function, file = None):
        super().__init__()
        self.queue = Queue()
        self.cmd = TraceUtils.get_start_trace_command(function, file)
        self.daemon = True
        self.process = None

    def run(self):
        with redirect_stdout(self.queue):
            self.process = Popen(self.cmd, shell=False)

    def get_output(self):
        try:
            return self.queue.get_nowait()
        except Empty:
            return None

    def print_line(self):
        print(self.queue.get_nowait())

    def stop_trace(self):
        if self.process is not None:
            os.kill(self.process.pid, signal.SIGINT)
            self.process = None