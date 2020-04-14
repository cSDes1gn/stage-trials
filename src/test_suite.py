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
import statistics as stats

import interface


class Assertions:
    """Test case assertions"""
    SPEED_TEST = 85
    MAX_RANGE_X = 100
    MAX_RANGE_Y = 100
    MICRON_ACC = 0.002

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
            self.actrl.set_speed(i, Assertions.SPEED_TEST)
            self.actrl.isoaxial_scan(i,Assertions.SPEED_TEST)
            time.sleep(1)
            with self.subTest(i=i):
                finish = self.actrl.get_position(i)
                self.assertEqual(finish,Assertions.SPEED_TEST)

    def test_max_diaxial_speed(self):
        # XY di-axial tests (simultaneous runtime)
        self.actrl.set_speed(1, Assertions.SPEED_TEST)
        self.actrl.set_speed(2, Assertions.SPEED_TEST)
        self.actrl.diaxial_scan(Assertions.SPEED_TEST,Assertions.SPEED_TEST)
        time.sleep(1)
        self.assertEqual(self.actrl.get_position(1),Assertions.SPEED_TEST)
        self.assertEqual(self.actrl.get_position(2),Assertions.SPEED_TEST)
        
    def test_accuracy_rating(self):
        # Accuracy rating
        self.actrl.set_speed(1, Assertions.SPEED_TEST/2)
        self.actrl.set_speed(2, Assertions.SPEED_TEST/2)
        data_x, data_y = list(), list()
        for i in range(100):
            with self.subTest(i=i):
                # rouding to µm level accuracy
                x_c = round(random.randint(0, Assertions.MAX_RANGE_X-1)+random.random(),3)
                y_c = round(random.randint(0, Assertions.MAX_RANGE_Y-1)+random.random(),3)
                # set wait flag until idle
                self.actrl.diaxial_scan(x_c, y_c, True)
                x_r = self.actrl.get_position(1)
                y_r = self.actrl.get_position(2)
                data_x.append(abs(x_c-x_r))
                data_y.append(abs(y_c-y_r))
                # for variance
                if len(data_x) == 100:
                    print("Variance in x: {}".format(stats.variance(data_x)))
                    print("Std deviation in x: {}".format(stats.stdev(data_x)))
                    print("Mean in x: {}".format(stats.stdev(data_x)))
                    print("Variance in y: {}".format(stats.variance(data_y)))
                    print("Std deviation in y: {}".format(stats.stdev(data_y)))
                    print("Mean in y: {}".format(stats.mean(data_y)))
                self.assertTrue(abs(x_c-x_r) <= Assertions.MICRON_ACC and 
                                abs(y_c-y_r) <= Assertions.MICRON_ACC)

if __name__ == "__main__":
    # launch test cases
    unittest.main()
