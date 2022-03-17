class Computer_LCD:

    # Constructor

    def __int__(self):
        self.message_header = "Display: "

    # Clear the LCD Screen

    def clear(self):
        return self.message_header + "Clear"

    # Turn off the LCD screen

    def off(self):
        return self.message_header + "Off"

    # Turn on the LCD screen

    def on(self):
        return self.message_header + "On"

    # Send a message to the LCD screen
    #
    # message: Message to display
    # line_num: Line number to display on (1-2)

    def display(self, message, line_num):
        if line_num >= 3:
            line_num = 2
        elif line_num <= 0:
            line_num = 1

        return self.message_header + f"L{line_num}: " + message
