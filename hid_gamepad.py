# SPDX-FileCopyrightText: 2018 Dan Halbert for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`Gamepad`
====================================================

* Author(s): Dan Halbert
"""

import struct
import time

from adafruit_hid import find_device


class Gamepad:
    """Emulate a generic gamepad controller with 16 buttons,
    numbered 1-16, and two joysticks, one controlling
    ``x` and ``y`` values, and the other controlling ``z`` and
    ``r_z`` (z rotation or ``Rz``) values.

    The joystick values could be interpreted
    differently by the receiving program: those are just the names used here.
    The joystick values are in the range -127 to 127."""

    def __init__(self, devices):
        """Create a Gamepad object that will send USB gamepad HID reports.

        Devices can be a list of devices that includes a gamepad device or a gamepad device
        itself. A device is any object that implements ``send_report()``, ``usage_page`` and
        ``usage``.
        """
        self._gamepad_device = find_device(devices, usage_page=0x1, usage=0x05)

        # Reuse this bytearray to send mouse reports.
        # Typically controllers start numbering buttons at 1 rather than 0.
        # report[0] buttons 1-8 (LSB is button 1)
        # report[1] buttons 9-16
        # report[2] buttons 17-24
        # report[3] buttons 25-32
        # report[4] buttons 33-40
        # report[5] buttons 41-48
        # report[6] buttons 49-56
        # report[7] buttons 57-64
        # report[8] slider 1 : 0 to 65535
        # report[9] slider 1 : 0 to 65535
        # report[10] slider 2 : 0 to 65535
        # report[11] slider 2: 0 to 65535
        # report[12] slider 3: 0 to 65535
        # report[13] slider 3: 0 to 65535

        self._report = bytearray(10)

        # Remember the last report as well, so we can avoid sending
        # duplicate reports.
        self._last_report = bytearray(10)

        # Store settings separately before putting into report. Saves code
        # especially for buttons.
        self._buttons_state = 0
        self._slider_one = 0
        self._slider_two = 0
        #self._slider_three = 0

        # Send an initial report to test if HID device is ready.
        # If not, wait a bit and try once more.
        try:
            self.reset_all()
        except OSError:
            time.sleep(1)
            self.reset_all()

    def press_buttons(self, *buttons):
        """Press and hold the given buttons."""
        for button in buttons:
            self._buttons_state |= 1 << self._validate_button_number(button) - 1
        self._send()

    def release_buttons(self, *buttons):
        """Release the given buttons."""
        for button in buttons:
            self._buttons_state &= ~(1 << self._validate_button_number(button) - 1)
        self._send()

    def release_all_buttons(self):
        """Release all the buttons."""

        self._buttons_state = 0
        self._send()

    def click_buttons(self, *buttons):
        """Press and release the given buttons."""
        self.press_buttons(*buttons)
        self.release_buttons(*buttons)

    def move_sliders(self, one=None, two=None, three=None):
        """Set and send the given joystick values.
        The joysticks will remain set with the given values until changed

        One joystick provides ``x`` and ``y`` values,
        and the other provides ``z`` and ``r_z`` (z rotation).
        Any values left as ``None`` will not be changed.

        All values must be in the range -127 to 127 inclusive.

        Examples::

            # Change x and y values only.
            gp.move_joysticks(x=100, y=-50)

            # Reset all joystick values to center position.
            gp.move_joysticks(0, 0, 0, 0)
        """
        if one is not None:
            self._slider_one = self._validate_joystick_value(one)
        if two is not None:
            self._slider_two = self._validate_joystick_value(two)
        #if three is not None:
        #    self._slider_three = self._validate_joystick_value(three)
        self._send()

    def reset_all(self):
        """Release all buttons and set joysticks to zero."""
        self._buttons_state = 0
        self._slider_one = 0
        self._slider_two = 0
        #self._slider_three = 0
        self._send(always=True)

    def _send(self, always=False):
        """Send a report with all the existing settings.
        If ``always`` is ``False`` (the default), send only if there have been changes.
        """
        struct.pack_into(
            "<Qbb",
            # "<QHHH",
            self._report,
            0,
            self._buttons_state,
            self._slider_one,
            self._slider_two,
            #self._slider_three,
        )

        if always or self._last_report != self._report:
            self._gamepad_device.send_report(self._report)
            # Remember what we sent, without allocating new storage.
            self._last_report[:] = self._report

    @staticmethod
    def _validate_button_number(button):
        if not 1 <= button <= 64:
            raise ValueError("Button number must in range 1 to 24")
        return button

    @staticmethod
    def _validate_joystick_value(value):
        if not -32768 <= value <= 32767:
            raise ValueError("Joystick value must be in range -127 to 127")
        return value
