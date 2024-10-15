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
		self.encoder_a_pin = encoder_a_pin
		self.encoder_b_pin = encoder_b_pin
		self.motors = motors
		self.turn_angle = turn_angle

		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.encoder_a_pin, GPIO.IN)
		GPIO.setup(self.encoder_b_pin, GPIO.IN)

	def get_encoder_counts(self):
		# Placeholder for actual encoder reading logic
		encoder_a_count = GPIO.input(self.encoder_a_pin)
		encoder_b_count = GPIO.input(self.encoder_b_pin)
		return encoder_a_count, encoder_b_count

	def calculate_displacement_and_angle(self, encoder_a_count, encoder_b_count):
		wheel_radius = self.motors.left_motor.wheel_radius  # Assuming both motors have the same wheel radius
		wheel_base = self.width

		# Calculate the distance each wheel has traveled
		left_distance = 2 * np.pi * wheel_radius * (encoder_a_count / 360.0)
		right_distance = 2 * np.pi * wheel_radius * (encoder_b_count / 360.0)

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
