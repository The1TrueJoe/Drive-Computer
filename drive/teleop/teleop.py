import sys
import logging
import time

from drive.drive import Mode

from drive.teleop.controller import Gamepad
from drive.teleop.remote_drive_server import Remote_Drive_Server

from drive_control.my_cart import MyCart

# Drive Computer
# Teleop Drive Mode
#
# Part of the GSSM Autonomous Golf Cart
# Written by: Joseph Telaak, class of 2022

class Teleop:

    def __init__(self, cart):
        # Kill
        self.kill = False

        # Mode
        self.mode = Mode.TELEOP

        # Setup the message logging
        self.logger = logging.getLogger("teleop_mode")
        file_handler = logging.FileHandler("logs/teleop_mode.log")
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
        self.logger.addHandler(file_handler)

        # Hardware
        if isinstance(cart, MyCart):
            self.my_cart = cart

        # Not instance
        else:
            self.logger.fatal("FAILED TO PASS CART HARDWARE")
            sys.exit(1)

        # Gamepad
        self.gamepad = Gamepad()

        # Connector
        self.connector = Remote_Drive_Server(gamepad=self.gamepad)

    # Mode Initialization, Called Once
    def initialize(self):
        self.my_cart.applyTeleop()
        self.connector.intialize()

        wait_time = 0

        while not self.connector.connection_established:
            wait_time += 1
            time.sleep(1)

            if wait_time % 5:
                self.logger.info("Waiting for Connection")

        self.logger.info("Teleop Initialization Complete")

    # Periodic Loop
    def perodic(self):
        ### NOTE: Connections Are Killed From the Client With a Pre-Defined Button
        while self.connector.connection_established and not self.kill:
            pass

    # Kills the Periodic Loop NOTE: Closing process is in the exit method
    def kill(self):
        self.kill = True

    def exit(self):
        self.connector.kill()
        self.my_cart.completeStop()