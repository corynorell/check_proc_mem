#!/usr/bin/env python

import sys
import optparse
import resource
import subprocess
import tempfile 

__VERSION__ = '1.0.0'

pidlist = []
memtotal = 0
low = 0
high = float('inf')
warning = ""
critical = ""
inclusive = False
alert = False
returncode = 1

def parse_args():

    global options

    version = 'check_proc_mem.py, Version %s' %__VERSION__

    parser = optparse.OptionParser() 
    
    parser.add_option("-P", "--procname", help="The name of the process to be checked.")
    parser.add_option("-w", "--warning", default=None, help="Warning threshold value to be passed for the check.")
    parser.add_option("-c", "--critical", default=None, help="Critical threshold vlue to be passed for the check.")
    parser.add_option("-u", "--units", default="kB", help="The unit prefix (k, Ki, M, Mi, G, Gi, T, Ti) for b and B unit types which calculates the value returned.")

    options, _ = parser.parse_args()    
	
    if not options.procname:
        parser.error("Process name is required for use")

    if not options.warning:
    	parser.error("Warning threshold is required for use")

    if not options.critical:
	    parser.error("Critical threshold is required for use")

    return options


def convert_units():
    
    global options
    global memtotal

    if options.units == "kb":
        memtotal = memtotal * 8
    elif options.units == "kB":
        memtotal = memtotal
    elif options.units == "kib":
        memtotal = memtotal * 7.8125
    elif options.units == "kiB":
        memtotal = memtotal * 0.976563
    elif options.units == "Mb":
        memtotal = memtotal * 0.008
    elif options.units == "MB":
        memtotal = memtotal * 0.001
    elif options.units == "mib":
        memtotal = memtotal * 0.00762939
    elif options.units == "miB":
        memtotal = memtotal * 0.000953674
    elif options.units == "Gb":
        memtotal = memtotal * 0.000008192
    elif options.units == "GB":
        memtotal = memtotal * 0.000000954
    elif options.units == "Gib":
        memtotal = memtotal * 0.00000074506
    elif options.units == "GiB":
        memtotal = memtotal * 0.00000093132
    elif options.units == "Tb":
        memtotal = memtotal * 0.000000007
    elif options.units == "TB":
        memtotal = memtotal * 0.0000000009313225746
    elif options.units == "Tib":
        memtotal = memtotal * 0.00000000727596
    elif options.units == "TiB":
        memtotal = memtotal * 0.00000000090949
    elif options.units == "nibble":
        memtotal = memtotal * 2048
    else:
        print "Please enter a valid unit and run check_proc_mem again"

def get_pids():

    output = tempfile.TemporaryFile()
    procname = options.procname

    proc = subprocess.Popen(['pgrep',procname], stdout=output)
    proc.wait()
    output.seek(0)

    for line in output.readlines():

        pid = line.strip()
        pidlist.append(pid)
        

def set_check_params():

    global warning
    global critical

    warning = options.warning
    critical = options.critical


def get_thresholds(param1):

    global low
    global high
    global inclusive

    string = param1

    if string[0] == "@":
        inclusive = True
        string = string[1:]

    brokenstring = string.split(':')
    if len(brokenstring) == 1:
        high = brokenstring[0]
    else:
        if brokenstring[0] == "~":
            low = 0
        else:
            low = brokenstring[0]
            try:
                if brokenstring[1] == "":
                    high = 9999999
                else:
                    high = brokenstring[1]
            except IndexError:
                high = 9999999
    
    # Turn strings into ints
    low = float(low)
    high = float(high)

def compare():

    global alert
    global memtotal
    global inclusive
    
    if inclusive == True:
        if low <= memtotal <= high:
            alert = True
        else:
            alert = False
    else:
        if (memtotal < low) or (memtotal > high):
            alert = True 
        else:
            alert = False


def get_rss_sum(arg1):

    output = tempfile.TemporaryFile()
    path = '/proc/%s/smaps' % (arg1)
    command = "cat /proc/%s/smaps | grep -e ^Rss: | awk '{print $2}'" % (arg1)

    ## Possibly better way to do this ## command = "cat /proc/%s/smaps | grep -e ^Rss: | awk '{sum += $2} END {print sum}'" % (arg1)
    
    global memtotal

    proc = subprocess.Popen(['cat',path], stdout=output)
    proc.wait()
    output.seek(0)


    for line in output.readlines():

        temp = subprocess.check_output(command,shell=True).split()

        for s in temp:
           memtotal += float(s)
        
        break

def create_return_data():
    
    userdata = "PROC_MEM %s - Current usage = %s %s" % (returncode, memtotal, units)
    perfdata = "proc_mem=%s %s;%s;%s;" % (memtotal, units, warning, critical)
    fulldata = "%s | %s" % (userdata, perfdata)

def main():	
   
    global returncode
    global options
    
    options = parse_args()
    get_pids()

    for pid in pidlist:
        get_rss_sum(pid)

    set_check_params()

    print "Current usage: %s kB" % (memtotal)

    get_thresholds(critical)
    convert_units()
    compare()

    print "Converted usage: %s %s" % (memtotal, options.units)    

    if alert == True:
        returncode = 2
    else:
        get_thresholds(warning)
        compare()
        if alert == True:
            returncode = 1
        else:
            returncode = 0    

    

main()
print returncode
sys.exit(returncode)
