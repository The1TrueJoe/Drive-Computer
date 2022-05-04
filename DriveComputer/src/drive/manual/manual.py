from DriveComputer.src.drive.drive import Mode
from DriveComputer.src.drive_control.my_cart import MyCart


class Manual:

    def __init__(self, cart: MyCart):
        self.kill = False
        self.mode = Mode.Auto
        self.my_cart = cart

    def initialize(self):
        self.my_cart.applyManual()

    def perodic(self):
        while not self.kill:
            if self.my_cart.vars["accel_pedal_sw"] == 1:
                self.my_cart.enableAccelerator()

                while self.my_cart.vars["accel_pedal_sw"] == 1:
                    wheel = self.my_cart.vars["steering_wheel"]

                    if wheel != 1:
                        if wheel == 2:
                            self.my_cart.turnLeft()
                        elif wheel == 3:
                            self.my_cart.turnRight()

                    self.my_cart.setSpeed(self.my_cart.vars["accel_pedal_pos"])

                self.my_cart.disableAccelerator()
                self.my_cart.setSpeed(0)

            else:
                wheel = self.my_cart.vars["steering_wheel"]

                if wheel != 1:
                    if wheel == 2:
                        self.my_cart.turnLeft()
                    elif wheel == 3:
                        self.my_cart.turnRight()

    def kill(self):
        self.kill = True

    def exit(self):
        self.my_cart.completeStop()