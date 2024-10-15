import cv2
import numpy as np
from capture import capture_image, detect_color
from blocks import Block

# Define your color bounds for green
lower_bound = np.array([35, 100, 100])  # Lower bound for green
upper_bound = np.array([85, 255, 255])  # Upper bound for green

# List of test images
test_images = ['blocks_image.jpg', 'blocks_image2.jpg', 'blocks_image3.jpg', 'blocks_image4.jpg']

def test_turn_angle():
	for image_path in test_images:
		# Load the test image
		img = cv2.imread(image_path)
		if img is None:
			print(f"Failed to load image: {image_path}")
			continue
		
		# Detect blocks in the image
		mask, blocks = detect_color(img, lower_bound, upper_bound, "Green")
		
		# Print the detected blocks and their turn angles
		for block in blocks:
			print(block)

		# Display the image and mask for visual verification
		cv2.imshow("Image", img)
		cv2.imshow("Mask", mask)
		
		if cv2.waitKey(0) & 0xFF == ord('q'):
			break

	cv2.destroyAllWindows()

if __name__ == "__main__":
	test_turn_angle()