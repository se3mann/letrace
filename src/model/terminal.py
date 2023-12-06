from subprocess import Popen, PIPE

class Terminal:
    def __init__(self, *args, **kwargs):
        pass

    # run only terminal commands that are terminte by default
    @staticmethod
    def run_simple_command(cmd):
        with Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE) as p:
            return p.stdout.read().decode('utf-8'), p.stderr.read().decode('utf-8')
