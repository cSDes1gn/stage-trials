# General Zaber Staging System Notes and Background

## Common terminology
> **positioner**: any motorized device with moving mechanic such as a linear stage, rotational stage, or a stepper.

>**peripheral**: a positioner including a motor and mechanics but doesn't use an integrated controller. Peripherals are designed for use with Zabers motor controllers and can be used with third-party motor drivers/controllers.

>**device**: stndalone controller or positioner with an integrated contoller. Devices are designed for use with Zabers motor controllers and can be used with third-party motor drivers/controllers.

>**joystick**: product that allows multi-axis manual input and push button input for positioners. Joysticks are not controllers but instead areinput devices to interface with Zabers motor controllers when connected in series.

For a comprehensive list of terms visit [Zaber's online glossary](https://www.zaber.com/glossary)

## Motor Mechanics
### Brushed vs Brushless
The principle behind the internal working of both a brushless DC motor and a brushed DC motor are essentially the same. When the motor windings become energized, a temporary magnetic field is created that repels and/or attracts against permanent magnets. This force is converted into shaft rotation, which allows the motor to do work. As the shaft rotates, electric current is routed to different sets of windings, maintaining electromotive repulsion/attraction, forcing the rotor to continually turn.

**brushed motors**: are driven by brushes which deliver current to the motor windings through commutator contacts. The windings are on the rotor and the magnets are on the stator (stationary part of motor). brushes create friction and can cause sparking which leads to unrelieable and inefficient operation.

<p align="center">
  <img src="img/brushed.gif"/>
</p>

**brushless motors**: are electronically driven by a device known as a *controller* transforming DC current into 3-phase variable-frequency current and supplied motor coils successively to create rotating field. These motors do not use a physical switch to transmit current.  The windings are on the stator and the magnets are on the rotator eliminating the need for brushes.

<p align="center">
  <img src="img/brushless.gif"/>
</p>

## Closed-loop devices:
Closed-loop devices use encoder feedback in order to inform trajectory of the controller.

### Stepper Motors:
Steppers are a subset of closed-loop devices which have a high pole-count (50-100) offering precision drive for motion control applications. The drive steps directly without encoder feedback.

Pros:
- inexpensive
- high level of precision
- less maintainence due to simplicity

Cons:
- Loses significant torque at high speeds (up to 80%)
- higher maintainence due to increased system complexity
- prone to damage from system resonance and internal vibrations
- inefficient with high heat dissipation

### Servo Motors
Servos are a subset of closed-loop devices which have a low pole count (4-12) offering high torque at high speed (due to reduced number of poles). The drive steps according to encoder feedback.

Pros:
- 80-90% operational efficiency
- AC and DC driver support
- Does not suffer from vibration or resonance complications

Cons:
- expensive as compared to stepper motors
- higher maintainence due to increased system complexity

## Resolution for Closed-Loop Motors
The resolution of a device is defined as the smallest increment you can command it to move. For examples `ASCII` protocol to instruct a device to move forward 1 unit.
```ascii
/move rel 1
```

The physical distance of the increment can be found according to the type of device

### Stepper Increments
An increment is a *microstep* of the motor and the corresponding size of an increment is the device's *microstep size* specification.

Stepper motors are designed for position control. In a motor revolution, they have a number of equally spaced step positions. Steppers in Zaber products normally have 200 steps per revolution. However these steps can be further subdivided into *microsteps* which during default operation yields 64 microsteps per step. The microstep count per step is configurable between [ADD RANGE SPEC]

*Microstep Size = Displacement per rev / microsteps per rev*

Microsteps vary from device to device so to view the microsteps for a particular system go to "Series Specs" tab for a particular product.

### Servo Increments
An increment is an *encoder count*, and the size of an increment is the device's *encoder resolution* specification. 

Unlike stepper motors, servo motors are designed with force control in mind; they can be driven using position control but the resolution is less accurate due smaller number of steps per revolution. For fine resolution positioning servos nneed positional feedback using position encoders. An encoder count is the smallest change in the encoder that reguisters as a movement by the controller.