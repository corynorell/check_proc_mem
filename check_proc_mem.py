#!/usr/bin/env python

import sys
import optparse
import resource

__VERSION__ = '1.0.0'

def parse_args():

    options = dict()

    version = 'check_proc_mem.py, Version %s' %__VERSION__

    parser = optparse.OptionParser() 
    
    parser.add_option("-p", "--procname", help="The name of the process to be checked.")
    parser.add_option("-w", "--warning", default=None, help="Warning threshold value to be passed for the check.")
    parser.add_option("-c", "--critical", default=None, help="Critical threshold vlue to be passed for the check.")

    options, _ = parser.parse_args()    
	
    if not options.procname:
        parser.error("Process name is required for use")

    if not options.warning:
	parser.error("Warning threshold is required for use")

    if not options.critical:
	parser.error("Critical threshold is required for use")

    return options

def get_memory_usage():


def main():
	
   
    options = parse_args()

    print options.procname

main()
