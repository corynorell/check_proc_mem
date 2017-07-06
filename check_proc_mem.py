#!/usr/bin/env python

import sys
import optparse
import resource
import subprocess
import tempfile 

__VERSION__ = '1.0.0'

pidlist = []

def parse_args():

    global options

    version = 'check_proc_mem.py, Version %s' %__VERSION__

    parser = optparse.OptionParser() 
    
    parser.add_option("-p", "--procname", help="The name of the process to be checked.")
    parser.add_option("-w", "--warning", default=None, help="Warning threshold value to be passed for the check.")
    parser.add_option("-c", "--critical", default=None, help="Critical threshold vlue to be passed for the check.")

    options, _ = parser.parse_args()    
	
    if not options.procname:
        parser.error("Process name is required for use")

#    if not options.warning:
#	parser.error("Warning threshold is required for use")

#    if not options.critical:
#	parser.error("Critical threshold is required for use")

    return options


def get_pids():

    output = tempfile.TemporaryFile()
    procname = options.procname

    proc = subprocess.Popen(['pgrep',procname], stdout=output)
    proc.wait()
    output.seek(0)

    for line in output.readlines():

        pid = line.strip()
        pidlist.append(pid)
        

    print pidlist

def get_rss_sum():

    output = tempfile.TemporaryFile()
    path = '/proc/3536/smaps'
    pid = 3536
    command = "cat /proc/3536/smaps | grep -e ^Rss: | awk '{print $2}'"
    memtotal = 0

    proc = subprocess.Popen(['cat',path], stdout=output)
    proc.wait()
    output.seek(0)

    for line in output.readlines():

        temp = subprocess.check_output(command,shell=True).split()

        for s in temp:
            memtotal += int(s)
        print memtotal
        break




def main():	
   
    options = parse_args()
    get_pids()

    for pid in pidlist:
        print pid

    #print options.procname



main()
