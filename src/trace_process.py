import multiprocessing
from contextlib import redirect_stdout
from queue import Empty
from subprocess import Popen

from trace_utils import TraceUtils


class TraceProcess(multiprocessing.Process):
    def __init__(self, function, file = None):
        super().__init__()
        self._queue = multiprocessing.Queue()
        self._cmd = TraceUtils.get_start_trace_command(function, file)

    def run(self):
        with redirect_stdout(self._queue):
            Popen(self._cmd, shell=True).wait()

    def get_output(self):
        try:
            return self._queue.get_nowait()
        except Empty:
            return None