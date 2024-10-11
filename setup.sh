#!/bin/bash

# Update system packages
echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python 3 and pip (if not already installed)
echo "Installing Python3 and pip..."
sudo apt install python3 python3-pip -y

# Install build tools and libraries required for OpenCV
echo "Installing OpenCV dependencies..."
sudo apt install build-essential cmake git pkg-config libjpeg-dev libtiff-dev libpng-dev -y
sudo apt install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev -y
sudo apt install libxvidcore-dev libx264-dev -y
sudo apt install libfontconfig1-dev libcairo2-dev -y
sudo apt install libgdk-pixbuf2.0-dev libpango1.0-dev libgtk2.0-dev libgtk-3-dev -y
sudo apt install libatlas-base-dev gfortran -y
sudo apt install libhdf5-dev libhdf5-103 -y

# Install Python libraries for OpenCV and related packages
echo "Installing Python libraries (NumPy, OpenCV, etc.)..."
sudo apt-get install puthon3-numpy

# Install OpenCV from pip
sudo apt-get install python3-opencv-python
sudo apt-get install python3-opencv-python-headless
sudo apt-get install python3-opencv-contrib-python

# Install Matplotlib for plotting
echo "Installing Matplotlib..."
sudo apt-get install python3-matplotlib


# Install PiCamera for interfacing with the Raspberry Pi camera module
echo "Installing PiCamera..."
sudo apt-get install python3-picamera2

# Optional: Install additional useful libraries (e.g., SciPy, Pandas)
# echo "Installing SciPy..."
# pip3 install scipy

# Clean up after installation
echo "Cleaning up unnecessary packages..."
sudo apt autoremove -y

# Installation complete
echo "All dependencies, including OpenCV, have been installed successfully!"
