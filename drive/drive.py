import enum
import threading

from drive.auto import Auto
from drive.manual import Manual
from drive.teleop import Teleop

from drive_control.my_cart import MyCart

class Mode(enum.Enum):
        AUTO = 1
        MANUAL = 2
        TELEOP = 3

class Drive:

        def __init__(self, cart = MyCart()):
            self.my_cart = cart

            self.mode = Mode.MANUAL
            self.run_state = Auto(cart=self.my_cart)

            self.run = threading.Thread(target=self.initLoop, daemon=True)
            self.run.start()

        def initLoop(self):
            pass

        def changeMode(self):
            if self.run.is_alive():
                self.run_state = True
                self.run.join()
                self.run_state.exit()

        def auto(self):
            self.changeMode()

            self.mode = Mode.AUTO
            self.run_state = Auto(cart=self.my_cart)
            self.run = threading.Thread(target=self.run_state.perodic(), daemon=True)

            self.run_state.initialize()
            self.run.start()

        def teleop(self):
            self.changeMode()

            self.mode = Mode.TELEOP
            self.run_state = Teleop(cart=self.my_cart)
            self.run = threading.Thread(target=self.run_state.perodic(), daemon=True)

            self.run_state.initialize()
            self.run.start()

        def manual(self):
            self.changeMode()

            self.mode = Mode.MANUAL
            self.run_state = Manual(cart=self.my_cart)
            self.run = threading.Thread(target=self.run_state.perodic(), daemon=True)

            self.run_state.initialize()
            self.run.start()