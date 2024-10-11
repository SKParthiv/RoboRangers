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

def define_blocks(mask_tuple, calibration_factor, image_width, fov):
	# Linear relation based on pre-calibrated data
	blocks = []
	color = 0
	for mask in mask_tuple:
		# Find contours in the mask
		color += 1
		colorr = ''
		contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		for contour in contours:
			# Get the bounding box of the contour
			x, _, w, _ = cv2.boundingRect(contour)
			# Assuming pixel_position is the x-coordinate of the center of the bounding box
			pixel_position = x + w / 2
			if color == 1:
				colorr = "red"
			elif color == 2:
				colorr = "blue"
			else:
				colorr = "brown"
			blocks.append(Block(calibration_factor/w, (pixel_position - image_width / 2) * (fov / image_width), colorr))
	return blocks

def detect_colors(image):
    # Define RGB color ranges in HSV
    red_lower = np.array([0, 100, 100])
    red_upper = np.array([10, 255, 255])
    
    green_lower = np.array([40, 100, 100])
    green_upper = np.array([70, 255, 255])
    
    brown_lower = np.array([10, 100, 20])
    brown_upper = np.array([20, 255, 200])
    
    # Convert image to HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    red_mask = cv2.inRange(hsv_image, red_lower, red_upper)
    green_mask = cv2.inRange(hsv_image, green_lower, green_upper)
    brown_mask = cv2.inRange(hsv_image, brown_lower, brown_upper)
    
    return red_mask, green_mask, brown_mask
