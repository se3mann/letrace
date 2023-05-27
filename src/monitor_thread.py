from threading import Thread, Event
from queue import Empty, Queue

from trace_utils import TraceUtils

class MonitorThread(Thread):
    def __init__(self, trace_thread):
        super().__init__()
        self.stop_event = Event()
        self.trace_thread = trace_thread

    def run(self):
        self.trace_thread.start()
        while not self.stop_event.is_set():
            # tracing not running due to error occurred
            if not self.trace_thread.is_alive():
                break
            print(self.trace_thread.get_output())
        if self.trace_thread.is_alive():
            self.trace_thread.stop_trace()
            self.trace_thread.join()
            print("Trace stopped")

    def stop_monitor(self):
        self.stop_event.set()
