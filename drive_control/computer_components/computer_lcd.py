import serial
import logging

# Drive Computer Core Library
# Drive Computer LCD
#
# Drive Computer LCD
#
# Part of the GSSM Autonomous Golf Cart
# Written by Joseph Telaak, class of 2022

class LCD:

    def __init__(self, serial_port = '/dev/ttyUSB1', baud = 11520):
        # Setup the message logging
        self.logger = logging.getLogger("lcd")
        file_handler = logging.FileHandler("logs/lcd.log")
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
        self.logger.addHandler(file_handler)

        # Init Message
        self.logger.info("Initializing LCD Adapter")

        try:
            # Attempt to establish connection to CAN adapter
            self.logger.info(f"Attempting to connect to {serial_port} at {baud} baud")
            self.arduino = serial.Serial(port = serial_port, baudrate = baud, timeout = .1)

            self.logger.info(f"Connection sucessful to {serial_port} at {baud} baud")

        except:
            self.logger.fatal(f"Failed To Connect to {serial_port} at {baud} baud")
            print("FATAL: Cannot connect to the drive computer's LCD adapter")
            quit()

        # Init Message
        self.logger.info("LCD Adapter Initialized")

    # Return a reference to the device
    #
    # return: arduino

    def get_device(self):
        return self.arduino

    # Read received serial message
    #
    # return: Received serial message

    def read(self):
        output = self.arduino.readLine()
        self.logger.debug("RX: " + str(output))

        return output


    # Manually send a message to the LCD Adapter
    #
    # message: Message to send

    def write(self, message):
        self.logger.debug("TX: " + message)
        self.arduino.write(message)

    # Clear the LCD Screen
    def clear(self):
        self.write("Display: Clear")

    # Turn off the LCD screen
    def off(self):
        self.write("Display: Off")

    # Turn on the LCD screen
    def on(self):
        self.write("Display: On")

    # Send a message to the LCD screen
    #
    # message: Message to display
    # line_num: Line number to display on (1-2)

    def display(self, message, line_num):
        if line_num >= 3:
            line_num = 2
        elif line_num <= 0:
            line_num = 1

        self.write(f"Display: L{line_num}: {message}")