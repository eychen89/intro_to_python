#!/usr/bin/env python

"""
This program was created for the final project.

This program will take a LicResults.txt file obtained from Tableau Server's
licensing results and creates a batch file which contains all of the commands
required to delete any license keys containing a "**BROKEN** HOST" trust flag.

The following arguments must be specified when running the command:
arg1: full file path for the LicResults.txt file
arg2: full file path for the output.bat file
"""

import sys

first_arg = sys.argv[1]
second_arg = sys.argv[2]
infile = first_arg
fid = []
hosts = []
keep_fid = ['Fulfillment ID']
keep_flags = ['Trust Flags']


# The parsefile function is used to read the file and strip out matching entries into a list
def parsefile():
    # Exception handling for errors related to the LicResults.txt file
    try:
        with open(infile) as f:
            f = f.readlines()
    except:
        print("There was an error reading the LicResults.txt file.")

# Strips out "Fulfillment ID:" from each matching entry and appends to the fid list
    for line in f:
        for value in keep_fid:
            if value in line:
                lines = line.replace('Fulfillment ID: ', '')
                fid.append(lines.rstrip())

# Strips out "Trust Flags:" from each matching entry and appends to the flags list
    for line in f:
        for value in keep_flags:
            if value in line:
                lines = line.replace('Trust Flags: ', '')
                hosts.append(lines.rstrip())

# The lencomp function compares the length of the fid and hosts list to make sure they match
def lencomp():
    if len(fid) == len(hosts):
        zipped = dict(zip(fid, hosts))
        return zipped
    else:
        print("The number of entries in the hosts and fid lists do not match!")

# The removeflags function requires a dictionary input (zipped) and outputs a dictionary with irrelevant values removed.
def removeflags(zipped):
# Uses dictionary comprehension in order to remove any key/value pair without "**BROKEN** HOST" trust flag
    removed_dict = {k:v for k,v in zipped.items() if v == '**BROKEN** HOST'}
    return removed_dict

# The writeoutput function requires a dictionary input (removed_dict) and will create a batch file output.
def writeoutput(removed_dict):
# Opens a new batch file and writes commands used to delete any fulfillments with "**BROKEN** HOST" trust flag.
    with open(second_arg, "w") as f:
        for key in removed_dict:
            f.write("START /WAIT serveractutil -delete " + key + "\n")
        print(f"Batch file {second_arg} has been created to delete broken fulfillments.")

def main():
    parsefile()
    zipped = lencomp()
    removed_dict = removeflags(zipped)
    writeoutput(removed_dict)

if __name__ == '__main__':
    main()