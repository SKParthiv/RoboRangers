from picamera2 import Picamera2 as PiCamera
import cv2
import numpy as np
from mapping.blocks import Block

# Initialize PiCamera
image_width = 640
camera = PiCamera()
def capture_image():
	camera.resolution = (image_width, 480)
	camera.start_preview()

	# Capture image and save it to the disk
	camera.capture('/home/pi/image.jpg')

	# Load image into OpenCV
	image = cv2.imread('/home/pi/image.jpg')
	return image

def define_blocks(mask, calibration_factor, image_width, fov, colour):
	# Linear relation based on pre-calibrated data
	blocks = []
	color = 0
	# Find contours in the mask
	contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	for contour in contours:
		# Get the bounding box of the contour
		x, y, w, h = cv2.boundingRect(contour)
		# Assuming pixel_position is the x-coordinate of the center of the bounding box
		pixel_position = x + w / 2
		blocks.append(Block(calibration_factor/w, (pixel_position - image_width / 2) * (fov / image_width), colour))

	return blocks

def detect_green(image):
    # Define RGB color ranges in HSV
    
    green_lower = np.array([40, 100, 100])
    green_upper = np.array([70, 255, 255])
    
    # Convert image to HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    green_mask = cv2.inRange(hsv_image, green_lower, green_upper)
    cv2.imshow(green_mask)
    return green_mask

def detect_red(image):
	red_lower = np.array([0, 100, 100])
	red_upper = np.array([10, 255, 255])

	hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

	red_mask = cv2.inRange(hsv_image, red_lower, red_upper)
	cv2.imshow(red_mask)
	return red_mask

def detect_brown(image):
	brown_lower = np.array([10, 100, 20])
	brown_upper = np.array([20, 255, 200])

	hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

	brown_mask = cv2.inRange(hsv_image, brown_lower, brown_upper)
	cv2.imshow(brown_mask)
	return brown_mask