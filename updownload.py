#!/usr/bin/env python3

from multiprocessing import Pool
from time import sleep
import argparse
from paramiko import SSHClient
from scp import SCPClient
import sys, glob, os
from timeit import default_timer as timer

fileprefix = 'outputfile_'
fileamount = 24

def upDownSingleThreaded(scp):
    # loop through files. Upload, then download
    for i in range(0,fileamount):
        file = fileprefix+str(i)
        scp.put(file)
        scp.get(file)

def upDownMultiThreaded(scp, i):
    # loop through files. Upload, then download
    file = fileprefix+str(i)
    scp.put(file)
    scp.get(file)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('hostname', help='remote machine to up- and download test files')
    parser.add_argument('-u', '--user', default=None, help='name of remote user')
    parser.add_argument('-k', '--key-file', default=None, help='path of private ssh key file')  
    parser.add_argument('-t', '--threads', action='store_true', help='if set, use multiple threads')  
    args = parser.parse_args()

    hostname = args.hostname
    user = args.user
    key_file = args.key_file

    filesize = 153600

    print ('Filesize is', filesize)
    print ('amount of generated files:', fileamount)
    print ('fileprefix is:', fileprefix)


    # Generate temporary test files with fixed size and random content
    print ('Generating random files...')
    for i in range (0, fileamount):
        filename = fileprefix+str(i)
        with open(filename, 'wb') as fout:
            fout.write(os.urandom(filesize))

    # Define SSH connection to remote server. Remote host is defined by cmd-line input
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.connect(hostname, username=user, key_filename=key_file)

    pre_start = timer()
    pool = Pool(10)
    start = timer()
    if args.threads:
        for i in range(0,fileamount):
            pool.apply_async(upDownMultiThreaded, [SCPClient(ssh.get_transport()), i])
            sleep(1./24.)
        pool.close()
        pool.join()
    else:
        upDownSingleThreaded(SCPClient(ssh.get_transport()))
    end = timer()

    print('Total time: %f' % (end-start))
    print('Average up- and download time per file: %f' % ((end - start)/fileamount))
    if args.threads:
        print("Initialization of threads: %f" % (start-pre_start))

    # cleanup
    fileList = glob.glob(fileprefix+'*')
    for filePath in fileList:
        try:
            os.remove(filePath)
            ssh.exec_command('rm %s' % filePath)
        except:
            print("Error while deleting file : ", filePath)

if __name__=="__main__":
    main()
