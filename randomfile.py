#!/usr/bin/env python3

# Little script to create one or multiple files with random content of a
# specified size
# Written by Sebastian Varga

import os, sys

# Define filesize (153600 = 150 KBytes), amount of files to be created and
# and the prefix of the files.


filesize = 153600
fileamount = 24
fileprefix = 'outputfile_'

print ('Filesize is', filesize)
print ('amount of generated files:', fileamount)
print ('fileprefix is:', fileprefix)

for i in range (0, fileamount):
    filename = fileprefix+str(i+1)
    print(filename)
    with open(filename, 'wb') as fout:
        fout.write(os.urandom(filesize))
