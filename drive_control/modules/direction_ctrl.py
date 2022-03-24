class Direction_Controller:

    def __int__(self, can_address = 4081):
        self.can_address = can_address

        # Setup the message logging
        logging.basicConfig(filename='direction_ctrl.log', filemode='w', format=' %(asctime)s - %(message)s')


    def disableSteeringMotor(self):
        pass

    def enableSteeringMotor(self):
        pass

    def reqSteeringMotorStatus(self):
        pass

    def runWheelLeft(self, power = 255):
        pass

    def runWheelRight(self, power = 255):
        pass

    def setWheelPos(self, pos):
        pass

    def reqWheelPos(self):
        pass

    def reqSteeringPos(self):
        pass

    def setWheelInputSteering(self):
        pass

    def setWheelInputSpeed(self, power = 128):
        pass

    def setControlledSteering(self):
        pass

    def reqSteeringMode(self):
        pass


    def disableBrakeMotor(self):
        pass

    def enableBrakeMotor(self):
        pass

    def reqBrakeMotorStatus(self):
        pass

    def runBrakeMotorForwards(self, power = 255):
        pass

    def runBrakeMotorReverse(self, power = 255):
        pass

    def resetBrakeMotorEncoder(self):
        pass

    def reqBrakeMotorTicks(self):
        pass