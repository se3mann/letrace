from contextlib import redirect_stdout
import multiprocessing
from multiprocessing.queues import Queue
from queue import Empty
from threading import Thread
import os
import signal

from trace_process import TraceProcess
from trace_utils import TraceUtils


class TraceController:
    def __init__(self):
        self._thread_enabled = False

    # start tracing process
    def start_trace(self, function, file = None):
        self._thread_enabled = True
        trace_process = TraceProcess(function, file)
        monitor_thread = Thread(target=self.monitor_trace, args=(trace_process,))
        trace_process.start()
        monitor_thread.start()

    def monitor_trace(self, trace_process):
        output = []
        while self._thread_enabled:
            if not trace_process.is_alive():
                break
            if(trace_process.get_output() is not None):
                print(trace_process.get_output())
        if trace_process.is_alive():
            os.killpg(os.getpgid(trace_process.pid), signal.SIGTERM)
            trace_process.terminate()
            trace_process.join()

    def stop_trace(self):
        self._thread_enabled = False



