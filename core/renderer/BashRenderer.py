import os
import sys
import datetime
import time

from core.renderer.EmptyRenderer import EmptyRenderer

def get_terminal_size():
    env = os.environ

    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
        except:
            return
        return cr

    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (env.get('LINES', 25), env.get('COLUMNS', 80))

    ### Use get(key[, default]) instead of a try/catch
    # try:
    #    cr = (env['LINES'], env['COLUMNS'])
    # except:
    #    cr = (25, 80)
    return int(cr[1]), int(cr[0]) - 1


def clean_terminal():
    (width, height) = get_terminal_size()

    for i in range(1, height + 1):
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[K")


class BashRenderer(EmptyRenderer):
    def __init__(self, runner):
        """
        :param runner:
        :type runner: Runner
        """
        super(BashRenderer, self).__init__(runner)

        (width, height) = get_terminal_size()
        for _ in range(1, height + 1):
            print("")

    def getTask(self):
        output = {
            "ERROR": [],
            "FINISHED": [],
            "RUNNING": [],
            "WAITING": [],
            "TIMEOUT": [],
        }
        for task in self.runner.tasks:
            if task.status is not None:
                if task.status == "TIMEOUT" or task.status == "ERROR":
                    output["FINISHED"].append(task)
                output[task.status].append(task)
        return output

    def render(self):
        (width, height) = get_terminal_size()
        clean_terminal()

        output = ""

        tasks = self.getTask()
        output += "%d Running, %d Waiting, %d/%d Finished, %d Error, %d Timeout\n" % (
            len(tasks['RUNNING']),
            len(tasks['WAITING']),
            len(tasks['FINISHED']),
            len(self.runner.tasks),
            len(tasks['ERROR']),
            len(tasks['TIMEOUT']))

        output += "Running: \n"
        line_number = 1
        for task in tasks['RUNNING']:
            starting_date = task.starting_date
            if starting_date is None:
                starting_date = time.time()
            execution_time = datetime.timedelta(seconds=int(time.time() - starting_date))
            output += "%d. %s '%s'\n" % (line_number, execution_time, task.command)
            line_number += 1

        output_length = len(output.split("\n"))
        if output_length < height:
            for i in range(1, height - output_length):
                output += "\n"
        elif output_length > height:
            output_lines = output.split("\n")

            output_tmp = ""
            for i in range(0, height - 1):
                output_tmp += output_lines[i] + "\n"
            output_tmp += "All data is not displayed due to small terminal size"
            output = output_tmp
        print(output)

    def render_final_result(self):
        clean_terminal()
        tasks = self.getTask()

        
        output = ""

        execution_time = datetime.timedelta(seconds=int(self.runner.end - self.runner.start))
        output += "%d Finished, %d Error, %d Timeout in %s\n\n" % (len(tasks['FINISHED']), len(tasks['ERROR']), len(tasks['TIMEOUT']), execution_time)

        print(output)