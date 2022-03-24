import cart_module as m
import module_util as util
import logging

# Drive Computer Core Library
# Accessory Controller Module
#
# Class to store messages for this module
#
# Part of the GSSM Autonomous Golf Cart
# Written by Joseph Telaak, class of 2022

class Accessory_Controller:

    # Constructor
    #
    # can_address: CAN Address of the module

    def __int__(self, can_address = "4082", right_signal = "1", left_signal = "2", head_light = "3", tail_light = "4", horn = "5", rear_buzzer = "6"):
        self.can_address = can_address
        self.right_signal = right_signal
        self.left_signal = left_signal
        self.head_light = head_light
        self.tail_light = tail_light
        self.horn = horn
        self.rear_buzzer = rear_buzzer

        # Setup the message logging
        logging.basicConfig(filename='accessory_ctrl.log', filemode='w', format=' %(asctime)s - %(message)s')

    # ----------------------------
    # Right Turn Signal
    # ----------------------------

    # Blink the Right Signal
    def rightSignalBlink(self, interval = "200", multiplier = "1"):
        logging.debug(f"Blink Right Signal {util.multiHexToDec(interval, multiplier)}ms")
        return f"{self.can_address} {m.op} {self.right_signal} {interval} {multiplier} {m.fill(4)}"

    # Turn on the Right Signal
    def rightSignalOn(self):
        logging.debug("Turn On Right Signal")
        return f"{self.can_address} {m.set} {self.right_signal} 1 {m.fill(5)}"

    # Turn off the Right Signal
    def rightSignalOff(self):
        logging.debug("Turn Off Right Signal")
        return f"{self.can_address} {m.set} {self.right_signal} 2 {m.fill(5)}"

    # Request the Right Signal Setting
    def getRightSignal(self):
        logging.debug("Get Right Signal Setting")
        return f"{self.can_address} {m.get} {self.right_signal} {m.fill(6)}"


    # ----------------------------
    # Right Turn Signal
    # ----------------------------

    # Blink the Left Signal
    def leftSignalBlink(self, interval = "200", multiplier = "1"):
        logging.debug(f"Blink Left Signal {util.multiHexToDec(interval, multiplier)}ms")
        return f"{self.can_address} {m.op} {self.left_signal} {interval} {multiplier} {m.fill(4)}"

    # Turn on the Left Signal
    def leftSignalOn(self):
        logging.debug("Turn On Left Signal")
        return f"{self.can_address} {m.set} {self.left_signal} 1 {m.fill(5)}"

    # Turn off the Left Signal
    def leftSignalOff(self):
        logging.debug("Turn Off Left Signal")
        return f"{self.can_address} {m.set} {self.left_signal} 2 {m.fill(5)}"

    # Request the Left Signal Status
    def getLeftSignal(self):
        logging.debug("Get Left Signal Setting")
        return f"{self.can_address} {m.get} {self.left_signal} {m.fill(6)}"


    # ----------------------------
    # Head Lights
    # ----------------------------

    # Blink Head Lights
    def headLightsBlink(self, interval = "200", multiplier = "1"):
        logging.debug(f"Blink Head Lights {util.multiHexToDec(interval, multiplier)}ms")
        return f"{self.can_address} {m.op} {self.head_light} {interval} {multiplier} {m.fill(4)}"

    # Turn on Head Lights
    def headLightsOn(self):
        logging.debug("Turn On Head Lights")
        return f"{self.can_address} {m.set} {self.head_light} 1 {m.fill(5)}"

    # Turn off Head Lights
    def headLightsOff(self):
        logging.debug("Turn Off Head Lights")
        return f"{self.can_address} {m.set} {self.head_light} 2 {m.fill(5)}"

    # Request the Head Lights Status
    def getHeadLights(self):
        logging.debug("Get Head Lights Setting")
        return f"{self.an_address} {m.get} {self.head_light} {m.fill(6)}"


    # ----------------------------
    # Head Lights
    # ----------------------------
    
    # Blink Tail Lights
    def tailLightsBlink(self, interval = "200", multiplier = "1"):
        logging.debug(f"Blink Tail Lights {util.multiHexToDec(interval, multiplier)}ms")
        return f"{self.can_address} {m.op} {self.tail_light} {interval} {multiplier} {m.fill(4)}"

    # Turn on Tail Lights
    def tailLightsOn(self):
        logging.debug("Turn On Tail Lights")
        return f"{self.an_address} {m.set} {self.tail_light} 1 {m.fill(5)}"

    # Turn off Tail Lights
    def tailLightsOff(self):
        logging.debug("Turn Off Tail Lights")
        return f"{self.can_address} {m.set} {self.tail_light} 2 {m.fill(5)}"

    # Request the Tail Lights Status
    def getTailLights(self):
        logging.debug("Get Tail Lights Setting")
        return f"{self.can_address} {m.get} {self.tail_light} {m.fill(6)}"


    # ----------------------------
    # Horn
    # ----------------------------

    # Honk the Horn
    def honk(self, interval = "50", multiplier = "1"):
        logging.debug(f"Honk Horn {util.multiHexToDec(interval, multiplier)}ms")
        return f"{self.can_address} {m.op} {self.horn} {interval} {multiplier} {m.fill(4)}"

    # Turn on the horn
    def hornOn(self):
        return f"{self.can_address} {m.set} {self.horn} 1 {m.fill(5)}"

    # Turn off the horn
    def hornOff(self):
        return f"{self.can_address} {m.set} {self.horn} 2 {m.fill(5)}"

    # Request the horn status
    def getHorn(self):
        return f"{self.can_address} {m.get} {self.horn} {m.fill(6)}"


    # ----------------------------
    # Rear Buzzer
    # ----------------------------

    # Turn on the Rear Buzzer
    def rearBuzzOn(self):
        return f"{self.can_address} {m.set} {self.rear_buzzer} 1 {m.fill(5)}"

    # Turn off the Rear Buzzer
    def rearBuzzOff(self):
        return f"{self.can_address} {m.set} {self.rear_buzzer} 2 {m.fill(5)}"

    # Request the Rear Buzzer status
    def getRearBuzz(self):
        return f"{self.can_address} {m.get} {self.rear_buzzer} {m.fill(6)}"

