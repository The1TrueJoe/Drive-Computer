from drive.drive import Mode

import time


class Disabled:

    def __init__(self, cart):
        self.kill = False
        self.mode = Mode.Auto
        self.my_cart = cart

        self.wait_count = 0

    def initialize(self):
        self.logger.info("Disabled: Waiting for Drive Mode")

    def perodic(self):
        while not self.kill:
            if self.wait_count % 60 == 0:
                self.logger.info(f"Disabled ({self.wait_count/60}min): Waiting for Drive Mode")

            time.sleep(1)
            self.wait_count += 1
                

    def kill(self):
        self.kill = True

    def exit(self):
        self.my_cart.completeStop()