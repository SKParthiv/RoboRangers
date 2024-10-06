from motors.motors import Motor

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