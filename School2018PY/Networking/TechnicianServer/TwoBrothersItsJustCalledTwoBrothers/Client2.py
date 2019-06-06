import socket
from Constants import *
import os.path


def print_functions():
    print "TAKE_SCREENSHOT"
    print "SEND_FILE"
    print "DIR"
    print "DELETE"
    print "COPY"
    print "EXECUTE"
    print "EXIT"


def read_from_server(sock):
    data_size = sock.recv(MSG_HEADER)
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
    with open(file_name + "_copy" + file_extension, "wb") as f:
        data = read_from_server(my_socket)
        if data is False:
            print "Invalid data_size"
            return
        while not done:
            f.write(data)
            downloaded_bytes = os.path.getsize(f.name)
            data = read_from_server(my_socket)
            if data is False:
                print "Invalid data_size"
                return
            if data == "FILE_SENT":
                done = True
                print '\n', data


def initiate_client_socket(ip, port):
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((ip, port))
    return my_socket


def valid_request(request):
    """
    checks if the request is in the command list
    """
    params_dict = {"TAKE_SCREENSHOT": 0, "SEND_FILE": 1, "DIR": 1, "DELETE": 1, "COPY": 2, "EXECUTE": 1, "QUIT": 0}
    # split to request and parameters
    command = ""
    params = ""
    req_and_prms = request.split()
    if len(req_and_prms) > 1:
        command = req_and_prms[0]
        params = req_and_prms[1:]
    else:
        command = req_and_prms[0]
        params = []

    return command.upper() in COMMAND_LIST and len(params) == params_dict[command.upper()]


def send_request_to_server(my_socket, request, params):
    """
    send the command request to the server
    """
    request = str(request)
    size = str(len(request) + len(str(params)))
    to_send = str(size).zfill(MSG_HEADER)
    to_send += request
    if params is not None:
        for item in params:
            to_send += " " + item
    my_socket.send(to_send)


def handle_server_response(my_socket, params):
    """
    receives the returned data from the server commands
    """
    data = read_from_server(my_socket)
    if data is not False:
        if data == PREPARE_FOR_FILE_MSG:
            print data
            receive_file(my_socket, params)
            return
        print data
    else:
        print 'invalid data size'


def split_req_and_params(request_and_params):
    request_and_params = request_and_params.split()
    if len(request_and_params) > 1:
        request = request_and_params[0]
        params = request_and_params[1:]
    else:
        request = request_and_params[0]
        params = None
    return request.upper(), params


def handle_user_input(my_socket):
    request = ""
    while request.upper() != 'QUIT':  # continues if the request is not quit
        request_and_params = raw_input("please enter operation:\n")  # asks the user for a command
        request, params = split_req_and_params(request_and_params)
        if valid_request(request_and_params):  # checks if the command is included in the command list
            send_request_to_server(my_socket, request, params)  # send the command request to the server
            handle_server_response(my_socket, params)  # receives the answer and prints it


def main():
    try:
        my_socket = initiate_client_socket(IP, PORT)
        handle_user_input(my_socket)
        my_socket.close()
    except socket.error as msg:
        print MESSAGE, msg
    #except Exception as msg:
        #print MESSAGE, msg


if __name__ == '__main__':
    main()
