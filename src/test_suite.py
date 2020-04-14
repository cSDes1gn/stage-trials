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
import unittest
import time
import interface


class Assertions:
    """Test case assertions"""
    ISO = 85
    DI = 60.1 # by pythagoran theorem and scaling by a factor of 0.5 so the trial fits

class TestSuite(unittest.TestCase):

    def setUp(self):
        # homes all axes to (0,0) in init so measurements are based off this ref
        self.actrl = interface.AutomatedController()

    def tearDown(self):
        # close resource
        self.actrl.shutdown()

    def test_max_isoaxial_speed(self):
        # Isoaxial tests X and Y
        for i in range(1,3):
            self.actrl.set_max(i)
            self.actrl.isoaxial_scan(i,Assertions.ISO)
            time.sleep(1)
            with self.subTest(i=i):
                finish = self.actrl.get_position(i)
                self.assertEqual(finish,Assertions.ISO)

    def test_max_diaxial_speed(self):
        # XY di-axial tests (simultaneous runtime)
        self.actrl.set_max(1)
        self.actrl.set_max(2)
        self.actrl.diaxial_scan(Assertions.ISO)
        time.sleep(1) # scaled by a factor of 0.5
        self.assertEqual(self.actrl.get_position(1),Assertions.ISO)
        self.assertEqual(self.actrl.get_position(2),Assertions.ISO)

if __name__ == "__main__":
    # launch test cases
    unittest.main()
