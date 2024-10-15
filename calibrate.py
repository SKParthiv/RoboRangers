import cv2
import numpy as np

def calculate_calibration_factor(image_path1, image_path2, actual_width_cm, lower_color, upper_color, depth_cm1, depth_cm2):
    """
    Calculate the calibration factor based on the actual width in cm, pixel width, and depth.
    Args:
        image_path1 (str): Path to the first image file.
        image_path2 (str): Path to the second image file.
        actual_width_cm (float): Known actual width of the object in cm.
        lower_color (tuple): Lower HSV color range for object detection.
        upper_color (tuple): Upper HSV color range for object detection.
        depth_cm1 (float): Depth of the object in the first image in cm.
        depth_cm2 (float): Depth of the object in the second image in cm.
    Returns:
        float: Calibration factor in cm/pixel.
    """
    def get_pixel_width(image_path):
        # Read the image
        image = cv2.imread(image_path)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Create a mask for the color range
        mask = cv2.inRange(hsv, lower_color, upper_color)
        
        # Find contours in the masked image
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            print(f"No contours found for this color in {image_path}.")
            return None

        # Get the largest contour by area
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Get the bounding box of the largest contour
        x, y, w, h = cv2.boundingRect(largest_contour)
        
        return w

    # Get pixel widths for both images
    pixel_width1 = get_pixel_width(image_path1)
    pixel_width2 = get_pixel_width(image_path2)

    if pixel_width1 is None or pixel_width2 is None:
        return None

    # Calculate the slope (rate of change of depth with respect to pixel width)
    slope = (depth_cm2 - depth_cm1) / (pixel_width2 - pixel_width1)
    
    return slope

# Example usage for Green block
image_path1 = 'blocks_image.jpg'  # Replace with the path to your first image
image_path2 = 'blocks_image2.jpg'  # Replace with the path to your second image
image_path3 = 'blocks_image3.jpg'
image_path4 = 'blocks_image4.jpg'

# Actual width in cm
green_width_cm = 11.0

# Depths in cm
depth_cm2 = 21.0  # Depth for the first image
depth_cm1 = 15.0  # Depth for the second image
depth_cm3 = 14.0
depth_cm4 = 17.4

# HSV range for green color
green_lower_hsv = (40, 100, 100)
green_upper_hsv = (70, 255, 255)

# Calculate calibration factor
green_calibration_factor = calculate_calibration_factor(image_path1, image_path2, green_width_cm, green_lower_hsv, green_upper_hsv, depth_cm1, depth_cm2)
green_calibration_factor2 = calculate_calibration_factor(image_path3, image_path4, green_width_cm, green_lower_hsv, green_upper_hsv,depth_cm3, depth_cm4)
# Display the result
if green_calibration_factor is not None:
    print(f'Green Block Calibration Factor: {green_calibration_factor:.4f} cm/pixel')
    print(f'Green Block Calibration Factor: {green_calibration_factor2:.4f} cm/pixel')
else:
    print('Calibration factor could not be calculated.')

