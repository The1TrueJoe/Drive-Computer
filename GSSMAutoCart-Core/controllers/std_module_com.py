set = "0x0A "
op = "0x0B"
get = "0x0C"

def fill(count):
    filled = ""
    for i in range(count + 1):
        filled += "0x0C "

    return filled.substring(0, len(filled) - 1)