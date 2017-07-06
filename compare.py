#!/usr/bin/env python

import sys
import optparse
import resource
import subprocess
import tempfile


warning = 100
critical = 200
measure = 250

def get_thresholds():

    string = "123:456"
    brokenstring = string.split(':')
    lowval = brokenstring[0]
    highval = brokenstring[1]
    print lowval
    print highval
   
     

get_thresholds()
        
