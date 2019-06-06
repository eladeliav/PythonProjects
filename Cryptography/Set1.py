import sys

ORIGINAL = ''
OUTPUT = ''

HEX_DIC = {
    'a': 10,
    'b': 11,
    'c': 12,
    'd': 13,
    'e': 14,
    'f': 15,
}
HEX_DICT = {value: key for key, value in HEX_DIC.items()}


def to_binary(string, base):
    test = int(string, base)
    bin_num = ""
    while test > 0:
        bin_num = str(test % 2) + bin_num
        test = int(test / 2)
    return bin_num


def bin_to_hex(string):
    dec = int(string, 2)
    hex_num = ""
    while dec > 0:
        hex_num = str(dec % 16) + hex_num if dec % 16 not in HEX_DICT else HEX_DICT[dec % 16] + hex_num
        dec = int(dec / 16)
    print(hex_num)
    return hex_num


def main(args):
    global ORIGINAL
    ORIGINAL = args
    thing = to_binary("a1", 16)
    bin_to_hex(thing)


if __name__ == '__main__':
    main(sys.argv[1])
