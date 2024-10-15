from picamera2 import Picamera2, Preview
import cv2
import numpy as np
import time
from mapping.blocks import Block

# Given values for angle calculations
fov_degrees = 72.4  # FOV in degrees
focal_length_mm = 3.29  # Focal length in mm
image_width_pixels = 2592  # Image width in pixels

# Step 1: Convert FOV to radians
fov_radians = np.radians(fov_degrees)

# Step 2: Calculate the Physical Width (optional)
physical_width = 2 * focal_length_mm * np.tan(fov_radians / 2)

# Step 3: Calculate Angle Per Pixel
angle_per_pixel = fov_degrees / image_width_pixels  # degrees per pixel

# Initialize PiCamera
# image_width = 640  # in pixels
# image_height = image_width * 3 // 4  # Maintain aspect ratio
# calibration_factor = 12.0  # Known object size in cm
# camera = Picamera2()
# camera_config = camera.create_preview_configuration(main={"size": (image_width, image_height)})
# camera.configure(camera_config)

def capture_image():
    # camera.start_preview(Preview.QTGL)
    # camera.start()
    # # Capture image in RGB format
    image = cv2.imread('frame.jpg')
    # Convert the captured image from RGB to BGR (OpenCV format)
    return cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

def merge_contours(contours, merge_distance=20):
    if not contours:
        return []

    merged_boxes = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        merged = False
        
        for i, (mx, my, mw, mh) in enumerate(merged_boxes):
            if (abs(mx - x) < merge_distance and abs(my - y) < merge_distance):
                merged_boxes[i] = (min(mx, x), min(my, y), 
                                    max(mx + mw, x + w) - min(mx, x), 
                                    max(my + mh, y + h) - min(my, y))
                merged = True
                break

        if not merged:
            merged_boxes.append((x, y, w, h))

    return merged_boxes

def calculate_turn_angle(pixel_position):
    # Calculate the angle to turn based on the object's position in pixels
    center_position = image_width / 2
    offset = pixel_position - center_position
    turn_angle = offset * angle_per_pixel  # Use angle_per_pixel calculated earlier
    return turn_angle

def define_blocks(image, mask, color_name):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    large_contours = [c for c in contours if cv2.contourArea(c) > 500]
    merged_boxes = merge_contours(large_contours)
    blocks = []
    
    for (x, y, w, h) in merged_boxes:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        pixel_position = x + w / 2
        depth = (calibration_factor * image_width) / w  # Depth in cm
        turn_angle = calculate_turn_angle(pixel_position)  # Turn angle in degrees
        blocks.append(Block(depth, turn_angle, color_name))
    
    return blocks

def detect_color(image, lower_bound, upper_bound, color_name):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_image, lower_bound, upper_bound)
    blocks = define_blocks(image, mask, color_name)
    return mask, blocks

# # Example usage
# try:
#     while True:
#         img = capture_image()
#         # Define your color bounds here
#         lower_bound = np.array([100, 150, 0])  # Example lower bound for a color
#         upper_bound = np.array([140, 255, 255])  # Example upper bound for a color
#         mask, blocks = detect_color(img, lower_bound, upper_bound, "ExampleColor")

#         # Display the image and mask
#         cv2.imshow("Image", img)
#         cv2.imshow("Mask", mask)
        
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
# finally:
#     cv2.destroyAllWindows()
