#!/usr/bin/env python3

from paramiko import SSHClient
from scp import SCPClient
import sys, glob, os
from timeit import default_timer as timer

hostname = str(sys.argv[1])
filesize = 153600
fileamount = 24
fileprefix = 'outputfile_'

print ('Filesize is', filesize)
print ('amount of generated files:', fileamount)
print ('fileprefix is:', fileprefix)


# Generate temporary test files with fixed size and random content
print ('Generating random files...')
for i in range (0, fileamount):
    filename = fileprefix+str(i+1)
    with open(filename, 'wb') as fout:
        fout.write(os.urandom(filesize))


# Define SSH connection to remote server. Remote host is defined by cmd-line input
ssh = SSHClient()
ssh.load_system_host_keys()
ssh.connect(hostname)

# Open SSH-Socket
with SCPClient(ssh.get_transport()) as scp:
    start = timer()
    # loop through files. Upload, then download
    for i in range(0,23):
        file = fileprefix+str(i+1)
        scp.put(file)
        scp.get(file)
    end = timer()
    print(end - start)


# cleanup
fileList = glob.glob(fileprefix+'*')
for filePath in fileList:
    try:
        os.remove(filePath)
    except:
        print("Error while deleting file : ", filePath)
