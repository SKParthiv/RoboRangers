from camera.capture import capture_image
from camera.capture import detect_red, detect_green, detect_brown, define_blocks
from camera.capture import image_width
from mapping.map_builder import create_map
from path_planning.rtt_path import rtt_path_planning
import numpy as np
import RPi.GPIO as GPIO
from motors.motors import Motor
import math
import time
import cv2

fov = 100 # Edit based on the physical params
calibration_factor = 12 # Edit based on the physical params
max_speed = 100 # Edit based on the physical params
robot_position = (10, 5) # Edit based on the physical params
pwm_pin = 12    # GPIO pin for PWM control
ticks_per_revolution = 2000 # Change based on the encoder specs
wheel_radius = 0.5 # Change based on the wheel radius

# Defining Motors
motor1 = Motor(1, 13, 14, 15, 16, pwm_pin, ticks_per_revolution)
motor2 = Motor(2, 17, 18, 19, 20, pwm_pin, ticks_per_revolution)
motor3 = Motor(3, 21, 22, 23, 24, pwm_pin, ticks_per_revolution)
motor4 = Motor(4, 25, 26, 27, 28, pwm_pin, ticks_per_revolution)
encoder_feedback = [(GPIO.LOW, 0),
                    (GPIO.LOW, 0),
                    (GPIO.LOW, 0),
                    (GPIO.LOW, 0)]
# Main loop
while True:
    time.sleep(0.1)
    # Capture image
    image = capture_image()
    if image != None:
        # Detect colors
        mask_red = detect_red(image)
        mask_green = detect_green(image)
        mask_brown = detect_brown(image)

        # Calculate Depth and Turn angles for each blocks
        blocks_red = define_blocks(mask_red, calibration_factor , image_width , fov)
        blocks_green = define_blocks(mask_green, calibration_factor , image_width , fov)
        blocks_brown = define_blocks(mask_brown, calibration_factor , image_width , fov)


    # # Get encoder feedback
    # for i, motor in enumerate([motor1, motor2, motor3, motor4]):
    #     last_A, position = encoder_feedback[i]
    #     last_A, new_position = motor.encoder_callback(last_A)
    #     encoder_feedback[i] = (last_A, new_position)
    #     motor.encoder_ticks = new_position

    # # Calculate displacement for each wheel
    # left_displacement = (motor1.calculate_wheel_displacement(wheel_radius) + motor2.calculate_wheel_displacement(wheel_radius)) / 2
    # right_displacement = (motor3.calculate_wheel_displacement(wheel_radius) + motor4.calculate_wheel_displacement(wheel_radius)) / 2

    # # Calculate the robot's displacement and turn angle
    # robot_displacement = (left_displacement + right_displacement) / 2
    # turn_angle = (left_displacement - right_displacement) / (2 * wheel_radius)

    #Ending sequence
    blocks_red = None
    blocks_green = None
    blocks_brown = None