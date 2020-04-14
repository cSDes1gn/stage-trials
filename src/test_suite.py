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
>>> import random
>>> import time
>>> import unittest

>>> import interface
 
Copyright © 2020 Incuvers, Inc - All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
"""
import random
import time
import unittest

import interface


class Assertions:
    """Test case assertions"""
    SPEED_TEST = 85
    MAX_RANGE_X = 100
    MAX_RANGE_Y = 100
    MICRON_ACC = 0.04

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
            self.actrl.isoaxial_scan(i,Assertions.SPEED_TEST)
            time.sleep(1)
            with self.subTest(i=i):
                finish = self.actrl.get_position(i)
                self.assertEqual(finish,Assertions.SPEED_TEST)

    def test_max_diaxial_speed(self):
        # XY di-axial tests (simultaneous runtime)
        self.actrl.set_max(1)
        self.actrl.set_max(2)
        self.actrl.diaxial_scan(Assertions.SPEED_TEST,Assertions.SPEED_TEST)
        time.sleep(1)
        self.assertEqual(self.actrl.get_position(1),Assertions.SPEED_TEST)
        self.assertEqual(self.actrl.get_position(2),Assertions.SPEED_TEST)
        
    def test_accuracy_rating(self):
        # Accuracy rating
        for i in range(100):
            with self.subTest(i=i):
                # rouding to µm level accuracy
                x_c = round(random.random(0, Assertions.MAX_RANGE_X-1)+random.random(),3)
                y_c = round(random.random(0, Assertions.MAX_RANGE_Y-1)+random.random(),3)
                self.actrl.diaxial_scan(x_c, y_c)
                x_r = self.actrl.get_position(1)
                y_r = self.actrl.get_position(2)
                self.assertTrue(abs(x_c-x_r) <= Assertions.MICRON_ACC and 
                                abs(y_c-y_r) <= Assertions.MICRON_ACC)

    def test_precision_rating(self):
        raise NotImplementedError
        
if __name__ == "__main__":
    # launch test cases
    unittest.main()
