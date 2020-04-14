# -*- coding: utf-8 -*-
"""
Zaber Motion Motion Control Wrapper
===================================
Contributors: Christian Sargusingh
Date: 2020-04-11
Repository: https://github.com/cSDes1gn/stage-trials
README available in repository root
Version: 1.0

Using X-MCB2 controller using Zaber Motion Library (ASCII)

Dependencies
------------
>>> from zaber_motion import Library 
>>> from zaber_motion.ascii import Connection
 
Copyright © 2020 Incuvers, Inc - All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
"""

from zaber_motion import Library
from zaber_motion import Units
# from zaber_motion import Measurement
from zaber_motion.ascii import Connection
# for synchronized axis motion
# A handle for a stream with this ID on the device. Streams provide a way to execute or store a
# sequence of actions. Stream methods append actions to a queue which executes or stores actions 
# in a first in, first out order.
# from zaber_motion.ascii import Stream
# from zaber_motion.ascii import StreamMode

import cv2

class bcolors:
    """Class defining escape sequences for terminal color printing"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class constants:
    """constants class"""
    STREAM_ID = 1
    V_PORT = -1
    FRAME_HEIGHT = 1920
    FRAME_WIDTH = 1080
    SERIAL_PORT = "/dev/ttyACM0"

class VideoStream:
    """Class `VideoStream` is a custom wrapper for the `VideoCapture` object for image capture from
    a USB camera. OpenCV takes 20x longer to read a frame than expected on the initial 
    capture. To eliminate this delay `VideoStream` initialization polls the read() method to verify
    the status of the video port. 
 
    Attributes:
     - `_buffer` (`list`): list buffered image captures as a pixel matrix.
     - `_stream` (`VideoCapture`): object reference for `cv2.VideoCapture`
     - `_status` (`bool`): `VideoCapture` video port operational status (refreshed per read())
    """
    def __init__(self):
        """Initialize empty buffer and `VideoCapture` object at specified port. The capture
        resolution is set by values as described in the constants class. Finally the microscope is
        polled for status verification and flushing the response time transient spike.
        """
        self._buffer = list()
        self._stream = cv2.VideoCapture(constants.V_PORT)
        # 1080p resolution recommended for better contour detection results
        self._stream.set(cv2.CAP_PROP_FRAME_HEIGHT,constants.FRAME_HEIGHT)
        self._stream.set(cv2.CAP_PROP_FRAME_WIDTH,constants.FRAME_WIDTH)
        # initial video capture poll
        self._status = True
 
    def read(self):
        """Reads an image capture from a LIFO buffer. Introduced blocking method until frame buffer 
        has data to read Python lists are inherently thread safe objects so modifying the buffer for
        multiple read() events will not cause any race conditions.
        """
        while not self._buffer:
            pass
        return self._buffer.pop(0)

    def stop(self):
        """Releases the `VideoCapture` object resources shutting down the port connection.
        """
        self._stream.release()
        print("Released stream resources.")
 
    def capture(self):
        """Captures a frame from the camera and stores into the `VideoStream` buffer for analysis.
        For each capture poll the status of the `_stream` object and update the status.
        
        Raises:
         - `IOError`: if the `VideoCapture` port status is `False` after the capture is taken.
        """
        # First verify initial capture status and update with subsequent capture results
        if self._status:
            self._status, frame = self._stream.read()
            print("Capture Complete")
            print(frame)
            self._buffer.append(frame)
        else:
            print(bcolors.FAIL + "VideoCapture status failure..\t" + bcolors.ENDC + "Exiting")
            raise IOError


class AutomatedController():

    def __init__(self):
        # The next time the library needs the database it will contact the web-service and save
        # the obtained data to the file system. When the library requires data later on, it uses the 
        # saved files instead of the web-service.
        Library.toggle_device_db_store(True)
        print("Initializing connection at " + constants.SERIAL_PORT)
        self.conn = Connection.open_serial_port(constants.SERIAL_PORT)
        self.device = self.conn.detect_devices()[-1]
        print("Found {} controller with id {}".format(self.device.name, self.device.serial_number))
        print("Homing all axes of {} peripheral device.. ".format(self.device.get_axis(1).peripheral_name))
        self.device.all_axes.home()

    def isoaxial_scan(self,axis_id, disp):
        axis = self.device.get_axis(axis_id)
        axis.move_absolute(disp, Units.LENGTH_MILLIMETRES, wait_until_idle=False)
    
    def diaxial_scan(self, disp1, disp2, wait_flag=False):
        axis1 = self.device.get_axis(1)
        axis2 = self.device.get_axis(2)
        axis1.move_absolute(disp1, Units.LENGTH_MILLIMETRES, wait_until_idle=False)
        axis2.move_absolute(disp2, Units.LENGTH_MILLIMETRES, wait_until_idle=False)
        # for accuracy and precision testing
        if wait_flag:
            axis1.wait_until_idle()
            axis2.wait_until_idle()
    
    def orbital_scan(self):
        raise NotImplementedError

    def square_scan(self):
        raise NotImplementedError

    def set_speed(self, axis_id, speed):
        self.device.get_axis(axis_id).settings.set("maxspeed", speed,
            Units.VELOCITY_MILLIMETRES_PER_SECOND)

    def get_position(self, axis_id):
        return self.device.get_axis(axis_id).get_position(Units.LENGTH_MILLIMETRES)

    def shutdown(self):
        # home
        self.device.all_axes.home()
        # shutdown connection
        self.conn.close()


if __name__ == "__main__":
    # show the output image
    # microscope = VideoStream()
    # microscope.capture()
    pass