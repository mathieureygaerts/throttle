import time
import board
import digitalio
import analogio
import usb_hid
from hid_gamepad import Gamepad

gamepad = Gamepad(usb_hid.devices)

def range_map(value_input, in_min, in_max, out_min, out_max):
    """
    Map a value from a range to another.

    Args:
        x (float): Value to transform.
        in_min (float): Minimum value of the input range.
        in_max (float): Maximum value of the input range.
        out_min (float): Minimum value of the output range.
        out_max (float): Maximum value of the output range.

    Returns:
        float: The mapped value.
    """
    return (value_input - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

# Define buttons
num_of_simple_switches = 7
num_of_two_way_switches = 5
num_of_spring_switches = 2
total_buttons = num_of_simple_switches + num_of_two_way_switches * 2 + num_of_spring_switches

buttons = []
for num in range(total_buttons):
    pin = getattr(board, 'GP%i' % num)
    button = digitalio.DigitalInOut(pin)
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.DOWN
    buttons.append(button)

# Define sliders (linear potentiometers)
sliders = []
for num in range(3):
    if num == 1:
        # TODO: the 2nd potentiometers was a lemon, I need to replace it.
        # Skipping it for now.
        continue
    slider = analogio.AnalogIn(getattr(board, 'A%i' % num))
    sliders.append(slider)

# Main Loop
while True:
    # This loop is a bit hard to understand.
    # I needed to get the On & Off positions of each switches as their own button on the gamepad.
    button_activated = 1  # First Gamepad Button (On Position)
    for button in buttons:
        button_deactivated = button_activated + 1  # Set the next Gamepad's button for the Off position.
        if button.value: # If the physical button activates:
            gamepad.press_buttons(button_activated)
            gamepad.release_buttons(button_deactivated)
        else:
            gamepad.press_buttons(button_deactivated)
            gamepad.release_buttons(button_activated)
            
        button_activated = button_deactivated + 1  # Move on to the next set of buttons.

    slider_outputs = []
    for slider in sliders:
        average_list = []
        for reading in range(8):
        # The potentiometers are a bit noisy, averaging a few readings to help a tiny bit.
            average_list.append(slider.value)
            time.sleep(0.008)
        average = sum(average_list) / len(average_list)
        
        # Cropping some head and toe to stop the noise on the 2 ends.
        cropped_value = max(500, min(65035, average))
        map_range = int(range_map(cropped_value, 500, 65035, -127, 127))
        slider_outputs.append(map_range)
        
    gamepad.move_sliders(*slider_outputs)
    time.sleep(0.1)
