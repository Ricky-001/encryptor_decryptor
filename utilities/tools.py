#!/usr/bin/env python
import os, datetime

# clear screen
def clear():    
    os.system(['clear', 'cls'][os.name == 'nt'])

# check if a string variable is empty
def is_empty(var):    
    empty = False
    if len(str(var)) == 0:
        empty = True
    return empty
