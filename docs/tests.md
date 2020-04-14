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

## Stage Accuracy Tests (Unidirectional Accuracy)
> How accurately can the stage position itself over any given point?

STUDY NOT CONDUCTED

## Stage Precision Tests (Repeatability)
> Repeatability claim of > 2μm

STUDY NOT CONDUCTED

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

The individual steppers do not meet the validated claims of 85 mm/s. I predict the speed they are referring to is the maximum instantaneous velocity and not its aggregate speed. Judging by audio queues, the motors seem to achieve its peak midway through the execution but slows back down as it approaches the specified distance. This is probably in place to reduce the stress on the motors. Stepper motors are susceptible to performance wear as they have a larger number of motor step positions (which allows for increased precision)so this makes sense. I ran some tests for shorter intervals to backup my prediction and saw diminishing returns in speed performance as the length decreased.

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