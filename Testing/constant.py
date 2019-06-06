PORT = 1788
IP = "127.0.0.1"
MSG_LEN = 1024
SCREENSHOT_FILE = "screenshots.png"
DCT_FUNC = { "TAKE_SCREENSHOT" : 0,
             "SEND_FILE" : 1,
             "DIR" : 1,
             "DELETE" : 1,
             "COPY" : 2,
             "EXECUTE" : 1,
             "EXIT" : 0,
             "QUIT" : 0
             }
LST_FILES_FUNCTION = ["SEND_FILE", "DELETE"]
LST_FOLDER_FUNCTION = ["DIR"]
PREPARE_FILE = "SEND_FILE"
FILE_SENT = "FILE_SENT"