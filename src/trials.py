# -*- coding: utf-8 -*-
"""
Zaber Motion ASR100B120B-T3 Stage Trials
========================================
Contributors: Christian Sargusingh
Date: 2020-04-11
Repository: https://github.com/cSDes1gn/stage-trials
README available in repository root
Version: 1.0

Using X-MCB2 controller

Dependencies
------------
>>> from zaber_motion import Library 
>>> from zaber_motion.ascii import Connection
 
Copyright © 2020 Incuvers, Inc - All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
"""
from zaber_motion import Library 
from zaber_motion.ascii import Connection

Library.toggle_device_db_store(True)

# open serial port
with Connection.open_serial_port("/dev/ttyACM0") as conn:
    pass
