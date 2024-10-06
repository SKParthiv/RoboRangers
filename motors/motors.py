import RPi.GPIO as GPIO

class Motor:
	def __init__(self, name, encoder_A, encoder_B, motor_in1, motor_in2, pwm_pin):
		self.name = name
		self.encoder_A = encoder_A
		self.encoder_B = encoder_B
		self.motor_in1 = motor_in1
		self.motor_in2 = motor_in2
		self.pwm_pin = pwm_pin

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