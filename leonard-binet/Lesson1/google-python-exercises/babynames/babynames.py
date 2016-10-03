# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
from html.parser import HTMLParser

"""Baby Names exercise

Define the extract_names() function below and change main()
to call it.

For writing regex, it's nice to include a copy of the target
text for inspiration.

Here's what the html looks like in the baby.html files:
...
<h3 align="center">Popularity in 1990</h3>
....
<tr align="right"><td>1</td><td>Michael</td><td>Jessica</td>
<tr align="right"><td>2</td><td>Christopher</td><td>Ashley</td>
<tr align="right"><td>3</td><td>Matthew</td><td>Brittany</td>
...

Suggested milestones for incremental development:
-Extract the year and print it
-Extract the names and rank numbers and just print them
-Get the names data into a dict and print it
-Build the [year, 'name rank', ... ] list and print it
-Fix main() to use the extract_names list
"""

regex_h3 = re.compile('<h3 align="center">Popularity in (\\d+)</h3>')
regex_rank_names = re.compile('<tr align="right"><td>(\\d+)</td><td>(\\w+)</td><td>(\\w+)</td>')

def extract_names(filename):
    """
    Given a file name for baby.html, returns a list starting with the year string
    followed by the name-rank strings in alphabetical order.
    ['2006', 'Aaliyah 91', Aaron 57', 'Abagail 895', ' ...]
    """

    result = []
    found_year = False

    for line in open(filename, 'r'):
        if not found_year:
            year = regex_h3.search(line)
            if year:
                result.append(str(year.group(1)))
                found_year = True

        else:
            rank_names = regex_rank_names.search(line)
            if rank_names:
                rank = rank_names.group(1)
                result.append(rank_names.group(2) + ' ' + rank)
                result.append(rank_names.group(3) + ' ' + rank)

    return [result[0]] + sorted(result[1:])

def main():
    # This command-line parsing code is provided.
    # Make a list of command line arguments, omitting the [0] element
    # which is the script itself.
    args = sys.argv[1:]

    if not args:
        print('usage: [--summaryfile] file [file ...]')
        sys.exit(1)

    # Notice the summary flag and remove it from args if it is present.
    summary = False
    if args[0] == '--summaryfile':
        summary = True
        del args[0]

    print(extract_names(args[1]))

    # +++your code here+++
    # For each filename, get the names, then either print the text output
    # or write it to a summary file

if __name__ == '__main__':
    main()
