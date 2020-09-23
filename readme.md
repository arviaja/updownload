# readme

This script generates a predefined amount of files (variable ```fileamount```) at a predefined size (variable ```filesize```) and sends them to a host that you need to specify as input (fqdn or IP address) via scp, and then redownloads the file(s) to measure the total time elapsed to do so. During the process, it will generate the file(s) and will then remove after the process.

Time measured excludes the time to open the socket as well as file-generation and deletion. Only the actual up- and download time is measured.

## Script Requirements
- Python 2.7 or higher
- Python Module paramiko (Install: ```$ pip install paramiko```)
- Python Module scp (Install: ```$ pip install scp```)
- Remote SSH server with scp connections enabled

## Usage
```
$ python updownload.py <hostname|host_ip>
```
