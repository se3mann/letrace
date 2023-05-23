import multiprocessing
from contextlib import redirect_stdout
from queue import Empty
from subprocess import Popen, PIPE

from trace_utils import TraceUtils


class TraceProcess(multiprocessing.Process):
    def __init__(self, function, file = None):
        super().__init__()
        self.queue = multiprocessing.Queue()
        self.cmd = TraceUtils.get_start_trace_command(function, file)
        self.process = Popen(self.cmd, shell=True, start_new_session=True)

    def run(self):
        with redirect_stdout(self.queue):
            self.process.wait()

    def get_output(self):
        try:
            return self.queue.get_nowait()
        except Empty:
            return None