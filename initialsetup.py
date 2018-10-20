#Original code by Rob Cowie
#https://gist.github.com/robcowie/1054427
#Modified for use by Austin Fritzemeier
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import os
import re
from getpass import getpass

replacements = {}
pattern = '<<([^>]*)>>'


def replace(match):
    cwd = os.getcwd()
    ## Pull from replacements dict or prompt
    placeholder = match.group(1)
    if placeholder in replacements:
        return replacements[placeholder]
    ## .setdefault(key, value) returns the value if present, else sets it then returns
    if placeholder == 'path':
        return replacements.setdefault(placeholder, cwd)
    elif placeholder == 'password of email address':
        while True:
            password = getpass('Enter password for email address: ')
            password2 = getpass('Retype password for email address: ')
            if password == password2:
                return replacements.setdefault(placeholder, password)
            else:
                print "Passwords did not match"
    elif placeholder == 'password to SSID':
        while True:
            password3 = getpass('Enter password for the router: ')
            password4 = getpass('Retype password for router: ')
            if password3 == password4:
                return replacements.setdefault(placeholder, password3)
            else:
                print "Passwords did not match"
    else:
        return replacements.setdefault(placeholder, raw_input('Enter %s: ' % placeholder))


def main():

    infiles = []
    outfiles = []

    k = 1
    for x in sys.argv[1:]:
	if k % 2 == 1:
		infiles.append(x)
	elif k % 2 == 0:
		outfiles.append(x)
	k = k + 1

    matcher = re.compile(pattern)

    k = 0
    for i in infiles:
	iname = open(i,'r')
	oname = open(outfiles[k], 'w')

	for line in iname:
		new_line = matcher.sub(replace, line)
		oname.write(new_line)

	iname.close()
	oname.close()
        k = k + 1

if __name__ == '__main__':
    main()
