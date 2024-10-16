import numpy as np
import math
import RPi.GPIO as GPIO

class Robot:
	def __init__(self, x, y, width, length, angle, encoder_a_pin, encoder_b_pin, motors, turn_angle=0):
		self.x = x
		self.y = y
		self.width = width
		self.length = length
		self.angle = angle
		self.motors = motors
		self.turn_angle = turn_angle

		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.encoder_a_pin, GPIO.IN)
		GPIO.setup(self.encoder_b_pin, GPIO.IN)

	def encoder_callback(self, channel):
		# Update encoder counts based on the channel triggered
		if channel == self.motors.left_motor.encoder_a:
			self.motors.left_motor.encoder_count += 1
		elif channel == self.motors.right_motor.encoder_b:
			self.motors.right_motor.encoder_count += 1

	def get_encoder_counts(self):
		# Return the current encoder counts
		encoder_a_count = self.motors.left_motor.encoder_count
		encoder_b_count = self.motors.right_motor.encoder_count
		return encoder_a_count, encoder_b_count

	def calculate_displacement_and_angle(self, encoder_a_count, encoder_b_count):
		wheel_radius = 3.0  # Example wheel radius in cm, to be adjusted later
		wheel_base = self.width

		# Calculate the distance each wheel has traveled
		left_distance = 2 * np.pi * wheel_radius * (encoder_a_count / self.motors.left_motor.ppr)
		right_distance = 2 * np.pi * wheel_radius * (encoder_b_count / self.motors.right_motor.ppr)

		# Calculate the average displacement
		displacement = (left_distance + right_distance) / 2.0

		# Calculate the change in angle (in radians)
		delta_angle = (right_distance - left_distance) / wheel_base

		return displacement, delta_angle

	def update_position(self):
		encoder_a_count, encoder_b_count = self.get_encoder_counts()
		displacement, delta_angle = self.calculate_displacement_and_angle(encoder_a_count, encoder_b_count)

		# Update the robot's angle
		self.angle += delta_angle

		# Update the robot's position
		self.x += displacement * np.cos(self.angle)
		self.y += displacement * np.sin(self.angle)

		return self.x, self.y, self.angle

	def calculate_coordinates(self, h, k):
		theta = math.radians(self.turn_angle)

		delta_x = math.sin(theta)
		delta_y = math.cos(theta)
		x = h + delta_x
		y = k + delta_y

		self.x = x
		self.y = y
