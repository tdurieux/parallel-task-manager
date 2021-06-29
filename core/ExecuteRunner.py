try:
   import queue
except ImportError:
   import Queue as queue
from threading import Thread
import time
import subprocess
import GPUtil


from core.renderer.renderer import get_renderer
from core.Runner import Runner

class RunnerWorker(Thread):
    def __init__(self, local_runner, process, callback, timeout=None):
        Thread.__init__(self)
        self.local_runner = local_runner
        self.callback = callback
        self.daemon = True
        self.pool = ThreadPool(process, timeout=timeout, with_gpu=local_runner.with_gpu)

    def run(self):
        for task in self.local_runner.tasks:
            task.status = "WAITING"
            self.pool.add_task(task, self.callback)

        self.pool.wait_completion()


class Worker(Thread):
    def __init__(self, tasks, timeout=None, gpu=None):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.timeout = timeout
        self.gpu = gpu
        self.start()

    def run(self):
        while True:
            (task, callback) = self.tasks.get()
            task.status = "RUNNING"
            try:
                task.run(timeout=self.timeout, gpu=self.gpu)  
            except subprocess.TimeoutExpired as e:
                task.status = "TIMEOUT"      
            except Exception as e:
                task.status = "ERROR"
                task.error = e
            finally:
                if callback is not None:
                    callback(task)
                self.tasks.task_done()


class ThreadPool:
    """Pool of threads consuming tasks from a queue"""
    def __init__(self, num_threads, timeout=None, with_gpu=False):
        self.tasks = queue.Queue(num_threads)
        self.workers = []
        nb_gpus = len(GPUtil.getGPUs())
        for i in range(num_threads):
            gpu = None
            if with_gpu and nb_gpus > 0:
                gpu = i % nb_gpus
            self.workers.append(Worker(self.tasks, timeout=timeout, gpu=gpu))

    def add_task(self, task, callback):
        """Add a task to the queue"""
        self.tasks.put((task, callback))

    def wait_completion(self):
        """Wait for completion of all the tasks in the queue"""
        self.tasks.join()


class TaskRunner(Runner):

    def __init__(self, tasks, args):
        """
        :type tasks: list of tasks
        """
        super(TaskRunner, self).__init__(tasks, args)
        self.tasks = tasks
        self.start = None
        self.end = None
        self.finished = []

    def done(self, task):
        if task.status == "RUNNING":
            task.status = "FINISHED"
        if task.error is not None:
            print("\nCommand %s finished with an error: \n\t: %s\n" %(task.command, task.error))
        task.end_date = time.time()
        self.finished += [task]
        pass

    def execute(self):
        self.start = time.time()
        worker = RunnerWorker(self, self.process, self.done, self.timeout)
        renderer = get_renderer(self)
        worker.start()

        while worker.is_alive():
            renderer.render()
            time.sleep(1)
        
        self.end = time.time()
        renderer.render_final_result()