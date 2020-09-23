# readme

This script sends a file (in this case called ```bigfile``` to a remote server via scp, and then redownloads the file to measure the total amount.

## Purpose of the tool
The tool should measure the total roundtrip time in a lifecycle of one or multiple frames (data stream) when creating a volume image.

### General description of the workflow
A 3d-mapping device will create a gray scale raw data set which is forwarded to the processing host. After processing, which converts the two-dimensional data into a 3D Voxel-based model which can be viewed and virtually moved (rotate, pan, zoom etc.) by the user (dentist), the newly acquired dataset will be send back to the user's display.

The mapping device is operated manually by the user (dentist) and moved around the patient's jaw to map the structure. The dentist requires a near-realtime (≥100ms) feedback from when he moves the device to the time the movement is represented on the screen. 100ms has to be considered the absolute maximum since this already marks noticeable latency and hence poor user experience. 


## Script Requirements
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
