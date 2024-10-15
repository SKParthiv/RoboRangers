import serial
import time

# Setup Bluetooth communication (update the port as necessary)
bluetooth = serial.Serial('/dev/rfcomm0', 9600)  # Replace with your Bluetooth port
time.sleep(2)  # Wait for the connection to establish

def send_angles(base_angle, joint1_angle, joint2_angle, gripper_state):
    # Format message: base_angle,joint1_angle,joint2_angle,gripper_state\n
    message = f"{base_angle},{joint1_angle},{joint2_angle},{gripper_state}\n"
    
    # Send the message
    bluetooth.write(message.encode('utf-8'))

    # Optional: Print confirmation
    print(f"Sent: {message}")

# Example usage:
send_angles(90, 45, 30, 1)  # Send angles and close gripper
time.sleep(2)
send_angles(90, 90, 90, 0)  # Send angles and open gripper
