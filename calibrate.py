from picamera2 import Picamera2, Preview
import cv2
import numpy as np
import time

# Initialize PiCamera
image_width = 640
camera = Picamera2()
camera_config = camera.create_preview_configuration(main={"size": (image_width, image_width * 3 // 4)})
camera.configure(camera_config)
camera.start_preview(Preview.QTGL)
camera.start()

def capture_image():
    # Capture image in RGB format
    image = camera.capture_array()
    # Convert the captured image from RGB to BGR (OpenCV format)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return image

def merge_contours(contours, merge_distance=20):
    # Merge close contours by calculating a bounding box that encompasses them
    if not contours:
        return []

    merged_boxes = []
    for contour in contours:
        # Get the bounding box of the contour
        x, y, w, h = cv2.boundingRect(contour)
        merged = False
        
        # Try to merge with existing bounding boxes
        for i, (mx, my, mw, mh) in enumerate(merged_boxes):
            # Check if the current bounding box is close enough to merge
            if (abs(mx - x) < merge_distance and abs(my - y) < merge_distance):
                # Update the existing bounding box to include the current one
                merged_boxes[i] = (min(mx, x), min(my, y), max(mx + mw, x + w) - min(mx, x), max(my + mh, y + h) - min(my, y))
                merged = True
                break

        if not merged:
            merged_boxes.append((x, y, w, h))

    return merged_boxes

def define_blocks(image, mask, color_name):
    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter small contours and merge close ones
    large_contours = [c for c in contours if cv2.contourArea(c) > 500] # Filter based on area
    merged_boxes = merge_contours(large_contours)
    
    for (x, y, w, h) in merged_boxes:
        # Draw the merged bounding box on the original image
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # Print the coordinates and dimensions of the bounding box
        print(f"{color_name} - x: {x}, y: {y}, w: {w}, h: {h}")

def detect_color(image, lower_bound, upper_bound, color_name):
    # Convert image to HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Create a mask for the color
    mask = cv2.inRange(hsv_image, lower_bound, upper_bound)
    define_blocks(image, mask, color_name)
    return mask

while True:
    time.sleep(2)
    image = capture_image()
    
    # Detect green color
    mask_green = detect_color(image, np.array([35, 100, 50]), np.array([85, 255, 255]), "Green")
    
    # Detect red color (requires two ranges to cover the wrap-around of red in HSV)
    mask_red1 = detect_color(image, np.array([0, 100, 100]), np.array([10, 255, 255]), "Red")
    mask_red2 = detect_color(image, np.array([160, 100, 100]), np.array([180, 255, 255]), "Red")
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)
    
    # Detect brown color
    mask_brown = detect_color(image, np.array([10, 100, 20]), np.array([20, 255, 200]), "Brown")
    
    # Display the original image with detected contours
    cv2.imshow("Original Image", image)
    
    # Wait for a key press and break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cv2.destroyAllWindows()
camera.stop()