from camera.capture import capture_image
from camera.capture import detect_color, capture_image
from camera.capture import image_width
from mapping.map_builder import create_map
from mapping.robots import Robot
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
rover = Robot(500, 0, 5, 5, 0) # Edit based on the physical params
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
    time.sleep(2)
    image = capture_image()
    
    # Detect green color
    mask_green, blocks_green = detect_color(image, np.array([0, 100, 0]), np.array([85, 255, 255]), "Green")
    
    # Detect red color (requires two ranges to cover the wrap-around of red in HSV)
    mask_red1, blocks_red = detect_color(image, np.array([0, 0, 100]), np.array([10, 255, 255]), "Red")
    
    # Detect brown color
    mask_brown, blocks_brown = detect_color(image, np.array([10, 20, 20]), np.array([40, 200, 255]), "Brown")
    
    # Display the original image with detected contours
    cv2.imshow("Original Image", image)
    
    # Get encoder feedback
    for i, motor in enumerate([motor1, motor2, motor3, motor4]):
        last_A, position = encoder_feedback[i]
        last_A, new_position = motor.encoder_callback(last_A)
        encoder_feedback[i] = (last_A, new_position)
        motor.encoder_ticks = new_position

    # Calculate displacement for each wheel
    left_displacement = (motor1.calculate_wheel_displacement(wheel_radius) + motor2.calculate_wheel_displacement(wheel_radius)) / 2
    right_displacement = (motor3.calculate_wheel_displacement(wheel_radius) + motor4.calculate_wheel_displacement(wheel_radius)) / 2

    # Calculate the robot's displacement and turn angle
    robot_displacement = (left_displacement + right_displacement) / 2
    turn_angle = (left_displacement - right_displacement) / (2 * wheel_radius)
    turn_angle = math.radians(turn_angle)
    rover.x = rover.x + robot_displacement * math.cos(turn_angle)
    rover.y = rover.y + robot_displacement * math.sin(turn_angle)
    
    #Ending sequence
    blocks_red = None
    blocks_green = None
    blocks_brown = None

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cv2.destroyAllWindows()