from camera.capture import capture_image
from camera.capture import detect_colors
from camera.capture import define_blocks
from camera.capture import image_width
from mapping.map_builder import create_map
from path_planning.rtt_path import rtt_path_planning
import numpy as np
import RPi.GPIO as GPIO
from motors.motors import Motor
import math

fov = 100 # Edit based on the physical params
calibration_factor = 12 # Edit based on the physical params
max_speed = 100 # Edit based on the physical params
robot_position = (10, 5) # Edit based on the physical params
pwm_pin = 12    # GPIO pin for PWM control

# Defining Motors
motor1 = Motor(1, 13, 14, 15, 16, pwm_pin)
motor2 = Motor(2, 17, 18, 19, 20, pwm_pin)
motor3 = Motor(3, 21, 22, 23, 24, pwm_pin)
motor4 = Motor(4, 25, 26, 27, 28, pwm_pin)
encoder_feedback = [(GPIO.LOW, 0),
                    (GPIO.LOW, 0),
                    (GPIO.LOW, 0),
                    (GPIO.LOW, 0)]
# Main loop
while True:
    # Capture image
    image = capture_image()
    
    # Detect colors
    masks = detect_colors(image)

    # Calculate Depth and Turn angles for each blocks
    blocks = define_blocks(masks, calibration_factor , image_width , fov)

    # Get encoder feedback
    positions = []
    for i in encoder_feedback:
        positions.append(i[1])
    encoder_feedback = [motor1.encoder_callback(encoder_feedback[0][0]), 
                        motor2.encoder_callback(encoder_feedback[1][0]),
                        motor3.encoder_callback(encoder_feedback[2][0]),
                        motor4.encoder_callback(encoder_feedback[3][0])]
    position_differences = []
    for i in range(4):
        position_differences.append(encoder_feedback[i][1]-positions[i])
    

    