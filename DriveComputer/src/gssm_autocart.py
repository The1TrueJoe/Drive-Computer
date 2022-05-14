import sys
import logging

from src.ControlLib.ControlLib.src.my_cart import MyCart

from src.modes.drive import Drive

import src.util as util

# Drive Computer Core Library
# Main
#
# This module controls the lights and horn.
#   - It also monitors the brake switch as that is normally considered 
#     a part of the accessory system (usually used to engage tail lights on braking)
#
# Hardware definition class to store messages for this module
#
# Part of the GSSM Autonomous Golf Cart
# Written by Joseph Telaak, class of 2022

drive: Drive = None

def main():
    # Setup the message logging
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Print to file
    file_handler = logging.FileHandler("logs/main.log")
    logging_format = logging.Formatter("%(asctime)s - %(name)s - %(threadName)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(logging_format)
    logger.addHandler(file_handler)

    # Print to console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging_format)
    logger.addHandler(console_handler)

    # Init
    logger.info("Initializing Cart System")

    # Function Setup
    drive = Drive(cart=MyCart(json_config_path="cart_sys_config.json"))
    drive.initialize()

    # Done
    logger.info("Initialization Complete")

    # Run
    drive.run()

    # Done
    logger.info("Shutdown")
