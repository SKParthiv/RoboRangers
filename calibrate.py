import cv2
import numpy as np

def calculate_calibration_factor(image_path, image_path2, actual_width_cm, lower_color, upper_color, depth_cm1, depth_cm2):
    """
    Calculate the calibration factor based on the actual width in cm, pixel width, and depth.
    Args:
        image_path (str): Path to the image file.
        actual_width_cm (float): Known actual width of the object in cm.
        lower_color (tuple): Lower HSV color range for object detection.
        upper_color (tuple): Upper HSV color range for object detection.
        depth_cm (float): Depth of the object in cm.
    Returns:
        float: Calibration factor in cm/pixel.
    """
    # Read the image
    image = cv2.imread(image_path)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Create a mask for the color range
    mask = cv2.inRange(hsv, lower_color, upper_color)
    
    # Find contours in the masked image
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        print("No contours found for this color.")
        return None

    # Get the largest contour by area
    largest_contour = max(contours, key=cv2.contourArea)
    
    # Get the bounding box of the largest contour
    x, y, w, h = cv2.boundingRect(largest_contour)
    
    # Calculate calibration factor
    calibration_factor = (w/ actual_width_cm) * depth_cm1

    image2 = cv2.imread(image_path2)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Create a mask for the color range
    mask = cv2.inRange(hsv, lower_color, upper_color)
    
    # Find contours in the masked image
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        print("No contours found for this color.")
        return None

    # Get the largest contour by area
    largest_contour = max(contours, key=cv2.contourArea)
    
    # Get the bounding box of the largest contour
    x, y, w2, h = cv2.boundingRect(largest_contour)
    
    # Calculate calibration factor
    calibration_factor = (w2 - w/ actual_width_cm) * (depth_cm2 - depth_cm1)
    return calibration_factor

# Example usage for Red, Green, and Brown blocks
image_path = 'blocks_image.jpg'  # Replace with the path to your image
image_path2 = 'blocks_image2.jpg'

# Actual widths in cm
red_green_width_cm = 11.0
brown_width_cm = 120.0

# Depths in cm
red_green_depth_cm2 = 14.0  # Example depth for red and green blocks
red_green_depth_cm = 17.4
brown_depth_cm = 100.0  # Example depth for brown block

# HSV ranges for red, green, and brown colors
red_lower_hsv = (0, 100, 100)
red_upper_hsv = (10, 255, 255)

green_lower_hsv = (40, 100, 100)
green_upper_hsv = (70, 255, 255)

brown_lower_hsv = (10, 100, 20)
brown_upper_hsv = (20, 255, 200)

# Calculate calibration factors
#red_calibration_factor = calculate_calibration_factor(image_path, image_path2, red_green_width_cm, red_lower_hsv, red_upper_hsv, red_green_depth_cm)
green_calibration_factor = calculate_calibration_factor(image_path, image_path2, red_green_width_cm, green_lower_hsv, green_upper_hsv, red_green_depth_cm, red_green_depth_cm2)
#brown_calibration_factor = calculate_calibration_factor(image_path, brown_width_cm, brown_lower_hsv, brown_upper_hsv, brown_depth_cm)

# Display the results
#print(f'Red Block Calibration Factor: {red_calibration_factor:.4f} cm/pixel')
print(f'Green Block Calibration Factor: {green_calibration_factor:.4f} cm/pixel')
#print(f'Brown Block Calibration Factor: {brown_calibration_factor:.4f} cm/pixel')