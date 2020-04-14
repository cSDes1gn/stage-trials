# Validation Tests

## Background

The abstracted specification for this model (pulled from [here](https://www.zaber.com/products/scanning-microscope-stages/ASR/details/ASR100B120B-T3)) are shown in the table below:


| ASR100B120B-T3 Relevant Properties  | Specification 
|-------------------------------------|-------------------|
| Microstep Size (Default Resolution) | 0.15625 µm        |
| Y Travel Range                      | 100 mm            |
| X Travel Range                      | 120 mm            |
| Accuracy (unidirectional)           | 40 µm             |
| Repeatability                       | < 2 µm            |
| Maximum Speed (@ low system load)   | 85 mm/s           |
| Minimum Speed                       | 0.000095 mm/s     |
| Motor Steps Per Rev                 | 200               |
| Motor Type                          | Stepper (2 phase) |
| Default Resolution                  | 1/64 of a step    |

>**unidirectional accuracy:** The maximum error possible when moving between any two positions, when both positions are approached from the same direction.

> **repeatability:** The maximum deviation in actual position when repeatedly instructing a device to move to a target position 100 times, approaching from the same direction every time, under stable thermal conditions.

## Stage Accuracy (Unidirectional Accuracy) and Precision Tests (Repeatability)
> Unidirectional accuracy claim of > 40μm

> Repeatability claim of > 2μm

The range of motion in the X and Y direction is described in the table above from the online specification. The test involves randomly selecting coordinate pairs of floats in mm to a precision of 3 decimal places. This corresponds to enabling movement to each µm on the coordinate grid. The device is executed to move to each coordinate on the plane then the stage position is measured by the encoders to verify its actual position. The `axis` objects `get_position()` method returns a float to 6 decimal places which is more than sufficient to validate both the claims.

The test was run over 100 randomly selected coordinate pairs. The absolute value of the difference between the requested and expected coordinates were seperated by the x and y motors running at half of their maximum graded speed at 42.5 mm/s. The analytics are compiled below:

|   | Standard Deviation | Variance  | Mean (mm) |
|---|--------------------|-----------|-----------|
| x | 2.393e-05          | 5.725e-10 | 2.393e-05 |
| y | 2.143e-05          | 4.593e-10 | 3.500e-05 |

Furthermore, to validate the claims hold while operating at its maximum speed rating of 85 mm/s we ran the same test case over a new 100 trials and compiled the results:

|   | Standard Deviation | Variance  | Mean (mm) |
|---|--------------------|-----------|-----------|
| x | 2.324e-05          | 5.401e-10 | 2.324e-05 |
| y | 2.281e-05          | 5.204e-10 | 3.688e-05 |

The steppers both far exceed the claims based on the collected data. Over the 100 trials for both speed ratings all test cases passed both the repeatability and accuracy specifications. Furthermore sinc the results for both the 42.5mm/s and the 85mm/s test are very similar we can conclude that the accuracy and repeatability tests continue to pass while operating variable speeds.

## Stage Motion Execution Time
> **Isoaxial Measurements:** Measure velocity vector for a basic linear motor command at maximum specification.

>**Diaxial Measurements:** Measure net velocity vector for a set of equally distributed, synchonized motor commands at maximum specification.

### Test Case 1: Isoaxial validation

For the first test I isolated each stepper and configured the motors to a speed of 85 mm/s according to the maximum rating given by the online specification. I executed commands to have the motor travel from the origin (0,0) to a displacement 85 mm in the motor control direction. 1 second after execution, I measure the net displacement of the stage from the origin. I ran 5 trials for each of the stepper motors and the compiled the net speed results:

| Trial | Large Platform Net Speed (mm/s) | Small Platform Net Speed (mm/s) |
|-------|---------------------------------|---------------------------------|
| 1     | 67.48                           | 67.45                           |
| 2     | 67.49                           | 67.45                           |
| 3     | 67.37                           | 67.45                           |
| 4     | 67.47                           | 67.47                           |
| 5     | 67.48                           | 67.47                           |

| Variance | Standard Deviation |
|----------|--------------------|
| 0.00115  | 0.03393            |

The individual steppers do not meet the validated claims of 85 mm/s. I predict the speed they are referring to is the maximum instantaneous velocity and not its aggregate speed. I checked the definition for 'maximum speed' online and it yielded this:

>[**Maximum Speed:**](https://www.zaber.com/glossary) The maximum speed at which a motorized device can move. Note that the speed is a function of load and the maximum speed can only be achieved at low loads.	(mm/s, "/s)

However, judging by audio queues, the motors seem to achieve its peak midway through the execution but slows back down as it approaches the specified distance. This is probably in place to reduce the stress on the motors. Stepper motors are susceptible to performance wear as they have a larger number of motor step positions (which allows for increased precision)so this makes sense. I ran some tests for shorter intervals to backup my prediction and saw diminishing returns in speed performance as the length decreased.

### Test Case 2: Di-axial validation
For the second test I scheduled execution for both steppers simultaneously. All the measurement setup was the same as described in Test Case 1.

| Trial | Net Speed (mm/s) |
|-------|------------------|
| 1     | 68.35            |
| 2     | 68.24            |
| 3     | 68.35            |
| 4     | 68.26            |
| 5     | 68.33            |

| Variance | Standard Deviation |
|----------|--------------------|
| 0.00273  | 0.05225            |

Using both motors simultaneuosly achieves minor speed improvements. The speedup from individual motor to synchronized motor performance is 1.2 % based on the best case runtimes of each. A slight speed increase could be explained by the added moment of force from the second motor slightly reducing the net force on each. Notably the velocity vectors of each motor are not additive since they are operating on different components therefore we shouldn't see major performance gains.

Overall we won't be able to run sampling at 85 mm/s however we can take away 3 key results:
1. Maximum sampling rate of approximately 67 mm/s which can be pushed to 68 mm/s for equally distributed di-axial movements (ie. diagonal movements following `y=x`).
2. Very consistent runtime speeds based on variance and std. deviation computations
   - Dual mmotor performance is half as consistent based on dual motor motion which is expected
3. At smaller displacements the runtime will decrease slightly from the aforementioned measurements