import os
import socket
from Constants import *

server_socket = socket.socket()
connected = False
server_exit = False
NAME = "Brandt's Amazing Server, I deserve to be in cyber"
CLIENT_CONNECTED = "Client Connected"
CLIENT_DISCONNECTED = "Client Disconnected"


def get_name():
    return NAME


def exit_client():
    global connected
    connected = False
    print CLIENT_DISCONNECTED
    return "Exiting..."


def quit_program():
    global connected
    global server_exit
    connected = False
    server_exit = True
    print CLIENT_DISCONNECTED
    return "Closing server and client"


COMMANDS = {
    "EXIT": exit_client,
    "QUIT": quit_program,
    "NAME": get_name,
}


def shutdown_socket(sock):
    try:
        sock.close()
    except socket.error as e:
        print e


def valid_file(filepath):
    """
    Checks if file exists
    :param filepath: file to check
    :return: True of False depending on if file exists
    """
    return os.path.exists(filepath)


def init_socket():
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen(1)


def listen_for_new_clients():
    global server_socket
    global connected
    global server_exit
    while not connected and not server_exit:
        client_socket, address = server_socket.accept()
        connected = True
        print CLIENT_CONNECTED
        handle_client(client_socket)
        shutdown_socket(client_socket)
        connected = False
    shutdown_socket(client_socket)
    shutdown_socket(server_socket)


def check_client_request(request, params):
    HAS_FILES = {"SEND_FILE"}
    if params is None:
        params = {}
    if request in COMMANDS_WITH_PARAMS and COMMANDS_WITH_PARAMS[request] == len(params):
        if request in HAS_FILES and params != {}:
            for file in params:
                if not valid_file(file):
                    return False
        return True
    return False


def handle_client_request(request, params, client_socket):
    NEEDS_SOCKET = {}
    if COMMANDS_WITH_PARAMS[request] == 0:
        if request in NEEDS_SOCKET:
            return COMMANDS[request](client_socket)
        return COMMANDS[request]()
    else:
        if request in NEEDS_SOCKET:
            return COMMANDS[request](params, client_socket)
        return COMMANDS[request](params)


def handle_client(client_socket):
    global connected
    global server_exit
    while connected and not server_exit:
        request, params = receive_from_client(client_socket)
        request = request.upper()
        valid = check_client_request(request, params)
        if valid:
            response = handle_client_request(request, params, client_socket)
            send_response_to_client(response, client_socket)
        else:
            send_response_to_client("Invalid Command", client_socket)


def format_response(msg):
    return str(len(msg)).zfill(SIZE_HEADER) + str(msg)


def send_response_to_client(response, client_socket):
    formatted = format_response(response)
    client_socket.send(formatted)


def receive_from_client(client_socket):
    size = client_socket.recv(SIZE_HEADER)
    if size.isdigit():
        data = client_socket.recv(int(size))
    else:
        return None, None

    request_and_params = data.split()
    if len(request_and_params) > 1:
        return request_and_params[0], request_and_params[1:]
    else:
        return request_and_params[0], None


def main():
    try:
        init_socket()
        listen_for_new_clients()
    except socket.error as e:
        print e


if __name__ == '__main__':
    main()
