# -*- coding: utf-8 -*-
import socket
from Constants import *

PORT = 1729
IP = "127.0.0.1"
VALIDATE_SHUT_DOWN = "shutting down client"
WELCOME_MSG = "############################################################################\n" \
              "WELCOME TO THE ULTIMATE TOASTER SERVER, WE SUPPORT THE FOLLOWING COMMANDS:\n"
              "EXIT- DISCONNECTS FROM THE SERVER\n" \
              "SHUTDOWN- SHUTDOWNS THE SERVER\n"

def socket_client_initiate(ip, port):
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((ip, port))
    return my_socket


def valid_request(request):
    """
    :param request: client request
    :return: true if the request is valid and false otherwise
    """
    return request in requests_list


def send_request_to_server(my_socket, message):
    my_socket.sendall(decToHex(len(message)) + message)


def handle_server_response(my_socket):
    """
    :return: server response
    """
    # read the size of the message and checks 8 instead of 4and uses hex cuz its much more efficent
    msg_size = my_socket.recv(8)
    # read the actual message
    response = my_socket.recv(hexToDec(msg_size))

    # check if we need to exit
    if response == VALIDATE_SHUT_DOWN:
        return False
    print response
    return True


def handle_user_input(my_socket):
    exit_check = True
    while exit_check:
        request = raw_input("\nPlease enter a command:\n").upper()
        if valid_request(request):
            send_request_to_server(my_socket, request)
            exit_check = handle_server_response(my_socket)
        else:
            print "illegal command"


def main():
    try:
        print WELCOME_MSG
        my_socket = socket_client_initiate(IP, PORT)
        handle_user_input(my_socket)
        my_socket.close()

    except socket.error as msg:
        print "socket error: ", msg
    except Exception as msg:
        print "General error: ", msg


if __name__ == '__main__':
    main()
