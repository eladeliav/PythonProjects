import socket
from Constants import *

connected = False


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


def init_client_socket(ip, port):
    """
    Inits client socket
    :param ip: ip to bind to client_socket
    :param port: port to bind to client_socket
    :return: the generated client_socket
    """
    global connected
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip, port))
        connected = True
        return client_socket
    except socket.error as e:
        print "Couldn't init client socket / couldn't connect to server"
        print e
        return None


def receive_user_input(sock):
    """
    Receiving user input, splitting request and params, and returning it
    :param sock: socket to close in case of keyboard interrupt
    :return:
    """
    global connected
    request_and_params = ""
    while request_and_params == "":
        request_and_params = raw_input("> ")

    request_and_params = request_and_params.split()
    if len(request_and_params) > 1:
        request = request_and_params[0]
        params = request_and_params[1:]
    else:
        request = request_and_params[0]
        params = None
    return request, params


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


def handle_user_input(my_socket):
    """
    handles user input
    :param my_socket: client socket
    """
    while connected:
        request, params = receive_user_input(my_socket)
        request = request.upper()
        if check_client_request(request, params):
            send_request_to_server(request, params, my_socket)
            handle_server_response(my_socket, params)
        else:
            print 'Illegal command or wrong use of parameters'


def receive_from_server(server_socket):
    size = server_socket.recv(SIZE_HEADER)
    if size.isdigit():
        data = server_socket.recv(int(size))
        return data
    return None


def handle_server_response(server_socket, params):
    """
    receives data size of whatever the server sent us and, if it's valid,
    read whatever data size we received
    then print it out
    :param server_socket: the server socket
    """
    data = receive_from_server(server_socket)
    if data is not None:
        print data
    else:
        print 'invalid data size'


def format_response(msg):
    return str(len(msg)).zfill(SIZE_HEADER) + str(msg)


def send_request_to_server(response, params, client_socket):
    global connected
    if params is not None and not {}:
        params = ' '.join(params)
        response += ' ' + params
    formatted = format_response(response)
    client_socket.send(formatted)
    if 'EXIT' in response or 'QUIT' in response:
        connected = False


def main():
    try:
        client_socket = init_client_socket(IP, PORT)
        if client_socket is not None:
            handle_user_input(client_socket)
            shutdown_socket(client_socket)
    except socket.error as e:
        print e


if __name__ == '__main__':
    main()
