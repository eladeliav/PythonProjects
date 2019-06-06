import socket
from constants import *
from PIL import ImageGrab
import os
import shutil
import subprocess


connected = False
server_exit = False
server_socket = socket.socket()
SERVER_NAME = "Elad's Amazing Server"  # name of server

TOOLBAR_WIDTH = 40  # constant for progress bar width
CLIENT_DC_MSG = "Client Disconnected"
CLIENT_C_MSG = "Client Connected"
ILLEGAL_COMMAND_MSG = "ILLEGAL COMMAND"
FILE_SENT_MSG = "FILE_SENT"  # a message to let the client know it's done sending the file
ZERO_BYTES = 0
SCREENSHOT_PATH = "./screenshot.png"  # where to save screenshot
FILE_CHUNK_SIZE = 1024  # size of chunks to send/receive

# list to keep track of which commands need a socket as a param as well
COMMANDS_NEED_SOCK = {'SEND_FILE', 'DIR', 'HELP'}


def get_name():
    """
    Functions simply returns server name
    :return: server name
    """
    return SERVER_NAME


def print_commands(client_socket):
    """
    Help command to print out the list of commands
    :return: string version of the command list
    """
    send_response_to_client(PRINT_DIR_SEPARATORS, client_socket)
    command_keys = COMMANDS.keys()
    for name in command_keys:
        send_response_to_client(name, client_socket)
    return PRINT_DIR_SEPARATORS


def server_shutdown():
    """
    Shutsdown client and server
    :return: shutdown msg to send to client
    """
    global connected
    connected = False
    global server_exit
    server_exit = True
    print CLIENT_DC_MSG
    print 'SHUTTING DOWN CLIENT AND SERVER'
    return 'SHUTTING DOWN CLIENT AND SERVER'


def exit_client():
    """
    Sets the global connected variable to False which will eventually disconnect the client
    :return: a string of shutting down the client to send to the client
    """
    global connected
    connected = False
    print CLIENT_DC_MSG
    return 'SHUTTING DOWN CLIENT'


def take_screenshot():
    """
    Takes a screenshot and returns a phrase to the client that says a screenshot was take.
    :return: 'screenshot taken'
    """
    im = ImageGrab.grab()
    im.save(SCREENSHOT_PATH)
    return 'Screenshot taken. File name: ' + SCREENSHOT_PATH


def format_response(response):
    """
    Formats the given response so it sends the size of the response in the response
    :param response: response to format
    :return: formatted response
    """
    to_send = ""
    to_send += str(len(str(response))).zfill(SIZE_HEADER)
    to_send += str(response)
    return to_send


def send_file_info(filepath, client_socket):
    """
    Sends info about a given file to the given client (size of file, name and extension)
    :param filepath: file to send info on
    :param client_socket: client to send info to
    """
    total_file_size = os.path.getsize(filepath)
    send_response_to_client(PREPARE_FOR_FILE_MSG, client_socket)
    send_response_to_client(total_file_size, client_socket)


def send_file(filepath, client_socket):
    """
    Sends the given file to the client (if valid)
    :param filepath: file to send to client
    :param client_socket: client to send file to
    :return: finished sending file msg
    """
    if filepath is None:
        return "Wrong use of paramaters"
    filepath = filepath[FIRST_ELEMENT]
    if not valid_file(filepath):
        return "File doesn't exist"

    send_file_info(filepath, client_socket)

    with open(filepath, 'rb')as f:
        data = f.read(FILE_CHUNK_SIZE)
        while len(data) > ZERO_BYTES:
            send_response_to_client(data, client_socket)
            data = f.read(FILE_CHUNK_SIZE)
    return FILE_SENT_MSG


def list_folder(params, client_socket):
    """
    Sends a list of folders in the given folder path to the client
    :param params: filepath to list
    :param client_socket: client to send to
    :return: done sending info msg
    """
    if not params:
        return "Wrong use of parameters"
    params = str(params[0])
    if not valid_folder(params):
        return "Folder doesn't exist"
    send_response_to_client(PRINT_DIR_SEPARATORS, client_socket)
    files = os.listdir(params)
    for name in files:
        send_response_to_client(name, client_socket)
    return PRINT_DIR_SEPARATORS


def delete_file(filepath):
    """
    deletes a given file
    :param filepath: given file
    :return: File deleted confirmation msg
    """
    if not filepath:
        return "Wrong use of parameters"
    filepath = filepath[0]
    if not valid_file(filepath):
        return "File doesn't exist"
    os.remove(filepath)
    return "File deleted"


def copy_file(params):
    """
    copies a given file to a given path
    :param params: give
    :return: either file/folder doesn't exist msg, or file copies msg
    """
    if not params:
        return "Wrong use of parameters"
    filepath1 = params[FIRST_ELEMENT]
    filepath2 = params[SECOND_ELEMENT]
    if not valid_file(filepath1):
        to_send = ""
        to_send += filepath1
        to_send += " Doesn't exist"
        return to_send
    if not valid_file(filepath2):
        to_send = ""
        to_send += filepath2
        to_send += " Doesn't exist"
        return to_send
    shutil.copy(filepath1, filepath2)
    return "File Copied"


def open_exe(params):
    """
    Opens a given exe file
    :param params: path to exe
    :return: command ran confirmation msg
    """
    if not params:
        return "Wrong use of parameters"
    command = params[0]
    try:
        subprocess.check_call(command)
    except WindowsError as e:
        return str(e)
    return "Command Ran"


# Commands dictionary where the keys are command strings and
# the keys are pointers to functions
COMMANDS = {
    'NAME': get_name,
    'HELP': print_commands,
    'QUIT': server_shutdown,
    'EXIT': exit_client,
    'TAKE_SCREENSHOT': take_screenshot,
    'SEND_FILE': send_file,
    'DIR': list_folder,
    'DELETE': delete_file,
    'COPY': copy_file,
    'EXECUTE': open_exe
}


def valid_file(filepath):
    """
    Checks if file exists
    :param filepath: file to check
    :return: True of False depending on if file exists
    """
    return os.path.exists(filepath)


def valid_folder(folderpath):
    """
    Checks if folder exists
    :param folderpath: folder to check
    :return: True of False depending on if folder exists
    """
    if os.path.isdir(folderpath):
        return True
    return False


def init_socket(ip, port):
    """
    Inits server socket with AF_INET and SOCK_STREAM, binds it to the given ip and port,
    starts listening, and returns it.
    :param ip: desired ip to bind to server_socket
    :param port: desired port to bind to server_socket
    :return: the created server_socket
    """
    global server_socket
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((ip, port))
        server_socket.listen(1)
        return server_socket
    except socket.error as e:
        print "Couldn't initialize server_socket"
        print e
    return None


def shutdown_socket(sock):
    """
    Tries to shutdown a given socket
    :param sock: socket to shutdown
    """
    try:
        sock.close()
    except socket.error as e:
        print "Couldn't shutdown socket properly"
        print e


def listen_for_client():
    """
    Loop to keep accepting client, handle client and wait for his exit, and looping.
    """
    global connected
    global server_exit
    while not connected and not server_exit:  # while we don't need to exit
        try:
            client_socket, address = server_socket.accept()
            connected = True
            print CLIENT_C_MSG
        except socket.error as e:
            print "Couldn't accept client socket"
            print e
            return
        except KeyboardInterrupt:
            print "\nShutting Down"
            shutdown_socket(server_socket)
            shutdown_socket(client_socket)
            exit()
        handle_client(client_socket)
        shutdown_socket(client_socket)
        connected = False
    shutdown_socket(server_socket)
    shutdown_socket(client_socket)


def handle_client(client_socket):
    """
    Handles client by receiving his request, processing, and returning a response
    :param client_socket: client to handle
    """
    while connected and not server_exit:
        request, params = receive_client_request(client_socket)
        if not request and not params:
            print CLIENT_DC_MSG
            return
        valid = check_client_request(request, params)
        if valid:
            response = handle_client_request(request, params, client_socket)
            send_response_to_client(response, client_socket)
        else:
            send_response_to_client(ILLEGAL_COMMAND_MSG, client_socket)


def receive_client_request(client_socket):
    """
    Receives client request
    :param client_socket: client to receive request form
    """
    global connected
    try:
        data_size = client_socket.recv(SIZE_HEADER)
    except KeyboardInterrupt:
        print "\n SHUTTING DOWN"
        shutdown_socket(server_socket)
        shutdown_socket(client_socket)
        exit()
    except socket.error as e:
        print "Couldn't receive client data size"
        connected = False
        return None, None
    if data_size.isdigit():
        try:
            data = client_socket.recv(int(data_size))
        except socket.error as e:
            print "Couldn't receive client data"
            print e
            connected = False
            return None, None
    else:
        return None, None
    request_and_params = data.split()
    if len(request_and_params) > 1:
        return request_and_params[FIRST_ELEMENT], request_and_params[SECOND_ELEMENT:]
    else:
        return request_and_params[FIRST_ELEMENT], None


def check_client_request(request, params):
    """
    Makes sure client request is valid
    :param request: request to check
    :param params: params to check
    :return: True or False
    """
    global connected
    request = request.upper()
    if params is None:
        params = {}
    if request in COMMANDS_WITH_PARAMS and COMMANDS_WITH_PARAMS[request] == len(params):
        return True
    return False


def handle_client_request(request, params, client_socket):
    """
    Handles the client request by calling the corresponding function in the commands
    dictionary
    :param request: request to handle
    :param params: params to pass if needed
    :param client_socket: client to send to
    """
    request = request.upper()
    if COMMANDS_WITH_PARAMS[request] > 0:  # request has params?
        if request in COMMANDS_NEED_SOCK:  # does it need a socket as well?
            return COMMANDS[request](params, client_socket)  # run command[request] with both params and socket

        return COMMANDS[request](params)  # needs params but not socket

    if request in COMMANDS_NEED_SOCK:
        return COMMANDS[request](client_socket)  # needs just socket

    return COMMANDS[request]()  # doesn't need anything


def send_response_to_client(response, client_socket):
    """
    Properly send a response to client by formatting it with
    the response size and wrapped in a try.
    :param response: response to send
    :param client_socket:  socket to send to
    """
    global connected
    try:
        to_send = format_response(response)
        client_socket.send(to_send)
    except socket.error as e:
        print "Couldn't send response to client"
        connected = False
        print CLIENT_DC_MSG


def main():
    """
    Inits server_socket and calls listen_for_client()
    :return:
    """
    global server_socket
    server_socket = init_socket(IP, PORT)
    if server_socket is not None:
        listen_for_client()


if __name__ == '__main__':
    main()
