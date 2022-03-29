# Drive Computer Core Library
#
# Utility methods to help with CAN Messages
#
# Part of the GSSM Autonomous Golf Cart
# Written by Joseph Telaak, class of 2022

# Turns a hex code into decimal
def hexToDec(hex):
    c = count = i = 0
    len = len(hex) - 1

    while len >= 0:
        if hex[len] >= '0' and hex[len] <= '9':
            rem = int(hex[len])

        elif hex[len] >= 'A' and hex[len] <= 'F':
            rem = ord(hex[len]) - 55

        elif hex[len] >= 'a' and hex[len] <= 'f':
            rem = ord(hex[len]) - 87

        else:
            c = 1
            break
        
        count = count + (rem * (16 ** i))
        len = len - 1
        i = i + 1

    return count

# Convert a 16bit integer to 2 8bit integers
def sixteentoeight(message):
    num = int(message)

    coarse = (num >> 8) & 0xff
    fine = num & 0xff

    return {coarse, fine}

# Remove the ID
def removeID(message):
    return message[message.find(")")+2:len(message)]

# Get the ID from the message
def getID(message):
    return message[message.find("(")+1:message.find(")")]