# readme

This script sends a file (in this case called ```bigfile``` to a remote server via scp, and then redownloads the file to measure the total amount.

## Requirements
- Python 2.7 or higher
- Python Module paramiko (Install: ```$ pip install paramiko```)
- Python Module scp (Install: ```$ pip install scp```)
- Remote SSH server with scp connections enabled
- Unix host (to run dd and scp, both can also be run on Windows)


## Create file

To create a file of 151 KBytes, use this command on any Unix-Shell:

```
$ dd bs=500 count=310 if=/dev/random of=bigfile
```

This will generate a file of 151 KByte size with random data called ```bigfile```
