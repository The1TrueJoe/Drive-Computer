import threading
import logging
import time

from drive.drive import Mode

from drive_control.computer_components.accelerometer import Accelerometer
from drive_control.computer_components.can_adapter import CAN_Adapter
import drive_control.computer_components.computer_lcd as LCD

from drive_control.modules.accessory_ctrl import Accessory_Controller
from drive_control.modules.direction_ctrl import Direction_Controller
from drive_control.modules.drive_ctrl import Drive_Controller

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
        self.drive_controller = Drive_Controller(can_address = "4083")

        # CAN Adapter
        self.can_adapter = CAN_Adapter()

        # Sensors
        self.accelerometer = Accelerometer()

        # Sub-Threads 
        self.listener = threading.Thread(target=self.listen, name="message_listener", daemon=True)   # Start Message RX Processing
        self.perodic = threading.Thread(target=self.periodic, name="periodic_updater", daemon=True)  # Start Perodic Update Requests

        # Message Processing
        self.update_list = {
            "set speed": self.drive_controller.digital_accelerator.reqPos,
            "direction": self.drive_controller.direction_controller.reqDirection,
            "speed input": self.drive_controller.input_mode_controller.reqMode,


        }

        self.check_list = {
            "set speed": self.drive_controller.digital_accelerator.checkPosResponse,
            "forwards": self.drive_controller.direction_controller.checkDirectionResponse,
            "reverse": self.drive_controller.direction_controller.checkDirectionResponse,
            "manual speed input": self.drive_controller.input_mode_controller.checkModeResponse,
            "computer speed input": self.drive_controller.input_mode_controller.checkModeResponse,
            

        }

        self.get_list = {
            "set speed": self.drive_controller.digital_accelerator.readPosResponse,
            "forwards": self.drive_controller.direction_controller.isForwards,
            "reverse": self.drive_controller.direction_controller.isReverse,
            "manual speed input": self.drive_controller.input_mode_controller.isManual,
            "computer speed input": self.drive_controller.input_mode_controller.isComputer,


        }

        self.vars = {
            "set speed": 0,
            "forwards": True,
            "reverse": False,

        }

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
        while not self.drive_controller.isReady(self.can_adapter.read()):
            time.sleep(1)
        self.logger.info("All Modules Ready")

        # Enable all Modules
        self.logger.info("Sending enable message to modules")
        self.can_adapter.write(self.direction_controller.enable())
        self.can_adapter.write(self.accessory_controller.enable())
        self.can_adapter.write(self.drive_controller.enable())

        # Start Periodic Updater
        self.perodic.start()

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
            # Read message
            message = self.can_adapter.read()

            # Check message
            if (message != ""):
                self.processMessage(message=message)

    # Process the CAN Message
    def processMessage(self, message):
        for update_check in self.check_list.keys():
            if self.check_list[update_check](message=message):
                self.vars[update_check] = self.get_list[update_check](message=message)

    # Periodic loop
    def periodic(self):
        self.logger.info("Cart Periodic Updater Thread Starting")

        # Main Loop
        while True:
            # Complete Period
            time.sleep(10)

            # Update loop
            for update in self.update_list.keys():
                self.can_adapter.write(self.update_list[update]())

    # ----------------------------
    # Mode
    # ----------------------------

    # Apply the Manual Mode to hardware
    def applyManual(self):
        # Come to a complete stop for hardware protection
        self.completeStop()
  
        self.can_adapter.write(self.drive_controller.input_mode_controller.manual())
        self.can_adapter.write(self.direction_controller.steering_mode.setWheelInputSteering())

    # Apply the Auto Mode to hardware
    def applyAuto(self):
        # Come to a complete stop for hardware protection
        self.completeStop()

        # Change mode
        self.can_adapter.write(self.drive_controller.input_mode_controller.computer())
        self.can_adapter.write(self.direction_controller.steering_mode.setControlledSteering())
        
    # Apply the Teleop Mode to hardware
    def applyTeleop(self):
        # Come to a complete stop for hardware protection
        self.completeStop()

        # Change mode
        self.can_adapter.write(self.drive_controller.input_mode_controller.computer())
        self.can_adapter.write(self.direction_controller.steering_mode.setControlledSteering())

    # ----------------------------
    # Wheel
    # ----------------------------

    # Turn left
    def turnLeft(self, power = 128):
        self.can_adapter.write(self.direction_controller.steering_motor.forwards(power=power))

    # Turn right
    def turnRight(self, power = 128):
        self.can_adapter.write(self.direction_controller.steering_motor.backwards(power=power))

    # ----------------------------
    # Accel
    # ----------------------------

    # Enagage Brakes NOTE: Not recommended, use completestop instead
    def brake(self):
        # Disable the accelerator
        self.setSpeed(0)
        self.can_adapter.write(self.drive_controller.enabler.disable())

        # Brake
        self.can_adapter.write(self.direction_controller.brake_motor.enable())
        self.can_adapter.write(self.direction_controller.brake_motor.forwards(power = 255))

    # Disengages brakes
    def disengageBrakes(self):
        self.can_adapter.write(self.direction_controller.brake_motor.forwards(power = 0))
        self.can_adapter.write(self.direction_controller.brake_motor.enable())

    # Set the accelerator speed
    def setSpeed(self, speed):
        self.can_adapter.write(self.drive_controller.setSpeedPotPos(pos = speed))

    # Come to a complete stop
    def completeStop(self, disengage_brakes_on_stop = False):
        if not self.accelerometer.isStopped():
            # Engage brakes
            self.brake()

            # Hold till stop
            while not self.accelerometer.isStopped():
                time.sleep(0.5)

            # Disengage if necessary
            if disengage_brakes_on_stop:
                self.disengageBrakes()

    # ----------------------------
    # Direction
    # ----------------------------

    # Set the direction to forwards
    def forwards(self):
        # Come to a complete stop for hardware protection
        self.completeStop()
        
        # Change mode
        self.can_adapter.write(self.drive_controller.direction_controller.forwards())
        self.can_adapter.write(self.accessory_controller.rear_buzzer.off())

        # Disengage brake pull
        self.disengageBrakes()

    # Set the direction to reverse
    def reverse(self):
        # Come to a complete stop for hardware protection
        self.completeStop()

        # Change mode
        self.can_adapter.write(self.drive_controller.direction_controller.reverse())

        # Disengage brake pull
        self.disengageBrakes()

    # ----------------------------
    # Turn Signals
    # ----------------------------

    # Blink the right signal
    def rightSignal(self):
        self.can_adapter.write(self.accessory_controller.right_signal.blink())

    # Blink the left signal
    def leftSignal(self):
        self.can_adapter.write(self.accessory_controller.left_signal.blink())

    # Stop signalling
    def stopSignal(self):
        self.can_adapter.write(self.accessory_controller.left_signal.off())
        self.can_adapter.write(self.accessory_controller.right_signal.off())

    # Hazards 
    def hazards(self):
        self.can_adapter.write(self.accessory_controller.tail_light.blink())

    # Stop hazards
    def stopHazards(self):
        self.can_adapter.write(self.accessory_controller.tail_light.off())

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

