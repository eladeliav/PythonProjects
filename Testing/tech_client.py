"""
SHIRA NEVO
YUD ALEF 2
CLIENT
"""
import socket
from constant import *


def recv_file(my_socket):
    name = receive_from_server(my_socket)
    extension = name[name.rfind('.'):]
    name = name[:name.rfind('.')]
    done = False
    with open(name + "_cp" + extension, 'wb') as fl:
        chunk = receive_from_server(my_socket)
        while not done:
            fl.write(chunk)
            chunk = receive_from_server(my_socket)
            if chunk == FILE_SENT:
                done = True
    print chunk


def initate_client_socket(IP, PORT):
    """ A FUNCTION THAT RECEIVES AN IP AND A PORT, MAKES A SOCKET AND CONECTS TO SERVER"""
    # initiate socket
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to server
    my_socket.connect((IP, PORT))
    return my_socket


def handle_user_input(my_socket):
    request = "&&&"
    data = "$$$"
    while request.upper() != 'QUIT' and request.upper() != "EXIT":
        print DCT_FUNC
        request = raw_input("please enter operation\n")
        if valid_request(request):
            send_request_to_server(my_socket, request)
            handle_server_response(my_socket)
    # close socket
    my_socket.close()


def valid_request(request):
    """ A FUNCTION THAT CHECKS IF THE REQUEST FROM THE CLIENT IS VALID"""
    if request is "" or not request:
        return False
    par_req = request.split()
    request = par_req[0]
    request = request.upper()
    params = par_req[1:]
    if params is None:
        length = 0
    else:
        length = len(params)
    if request in DCT_FUNC and DCT_FUNC[request] == length:
        return True
    print "pkuda lo hukit"
    return False


def send_request_to_server(my_socket, request):
    """ A FUNCTION THAT SENDS THE REQUEST TO THE SERVER"""
    valid_answer = format_answer(request)
    # sends data
    my_socket.send(valid_answer)


def receive_from_server(my_socket):
    data = " "
    data_size = my_socket.recv(4)
    if data_size.isdigit():
        data = my_socket.recv(int(data_size))
    return data


def handle_server_response(my_socket):
    # receives answer
    data = receive_from_server(my_socket)
    print data
    if data == PREPARE_FILE:
        recv_file(my_socket)
    return data


def format_answer(response):
    valid_send = str(len(str(response))).zfill(4) + response
    return valid_send


def main():
    """
    THE MAIN OF THE CLIENT
    """
    # try:
    my_socket = initate_client_socket(IP, PORT)
    handle_user_input(my_socket)
    # except socket.error as msg:
    #     print "socket error: ", msg
    # except Exception as msg:
    #     print "general error: ", msg


if __name__ == '__main__':
    main()
