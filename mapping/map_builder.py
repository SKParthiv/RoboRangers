import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

# Arena dimensions
arena_width = 117.1
arena_height = 114.3

# Refuge dimensions and coordinates
refuge_x = 94.3  # 1143 - 200 (offset from right side)
refuge_y = 0
refuge_width = 20.0
refuge_length = 30.0

# Hospital dimensions
hospital_center_x = 0
hospital_center_y = 0
hospital_radius = 23.05


def create_map(blocks, robot):
    # Create the figure and axis
    fig, ax = plt.subplots()
    ax.set_xlim(0, arena_width)
    ax.set_ylim(0, arena_height)
    ax.set_aspect('equal')

    # Draw refuge (rectangular)
    refuge_rect = Rectangle((refuge_x - 100, refuge_y), refuge_width, refuge_length, color="blue", alpha=0.5)
    elevated = Rectangle((refuge_x, refuge_y), 100, 200, color="green", alpha=0.5)
    ax.add_patch(refuge_rect)
    ax.add_patch(elevated)

    # Draw hospital (circular)
    hospital_circle = Circle((hospital_center_x, hospital_center_y), hospital_radius, color="blue", alpha=0.5)
    hospital_circle_till_doctor = Circle((hospital_center_x, hospital_center_y), 200, color="green", alpha=0.5)
    hospital_roof = Circle((hospital_center_x, hospital_center_y), 150.5, color="red", alpha=0.5)
    ax.add_patch(hospital_circle)
    ax.add_patch(hospital_circle_till_doctor)
    ax.add_patch(hospital_roof)

    # Draw blocks
    for block in blocks:
        block_rect = Rectangle((block.x, block.y), block.width, block.height, color=block.color, alpha=0.5)
        ax.add_patch(block_rect)

    # Draw robot
    robot_circle = Circle((robot.x, robot.y), robot.radius, color=robot.color, alpha=0.5)
    ax.add_patch(robot_circle)

    # Set titles and labels
    ax.set_title("Arena Map with Hospital, Refuge, Blocks, and Robot")
    ax.set_xlabel("X-coordinate")
    ax.set_ylabel("Y-coordinate")
    ax.legend(["Refuge", "Elevated Area", "Hospital", "Doctor Area", "Hospital Roof", "Blocks", "Robot"])

    # Show the map
    plt.grid(True)
    plt.show()

# Example usage
# blocks = [
#     Block(10, 10, 5, 5, "yellow"),
#     Block(20, 20, 10, 10, "purple")
# ]
# robot = Robot(50, 50, 5, "black")

# create_map(blocks, robot)