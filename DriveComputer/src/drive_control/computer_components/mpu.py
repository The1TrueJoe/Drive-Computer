import serial
import logging

# Drive Computer Core Library
# Drive Computer MPU
#
# Drive Computer MPU
#
# Part of the GSSM Autonomous Golf Cart
# Written by Joseph Telaak, class of 2022

class MPU:

    def __init__(self, serial_port = '/dev/ttyUSB2', baud = 11520):
        # Setup the message logging
        self.logger = logging.getLogger("mpu")
        file_handler = logging.FileHandler("logs/mpu.log")
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
            print("FATAL: Cannot connect to the drive computer's MPU adapter")
            quit()

        # Init Message
        self.logger.info("MPU Adapter Initialized")