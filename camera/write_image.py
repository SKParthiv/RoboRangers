import serial
import numpy as np
from PIL import Image

# Open the serial connection to Arduino
ser = serial.Serial('/dev/ttyUSB0', 115200)

# Image parameters (adjust according to the resolution you're using)
WIDTH = 640
HEIGHT = 480
image_array = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

def read_frame():
    for y in range(HEIGHT):
        for x in range(WIDTH):
            # Read two bytes (RGB565 format)
            high_byte = ser.read(1)
            low_byte = ser.read(1)
            
            # Combine high and low bytes to form the RGB565 pixel
            pixel = (ord(high_byte) << 8) | ord(low_byte)
            
            # Convert RGB565 to RGB888 (R, G, B values in 8 bits each)
            r = (pixel >> 11) & 0x1F
            g = (pixel >> 5) & 0x3F
            b = pixel & 0x1F
            
            # Convert 5/6-bit colors to 8-bit colors
            r = (r * 255) // 31
            g = (g * 255) // 63
            b = (b * 255) // 31
            
            # Store the pixel in the image array
            image_array[y, x] = [r, g, b]

def save_image(filename):
    img = Image.fromarray(image_array, 'RGB')
    img.save(filename)

while True:
    # Wait for a new frame from Arduino
    read_frame()
    # Save the frame as an image file
    save_image('frame.jpg')