PORT = 1729  # port
IP = '127.0.0.1'  # ip

SIZE_HEADER = 4  # header size for every message the defines the size of the message
PREPARE_FOR_FILE_MSG = "SENDING_FILE"  # a message to let the client know  a file is coming
PRINT_DIR_SEPARATORS = "********"  # a separator for before and after the dir command and help command

FIRST_ELEMENT = 0  # first element index in lists
SECOND_ELEMENT = 1  # second element index in lists


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
