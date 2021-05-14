import argparse
import os
import sys
from pathlib import Path
import subprocess

def define_parser_with_arguments():
	description_text = "Prints different information about the given <PROCESS_ID> \
\nor if none given the current process.\n\
If no option is given it is assumed that\
all options were given."
 
	parser = argparse.ArgumentParser(description=description_text,
					formatter_class=argparse.RawDescriptionHelpFormatter,
					usage="%(prog)s [-h|--help] [-p|--pid] [-f|--homefolder] [<PROCESS_ID>]")

	parser.add_argument("-p", "--pid",type=int,
						help="Show a list of all the parent process ids of the given <PROCESS_ID>.")
	parser.add_argument("-f", "--homefolder", type=str,
						help="Show the path to the process owner‘s homefolder.")
	return parser.parse_args()


args = define_parser_with_arguments()

if args.homefolder:
	home = str(Path.home())
	print(home)

def get_parent_id(child_pid):
	pid_str = subprocess.run(["ps", "-o", "ppid=", "-p", "%i" %child_pid], capture_output=True, text=True)
	return int(pid_str.stdout)

if args.pid:
	current_pid = int(sys.argv[-1])
	all_pid = [current_pid]
	while True:
		if current_pid == 1:
			break
		try:
			current_pid = get_parent_id(current_pid)
		except(ValueError):
			print("Invalid Process ID")
			all_pid = []
			break

		all_pid.append(current_pid)
	print(all_pid)
