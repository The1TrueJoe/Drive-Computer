import serial
import logging

# Drive Computer Core Library
#
# Class to access the drive computer's CAN adapter
# Accepts and receives messages
#
# Part of the GSSM Autonomous Golf Cart
# Written by Joseph Telaak, class of 2022

class CAN_Adapter:

    # Constructor
    #
    # serial_port: Serial port where the Arduino CAN Adapter is located
    # baud: Arduino serial baud rate

    def __init__(self, serial_port = '/dev/ttyUSB0', baud = 11520):
        # Setup the message logging
        self.logger = logging.getLogger("can")
        file_handler = logging.FileHandler("logs/can.log")
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
        self.logger.addHandler(file_handler)

        # Init Message
        self.logger.info("Initializing CAN Adapter")

        try:
            # Attempt to establish connection to CAN adapter
            self.logger.info(f"Attempting to connect to {serial_port} at {baud} baud")
            self.arduino = serial.Serial(port = serial_port, baudrate = baud, timeout = .1)

            self.logger.info(f"Connection sucessful to {serial_port} at {baud} baud")

        except:
            self.logger.fatal(f"Failed To Connect to {serial_port} at {baud} baud")
            print("FATAL: Cannot connect to the drive computer's CAN adapter")
            quit()

        # Init Message
        self.logger.info("CAN Adapter Initialized")
            

    # Return a reference to the device
    #
    # return: arduino

    def get_device(self):
        return self.arduino


    # Manually send a message to the CAN Adapter
    #
    # message: Message to send

    def send_string_to_adapter(self, message):
        self.logger.debug("MAN: " + message)
        self.arduino.write(message)


    # Read received CAN message
    #
    # return: Received can message

    def read(self):
        output = self.arduino.readLine()

        if "CAN-RX:" in output:
            self.logger.debug("RX: " + str(output))
            return str(output).replace("CAN-RX: ", "")

        elif "CAN-TX:" in output:
            self.logger.debug("TX: " + str(output))

        else:
            self.logger.info("Adapter-Hardware: " + str(output))

        return ""


    # Send CAN message
    #
    # id: 32-bit CAN Bus ID
    # data: 8x 8-bit CAN Message

    def write(self, id, data):
        # Check Message Size
        if len(data) != 8:
            self.logger.warning(f"Invalid Message Size {len(data)}")
            return

        # Format Message
        formatted_data = ""
        for dat in data:
            formatted_data += f"{dat} "

        # Send message as String
        output = f"({id}) {formatted_data}"
        self.logger.debug(f"TX: {output}")
        self.arduino.write(f"CMD-Send: {output}")

    # Send CAN message
    def write(self, message):
        self.logger.debug(f"TX: {message}")
        self.arduino.write(f"CMD-Send: {message}")
