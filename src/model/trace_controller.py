from threading import Thread

from model.trace_thread import TraceThread
from model.monitor_thread import MonitorThread
from model.callstack_data import CallGraph


class TraceController:
    def __init__(self):
        self.trace_thread = None
        self.thread_enabled = False
        self.monitor_thread = None
        self.call_graph = CallGraph()

    # start tracing process
    def start_trace(self, function, file=None):
        self.call_graph.clear()
        self.thread_enabled = True
        self.trace_thread = TraceThread(function, file)
        self.monitor_thread = MonitorThread(self.trace_thread, self.call_graph)
        self.monitor_thread.start()

    def stop_trace(self):
        self.thread_enabled = False
        self.monitor_thread.stop_monitor()
        self.monitor_thread.join()


class TraceControllerFactory:
    __instance = None

    @staticmethod
    def get_instance():
        if TraceControllerFactory.__instance is None:
            TraceControllerFactory.__instance = TraceController()
        return TraceControllerFactory.__instance
