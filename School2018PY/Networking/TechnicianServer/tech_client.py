import socket
from constants import *
import sys
import os

connected = False  # connected flag
RECEIVED_FILES_LOCATION = "./ReceivedFiles/"

# list of commands

def progress(count, total, status=''):
    """
    Prints out a progress bar
    :param count: current percentage
    :param total: total percentage
    :param status: message to print out
    """
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('\r[%s] %s%s ...%s' % (bar, percents, '%', status))
    sys.stdout.flush()


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


def read_from_server(sock):
    """
    Gets data from server socket
    :param sock: socket to read from
    :return: data if read, False it couldn't read
    """
    data_size = sock.recv(SIZE_HEADER)
    if data_size.isdigit():
        to_return = sock.recv(int(data_size))
    else:
        to_return = False
    return to_return


def receive_file(my_socket, params):
    """
    Loop to read chunk from server, save to file and repeat until done
    :param my_socket: socket to read file chunks from
    :param params: file we're receiving
    """
    total_file_size = read_from_server(my_socket)
    params = params[0]
    file_name = os.path.basename(params[:params.rfind('.')])
    file_extension = params[params.rfind('.'):]
    if total_file_size is False:
        print "Invalid data_size"
        return
    done = False
    params = params[0]
    with open(RECEIVED_FILES_LOCATION + file_name + "_copy" + file_extension, 'wb') as f:
        data = read_from_server(my_socket)
        if data is False:
            print "Invalid data_size"
            return
        while not done:
            f.write(data)
            downloaded_bytes = os.path.getsize(f.name)
            progress(downloaded_bytes, total_file_size, status="Downloading File")
            data = read_from_server(my_socket)
            if data is False:
                print "Invalid data_size"
                return
            if data == "FILE_SENT":
                done = True
                print '\n', data


def receive_multiple_strings(server_socket):
    """
    Receives multiple strings from the server until we get the 'done sending' msg
    :param server_socket: socket receiving from
    """
    done = False
    data = read_from_server(server_socket)
    if data is not False:
        while not done:
            print data
            data = read_from_server(server_socket)
            if data is not False:
                if data == PRINT_DIR_SEPARATORS:
                    done = True
                    print data
            else:
                print "Invalid data size"
    else:
        print "Invalid data size"


def handle_user_input(my_socket):
    """
    handles user input
    :param my_socket: client socket
    """
    while connected:
        print PRINT_DIR_SEPARATORS
        for key in COMMANDS_WITH_PARAMS:
            print key
        print PRINT_DIR_SEPARATORS
        request, params = receive_user_input(my_socket)
        if valid_request(request, params):
            send_request_to_server(my_socket, request, params)
            handle_server_response(my_socket, params)
        else:
            print 'Illegal command or wrong use of parameters'
    print 'exiting...'


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


def receive_user_input(sock):
    """
    Receiving user input, splitting request and params, and returning it
    :param sock: socket to close in case of keyboard interrupt
    :return:
    """
    global connected
    request_and_params = ""
    while request_and_params == "":
        try:
            request_and_params = raw_input("> ")
        except KeyboardInterrupt:
            print "\nExiting..."
            shutdown_socket(sock)
            exit()
    request_and_params = request_and_params.split()
    if len(request_and_params) > 1:
        request = request_and_params[FIRST_ELEMENT]
        params = request_and_params[SECOND_ELEMENT:]
    else:
        request = request_and_params[FIRST_ELEMENT]
        params = None
    return request, params


def valid_request(request, params):
    """
    checks if the given request is in commands
    :param params: parameters to check
    :param request: request to check
    :return: true if it is in commands and false if not
    """
    request = request.upper()
    if params is None:
        params = {}
    if request in COMMANDS_WITH_PARAMS and COMMANDS_WITH_PARAMS[request] == len(params):
        return True
    return False


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


def send_request_to_server(server_socket, request, params):
    """
    sends request to server
    :param server_socket: server socket
    :param request: request to send to server
    """
    request = request.upper()
    global connected
    try:
        size = sys.getsizeof(request) + sys.getsizeof(params)
        to_send = str(size).zfill(SIZE_HEADER)
        to_send += request
        if params is not None:
            for item in params:
                to_send += " " + item
        server_socket.send(to_send)
    except socket.error as e:
        print "Couldn't send request to server"
        print e
        return
    if request == 'EXIT' or request == 'QUIT':
        connected = False


def handle_server_response(server_socket, params):
    """
    receives data size of whatever the server sent us and, if it's valid,
    read whatever data size we received
    then print it out
    :param server_socket: the server socket
    """
    data = read_from_server(server_socket)
    if data is not False:
        if data == PREPARE_FOR_FILE_MSG:
            print data
            receive_file(server_socket, params)
            return
        if data == PRINT_DIR_SEPARATORS:
            print data
            receive_multiple_strings(server_socket)
            return
        print data
    else:
        print 'invalid data size'


def main():
    """
    inits client socket then callds handle_user_input.
    When we return from handle user input we close the socket.
    """
    try:
        client_socket = init_client_socket(IP, PORT)
        if client_socket is not None:
            handle_user_input(client_socket)
            shutdown_socket(client_socket)
    except socket.error as e:
        print "exiting..."
        shutdown_socket(client_socket)


if __name__ == '__main__':
    main()
