#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import os
import shutil
import subprocess

"""Copy Special exercise
"""


def get_special_paths(dirs):
    specials = []
    for directory in dirs:
        files = os.listdir(directory)
        for filename in files:
            match = re.search("__\w+__", filename)
            if match:
                specials.append(os.path.abspath(filename))

    return specials


def copy_to(paths, target):
    if not os.path.exists(target):
        os.mkdir(target)
    for path in paths:
        shutil.copy(path, target)


def zip_to(paths, target):
    command = "zip -j zipfile"
    for path in paths:
        command += " " + path
    print("Command I'm going to do: " + command)
    code, output = subprocess.getstatusoutput(command)
    if code != 0:
        print(output)
        sys.exit(1)


def main():
    # This basic command line argument parsing code is provided.
    # Add code to call your functions below.

    # Make a list of command line arguments, omitting the [0] element
    # which is the script itself.
    args = sys.argv[1:]
    if not args:
        print("usage: [--todir dir][--tozip zipfile] dir [dir ...]")
        sys.exit(1)

    # todir and tozip are either set from command line
    # or left as the empty string.
    # The args array is left just containing the dirs.
    todir = ''
    if args[0] == '--todir':
        todir = args[1]
        del args[0:2]

    tozip = ''
    if args[0] == '--tozip':
        tozip = args[1]
        del args[0:2]

    if len(args) == 0:
        print("error: must specify one or more dirs")
        sys.exit(1)

    specials = get_special_paths(args)
    if not (todir or tozip):
        for special in specials:
            print(special)
    elif todir:
        copy_to(specials, todir)
    else:
        zip_to(specials, tozip)

if __name__ == "__main__":
    main()
