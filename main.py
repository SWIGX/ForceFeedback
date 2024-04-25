import os

# link to how to access the usb devices:
# https://github.com/pyusb/pyusb/blob/master/docs/tutorial.rst
import usb.core


def main():
    print("Started program...")

    #####################
    # EVENT FILE NAME

    # get the event file name for the Fanatec wheel
    try:
        event_file_name = get_event_file_name()
        print(f"Device file name: {event_file_name}")
    except FileNotFoundError as e:
        print(e)
        exit(1)  # exit program with error

    #####################
    # ENDPOINT ADDRESSES

    # get the bEndpointAddresses for the Fanatec wheel
    # get_endpointaddress()

    #####################

    print("Program ended successfully")
    exit(0)  # exit program successfully


##################################################################
# GET DEVICE FILE NAME FOR FANATEC WHEEL
def get_event_file_name():

    # Vendor id for Fanatec wheel
    VENDOR_ID = "0eb7"

    # Product id for Fanatec wheel
    PRODUCT_ID = "0020"

    # Run lsusb command to list USB devices and parse the output
    lsusb_output = os.popen("lsusb").read()

    print(lsusb_output)

    # Iterate over each line of lsusb output
    for line in lsusb_output.splitlines():
        # Check if the line contains the vendor and product IDs
        if VENDOR_ID in line and PRODUCT_ID in line:
            # Extract the bus and device number from the line
            bus_number, device_number = line.split()[:2]
            # Construct the path to the event file using bus and device number
            event_file_path = f"/dev/input/event{device_number}"
            # Check if the event file exists
            if os.path.exists(event_file_path):
                return event_file_path

    # If no event file is found, raise FileNotFoundError
    raise FileNotFoundError("Input event device file not found.")

    return

    # Find the USB device directory
    usb_dirs = [
        d
        for d in os.listdir("/sys/bus/usb/devices/")
        if f"{VENDOR_ID}:{PRODUCT_ID}" in d
    ]

    print(usb_dirs)

    # if no usb device found, return false
    if not usb_dirs:
        raise FileNotFoundError("USB device not found.")

    # Choose the first found directory, you may want to refine this logic if multiple directories are found
    USB_DIR = os.path.join("/sys/bus/usb/devices/", usb_dirs[0])

    # Navigate to the input directory to find the event device file
    input_dir = os.path.join(USB_DIR, "input")
    event_files = [f for f in os.listdir(input_dir) if f.startswith("event")]

    # if no event file found, return false
    if not event_files:
        raise FileNotFoundError("Input event device file not found.")

    # Choose the first found event file, you may want to refine this logic if multiple files are found
    EVENT_FILE = os.path.join(input_dir, event_files[0])

    # Return the event device file name
    return EVENT_FILE


##################################################################
# GET ENDPOINT ADDRESSES FOR FANATEC WHEEL
def get_endpointaddress():

    # Vendor id for Fanatec wheel
    VENDOR_ID = 0x0EB7

    # Product id for Fanatec wheel
    PRODUCT_ID = 0x0020

    # find device with vendor and product id
    dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

    # check if device is connected
    if dev is None:
        raise ValueError("Device is not connected")
    else:

        # print all information about the device
        # print(dev)

        # enter configurations of the device
        for cfg in dev:

            # enter interfaces of the device
            for intf in cfg:

                # enter endpoints of the device
                # index 0 is IN endpoint
                # index 1 is OUT endpoint
                for ep in intf:
                    print(
                        "get_endpointaddress: "
                        + "bEndpointAddress at endpoint-index "
                        + str(ep.index)
                        + " is        :          "
                        + str(ep.bEndpointAddress)
                    )

                    # how to write a string to an endpoint address 1
                    # dev.write(1, 'test')

                    # maybe this???
                    # dev.write(ep[0].bEndpointAddress, "")


# necessary to run main
if __name__ == "__main__":
    main()
