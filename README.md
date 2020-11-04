# Parallel Task Manager

Parallel Task Manager is a utility package that helps to parallelize tasks on a simple node.

## Usage
1. Create a file that contains all the command line that you need to execute. Each line represent a task
2. parallel-task-manager.py -f <path_to_the_file> -p <number of process> [--timeout <timeout in sec>]

```
usage: parallel-task-manager.py [-h] --path PATH --process PROCESS [--timeout TIMEOUT]

Handle parallel execution

optional arguments:
  -h, --help            show this help message and exit
  --path PATH, -f PATH  The path the the file that contains a command per line
  --process PROCESS, -p PROCESS
                        The number of parallel process
  --timeout TIMEOUT, -t TIMEOUT
                        The maximum execution time (in sec)
```