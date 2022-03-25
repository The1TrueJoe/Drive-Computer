import threading
import logging
import time
import enum

from drive_control.computer_components.accelerometer import Accelerometer
from drive_control.computer_components.can_adapter import CAN_Adapter
import drive_control.computer_components.computer_lcd as LCD

from drive_control.modules.accessory_ctrl import Accessory_Controller
from drive_control.modules.direction_ctrl import Direction_Controller
from drive_control.modules.speed_ctrl import Speed_Controller

# Drive Computer Core Library
# Cart Control
#
# Class to control the cart's drive hardware
#
# Part of the GSSM Autonomous Golf Cart
# Written by Joseph Telaak, class of 2022

class MyCart:

    def __init__(self):
        # Assign the Modules
        self.direction_controller = Direction_Controller(can_address = "4081")
        self.accessory_controller = Accessory_Controller(can_address = "4082")
        self.speed_controller = Speed_Controller(can_address = "4083")

        # Setup the message logging
        logging.basicConfig(filename='my_cart.log', filemode='w', format=' %(asctime)s - %(message)s')

        # CAN Adapter
        self.can_adapter = CAN_Adapter()

        # Accelerometer
        self.accelerometer = Accelerometer()

        # Mode
        self.current_mode = self.Mode.AUTO

        # Start Message RX Processing
        listener = threading.Thread(target=self.listen, daemon=True)
        listener.start()

        # Start Perodic Update Requests
        perodic = threading.Thread(target=self.periodicLoop, daemon=True)
        perodic.start()

    # ----------------------------
    # Threads
    # ----------------------------

    def listen(self):
        message = self.can_adapter.read()

        if (message != ""):
            self.processMessage(message = message)

    def periodicLoop(self):
        while True:
            time.sleep(100)

    def processMessage(self, message):
        pass

    # ----------------------------
    # Mode
    # ----------------------------

    class Mode(enum.Enum):
        AUTO = 1
        MANUAL = 2
        TELEOP = 3

    def setManual(self):
        self.current_mode = self.Mode.MANUAL

        self.can_adapter.write(self.speed_controller.setManualInput())
        self.can_adapter.write(self.direction_controller.setWheelInputSteering())

    def setAuto(self):
        self.current_mode = self.Mode.AUTO

        self.can_adapter.write(self.speed_controller.setComputerInput())
        self.can_adapter.write(self.direction_controller.setControlledSteering())
        

    def setTeleop(self):
        self.current_mode = self.Mode.TELEOP

        self.can_adapter.write(self.speed_controller.setComputerInput())
        self.can_adapter.write(self.direction_controller.setControlledSteering())

    # ----------------------------
    # Wheel
    # ----------------------------

    def turnLeft(self, power = 128):
        self.can_adapter.write(self.direction_controller.runWheelLeft(power = power))

    def turnRight(self, power = 128):
        self.can_adapter.write(self.direction_controller.runWheelRight(power = power))

    # ----------------------------
    # Accel
    # ----------------------------

    def brake(self):
        self.can_adapter.write(self.direction_controller.enableBrakeMotor())
        self.can_adapter.write(self.direction_controller.runBrakeMotorForwards(power = 255))

    def disengageBrakes(self):
        self.can_adapter.write(self.direction_controller.runBrakeMotorForwards(power = 0))
        self.can_adapter.write(self.direction_controller.disableBrakeMotor())

    def setSpeed(self, speed):
        self.can_adapter.write(self.speed_controller.setSpeedPotPos(pos = speed))

    def completeStop(self):
        if not self.accelerometer.isStopped():
            self.brake()

            while not self.accelerometer.isStopped():
                time.sleep(100)

    # ----------------------------
    # Direction
    # ----------------------------

    def forwards(self):
        self.completeStop()
        self.can_adapter.write(self.speed_controller.setForwards())
        self.disengageBrakes()

    def reverse(self):
        self.completeStop()
        self.can_adapter.write(self.speed_controller.setReverse())
        self.disengageBrakes()

    # ----------------------------
    # Turn Signals
    # ----------------------------

    def rightSignal(self):
        self.can_adapter.write(self.accessory_controller.rightSignalBlink())

    def leftSignal(self):
        self.can_adapter.write(self.accessory_controller.leftSignalBlink())

    def stopSignal(self):
        self.can_adapter.write(self.accessory_controller.leftSignalOff())
        self.can_adapter.write(self.accessory_controller.rightSignalOff())

    # ----------------------------
    # Horn
    # ----------------------------

    def honk(self):
        self.can_adapter.write(self.accessory_controller.honk())

    # ----------------------------
    # Debug Display
    # ----------------------------

    def debugDisplayOn(self):
        self.can_adapter.send_string_to_adapter(LCD.on)

    def debugDisplayOff(self):
        self.can_adapter.send_string_to_adapter(LCD.off)

    def debugDisplayClear(self):
        self.can_adapter.send_string_to_adapter(LCD.clear)

    def debugDisplay(self, line_num, message):
        self.can_adapter.send_string_to_adapter(LCD.display(message = message, line_num = line_num))

