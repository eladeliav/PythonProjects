import struct
PORT = 1729
IP = "127.0.0.1"
FIRST_ELEMENT = 0  # first element index in lists
SECOND_ELEMENT = 1  # second element index in lists


#turns a num from heximal to decimal
def hexToDec(numHex):
    return struct.unpack("!Q", numHex)[0]


#turns a num from decimal to heximal
def decToHex(numDec):
    return struct.pack("!Q", numDec)

requests_list = ["TIME", "SHUTDOWN", "DELETE FILE", "DIR", "COPY"]