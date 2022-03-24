class Speed_Controller:

    def __int__(self, can_address = 4083):
        self.can_address = can_address

        # Setup the message logging
        logging.basicConfig(filename='speed_ctrl.log', filemode='w', format=' %(asctime)s - %(message)s')


    def setSpeedPotPos(self, pos):
        pass

    def incrementPotPos(self):
        pass

    def decrementPotPos(self):
        pass

    def reqSpeedPotPos(self):
        pass


    def setManualInput(self):
        pass

    def setComputerInput(self):
        pass

    def reqInputMode(self):
        pass


    def setReverse(self):
        pass

    def setForwards(self):
        pass

    def reqDirection(self):
        pass


    def enable(self):
        pass

    def disable(self):
        pass

    def isEnabled(self):
        pass

    
    def enableAutoBuzzer(self):
        pass

    def disableAutoBuzzer(self):
        pass

    def isAutoBuzzer(self):
        pass

    
