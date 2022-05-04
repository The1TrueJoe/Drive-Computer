import enum
import threading
import logging
import time

from DriveComputer.src.drive_control.my_cart import MyCart

from DriveComputer.src.drive.auto.auto import Auto
from DriveComputer.src.drive.disabled.disabled import Disabled
from DriveComputer.src.drive.manual.manual import Manual
from DriveComputer.src.drive.teleop.teleop import Teleop

class Mode(enum.Enum):
        AUTO = 1
        MANUAL = 2
        TELEOP = 3
        DISABLED = 100

        names = {
            AUTO: "Auto",
            MANUAL: "Manual",
            TELEOP: "Teleop",
            DISABLED: "Disabled"

        }

class Drive:

        def __init__(self, cart = MyCart(), default_mode = Mode.DISABLED):
            # Setup the message logging
            self.logger = logging.getLogger("drive_controller")
            self.logger.info("Pre-Initializing Drive System")

            # Cart
            self.my_cart = cart
            
            # Kill
            self.kill = False

            # Mode
            self.mode = default_mode
            self.run_state = Disabled(cart=self.my_cart)
            self.run = threading.Thread(target=self.run_state.perodic, name="drive-init-thread", daemon=True)

            # Init Message
            self.logger.info("Pre-Initialization Complete")

        # Teleop
        def teleop(self):
            self.setMode(Mode.TELEOP)

        # Manual
        def manual(self):
            self.setMode(Mode.MANUAL)

        # Auto
        def auto(self):
            self.setMode(Mode.AUTO)

        # Disable
        def disable(self):
            self.setMode(Mode.DISABLED)
            
        # Initialize the drive system and hardware
        def initialize(self):
            # Init Message
            self.logger.info("Initializing Drive System")

            # Start
            self.my_cart.intialize()

            # Init Message
            self.logger.info("Initialization Complete")

            # Disabled Mode
            self.run_state.initialize()
            self.run.start()

        # Edit the drive mode vairable
        def setMode(self, mode: Mode):
            self.logger.info(f"Requesting Mode Switch from {Mode.names[self.run_state.mode]} to {Mode.names[self.run_state.mode]}")
            self.mode = mode

        # Kill the drive system
        def kill(self):
            self.logger.info("Request to Kill Drive System")
            self.kill = True

        # Run the drive system
        def run(self):
            self.logger.info("Drive System Starting")

            while not self.kill:
                if self.mode != self.run_state.mode:
                    self.logger.info("Preparing Drive Mode Switch")

                    # End current mode
                    if self.run.is_alive():
                        self.run_state.kill()
                        self.run.join()
                        self.run_state.exit()
                        
                    self.logger.info("Ready for Drive Mode Switch")
                    
                    # Auto Mode Switch
                    if self.mode == Mode.AUTO:
                        self.logger.info("Changing to Auto Drive")
                        self.run_state = Auto(cart=self.my_cart)
                        self.run = threading.Thread(target=self.run_state.perodic, name="auto-drive-thread", daemon=True)

                    # Teleop Mode Switch
                    elif self.mode == Mode.TELEOP:
                        self.logger.info("Changing to Teleoperated Drive")
                        self.run_state = Teleop(cart=self.my_cart)
                        self.run = threading.Thread(target=self.run_state.perodic, name="teleop-drive-thread", daemon=True)

                    # Manual Mode Switch
                    elif self.mode == Mode.MANUAL:
                        self.logger.info("Changing to Manual Drive")
                        self.run_state = Manual(cart=self.my_cart)
                        self.run = threading.Thread(target=self.run_state.perodic, name="manual-drive-thread", daemon=True)

                    # Disabled Mode Switch
                    elif self.mode == Mode.DISABLED:
                        self.logger.info("Disabling")
                        self.run_state = Disabled(cart=self.my_cart)
                        self.run = threading.Thread(target=self.run_state.perodic, name="disabled-thread", daemon=True)

                    # Invalid Mode
                    else:
                        self.logger.warning(f"Invalid Drive Mode Passed: {self.mode}")
                        self.logger.info("Disabling")
                        self.mode = Mode.DISABLED
                        self.run_state = Disabled(cart=self.my_cart)
                        self.run = threading.Thread(target=self.run_state.perodic, name="disabled-thread", daemon=True)

                    # Apply new mode
                    self.logger.info("Mode Switch Complete")
                    self.run.start()

                else:
                    time.sleep(2)

            # Shutdown
            self.mode = Mode.DISABLED
            self.run_state.exit()
            self.logger.info("Drive System Killed")

