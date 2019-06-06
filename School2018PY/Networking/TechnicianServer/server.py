import random
import socket
from datetime import datetime
from sys import getsizeof
from constants import *

SERVER_NAME = 'Zupniks Server Sucks, This is best Ayelet Give 100'
connected = False
server_exit = False


def get_name():
    """

    :return: server_name
    """
    return SERVER_NAME


def get_time():
    """
    Gets current datetime
    :return: returns datetime to send to client
    """
    return str(datetime.now())


def exit_client():
    """
    Sets the global connected variable to False which will eventually disconnect the client
    :return: a string of shutting down the client to send to the client
    """
    global connected
    CONNECTED = False
    print 'Client Disconnected'
    return 'SHUTTING DOWN CLIENT'


def get_rand():
    """
    Generates a random number between 1 and 10
    :return: a string of a random number between 1 and 10
    """
    return str(random.randint(1, 10)).encode()


def print_commands():
    """
    Help command to print out the list of commands
    :return: string version of the command list
    """
    command_keys = COMMANDS.keys()
    return str(command_keys)


def server_shutdown():
    """
    Shutsdown client and server
    :return: shutdown msg to send to client
    """
    global connected
    CONNECTED = False
    global server_exit
    SERVER_EXIT = True
    print 'Client Disconnected'
    print 'SHUTTING DOWN CLIENT AND SERVER'
    return 'SHUTTING DOWN CLIENT AND SERVER'


# command dictionary with values pointing to the corresponding function
COMMANDS = {'NAME': get_name,
            'TIME': get_time,
            'EXIT': exit_client,
            'RAND': get_rand,
            'HELP': print_commands,
            'SERVER_SHUTDOWN': server_shutdown
            }


def init_socket(ip, port):
    """
    Inits server socket with AF_INET and SOCK_STREAM, binds it to the given ip and port,
    starts listening, and returns it.
    :param ip: desired ip to bind to server_socket
    :param port: desired port to bind to server_socket
    :return: the created server_socket
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(1)
    return server_socket


def handle_clients(server_socket):
    """
    while connected to client and the server exit flag is False:
    accept a new client and call handle_single_client for it.
    Continue until client disconnected or server exit flag is True.
    :param server_socket: the server socket
    """
    global connected
    while not CONNECTED and not server_exit:
        try:
            client_socket, address = server_socket.accept()
        except socket.error as e:
            print 'couldnt accept socket', e
        print 'Client Connected'
        CONNECTED = True
        handle_single_client(client_socket)
        try:
            client_socket.close()
        except socket.error as e:
            print 'couldnt close client socket properly', e
        CONNECTED = False
    try:
        server_socket.close()
    except socket.error as e:
        print 'couldnt shutdown server properly'
        print e


def handle_single_client(client_socket):
    """
    While client connected and server_exit flag is false:
    receive requests from the client, and if valid, do the corresponding command
    by calling handle_client_request
    :param client_socket: the client socket
    """
    while connected and not server_exit:
        request = receive_client_request(client_socket)
        valid = check_client_request(request)
        if valid:
            response = handle_client_request(request)
            send_response_to_client(response, client_socket)
        else:
            send_response_to_client('Illegal command', client_socket)


def receive_client_request(client_socket):
    """
    receives client data
    :param client_socket: the client socket
    :return: the received data
    """
    received_data = client_socket.recv(SIZE_HEADER)
    return received_data


def check_client_request(request):
    """
    checks if the given request is in command.keys()
    :param request: the request to check
    :return: True or false depending on whether or not the request is in commands.keys()
    """
    command_keys = COMMANDS.keys()
    if request.upper() in command_keys:
        return True
    return False


def handle_client_request(request):
    """
    runs the corresponding function commands[request]
    :param request: the request to run
    :return: whatever the corresponding function returns
    """
    request = request.upper()
    return COMMANDS[request]()


def send_response_to_client(response, client_socket):
    """
    sens the response to the client_socket
    :param response: what to send to client
    :param client_socket: the client socket to send the response in
    """
    size = getsizeof(response)
    to_send = str(size).zfill(4)
    to_send += response
    # print to_send
    client_socket.send(to_send)


def main():
    """
    inits server_socket and calls handle_clients.
    """
    try:
        server_socket = init_socket(IP, PORT)
        handle_clients(server_socket)
    except socket.error as msg:
        print 'socket error', msg
    except Exception as msg:
        print 'general error', msg


if __name__ == '__main__':
    main()
