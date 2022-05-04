import logging

# Drive Computer Core Library
# Speed Controller Module
#
# This module controls the cart's built-in speed controller.
# Controls:
#   Acceleration
#   Fwd/Rev
#   Motor Control Enable
#
# Hardware definition class to store messages for this module
#
# Part of the GSSM Autonomous Golf Cart
# Written by Joseph Telaak, class of 2022

class Drive_Controller:

    def __int__(self, can_address = 3):
        # CAN Address
        self.can_address = can_address

        # Setup the message logging
        self.logger = logging.getLogger("drive_controller")
        file_handler = logging.FileHandler("logs/drive_ctrl.log")
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
        self.logger.addHandler(file_handler)

        # Components
        self.digital_accelerator = self.Digital_Accelerator(can_address=self.can_address, logger=self.logger)
        self.direction_controller = self.Direction_Controller(can_address=self.can_address, logger=self.logger)
        self.accelerator_pedal = self.Accelerator_Pedal(can_address=self.can_address, logger=self.logger)

    # Digital Accelerator Component
    class Digital_Accelerator:
        
        def __init__(self, can_address, logger):
            self.logger = logger
            self.can_address = can_address

        def setPotPos(self, pos):
            self.logger.info("Setting Accelerator Pot Position")
            return f"({self.can_address}) 10 10 10 {pos} 0 0 0 0"

        def increment(self):
            self.logger.info("Incrementing Accelerator")
            return f"({self.can_address}) 11 10 1 0 0 0 0 0"

        def decrement(self):
            self.logger.info("Decrementing Accelerator")
            return f"({self.can_address}) 11 10 1 0 0 0 0 0"

        def reqPos(self):
            self.logger.info("Requesting Accelerometer Positon")
            return f"({self.can_address}) 12 10 10 0 0 0 0 0"

        def enable(self):
            self.logger.info("Enabling Digital Accelerator")
            return f"({self.can_address}) 10 10 15 1 0 0 0 0"

        def disable(self):
            self.logger.info("Disabling Digital Accelerator")
            return f"({self.can_address}) 10 10 15 2 0 0 0 0"

        def reqEn(self):
            self.logger.info("Requesing Enable Status")
            return f"({self.can_address}) 12 10 15 0 0 0 0 0"

    class Accelerator_Pedal:

        def __init__(self, can_address, logger):
            self.logger = logger
            self.can_address = can_address

        def reqPos(self):
            self.logger.info("Requesing Accelerator Pedal Pos")
            return f"({self.can_address} 12 10 13 0 0 0 0 0"

    class Direction_Controller:

        def __init__(self, can_address, logger):
            self.logger = logger
            self.can_address = can_address

        def reverse(self):
            self.logger.info("Switching to Reverse")
            return f"({self.can_address}) 10 13 2 0 0 0 0 0"

        def forwards(self):
            self.logger.info("Switching to Forwards")
            return f"({self.can_address}) 10 13 1 0 0 0 0 0"

        def reqDirection(self):
            self.logger.info("Requesing Direction")
            return f"({self.can_address}) 10 12 0 0 0 0 0 0"
