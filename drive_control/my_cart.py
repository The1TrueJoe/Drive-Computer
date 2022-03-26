import threading
import logging
import time

from drive.drive import Mode

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
        # Setup the message logging
        self.logger = logging.getLogger("hardware_manager")
        file_handler = logging.FileHandler("logs/hardware_manager.log")
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(threadName)s - %(message)s"))
        self.logger.addHandler(file_handler)

        # Assign the Modules
        self.logger.info("Preparing to Initialize Hardware Manager")
        self.direction_controller = Direction_Controller(can_address = "4081")
        self.accessory_controller = Accessory_Controller(can_address = "4082")
        self.speed_controller = Speed_Controller(can_address = "4083")

        # CAN Adapter
        self.can_adapter = CAN_Adapter()

        # Sensors
        self.accelerometer = Accelerometer()

        # Sub-Threads 
        self.listener = threading.Thread(target=self.listen, name="message_listener", daemon=True)   # Start Message RX Processing
        self.perodic = threading.Thread(target=self.periodic, name="periodic_updater", daemon=True)  # Start Perodic Update Requests



        # Init Message
        self.logger.info("Hardware Manager Initialization Preparation Complete")
        

    def intialize(self):
        # Init Message
        self.logger.info("Initializing Hardware Manager")

        # Starting listener thread
        self.listener.start()

        # Wait for all modules
        self.logger.info("Waiting for all modules to annouce ready")
        while not self.direction_controller.isReady(self.can_adapter.read()):
            time.sleep(1)
        while not self.accessory_controller.isReady(self.can_adapter.read()):
            time.sleep(1)
        while not self.speed_controller.isReady(self.can_adapter.read()):
            time.sleep(1)
        self.logger.info("All Modules Ready")

        # Enable all Modules
        self.logger.info("Sending enable message to modules")
        self.can_adapter.write(self.direction_controller.enable())
        self.can_adapter.write(self.accessory_controller.enable())
        self.can_adapter.write(self.speed_controller.enable())

        # Start Periodic Updater
        self.perodic.start()

        # Init Message
        self.logger.info("Hardware Manager Initialization Complete")


    # ----------------------------
    # Threads
    # ----------------------------

    def listen(self):
        self.logger.info("CAN Listener Thread Starting")

        while True:
            message = self.can_adapter.read()

            if (message != ""):
                self.processMessage(message = message)

    def periodic(self):
        self.logger.info("Cart Periodic Updater Thread Starting")

        while True:
            time.sleep(100)

    def processMessage(self, message):
        pass

    # ----------------------------
    # Mode
    # ----------------------------

    def applyManual(self):
        self.completeStop()

        self.can_adapter.write(self.speed_controller.setManualInput())
        self.can_adapter.write(self.direction_controller.setWheelInputSteering())

    def applyAuto(self):
        self.completeStop()

        self.can_adapter.write(self.speed_controller.setComputerInput())
        self.can_adapter.write(self.direction_controller.setControlledSteering())
        
    def applyTeleop(self):
        self.completeStop()

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
        self.can_adapter.write(self.speed_controller.direction_controller.forwards())
        self.disengageBrakes()

    def reverse(self):
        self.completeStop()
        self.can_adapter.write(self.speed_controller.direction_controller.reverse())
        self.disengageBrakes()

    # ----------------------------
    # Turn Signals
    # ----------------------------

    def rightSignal(self):
        self.can_adapter.write(self.accessory_controller.right_signal.blink())

    def leftSignal(self):
        self.can_adapter.write(self.accessory_controller.left_signal.blink())

    def stopSignal(self):
        self.can_adapter.write(self.accessory_controller.left_signal.off())
        self.can_adapter.write(self.accessory_controller.right_signal.off())

    # ----------------------------
    # Horn
    # ----------------------------

    def honk(self):
        self.can_adapter.write(self.accessory_controller.horn.honk())

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

