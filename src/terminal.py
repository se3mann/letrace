from subprocess import Popen, PIPE

class Terminal:
    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def run_simple_command(cmd):
        with Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE) as p:
            return p.stdout.read().decode('utf-8')

