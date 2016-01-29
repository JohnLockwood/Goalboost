#!/usr/bin/env python3

'''
By the way, on windows that line above proabably needs to be
#!/usr/bin/env python3

This python script really doesn't do much yet, but it is the starting point for a utility
that will provide a timer "wrapper" around the git command line.  
'''

import argparse
import os
import configparser

# Classes that implement more complex tasks

class GitboostInit:
	static 

# S
APP_NAME = "Gitboost"

def start_timer():
	print("Starting...")

def stop_timer():
	print("Stopping...")

def commit_timer(message):
	print("Committing with message = " + message)

def init_gb():
	print("Initializing gb directory.")

def commit_timer(message):
	print("Committing with message = " + message)

parser = argparse.ArgumentParser(description='A task timer for GIT.')

subparsers = parser.add_subparsers(help='sub-command help', dest='subparser_name') # (help='sub-command help')

# Could be a dict and a loop
parser_start = subparsers.add_parser('start', help='start a timer')
parser_start.set_defaults(func=start_timer)

parser_stop = subparsers.add_parser('stop', help='stop a timer')
parser_stop.set_defaults(func=stop_timer)

parser_stop = subparsers.add_parser('init', help='Initialize ' + APP_NAME +  " database")
parser_stop.set_defaults(func=init_gb)


parser_commit = subparsers.add_parser('commit', help='commits work, setting note in git message and for timer')
# Needs a --note argument
parser_commit.add_argument('-m', '--message', metavar='', type=str, default="", help="must be set at some point before committing")
parser_commit.set_defaults(func=commit_timer)

args = parser.parse_args()
# DEBUG ONLY:  print(args)

if args.subparser_name == 'commit':
	args.func(args.message)
elif args.subparser_name is not None:
	args.func()
else:
	parser.print_help()

