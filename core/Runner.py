import datetime


class Runner(object):

    def __init__(self, tasks, args):
        """
        :type tasks: list of RepairTask
        """
        self.tasks = tasks
        self.finished = []
        self.running = []
        self.waiting = []
        self.args = args
        self.timeout = None
        if args.timeout is not None:
            self.timeout = args.timeout
        if args.process is not None:
            self.process = args.process