import usb_hid

# This is only one example of a gamepad descriptor.
# It may not suit your needs, or be supported on your host computer.

GAMEPAD_REPORT_DESCRIPTOR = bytes((
    0x05, 0x01,  # Usage Page (Generic Desktop Ctrls)
    0x09, 0x05,  # Usage (Game Pad)
    0xA1, 0x01,  # Collection (Application)
    0x85, 0x04,  #   Report ID (4)
    0x05, 0x09,  #   Usage Page (Button)
    0x19, 0x01,  #   Usage Minimum (Button 1)
    0x29, 0x40,  #   Usage Maximum (Button 64)
    0x15, 0x00,  #   Logical Minimum (0)
    0x25, 0x01,  #   Logical Maximum (1)
    0x75, 0x01,  #   Report Size (1)
    0x95, 0x40,  #   Report Count (64)
    0x81, 0x02,  #   Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0x05, 0x01,  #   Usage Page (Generic Desktop Ctrls)
    0x09, 0x30,  #   Usage (Slider)
    0x09, 0x31,  #   Usage (Slider)
#    0x09, 0x32,  #   Usage (Slider)
#    0x15, 0x00,  #   Logical Minimum (0)
#    0x25, 0xff, 0xff,  #   Logical Maximum (65535)
#    0x15, 0x01, 0x80,  #   Logical Minimum (-32767)
#    0x25, 0xff, 0x7f,  #   Logical Maximum (32767)
    0x15, 0x81,  #   Logical Minimum (-127)
    0x25, 0x7f,  #   Logical Maximum (127)
#    0x75, 0x10,  #   Report Size (16)
    0x75, 0x08,  #   Report Size (8)
    0x95, 0x02,  #   Report Count (3)
    0x81, 0x02,  #   Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0xC0,        # End Collection
))

gamepad = usb_hid.Device(
    report_descriptor=GAMEPAD_REPORT_DESCRIPTOR,
    usage_page=0x01,           # Generic Desktop Control
    usage=0x05,                # Gamepad
    report_ids=(4,),           # Descriptor uses report ID 4.
    in_report_lengths=(10,),    # This gamepad sends 11 bytes in its report.
#    in_report_lengths=(14,),    # This gamepad sends 11 bytes in its report.
    out_report_lengths=(0,),   # It does not receive any reports.
)

usb_hid.enable(
    (usb_hid.Device.KEYBOARD,
     usb_hid.Device.MOUSE,
     usb_hid.Device.CONSUMER_CONTROL,
     gamepad)
)
