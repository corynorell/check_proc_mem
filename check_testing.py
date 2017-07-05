#!/usr/bin/env python

import sys
import optparse
import resource
import subprocess
import tempfile

def main():
    
    output = tempfile.TemporaryFile()	
    procname = "httpd"    

    proc = subprocess.Popen(['pgrep',procname], stdout=output)
    proc.wait()
    output.seek(0)

    for line in output.readlines():
	
	pid = line.strip()
        

	#cat /proc/$pid/smaps | grep -m 1 -e ^Size: | awk '{print $2}' run this in Popen?

        print pid
        
    

main()
