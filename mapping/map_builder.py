import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from matplotlib.collections import PatchCollection
from mapping.blocks import Block
from mapping.robots import Robot

start_x = 10 # x-cordinate of the bottom left corner of the robot
start_y = 2.5 # y-coordinate of the bottom left corner of the robot
length = 5 # Length of the robot (Vertical length)
width = 5 # Width of the robot (Horizontal lenght)
Rover = Robot(start_x, start_y, width, length)

# Map Dimensions and co-ordinates of various map feautures
refuge_x = 100
refuge_y = 0
refuge_width = 5
refuge_length = 10
hospital_r = 5
# Example map of the environment
def create_map(Rover, blocks):
    _, ax = plt.subplots()
    rover_rect = Rectangle((Rover.x, Rover.y), Rover.width, Rover.length, Rover.angle, (Rover.x+(Rover.width/2), Rover.y+(Rover.length/2)))
    
    # Draw refuge (rectangular)
    refuge_rect = Rectangle((refuge_x, refuge_y), refuge_width, refuge_length)
    ax.add_patch(refuge_rect)

    # Draw hospital (semi-circular)
    hospital_circle = Circle((0, 0), 5)
    ax.add_patch(hospital_circle)
    
    for block in blocks:
        block.calculate_coordinates(Rover.x, Rover.y)
        ax.plot(block.x, block.y, 'ro' if block.color == 'Red' else 'go' if block.color == 'Green' else 'brown', label=block.color)
    ax.legend()
    plt.show()
