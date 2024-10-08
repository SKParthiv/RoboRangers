# RoboRangers
Making the winning robot(s) for "Robotics for Good Youth Challenge"

## Instructions for Calibrating:


## Intructions for Testing:
### Step 1:
- Open your terminal in Raspberry Pi with git installed and type:
`git clone https://github.com/SKParthiv/RoboRangers.git
#cloning of repo
cd RoboRangers
chmod +x setup.sh
chmod +x run.sh
./setup.sh
code .`
### Step 2:
- Wait for all the installations to complete and wait for VSCode to open
### Step 3:
- Open `main.py` where you will see all the variables with the comment ` # Edit based on the physical params` and pin definitions
### Step 4:
- Edit those based on camera specifications and connections of motor driver to the RPi and encoder_A and encoder_B connections
### Step 5:
- Run the following cmd:
`./run.sh`
