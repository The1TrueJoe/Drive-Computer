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

    def __init__(self, cart: MyCart):
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
        self.my_cart = cart

        # Gamepad
        self.gamepad = Gamepad()

        # Connector
        self.connector = Remote_Drive_Server(gamepad=self.gamepad)

        # Controller Buttons
        self.button_map = {
            'BTN_TL': self.noAction,
            'BTN_TR': self.noAction,
            'BTN_NORTH': self.my_cart.honk,
            'BTN_EAST': self.noAction,
            'BTN_SOUTH': self.noAction,
            'BTN_WEST': self.noAction,
            'BTN_THUMBL': self.noAction,
            'BTN_THUMBR': self.noAction,
            'BTN_START': self.noAction,
            'BTN_SELECT': self.noAction,
            'DPAD_NORTH': self.my_cart.forwards,
            'DPAD_SOUTH': self.my_cart.reverse,
            'DPAD_EAST': self.my_cart.rightSignal,
            'DPAD_WEST': self.my_cart.leftSignal

        }

        self.stick_map = {
            'LSTICK_X': self.noAction,
            'LSTICK_Y': self.noAction,
            'RSTICK_X': self.noAction,
            'RSTICK_Y': self.my_cart.setSpeed

        }

        self.trigger_map = {
            'ABS_Z': self.my_cart.turnLeft,
            'ABS_RZ': self.my_cart.turnRight

        }

    # Mode Initialization, Called Once
    def initialize(self):
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
            for button_event in self.gamepad.buttons.keys():
                if self.gamepad.buttons[button_event]:
                    self.button_map[button_event]()
                    continue

            for stick_event in self.gamepad.sticks.keys():
                if self.gamepad.sticks[stick_event] != 0.0:
                    self.stick_map[stick_event](self.gamepad.sticks[stick_event])
                    continue

            for trigger_event in self.gamepad.triggers.keys():
                if self.gamepad.triggers[trigger_event] != 0:
                    self.trigger_map[trigger_event](self.gamepad.triggers[trigger_event])
                    continue

    # Kills the Periodic Loop NOTE: Closing process is in the exit method
    def kill(self):
        self.kill = True

    def exit(self):
        self.connector.kill()
        self.my_cart.completeStop()

    def noAction(self):
        pass