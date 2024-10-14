import RPi.GPIO as GPIO

class Motor:
    def __init__(self, name, pwm_pin, motor_in1, motor_in2):
        self.name = name
        self.pwm_pin = pwm_pin
        self.motor_in1 = motor_in1
        self.motor_in2 = motor_in2

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
    def __init__(self, left_motor, right_motor):
        self.left_motor = left_motor
        self.right_motor = right_motor

    def move_left(self, speed, direction):
        self.left_motor.move(speed, direction)

    def move_right(self, speed, direction):
        self.right_motor.move(speed, direction)

    def stop(self):
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
