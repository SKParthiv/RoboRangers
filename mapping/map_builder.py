import matplotlib.pyplot as plt
from mapping.blocks import Block

# Example map of the environment
def create_map(robot_position, refuge_coords, hospital_coords, blocks):
    _, ax = plt.subplots()
    ax.plot(robot_position[0], robot_position[1], 'bo', label='Robot')
    
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
