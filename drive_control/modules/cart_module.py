# Drive Computer Core Library
# Module Utilites
#
# Utilites in building the hex codes for the can messages
#
# Part of the GSSM Autonomous Golf Cart
# Written by Joseph Telaak, class of 2022

# Set operation
set = "10"

# Operation
op = "11"

# Get request
get = "12"

# Fill the rest of the message with zeroes
def fill(count):
    filled = ""
    
    for i in range(count + 1):
        filled += "C "

    return filled.substring(0, len(filled) - 1)