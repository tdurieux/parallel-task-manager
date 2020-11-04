#!/usr/bin/env python

import argparse
from core.ExecuteRunner import TaskRunner
from core.Task import Task



if __name__ == "__main__":
  parser = argparse.ArgumentParser(prog="Runner", description='Handle parallel execution')
  parser.add_argument("--path", "-f", required=True, help="The path the the file that contains a command per line")
  parser.add_argument("--process", "-p", required=True, help="The number of parallel process", type=int)
  parser.add_argument("--timeout", "-t", help="The maximum execution time (in sec)", type=int, default=None)

  args = parser.parse_args()

  tasks = []
  with open(args.path, 'r', encoding="utf8") as fd:
    content = fd.read()
    for line in content.split("\n"):
      tasks.append(Task(line))
  runner = TaskRunner(tasks, args)
  runner.execute()