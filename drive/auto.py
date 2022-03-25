class Auto:

    def __init__(self, cart):
        self.kill = False
        self.my_cart = cart

    def initialize(self):
        self.my_cart.applyManual()

    def perodic(self):
        while not self.kill:
            pass

    def exit(self):
        self.my_cart.completeStop()