from threading import Thread, Event
from queue import Empty, Queue

from trace_utils import TraceUtils

class MonitorThread(Thread):
    def __init__(self, trace_thread, callgraph):
        super().__init__()
        self.stop_event = Event()
        self.trace_thread = trace_thread
        self.callgraph = callgraph

    def run(self):
        self.trace_thread.start()
        stack_lines = []
        while not self.stop_event.is_set():
            # tracing not running due to error occurred
            if not self.trace_thread.is_alive():
                print("Trace is stopped due to error occurred")
                break
            line = self.trace_thread.get_output()
            if line is not None:
                if line.startswith("Attaching"):
                    print("Start monitoring bpftrace output: " + line, end="")
                elif line == '\n':
                    # sometimes it creates an empty list
                    # because of double new line
                    if len(stack_lines) > 0:
                        print("--------------------")
                        self.callgraph.parse_from_list(stack_lines)
                        self.callgraph.print_edges()
                        stack_lines.clear()
                else:
                    stack_lines.append(line)
        if self.trace_thread.is_alive():
            self.trace_thread.stop_trace()
            self.trace_thread.join()
            print("Trace thread stopped\n")

    def stop_monitor(self):
        self.stop_event.set()
        print("Monitor thread stopped\n")
