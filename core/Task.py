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
        self.error = None

    def run(self, timeout=None, gpu=None):
        self.starting_date = time.time()
        cmd = self.command
        if gpu is not None:
            cmd = "CUDA_VISIBLE_DEVICES=%d %s" % (gpu, cmd)
        self.process = subprocess.Popen(cmd, shell=True)
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