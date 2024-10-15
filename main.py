from camera.capture import capture_image, detect_color, image_width
from mapping.map_builder import create_map
from mapping.robots import Robot
from path_planning.rtt_path import rtt_path_planning
import numpy as np
from calibrate import green_calibration_factor
import RPi.GPIO as GPIO
from motors.motors import Motor
import math
import time
import cv2

fov = 100  # Edit based on the physical params
calibration_factor = green_calibration_factor  # Edit based on the physical params
max_speed = 100  # Edit based on the physical params
rover = Robot(500, 0, 5, 5, 0, 17, 27, [Motor('left', 12, 6), Motor('right', 13, 5)])  # Edit based on the physical params
pwm_pin = 12  # GPIO pin for PWM control
ticks_per_revolution = 2000  # Change based on the encoder specs
wheel_radius = 0.5  # Change based on the wheel radius

# Defining Motors
motor1 = Motor('a', 12, 6)
motor2 = Motor('b', 13, 5)
motor3 = Motor('c', 14, 7)
motor4 = Motor('d', 15, 8)
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
    mask_green, blocks_green = detect_color(image, np.array([35, 100, 100]), np.array([85, 255, 255]), "Green")
    
    # Detect red color (requires two ranges to cover the wrap-around of red in HSV)
    mask_red1, blocks_red1 = detect_color(image, np.array([0, 100, 100]), np.array([10, 255, 255]), "Red")
    mask_red2, blocks_red2 = detect_color(image, np.array([160, 100, 100]), np.array([180, 255, 255]), "Red")
    blocks_red = blocks_red1 + blocks_red2
    
    # Detect brown color
    mask_brown, blocks_brown = detect_color(image, np.array([10, 100, 20]), np.array([20, 200, 200]), "Brown")
    
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
    
    # Update map
    create_map()

    # Plan the path using RTT algorithm
    start = (rover.x, rover.y)
    goal = (1000, 1000)  # Example goal, should be set based on your requirements
    checkpoints = blocks_green + blocks_red + blocks_brown  # Example, prioritize based on color if needed
    obstacles = []  # Define obstacles if any
    arena_width = 2000  # Example width
    arena_height = 2000  # Example height
    path = rtt_path_planning(start, goal, checkpoints, obstacles, arena_width, arena_height)

    # Create motor instructions
    for i in range(1, len(path)):
        current_pos = path[i-1]
        next_pos = path[i]
        direction = "forward" if next_pos[1] > current_pos[1] else "backward"
        speed = 50  # Example speed value
        motor1.move(speed, direction)
        motor2.move(speed, direction)
        motor3.move(speed, direction)
        motor4.move(speed, direction)

    # Ending sequence
    blocks_red = None
    blocks_green = None
    blocks_brown = None

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cv2.destroyAllWindows()