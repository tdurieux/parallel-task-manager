import time
import subprocess
import GPUtil

class Task(object):

    def __init__(self, command, with_gpu=False):
        """"
        :type str: command
        """
        self.command = command
        self.status = None
        self.starting_date = None
        self.done = False
        self.process = None
        self.with_gpu = with_gpu

    def run(self, timeout=None):
        self.starting_date = time.time()
        cmd = self.command
        if self.with_gpu:
            gpu_ids = GPUtil.getAvailable(order = 'memory', limit = 1, includeNan=False)
            cmd = "CUDA_VISIBLE_DEVICES=%d %s" % (gpu_ids[0], cmd)
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