#!/usr/bin/env python3

from paramiko import SSHClient
from scp import SCPClient
import sys
from timeit import default_timer as timer

filename = 'outputfile_'

ssh = SSHClient()
ssh.load_system_host_keys()
ssh.connect('server')

with SCPClient(ssh.get_transport()) as scp:
    start = timer()
    for i in range(0,23):
        file=filename+str(i)
        scp.put(file)
        scp.get(file)
    end = timer()
    print(end - start)
