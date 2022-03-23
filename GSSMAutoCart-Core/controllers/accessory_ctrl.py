import std_module_com as m
import drivecomp_util as util
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

    def __int__(self, can_address, right_signal = "0x01", left_signal = "0x02", head_light = "0x03", tail_light = "0x04", horn = "0x05", rear_buzzer = "0x06"):
        # Setup the message logging
        logging.basicConfig(filename='accessory_ctrl.log', filemode='w', format=' %(asctime)s - %(message)s')

    def rightSignalBlink(self, interval = "0xC8", multiplier = "0x01"):
        logging.debug(f"Blink Right Signal {util.multiHexToDec(interval, multiplier)}ms")
        return f"{can_address} {m.op} {right_signal} {interval} {multiplier} {m.fill(4)}"

    def rightSignalOn(self):
        logging.debug("Turn On Right Signal")
        return f"{can_address} {m.set} {right_signal} 0x01 {m.fill(5)}"

    def rightSignalOff(self):
        logging.debug("Turn Off Right Signal")
        return f"{can_address} {m.set} {right_signal} 0x02 {m.fill(5)}"

    def getRightSignal(self):
        logging.debug("Get Right Signal Setting")
        return f"{can_address} {m.get} {right_signal} {m.fill(6)}"


    def leftSignalBlink(self, interval = "0xC8", multiplier = "0x01"):
        logging.debug(f"Blink Left Signal {util.multiHexToDec(interval, multiplier)}ms")
        return f"{can_address} {m.op} {left_signal} {interval} {multiplier} {m.fill(4)}"

    def leftSignalOn(self):
        logging.debug("Turn On Left Signal")
        return f"{can_address} {m.set} {left_signal} 0x01 {m.fill(5)}"

    def leftSignalOff(self):
        logging.debug("Turn Off Left Signal")
        return f"{can_address} {m.set} {left_signal} 0x02 {m.fill(5)}"

    def getLeftSignal(self):
        logging.debug("Get Left Signal Setting")
        return f"{can_address} {m.get} {left_signal} {m.fill(6)}"


    def headLightsBlink(self, interval = "0xC8", multiplier = "0x01"):
        logging.debug(f"Blink Head Lights {util.multiHexToDec(interval, multiplier)}ms")
        return f"{can_address} {m.op} {head_light} {interval} {multiplier} {m.fill(4)}"

    def headLightsOn(self):
        logging.debug("Turn On Head Lights")
        return f"{can_address} {m.set} {head_light} 0x01 {m.fill(5)}"

    def headLightsOff(self):
        logging.debug("Turn Off Head Lights")
        return f"{can_address} {m.set} {head_light} 0x02 {m.fill(5)}"

    def getHeadLights(self):
        logging.debug("Get Head Lights Setting")
        return f"{can_address} {m.get} {head_light} {m.fill(6)}"


    def tailLightsBlink(self, interval = "0xC8", multiplier = "0x01"):
        logging.debug(f"Blink Tail Lights {util.multiHexToDec(interval, multiplier)}ms")
        return f"{can_address} {m.op} {tail_light} {interval} {multiplier} {m.fill(4)}"

    def tailLightsOn(self):
        logging.debug("Turn On Tail Lights")
        return f"{can_address} {m.set} {tail_light} 0x01 {m.fill(5)}"

    def tailLightsOff(self):
        logging.debug("Turn Off Tail Lights")
        return f"{can_address} {m.set} {tail_light} 0x02 {m.fill(5)}"

    def getTailLights(self):
        logging.debug("Get Tail Lights Setting")
        return f"{can_address} {m.get} {tail_light} {m.fill(6)}"


    def honk(self, interval = "0x32", multiplier = "0x01"):
        logging.debug(f"Honk Horn {util.multiHexToDec(interval, multiplier)}ms")
        return f"{can_address} {m.op} {horn} {interval} {multiplier} {m.fill(4)}"

    def hornOn(self):
        return f"{can_address} {m.set} {horn} 0x01 {m.fill(5)}"

    def hornOff(self):
        return f"{can_address} {m.set} {horn} 0x02 {m.fill(5)}"

    def getHorn(self):
        return f"{can_address} {m.get} {horn} {m.fill(6)}"


    def rearBuzzOn(self):
        return f"{can_address} {m.set} {rear_buzzer} 0x01 {m.fill(5)}"

    def rearBuzzOff(self):
        return f"{can_address} {m.set} {rear_buzzer} 0x02 {m.fill(5)}"

    def getRearBuzz(self):
        return f"{can_address} {m.get} {rear_buzzer} {m.fill(6)}"

