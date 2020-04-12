# X-MCB2 Controller Interface Setup

## Setup for Python3
1. Ensure `python3` and `pip3` are update to install `zaber-motion` pkg.
```bash
$ pip3 install --user zaber-motion
```

2. A basic integration test is provided by Zaber [here](https://www.zaber.com/software/docs/motion-library/ascii/tutorials/initialize/) and [here](https://www.zaber.com/software/docs/motion-library/ascii/tutorials/open_port/)

```python
from zaber_motion import Library 
from zaber_motion.ascii import Connection
Library.toggle_device_db_store(True)

# open serial port
with Connection.open_serial_port("/dev/ttyACM0") as conn:
    print("Found {} devices".format(conn.detect_devices()))
```
3. Save as `trials.py` and execute

```bash
ubuntu@ubuntu:~/stage-trials/src$ python3 trials.py
Found [Device 1 SN: 64167 (X-MCB2) -> Connection 1 (ASCII Serial port: /dev/ttyACM0)] devices
```
4. Verfiy `SN` matches name and ID of the connected controller. 



