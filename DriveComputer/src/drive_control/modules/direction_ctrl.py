import src.drive_control.computer_components.can_adapter as can_util
import logging

# Drive Computer Core Library
# Direction Controller Module
#
# This module controls both steering and braking
#
# Hardware definition class to store messages for this module
#
# Part of the GSSM Autonomous Golf Cart
# Written by Joseph Telaak, class of 2022

class Direction_Controller:

    def __int__(self, can_address = 1):
        # CAN Address
        self.can_address = can_address

        # Setup the message logging
        self.logger = logging.getLogger("direction_controller")
        file_handler = logging.FileHandler("logs/direction_ctrl.log")
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
        self.logger.addHandler(file_handler)

        # Components
        self.steering_motor = self.Steering_Motor(can_address=self.can_address, logger=self.logger)
        self.wheel_input = self.Wheel(can_address=self.can_address, logger=self.logger)
        self.brake_motor = self.Brake_Motor(can_address=self.can_address, logger=self.logger)
    
    # ----------------------------
    # Steering Motor Controller
    # ----------------------------

    class Steering_Motor:

        def __init__(self, can_address, logger):
            self.can_address = can_address
            self.logger = logger

        # Disable Steering Motor
        def disable(self):
            self.logger.debug("Disabling Steering Motor")
            return f"({self.can_address}) 10 1 10 1 0 0 0 0"

        # Enable Steering Motor
        def enable(self):
            self.logger.debug("Enabling Steering Motor")
            return f"({self.can_address}) 10 1 10 2 0 0 0 0"

        def reqStatus(self):
            self.logger.debug("Requesting the Steering Motor Status")
            return f"({self.can_address}) 12 1 10 0 0 0 0"

        # Run Motor Forwards
        def left(self, power = 255):
            self.logger.debug(f"Running Steering Motor Forwards, Power: {power}")
            return f"({self.can_address}) 10 1 12 1 {power} 0 0 0"

        # Run Motor Backwards
        def right(self, power = 255):
            self.logger.debug(f"Running Steering Motor Backwards, Power: {power}")
            return f"({self.can_address}) 10 1 12 2 {power} 0 0 0"

        def goTo(self, postion, power = 255):
            self.logger.debug(f"Running to Postion {postion} at {power}")
            return f"({self.can_address}) 11 1 {power} {can_util.sixteentoeight_coarse(postion)} {can_util.sixteentoeight_fine(postion)} 0 0 0"

        # Request the steering motor position
        def reqPos(self):
            self.logger.debug("Requesting to Current Steering Motor Position")
            return f"({self.can_address}) 12 1 16 0 0 0 0"

    # ----------------------------
    # Steering Wheel Input
    # ----------------------------

    class Wheel:

        def __init__(self, can_address, logger):
            self.can_address = can_address
            self.logger = logger

        def reqPos(self):
            self.logger.info("Requesing Steering Wheel Change")
            return f"({self.can_address}) 12 1 15 0 0 0 0 0"

    class Brake_Motor:

        def __init__(self, can_address, logger):
            self.can_address = can_address
            self.logger = logger

        # Disable Brake Motor
        def disable(self):
            self.logger.debug("Disabling Brake Motor")
            return f"({self.can_address}) 10 2 10 1 0 0 0 0"

        # Enable Steering Motor
        def enable(self):
            self.logger.debug("Enabling Brake Motor")
            return f"({self.can_address}) 10 2 10 2 0 0 0 0"

        def reqStatus(self):
            self.logger.debug("Requesting the Brake Motor Status")
            return f"({self.can_address}) 12 2 10 0 0 0 0"

        # Run Motor Forwards
        def pull(self, power = 255):
            self.logger.debug(f"Running Brake Motor Forwards, Power: {power}")
            return f"({self.can_address}) 10 2 12 1 {power} 0 0 0"

        # Run Motor Backwards
        def push(self, power = 255):
            self.logger.debug(f"Running Brake Motor Backwards, Power: {power}")
            return f"({self.can_address}) 10 2 12 2 {power} 0 0 0"

        # Request the steering motor position
        def reqPos(self):
            self.logger.debug("Requesting to Current Brake Motor Position")
            return f"({self.can_address}) 12 2 16 0 0 0 0"