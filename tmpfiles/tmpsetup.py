#Original code by Rob Cowie
#https://gist.github.com/robcowie/1054427
#Modified for use by Austin Fritzemeier
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import re
from getpass import getpass

replacements = {"name of Raspberry Pi account":"<<name of Raspberry Pi account>>", "path":"<<path>>", "phone number from which you will be sending commands -- including area code":"<<phone number from which you will be sending commands -- including area code>>", "email which Pi uses to receive texts":"<<email which Pi uses to receive texts>>", "password of email address":"<<password of email address>>", "IP of NodeJS server":"<<IP of NodeJS server>>", "port of NodeJS server":"<<port of NodeJS server>>", "name of SSID":"<<name of SSID>>"}
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
    elif placeholder == 'password of SSID':
        while True:
            password = getpass('Enter password for SSID: ')
            password2 = getpass('Retype password for SSID: ')
            if password == password2:
                return replacements.setdefault(placeholder, password)
            else:
                print "Passwords did not match"
    else:
        return replacements.setdefault(placeholder, raw_input('Enter %s: ' % placeholder))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=argparse.FileType('r'))
    parser.add_argument('outfile', type=argparse.FileType('w'))
    parser.add_argument('infile2', type=argparse.FileType('r'))
    parser.add_argument('outfile2', type=argparse.FileType('w'))
    parser.add_argument('infile3', type=argparse.FileType('r'))
    parser.add_argument('outfile3', type=argparse.FileType('w'))
    args = parser.parse_args()

    matcher = re.compile(pattern)

    for line in args.infile:
        new_line = matcher.sub(replace, line)
        args.outfile.write(new_line)

    args.infile.close()
    args.outfile.close()

    for line in args.infile2:
        new_line = matcher.sub(replace, line)
        args.outfile2.write(new_line)

    args.infile2.close()
    args.outfile2.close()

    for line in args.infile3:
        new_line = matcher.sub(replace, line)
        args.outfile3.write(new_line)

    args.infile3.close()
    args.outfile3.close()

if __name__ == '__main__':
    main()
