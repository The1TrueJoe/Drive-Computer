from drive.drive import Mode


class Manual:

    def __init__(self, cart):
        self.kill = False
        self.mode = Mode.Auto
        self.my_cart = cart

    def initialize(self):
        self.my_cart.applyManual()

    def perodic(self):
        while not self.kill:
            pass

    def kill(self):
        self.kill = True

    def exit(self):
        self.my_cart.completeStop()