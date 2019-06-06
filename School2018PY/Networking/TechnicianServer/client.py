import socket
from constants import *

connected = False  # connected flag
# list of commands
COMMANDS = {'NAME',
            'TIME',
            'EXIT',
            'RAND',
            'HELP',
            'SERVER_SHUTDOWN'
            }


def init_client_socket(ip, port):
    """
    Inits client socket
    :param ip: ip to bind to client_socket
    :param port: port to bind to client_socket
    :return: the generated client_socket
    """
    global connected
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))
    CONNECTED = True
    return client_socket


def handle_user_input(my_socket):
    """
    handles user input
    :param my_socket: client socket
    """
    request = "temp"
    while connected:
        request = raw_input("please enter operation:\n")
        request = request.upper()
        if valid_request(request):
            send_request_to_server(my_socket, request)
            handle_server_response(my_socket)
        else:
            print 'Illegal command: ', request
    print 'exiting...'


def valid_request(request):
    """
    checks if the given request is in commands
    :param request: request to check
    :return: true if it is in commands and false if not
    """
    if request.upper() in COMMANDS:
        return True
    return False


def send_request_to_server(server_socket, request):
    """
    sends request to server
    :param server_socket: server socket
    :param request: request to send to server
    """
    global connected
    server_socket.send(request)
    if request == 'EXIT' or request == 'SERVER_SHUTDOWN':
        CONNECTED = False


def handle_server_response(server_socket):
    """
    receives data size of whatever the server sent us and, if it's valid,
    read whatever data size we received
    then print it out
    :param server_socket: the server socket
    """
    data_size = server_socket.recv(4)
    data = str()
    if data_size.isdigit():
        data = server_socket.recv(int(data_size))
    else:
        print 'invalid data size'
    print data


def main():
    """
    inits client socket then callds handle_user_input.
    When we return from handle user input we close the socket.
    """
    try:
        my_socket = init_client_socket(IP, PORT)
        handle_user_input(my_socket)
        my_socket.close()
    except socket.error as msg:
        print 'Socket Error: ', msg
    except Exception as msg:
        print 'General Error: ', msg


if __name__ == '__main__':
    main()
