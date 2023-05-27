from threading import Thread

from trace_thread import TraceThread
from monitor_thread import MonitorThread


class TraceController:
    def __init__(self):
        self.trace_thread = None
        self.thread_enabled = False
        self.monitor_thread = None

    # start tracing process
    def start_trace(self, function, file = None):
        self.thread_enabled = True
        self.trace_thread = TraceThread(function, file)
        self.monitor_thread = MonitorThread(self.trace_thread)
        # monitor_thread = Thread(target=self.monitor_trace, args=(self.trace_thread,))
        # self.trace_thread.start()
        # monitor_thread.start()
        self.monitor_thread.start()

    def stop_trace(self):
        self.thread_enabled = False
        self.monitor_thread.stop_monitor()
        self.monitor_thread.join()

"""
    def monitor_trace(self, trace_thread):
        output = []
        while self.thread_enabled:
            if not trace_thread.is_alive():
                print("Tracing thread is not alive")
                break
            if(trace_thread.get_output() is not None):
                print(trace_thread.get_output())
        print("Monitor while loop ended")
        if trace_thread.is_alive():
            trace_thread.stop_trace()
            trace_thread.join()
"""
