import time
import subprocess


class Task(object):

    def __init__(self, command):
        """"
        :type str: command
        """
        self.command = command
        self.status = None
        self.starting_date = None
        self.done = False
        self.process = None

    def run(self, timeout=None):
        self.starting_date = time.time()
        self.process = subprocess.Popen(self.command, shell=True)
        if timeout is not None:
            self.process.wait(timeout)
        else:
            self.process.wait()
        self.done = True

    def stop(self):
        if not self.done:
            self.process.terminate()
            self.process.wait()
        pass