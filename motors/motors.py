import RPi.GPIO as GPIO
import numpy as np
import math

class Motor:
	def __init__(self, name, encoder_A, encoder_B, motor_in1, motor_in2, pwm_pin, encoder_ticks, ticks_per_revolution):
		self.name = name
		self.encoder_A = encoder_A
		self.encoder_B = encoder_B
		self.motor_in1 = motor_in1
		self.motor_in2 = motor_in2
		self.pwm_pin = pwm_pin
		self.encoder_ticks = encoder_ticks
		self.ticks_per_revolution = ticks_per_revolution

		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.encoder_A, GPIO.IN)
		GPIO.setup(self.encoder_B, GPIO.IN)
		GPIO.setup(self.motor_in1, GPIO.OUT)
		GPIO.setup(self.motor_in2, GPIO.OUT)
	
	def move(self, speed, direction):
		# Setup PWM
		pwm = GPIO.PWM(self.pwm_pin, 1000)  # Set PWM frequency to 1kHz
		pwm.start(0)  # Start PWM with 0% duty cycle (motor off)
		if direction == 'forward':
			GPIO.output(self.motor_in1, GPIO.HIGH)
			GPIO.output(self.motor_in2, GPIO.LOW)
		elif direction == 'backward':
			GPIO.output(self.motor_in1, GPIO.LOW)
			GPIO.output(self.motor_in2, GPIO.HIGH)

    # Set motor speed
		pwm.ChangeDutyCycle(speed)
	
	def encoder_callback(self, last_A):
		position = 0
		A = GPIO.input(self.encoder_A)
		B = GPIO.input(self.encoder_B)

		# Determine direction and update position
		if A == GPIO.HIGH and last_A == GPIO.LOW:  # Rising edge on A
			if B == GPIO.LOW:
				position += 1  # Clockwise
			else:
				position -= 1  # Counterclockwise
		last_A = A
		return last_A, position
	# Function to calculate distance traveled by each wheel
	def calculate_wheel_displacement(self, wheel_radius):
		# Calculate the wheel rotation in radians
		wheel_circumference = 2 * np.pi * wheel_radius
		# Displacement is proportional to the fraction of wheel circumference covered by the encoder ticks
		displacement = (self.encoder_ticks / self.ticks_per_revolution) * wheel_circumference
		return displacement