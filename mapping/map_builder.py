import matplotlib.pyplot as plt
from mapping.blocks import Block
from mapping.robots import Robot

start_x = 10 # x-cordinate of the bottom left corner of the robot
start_y = 2.5 # y-coordinate of the bottom left corner of the robot
length = 5 # Length of the robot (Vertical length)
width = 5 # Width of the robot (Horizontal lenght)
Rover = Robot(start_x, start_y, width, length)
# Example map of the environment
def create_map(Rover, refuge_coords, hospital_coords, blocks):
    _, ax = plt.subplots()
    rover_rect = plt.Rectangle((Rover.x, Rover.y), Rover.length, Rover.height, Rover.angle, (Rover.x+(Rover.width/2), Rover.y+(Rover.length/2)))
    
    # Draw refuge (rectangular)
    refuge_rect = plt.Rectangle(refuge_coords[:2], refuge_coords[2], refuge_coords[3], color='green', label='Refuge')
    ax.add_patch(refuge_rect)

    # Draw hospital (semi-circular)
    hospital_circle = plt.Circle(hospital_coords[:2], hospital_coords[2], color='blue', label='Hospital', fill=False)
    ax.add_patch(hospital_circle)
    
    for block in blocks:
        ax.plot(block.x, block.y, 'ro' if block.color == 'Red' else 'go' if block.color == 'Green' else 'brown', label=block.color)
    
    ax.legend()
    plt.show()
