# Drive Computer Core Library
# Drive Computer LCD
#
# Drive Computer LCD
#
# Part of the GSSM Autonomous Golf Cart
# Written by Joseph Telaak, class of 2022

# Clear the LCD Screen
def clear():
    return "Display: Clear"

# Turn off the LCD screen
def off():
    return "Display: Off"

# Turn on the LCD screen
def on():
    return "Display: On"

# Send a message to the LCD screen
#
# message: Message to display
# line_num: Line number to display on (1-2)

def display(message, line_num):
    if line_num >= 3:
        line_num = 2
    elif line_num <= 0:
        line_num = 1

    return f"Display: L{line_num}: {message}"