#!/bin/bash

# Update system packages
echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python 3 and pip (if not already installed)
echo "Installing Python3 and pip..."
sudo apt install python3 python3-pip -y

# Install NumPy
echo "Installing NumPy..."
pip3 install numpy

# Install OpenCV (cv2)
echo "Installing OpenCV..."
sudo apt install python3-opencv -y

# Install Matplotlib
echo "Installing Matplotlib..."
pip3 install matplotlib

# Install RPi.GPIO for controlling GPIO pins on the Raspberry Pi
echo "Installing RPi.GPIO..."
pip3 install RPi.GPIO

# Install PiCamera for interfacing with the Raspberry Pi camera module
echo "Installing PiCamera..."
pip3 install picamera

# Optional: Install additional libraries (for example, SciPy, Pandas, etc.)
# echo "Installing SciPy..."
# pip3 install scipy

# Clean up
echo "Cleaning up..."
sudo apt autoremove -y

# Installation complete
echo "All dependencies have been installed successfully!"
