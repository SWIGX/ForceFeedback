
# vendor id for fanatec wheel 
VID="0eb7"

# product id for fanatec wheel 
PID="0020"

# find the USB device directory 
USB_DIR=$(find /sys/bus/usb/devices/ -maxdepth 1 -type d -name "*:${VID}:${PID}*")

# check if the USB device directory was found 
if [ -z "$USB_DIR" ]; then
    echo "USB device not found."
    exit 1
fi

# navigate to the input directory to find the event device file
INPUT_DIR="$USB_DIR/input"
EVENT_FILE=$(ls -1 $INPUT_DIR/event*)

# check if the event device file was found 
if [ -z "$EVENT_FILE" ]; then
    echo "Input event device file not found."
    exit 1
fi

# print the event device file name 
echo "Device file name: $EVENT_FILE"
