from calculate import calculate_angles, control_gripper
from recieve import send_angles


# Coordinates of the block and platform
block_x, block_y = 12.0, 5.0
platform_x, platform_y = 15.0, 8.0
platform_height = 5.0

# Calculate angles for the arm
base_angle, joint1_angle, joint2_angle = calculate_angles(block_x, block_y, platform_height)

# Determine if the gripper should open or close
gripper_state = control_gripper(block_x, block_y, platform_x, platform_y)

# Send the angles and gripper state via Bluetooth
if gripper_state is not None:
    send_angles(base_angle, joint1_angle, joint2_angle, gripper_state)
