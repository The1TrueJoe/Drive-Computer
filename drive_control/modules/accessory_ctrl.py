import cart_module as m
import logging

# Drive Computer Core Library
# Accessory Controller Module
#
# This module controls the lights and horn.
#   - It also monitors the brake switch as that is normally considered 
#     a part of the accessory system (usually used to engage tail lights on braking)
#
# Hardware definition class to store messages for this module
#
# Part of the GSSM Autonomous Golf Cart
# Written by Joseph Telaak, class of 2022

class Accessory_Controller:

    # Constructor
    #
    # can_address: CAN Address of the module

    def __int__(self, can_address = "4082", right_signal = "1", left_signal = "2", head_light = "3", tail_light = "4", horn = "5", rear_buzzer = "6"):
        # CAN Address
        self.can_address = can_address
        
        # Components
        self.right_signal = self.Right_Signal(can_address=self.can_address, id=right_signal)
        self.left_signal = self.Left_Signal(can_address=self.can_address, id=left_signal)
        self.head_light = self.Head_Lights(can_address=self.can_address, id=head_light)
        self.tail_light = self.Tail_Lights(can_address=self.can_address, id=tail_light)
        self.horn = self.Horn(can_address=self.can_address, id=horn)
        self.rear_buzzer = self.Rear_Buzzer(can_address=self.can_address, id=rear_buzzer)

        # Setup the message logging
        logging.basicConfig(filename='accessory_ctrl.log', filemode='w', format=' %(asctime)s - %(message)s')

    # ----------------------------
    # Right Turn Signal
    # ----------------------------

    class Right_Signal:

        # Constructor
        def __init__(self, can_address, id):
            # CAN Address
            self.can_address = can_address

            # ID
            self.right_signal = id

        # Blink the Right Signal
        def blink(self, interval = "200", multiplier = "1"):
            logging.debug(f"Blink Right Signal {util.multiHexToDec(interval, multiplier)}ms")
            return f"({self.can_address}) {m.op} {self.right_signal} {interval} {multiplier} {m.fill(4)}"

        # Turn on the Right Signal
        def on(self):
            logging.debug("Turn On Right Signal")
            return f"({self.can_address}) {m.set} {self.right_signal} 1 {m.fill(5)}"

        # Turn off the Right Signal
        def off(self):
            logging.debug("Turn Off Right Signal")
            return f"({self.can_address}) {m.set} {self.right_signal} 2 {m.fill(5)}"

        # Request the Right Signal Setting
        def get(self):
            logging.debug("Get Right Signal Setting")
            return f"({self.can_address}) {m.get} {self.right_signal} {m.fill(6)}"

        # Check if the message matches the response
        def checkResponse(self, message):
            return m.isResponseMessage(incoming_message=message, expected_message=f"12 12 10 {self.right_signal}")

        # Read the Request Response Message
        def readGet(self, message):
            return m.getAsBoolean(message_byte=message[4])


    # ----------------------------
    # Left Turn Signal
    # ----------------------------
    
    class Left_Signal:

        # Constructor
        def __init__(self, can_address, id):
            # CAN Address
            self.can_address = can_address

            # ID
            self.left_signal = id

        # Blink the Left Signal
        def blink(self, interval = "200", multiplier = "1"):
            logging.debug(f"Blink Left Signal {util.multiHexToDec(interval, multiplier)}ms")
            return f"({self.can_address}) {m.op} {self.left_signal} {interval} {multiplier} {m.fill(4)}"

        # Turn on the Left Signal
        def on(self):
            logging.debug("Turn On Left Signal")
            return f"({self.can_address}) {m.set} {self.left_signal} 1 {m.fill(5)}"

        # Turn off the Left Signal
        def off(self):
            logging.debug("Turn Off Left Signal")
            return f"({self.can_address}) {m.set} {self.left_signal} 2 {m.fill(5)}"

        # Request the Left Signal Setting
        def get(self):
            logging.debug("Get Left Signal Setting")
            return f"({self.can_address}) {m.get} {self.left_signal} {m.fill(6)}"

        # Check if the message matches the response
        def checkResponse(self, message):
            return m.isResponseMessage(incoming_message=message, expected_message=f"12 12 10 {self.left_signal}")

        # Read the Request Response Message
        def readGet(self, message):
            return m.getAsBoolean(message_byte=message[4])


    # ----------------------------
    # Head Lights
    # ----------------------------
    
    class Head_Lights:

        # Constructor
        def __init__(self, can_address, id):
            # CAN Address
            self.can_address = can_address

            # ID
            self.head_lights = id

        # Blink the Head Lights
        def blink(self, interval = "200", multiplier = "1"):
            logging.debug(f"Blink Head Lights {util.multiHexToDec(interval, multiplier)}ms")
            return f"({self.can_address}) {m.op} {self.head_lights} {interval} {multiplier} {m.fill(4)}"

        # Turn on the Head Lights
        def on(self):
            logging.debug("Turn On Head Lights")
            return f"({self.can_address}) {m.set} {self.head_lights} 1 {m.fill(5)}"

        # Turn off the Head Lights
        def off(self):
            logging.debug("Turn Off Head Lights")
            return f"({self.can_address}) {m.set} {self.head_lights} 2 {m.fill(5)}"

        # Request the Head Light Setting
        def get(self):
            logging.debug("Get Head Light Setting")
            return f"({self.can_address}) {m.get} {self.head_lights} {m.fill(6)}"

        # Check if the message matches the response
        def checkResponse(self, message):
            return m.isResponseMessage(incoming_message=message, expected_message=f"12 12 10 {self.head_lights}")

        # Read the Request Response Message
        def readGet(self, message):
            return m.getAsBoolean(message_byte=message[4])


    # ----------------------------
    # Tail Lights
    # ----------------------------
    
    class Tail_Lights:

        # Constructor
        def __init__(self, can_address, id):
            # CAN Address
            self.can_address = can_address

            # ID
            self.tail_lights = id

        # Blink the Tail Lights
        def blink(self, interval = "200", multiplier = "1"):
            logging.debug(f"Blink Tail Lights {util.multiHexToDec(interval, multiplier)}ms")
            return f"({self.can_address}) {m.op} {self.tail_lights} {interval} {multiplier} {m.fill(4)}"

        # Turn on the Tail Lights
        def on(self):
            logging.debug("Turn On Tail Lights")
            return f"({self.can_address}) {m.set} {self.tail_lights} 1 {m.fill(5)}"

        # Turn off the Tail Lights
        def off(self):
            logging.debug("Turn Off Tail Lights")
            return f"({self.can_address}) {m.set} {self.tail_lights} 2 {m.fill(5)}"

        # Request the Tail Light Setting
        def get(self):
            logging.debug("Get Tail Light Setting")
            return f"({self.can_address}) {m.get} {self.tail_lights} {m.fill(6)}"

        # Check if the message matches the response
        def checkResponse(self, message):
            return m.isResponseMessage(incoming_message=message, expected_message=f"12 12 10 {self.tail_lights}")

        # Read the Request Response Message
        def readGet(self, message):
            return m.getAsBoolean(message_byte=message[4])


    # ----------------------------
    # Horn
    # ----------------------------

    class Horn:

        # Constructor
        def __init__(self, can_address, id):
            # CAN Address
            self.can_address = can_address

            # ID
            self.horn = id


        # Honk the Horn
        def honk(self, interval = "50", multiplier = "1"):
            logging.debug(f"Honk Horn {util.multiHexToDec(interval, multiplier)}ms")
            return f"({self.can_address}) {m.op} {self.horn} {interval} {multiplier} {m.fill(4)}"

        # Turn on the horn
        def on(self):
            logging.debug("Turn on Horn")
            return f"({self.can_address}) {m.set} {self.horn} 1 {m.fill(5)}"

        # Turn off the horn
        def off(self):
            logging.debug("Turn Off Horn")
            return f"({self.can_address}) {m.set} {self.horn} 2 {m.fill(5)}"

        # Request the horn status
        def get(self):
            logging.debug("Get Horn Status")
            return f"({self.can_address}) {m.get} {self.horn} {m.fill(6)}"

        # Check if the message matches the response
        def checkResponse(self, message):
            return m.isResponseMessage(incoming_message=message, expected_message=f"12 12 10 {self.horn}")

        # Read the Request Response Message
        def readGet(self, message):
            return m.getAsBoolean(message_byte=message[4])


    # ----------------------------
    # Rear Buzzer
    # ----------------------------

    class Rear_Buzzer:

        # Constructor
        def __init__(self, can_address, id):
            # CAN Address
            self.can_address = can_address

            # ID
            self.rear_buzzer = id

        # Turn on the Rear Buzzer
        def on(self):
            logging.debug("Turning on Rear Buzzer")
            return f"({self.can_address}) {m.set} {self.rear_buzzer} 1 {m.fill(5)}"

        # Turn off the Rear Buzzer
        def off(self):
            logging.debug("Turning Off Rear Buzzer")
            return f"({self.can_address}) {m.set} {self.rear_buzzer} 2 {m.fill(5)}"

        # Request the Rear Buzzer status
        def get(self):
            logging.debug("Get Rear Buzzer Status")
            return f"({self.can_address}) {m.get} {self.rear_buzzer} {m.fill(6)}"

        # Check if the message matches the response
        def checkResponse(self, message):
            return m.isResponseMessage(incoming_message=message, expected_message=f"12 12 10 {self.rear_buzzer}")

        # Read the Request Response Message
        def readGet(self, message):
            return m.getAsBoolean(message_byte=message[4])

