import RPi.GPIO as GPIO

class Motor:
    def __init__(self, name, pwm_pin, motor_in1, motor_in2, ppr, encoder_a, encoder_b):
        self.name = name
        self.pwm_pin = pwm_pin
        self.motor_in1 = motor_in1
        self.motor_in2 = motor_in2
        self.ppr = ppr
        self.encoder_a = encoder_a
        self.encoder_b = encoder_b

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.motor_in1, GPIO.OUT)
        GPIO.setup(self.motor_in2, GPIO.OUT)

        # Setup PWM
        self.pwm = GPIO.PWM(self.pwm_pin, 1000)  # Set PWM frequency to 1kHz
        self.pwm.start(0)  # Start PWM with 0% duty cycle (motor off)

    def move(self, speed, direction):
        """
        Move the motor.
        
        :param speed: Speed percentage (0-100)
        :param direction: 'forward' or 'backward'
        """
        if direction == 'forward':
            GPIO.output(self.motor_in1, GPIO.HIGH)
            GPIO.output(self.motor_in2, GPIO.LOW)
        elif direction == 'backward':
            GPIO.output(self.motor_in1, GPIO.LOW)
            GPIO.output(self.motor_in2, GPIO.HIGH)
        else:
            raise ValueError("Direction must be 'forward' or 'backward'")

        # Set motor speed
        self.pwm.ChangeDutyCycle(speed)

    def stop(self):
        """Stop the motor."""
        self.pwm.ChangeDutyCycle(0)
        GPIO.output(self.motor_in1, GPIO.LOW)
        GPIO.output(self.motor_in2, GPIO.LOW)


class DualMotorController:
    def __init__(self, left_motor, right_motor, robot):
        self.left_motor = left_motor
        self.right_motor = right_motor
        self.robot = robot

    def turn(self, turn_angle):
        """
        Turn the robot by a specific angle.
        
        :param turn_angle: Angle to turn in degrees
        """
        # Calculate the distance each wheel needs to travel
        wheel_base = self.robot.width  # Distance between the wheels
        wheel_radius = 3.0  # Example wheel radius in cm, to be adjusted later

        # Calculate the arc length for each wheel
        arc_length = (turn_angle / 360.0) * (2 * np.pi * wheel_base / 2)

        # Calculate the speed for each wheel
        left_wheel_speed = arc_length / (2 * np.pi * wheel_radius) * 100
        right_wheel_speed = -left_wheel_speed

        # Move the motors
        self.left_motor.move(abs(left_wheel_speed), 'forward' if left_wheel_speed > 0 else 'backward')
        self.right_motor.move(abs(right_wheel_speed), 'forward' if right_wheel_speed > 0 else 'backward')

    def move(self, speed, direction):
        """
        Move the robot in a specific direction.
        
        :param speed: Speed percentage (0-100)
        :param direction: 'forward' or 'backward'
        """
        self.left_motor.move(speed, direction)
        self.right_motor.move(speed, direction)

    def stop(self):
        """Stop the robot."""
        self.left_motor.stop()
        self.right_motor.stop()


# Example usage
# if __name__ == "__main__":
#     left_motor = Motor("Left Motor", pwm_pin=18, motor_in1=23, motor_in2=24)
#     right_motor = Motor("Right Motor", pwm_pin=25, motor_in1=5, motor_in2=6)
#     controller = DualMotorController(left_motor, right_motor)

#     try:
#         controller.move_left(50, 'forward')  # Move left motor forward at 50% speed
#         controller.move_right(50, 'backward')  # Move right motor backward at 50% speed
#     except KeyboardInterrupt:
#         controller.stop()
#     finally:
#         GPIO.cleanup()
