IP = "127.0.0.1"
PORT = 27015
MSG_LEN = 1024
SIZE_HEADER = 4


# Dictionary to know how many parameters each command needs
COMMANDS_WITH_PARAMS = {'NAME': 0,
                        'EXIT': 0,
                        'HELP': 0,
                        'QUIT': 0,
                        'TAKE_SCREENSHOT': 0,
                        'SEND_FILE': 1,
                        'DIR': 1,
                        "DELETE": 1,
                        "COPY": 2,
                        'EXECUTE': 1
                        }
