#!/usr/bin/env python

import argparse
from core.ExecuteRunner import TaskRunner
from core.Task import Task



if __name__ == "__main__":
  parser = argparse.ArgumentParser(prog="Runner", description='Handle parallel execution')
  parser.add_argument("--path", "-f", required=True, help="The path the the file that contains a command per line")
  parser.add_argument("--process", "-p", required=True, help="The number of parallel process", type=int)
  parser.add_argument("--timeout", "-t", help="The maximum execution time (in sec)", type=int, default=None)
  parser.add_argument("--gpu", help="The processes are using a CPU", action='store_true', default=False)


  args = parser.parse_args()
  print(args.gpu)
  tasks = []
  with open(args.path, 'r', encoding="utf8") as fd:
    content = fd.read()
    for line in content.split("\n"):
      if len(line.strip()) == 0:
        continue
      tasks.append(Task(line, with_gpu=args.gpu))
  runner = TaskRunner(tasks, args)
  runner.execute()
  