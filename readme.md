# readme

This script sends one or multiple files defined in the script to a remote server via scp, and then redownloads the file to measure the total time elapsed to do so amount.

## Script Requirements
- Python 2.7 or higher
- Python Module paramiko (Install: ```$ pip install paramiko```)
- Python Module scp (Install: ```$ pip install scp```)
- Remote SSH server with scp connections enabled

## Create file(s)

To create a set of random binary files of a certain size (all equally big), use the script randomfile.py in this folder. Adapt the parameters according to your needs in the script.

## Usage
Make sure the files to be up and downloaded are placed in the root folder. Make sure you change the parameter ```filename``` in the script ```updownload.py``` to match the filename (if you're using one file) or the prefix pattern (if you're using multiple files) which you have generated with the script ```randomfile.py```.
