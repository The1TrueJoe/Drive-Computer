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

def multiHexToDec(hex_1, hex_2):
    return hexToDec(hex_1) * hexToDec(hex_2);