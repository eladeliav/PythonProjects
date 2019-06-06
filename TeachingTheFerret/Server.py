# -*- coding: utf-8 -*-
import socket
from Constants import *
from PIL import ImageGrab
import glob
import os
import shutil
import subprocess


SERVER_NAME = "TOASTER SERVER 3OOOX"
INVALID = "INVALID COMMAND"
SHUT_DOWN_CLIENT = "shutting down client"
SHUT_DOWN_SERVER = "shutting sown server"
MAX_PACKET_BODY_SIZE = 0x1000
SCREENSHOT_PATH = "./screenshot.png"  # where to save screenshot


def initiate_server_socket(ip, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(1)
    return server_socket


def handle_clients(server_socket):
    shut_down_server = True
    while shut_down_server:
        client_socket, address = server_socket.accept()
        shut_down_server = handle_single_client(client_socket)
        client_socket.close()


# gets the clients request and the first 8 bytes of the msg that was sent  and returns the msg's body and checks to see if the len of the msg is valid
def receive_client_request(client_socket):
    try:
        msg_size = client_socket.recv(8)
        numSize = hexToDec(msg_size)
        if numSize > MAX_PACKET_BODY_SIZE:
            print "packet too big!!"
            return None, None
        request = client_socket.recv(numSize)
        req_and_prms = request.split()
        if len(req_and_prms) > 1:
            return req_and_prms[0], req_and_prms[1:]
        else:
            return req_and_prms[0], None
    except Exception as error:
        print "unexpected error"
        return None, None


def handle_client_request(request, paramaters):
    if request.upper() == "EXIT":
        return SHUT_DOWN_CLIENT
    if request.upper() == "SHUTDOWN":
        return SHUT_DOWN_SERVER
    if request.upper == "TAKE_SCREENSHOT":
        return take_screenshot(request, paramaters)
    if request.upper() == "DIR":
        return list_folder(paramaters)
    if request.upper() == "DELETE_FILE":
        return delete_file(paramaters)
    if request.upper() == "COPY_FILE":
        return copy_file(paramaters)

def send_response_to_client(response, client_socket):
    client_socket.sendall(decToHex(len(response)) + response)


def handle_single_client(client_socket):
    while True:
        operation, paramaters = receive_client_request(client_socket)
        if operation is None:
            continue
        response = handle_client_request(operation, paramaters)
        if response == SHUT_DOWN_CLIENT:
            send_response_to_client(response, client_socket)
            return True
        if response == SHUT_DOWN_SERVER:
            send_response_to_client(SHUT_DOWN_CLIENT, client_socket)
            return False
        send_response_to_client(response, client_socket)


def take_screenshot(request, paramaters):
    """
       Takes a screenshot and returns a phrase to the client that says a screenshot was take.
    """
    im = ImageGrab.grab()
    im.save(SCREENSHOT_PATH)
    return 'Screenshot taken. File name: ' + SCREENSHOT_PATH


def list_folder(folder_path):
    folder_path += "\*"
    files_list = glob.glob(folder_path)
    return " ,".join(files_list)


def check_client_request(request, parameters):
    if parameters is None:
        parameters = {}
    if request in requests_list and requests_list[request] == len(parameters):
        return True
    return False


def valid_folder(folderpath):
    """
    Checks if folder exists
    """
    if os.path.isdir(folderpath):
        return True
    return False


def valid_file(filepath):
    """
    Checks if file exists
    """
    if os.path.exists(filepath):
        return True
    return False



def delete_file(filepath):
    """
    deletes a given file
    """
    if not filepath:
        return "Wrong use of parameters"
    filepath = filepath[0]
    if not valid_file(filepath):
        return "File doesn't exist"
    os.remove(filepath)
    return "File deleted"


def copy_file(parameters):
    """
    copies a given file to a given path
    """
    if not parameters:
        return "Wrong use of parameters"
    filepath1 = parameters[FIRST_ELEMENT]
    filepath2 = parameters[SECOND_ELEMENT]
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
    """
    if not params:
        return "Wrong use of parameters"
    command = params[0]
    try:
        subprocess.check_call(command)
    except WindowsError as e:
        return str(e)
    return "Command Ran"



def main():
    try:
        server_socket = initiate_server_socket(IP, PORT)

        handle_clients(server_socket)

        server_socket.close()

    except socket.error as msg:
        print "socket error: ", msg
    except Exception as msg:
        print "General error: ", msg


if __name__ == '__main__':
    main()