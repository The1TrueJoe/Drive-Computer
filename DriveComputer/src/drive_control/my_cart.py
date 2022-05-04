import threading
import logging
import time

from numpy import abs

from DriveComputer.src.drive_control.modules.accessory_ctrl import Accessory_Controller
from DriveComputer.src.drive_control.modules.direction_ctrl import Direction_Controller
from DriveComputer.src.drive_control.modules.drive_ctrl import Drive_Controller

from DriveComputer.src.drive_control.computer_components.can_adapter import CAN_Adapter
from DriveComputer.src.drive_control.computer_components.computer_lcd import LCD
from DriveComputer.src.drive_control.computer_components.mpu import MPU

import DriveComputer.src.drive_control.computer_components.can_adapter as can_util



# Drive Computer Core Library
# Cart Control
#
# Class to control the cart's drive hardware
#
# Part of the GSSM Autonomous Golf Cart
# Written by Joseph Telaak, class of 2022

class MyCart:

    def __init__(self):
        # Setup the message logging
        self.logger = logging.getLogger("hardware_manager")
        file_handler = logging.FileHandler("logs/hardware_manager.log")
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(threadName)s - %(message)s"))
        self.logger.addHandler(file_handler)

        # Assign the Modules
        self.logger.info("Preparing to Initialize Hardware Manager")
        self.direction_controller = Direction_Controller(can_address = "1")
        self.accessory_controller = Accessory_Controller(can_address = "2")
        self.drive_controller = Drive_Controller(can_address = "3")

        # Internal Hardware
        self.can = CAN_Adapter(serial_port='/dev/ttyUSB0')
        self.lcd = LCD(serial_port='/dev/ttyUSB1')
        self.mpu = MPU(serial_port='/dev/ttyUSB2')

        # Sub-Threads 
        self.listener = threading.Thread(target=self.listen, name="message_listener", daemon=True)   # Start Message RX Processing
        
        self.vars = {
            "accel_pos": 0,
            "accel_enable": 0,
            "direction": 0, # 0 Forwards, 1 Reverse
            "accel_pedal_sw": 0, 
            "accel_pedal_pos": 0,
            "right_signal": 0,
            "left_signal": 0,
            "head_light": 0,
            "tail_light": 0,
            "horn": 0,
            "buzzer": 0,
            "steering_motor_en": 0,
            "steering_wheel": 0, # 1 No Change, 2 Left, 3 Right
            "steering_pos": 0,
            "brake_motor_en": 0,
            "brake_pos": 0

        }

        # Init Message
        self.logger.info("Hardware Manager Initialization Preparation Complete")
        

    def intialize(self):
        # Init Message
        self.logger.info("Initializing Hardware Manager")

        # Starting listener thread
        self.listener.start()

        # Init Message
        self.logger.info("Hardware Manager Initialization Complete")


    # ----------------------------
    # Threads
    # ----------------------------

    # Listen for messages
    def listen(self):
        self.logger.info("CAN Listener Thread Starting")
        
        # Main loop
        while True:
            message = self.can.read()

            if message != "":
                message_id = can_util.getID()
                message = can_util.removeID(message=message).split(" ")

                if message[0] == "10" and message[1] == "10": # Is a data response message
                    if message_id == "3": # Message from drive controller
                        if message[2] == "10":
                            if message[3] == "10":
                                self.vars["accel_pos"] = can_util.eighttosixteen(int(message[6]), int(message[7]))
                            elif message[3] == "13":
                                self.vars["accel_pedal_pos"] = can_util.eighttosixteen(int(message[6]), int(message[7]))
                            elif message[3] == "15":
                                self.vars["accel_enable"] = can_util.canbool(int(message[7]))
                        elif message[2] == "13":
                            self.vars["direction"] = can_util.canbool(int(message[7]))
                        elif message[2] == "15":
                            self.vars["accel_pedal_sw"] = can_util.canbool(int(message[7]))

                    elif message_id == "2":
                        if message[2] == "10":
                            if message[3] == "1":
                                self.vars["right_signal"] = can_util.canbool(int(message[7]))
                            elif message[3] == "2":
                                self.vars["left_signal"] = can_util.canbool(int(message[7]))
                            elif message[3] == "3":
                                self.vars["head_light"] = can_util.canbool(int(message[7]))
                            elif message[3] == "4":
                                self.vars["tail_light"] = can_util.canbool(int(message[7]))
                            elif message[3] == "5":
                                self.vars["horn"] = can_util.canbool(int(message[7]))
                            elif message[3] == "6":
                                self.vars["buzzer"] = can_util.canbool(int(message[7]))

                    elif message_id == "1":
                        if message[2] == "1":
                            if message[3] == "10":
                                self.vars["steering_motor_en"] = can_util.canbool(int(message[7]))
                            elif message[3] == "15":
                                self.vars["steering_wheel"] = int(message[7])
                            elif message[3] == "16":
                                self.vars["steering_pos"] = can_util.eighttosixteen(int(message[6]), int(message[7]))
                        elif message[2] == "2":
                            if message[3] == "10":
                                self.vars["brake_motor_en"] = can_util.canbool(int(message[7]))
                            elif message[3] == "16":
                                self.vars["brake_pos"] = can_util.eighttosixteen(int(message[6]), int(message[7]))

    # ----------------------------
    # Wheel
    # ----------------------------

    # Turn left
    def turnLeft(self, power = 128):
        if self.vars["steering_motor_en"] != 1:
            self.can.write(self.direction_controller.steering_motor.enable())

        self.can.write(self.direction_controller.steering_motor.left(power))

    # Turn right
    def turnRight(self, power = 128):
        if self.vars["steering_motor_en"] != 1:
            self.can.write(self.direction_controller.steering_motor.enable())

        self.can.write(self.direction_controller.steering_motor.right(power))

    def stopTurn(self):
        self.can.write(self.direction_controller.steering_motor.disable())

    # Run to positon
    def turnToPos(self, position, power = 128):
        if abs(self.vars["steering_pos"] - position) > 500 and not (position < 600 and position > 400):
            if (self.vars["steering_pos"] - position < 0):
                self.leftSignal()
            else:
                self.rightSignal()

        if self.vars["steering_motor_en"] != 1:
            self.can.write(self.direction_controller.steering_motor.enable())

        self.can.write(self.direction_controller.steering_motor.goTo(position, power))

    # ----------------------------
    # Accel
    # ----------------------------

    # Enagage Brakes NOTE: Not recommended, use completestop instead
    def brake(self):
        # Disable the accelerator
        self.setSpeed(0)
        self.can.write(self.drive_controller.digital_accelerator.disable)

        # Brake
        self.can.write(self.direction_controller.brake_motor.pull())
        self.can.write(self.direction_controller.brake_motor.enable())

    # Disengages brakes
    def disengageBrakes(self):
        self.can.write(self.direction_controller.brake_motor.push())
        self.can.write(self.direction_controller.brake_motor.enable())

    # Come to a complete stop
    def completeStop(self):
        if self.vars["brake_pos"] <= 10:
            return
        else:
            self.brake()

            while self.vars["brake_pos"] > 10:
                time.sleep(.1)

            time.sleep(5)

    # Set the accelerator speed
    def setSpeed(self, speed: int):
        if (speed < 0):
                speed = 0
        elif (speed > 255):
                speed = 255

        self.can.write(self.drive_controller.digital_accelerator.setPotPos(speed))


    def enableAccelerator(self):
        self.can.write(self.drive_controller.digital_accelerator.enable())

    def disableAccelerator(self):
        self.can.write(self.drive_controller.digital_accelerator.disable())


    # ----------------------------
    # Direction
    # ----------------------------

    # Set the direction to forwards
    def forwards(self):
        if (self.vars["direction"] == 0):
            return

        # Come to a complete stop for hardware protection
        self.completeStop()
        
        # Change mode
        self.can.write(self.drive_controller.direction_controller.forwards())

        # Disengage brake pull
        self.disengageBrakes()

    # Set the direction to reverse
    def reverse(self):
        if (self.vars["direction"] == 1):
            return

        # Come to a complete stop for hardware protection
        self.completeStop()

        # Change mode
        self.can.write(self.drive_controller.direction_controller.reverse())

        # Disengage brake pull
        self.disengageBrakes()

    # ----------------------------
    # Turn Signals
    # ----------------------------

    # Blink the right signal
    def rightSignal(self):
        self.can.write(self.accessory_controller.right_signal.blink())

    # Blink the left signal
    def leftSignal(self):
        self.can.write(self.accessory_controller.left_signal.blink())

    # Stop signalling
    def stopSignal(self):
        self.can.write(self.accessory_controller.left_signal.off())
        self.can.write(self.accessory_controller.right_signal.off())

    # Hazards 
    def hazards(self):
        self.can.write(self.accessory_controller.tail_light.blink())

    # Stop hazards
    def stopHazards(self):
        self.can.write(self.accessory_controller.tail_light.off())

    # ----------------------------
    # Horn
    # ----------------------------

    def honk(self):
        self.can.write(self.accessory_controller.horn.honk())

