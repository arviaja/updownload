#!/usr/bin/env python3

from multiprocessing import Pool, Process, Queue
from time import sleep
import argparse
from paramiko import SSHClient
from scp import SCPClient
import sys, glob, os
from timeit import default_timer as timer
import pickle

downloadPath = './down'
fileprefix = 'outputfile_'
fileamount = 100
nthreads = 5

def upDownSingleThreaded(scp):
    # loop through files. Upload, then download
    for i in range(0,fileamount):
        file = fileprefix+str(i)
        scp.put(file)
        scp.get(file, local_path=downloadPath)

def upDownMultiThreaded1(hostname, user, key_file, i):
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.connect(hostname, username=user, key_filename=key_file)
    scp = SCPClient(ssh.get_transport())

    file = fileprefix+str(i)
    scp.put(file)
    scp.get(file, local_path=downloadPath)

def upDownMultiThreaded2(hostname, user, key_file, queue):
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.connect(hostname, username=user, key_filename=key_file)
    scp = SCPClient(ssh.get_transport())

    file_id = queue.get()
    file = fileprefix+str(file_id)
    scp = SCPClient(ssh.get_transport())
    scp.put(file)
    scp.get(file, local_path=downloadPath)

def upDownMultiThreaded3(hostname, user, key_file, queue):
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.connect(hostname, username=user, key_filename=key_file)
    scp = SCPClient(ssh.get_transport())

    file_id = queue.get()
    while file_id >= 0:
        file = fileprefix+str(file_id)
        scp = SCPClient(ssh.get_transport())
        scp.put(file)
        scp.get(file, local_path=downloadPath)
        file_id = queue.get()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('hostname', help='remote machine to up- and download test files')
    parser.add_argument('-u', '--user', default=None, help='name of remote user')
    parser.add_argument('-k', '--key-file', default=None, help='path of private ssh key file')  
    parser.add_argument('-m', '--transfer-mode', help='0: single threaded scp, 1: single ssh client, multi-threaded, 2: multiple ssh clients, multi-threaded')  
    parser.add_argument('-c', '--keep-files', action='store_true', help='donnot clean up files after test')  
    args = parser.parse_args()

    hostname = args.hostname
    user = args.user
    key_file = args.key_file
    transfer_mode = int(args.transfer_mode)

    filesize = 153600

    print ('Filesize is', filesize)
    print ('amount of generated files:', fileamount)
    print ('fileprefix is:', fileprefix)
    print ('transfer mode is : %d' % transfer_mode)

    # Generate temporary test files with fixed size and random content
    print ('Generating random files...')
    for i in range (0, fileamount):
        filename = fileprefix + str(i)
        with open(filename, 'wb') as fout:
            fout.write(os.urandom(filesize))
    
    print('Start test...')
    # Define SSH connection to remote server. Remote host is defined by cmd-line input
    if transfer_mode == 0:
        start = timer()
        ssh = SSHClient()
        ssh.load_system_host_keys()
        ssh.connect(hostname, username=user, key_filename=key_file)
        scp = SCPClient(ssh.get_transport())
        upDownSingleThreaded(scp)
        end = timer()

    elif transfer_mode == 1:
        pre_start = timer()
        processes = []
        start = timer()
        for i in range(0,fileamount):
            job = Process(target = upDownMultiThreaded1, args=(hostname, user, key_file, i,) )
            job.start()
            processes.append(job)
            sleep(1./24.)      
        for job in processes:
            job.join()
        end = timer()

    elif transfer_mode ==2:
        pre_start = timer()
        queue = Queue()
        processes = []
        for i in range(0,fileamount):
            job = Process(target = upDownMultiThreaded2, args=(hostname, user, key_file, queue) )
            job.start()
            processes.append(job)

        start = timer()
        for i in range(0,fileamount):
            queue.put(i)
            sleep(1./24.)      

        for job in processes:
            job.join()
        end = timer()

    elif transfer_mode == 3:
        pre_start = timer()
        queue = Queue()
        processes = []
        for i in range(0,nthreads):
            job = Process(target = upDownMultiThreaded3, args=(hostname, user, key_file, queue) )
            job.start()
            processes.append(job)

        for i in range(0,nthreads):
            queue.put(i)
        sleep(nthreads)
        start = timer()
        for i in range(0,fileamount):
            queue.put(i)
            sleep(1./24.)      

        for job in processes:
            queue.put(-1)
        for job in processes:
            job.join()
        end = timer()

    else:
        print('Unknown transfer mode!')
        return

       
    print('Total time: %f' % (end-start))
    print('Average up- and download time per file: %f' % ((end - start)/fileamount))
    if transfer_mode > 0:
        print("Initialization of threads: %f" % (start-pre_start))

    # cleanup
    if not args.keep_files:
        try:
            fileList = glob.glob(fileprefix+'*')
            for filePath in fileList:
                os.remove(filePath)
                os.remove(downloadPath + '/' + filePath)
            ssh = SSHClient()
            ssh.load_system_host_keys()
            ssh.connect(hostname, username=user, key_filename=key_file)
            ssh.exec_command('rm %s*' % fileprefix)
        except:
            print("Error while deleting file : ", filePath)

if __name__=="__main__":
    main()
