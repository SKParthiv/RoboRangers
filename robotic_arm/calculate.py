import math

# Link lengths in cm
link1 = 10.0
link2 = 10.0
link3 = 5.0  # Gripper

# Function to calculate angles from target coordinates
def calculate_angles(x, y, platform_height):
    # Distance from base to target
    r = math.sqrt(x**2 + y**2)

    # Consider platform height if needed
    h = platform_height

    # Inverse kinematics for a 2-link arm
    cos_angle2 = (r**2 - link1**2 - link2**2) / (2 * link1 * link2)
    joint2_angle = math.degrees(math.acos(cos_angle2))

    sin_angle1 = ((link1 + link2 * math.cos(math.radians(joint2_angle))) * y - (link2 * math.sin(math.radians(joint2_angle))) * x) / r**2
    joint1_angle = math.degrees(math.asin(sin_angle1))

    # Base angle (rotation in XY plane)
    base_angle = math.degrees(math.atan2(y, x))

    return base_angle, joint1_angle, joint2_angle

# Example: Coordinates (x, y) of the block and platform height
x = 12.0
y = 5.0
platform_height = 5.0

# Calculate the angles for the arm
base_angle, joint1_angle, joint2_angle = calculate_angles(x, y, platform_height)
print(f"Base: {base_angle}, Joint1: {joint1_angle}, Joint2: {joint2_angle}")

def control_gripper(x, y, platform_x, platform_y):
    # Calculate the distance to the block and platform
    distance_to_block = math.sqrt(x**2 + y**2)
    distance_to_platform = math.sqrt(platform_x**2 + platform_y**2)

    # Decide when to open or close the gripper based on proximity
    if distance_to_block < 1.0:  # Close gripper near the block
        return 1  # Close
    elif distance_to_platform < 1.0:  # Open gripper near the platform
        return 0  # Open
    else:
        return None  # No change
