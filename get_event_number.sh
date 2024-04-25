#!/bin/bash

VID="0eb7"
PID="0020"

# Find the USB device directory
USB_DIR=$(find /sys/bus/usb/devices/ -maxdepth 1 -type d -name "*:${VID}:${PID}*")

if [ -z "$USB_DIR" ]; then
    echo "USB device not found."
    exit 1
fi

# Navigate to the input directory to find the event device file
INPUT_DIR="$USB_DIR/input"
EVENT_FILE=$(ls -1 $INPUT_DIR/event*)

if [ -z "$EVENT_FILE" ]; then
    echo "Input event device file not found."
    exit 1
fi

echo "Device file name: $EVENT_FILE"


