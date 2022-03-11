import serial
import logging

class CAN_Adapter:

    def __init__(self, serial_port = '/dev/ttyUSB0', baud = 11520):
        logging.basicConfig(filename = 'can.log', filemode = 'w', format =' %(asctime)s - %(message)s')

        logging.info(f"Attempting to connect to {serial_port} at {baud} baud")

        try:
            self.arduino = serial.Serial(port = serial_port, baudrate = baud, timeout = .1)
            logging.info(f"Connection sucessful to {serial_port} at {baud} baud")

        except:
            logging.warning(f"Failed To Connect to {serial_port} at {baud} baud")


    def read(self):
        output = self.arduino.readLine()

        if "CAN-RX:" in output:
            logging.debug("RX: " + str(output))
            return str(output).replace("CAN-RX: ", "")

        elif "CAN-TX:" in output:
            logging.debug("TX: " + str(output))

        else
            logging.info("Adapter-Hardware: " + str(output))

        return ""

    def write(self, id, data):
        if (len(data) != 8):
            logging.warning(f"Invalid Message Size {len(data)}")
            return

        formatted_data = ""
        for dat in data:
            formatted_data += f"{dat} "

        logging.debug("TX: " + str(output))
        serial.write(f"CMD-Send: ({id}) {formatted_data}")