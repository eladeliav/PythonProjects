"""
SHIRA NEVO
YUD ALEF 2
SERVER
"""
import shutil

from PIL import ImageGrab
import socket
import os
from constant import *
import glob
import subprocess


def take_screenshot():
    """ TAKES A SCREENSHOT OF THE SERVER """
    # grab fullscreen
    im = ImageGrab.grab()
    # save image file
    im.save(SCREENSHOT_FILE)
    return 'The screenshot was taken, File name: ' + SCREENSHOT_FILE


def delete_file(parms):
    os.remove(parms)
    return "File Delited"


def list_folder(folder_path):
    folder_path += "*"
    files_list = glob.glob(folder_path)
    return " ,\n".join(files_list)


def exit(client_socket):
    """ CLOSES THE SOCKET OF THE CLIENT """
    client_socket.close()


def send_file_info(parms, client_socket):
    send_response_to_client(PREPARE_FILE, client_socket)  # teling clint to get redy to recv file
    file_name = os.path.basename(parms)  # get file name from path
    send_response_to_client(file_name, client_socket)  # send name


def send_file(parms, client_socket):
    send_file_info(parms, client_socket)

    with open(parms, 'rb') as fl:
        chunk = fl.read(MSG_LEN)  # red chunk
        while len(chunk) > 0:  # if chunk not 0
            send_response_to_client(chunk, client_socket)  # send chunk
            chunk = fl.read(MSG_LEN)  # red new chunk (last chunk not 1024)
    return FILE_SENT  # NOW I DESERVE CHUnKY MONKEY


def initiate_server_socket(IP, PORT):
    """ A FUNCTION THAT RECIEVES AN IP AND A PORT, MAKES A SOCKET AND STARTS TO LISTEN"""
    # initiating server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # the server binds itself to a certain socket
    server_socket.bind((IP, PORT))
    # listening to the socket
    server_socket.listen(1)
    return server_socket


def handle_clients(server_socket):
    """ A FUNCTION THAT RECIEVES A SOCKET AND WAITS FOR A CLIENT
    THE MOMENT THE CLIENT SENDS A SERVICE REQUEST IT CALLS THE FUNCTION
    handle_single_client THAT HANDLES WHITH THE COSTUMER UNTIL HE ASKS TO QUIT"""
    done = False
    while not done:
        # accepting a connect request
        client_socket, address = (server_socket.accept())
        # calling the function that handles the client
        done = handle_single_client(client_socket)
    # closing socket when the client quits
    client_socket.close()
    server_socket.close()


def handle_single_client(client_socket):
    """ A FUNCTION THAT GETS A SINGLE CLIENT SOCKET AND HANDLES HIS REQUEST"""
    request = "$$$"
    while request != '' and request != 'QUIT' and request != 'EXIT':
        # try:
        # receiving data
        request, params = receive_client_request(client_socket)
        request = request.upper()
        valid = check_client_request(request, params)  # CHECKING IF THE REQUEST IS VALID
        if valid:
            response = handle_client_request(request, params,
                                             client_socket)  # CHECKING THE RESPONS ACOORDING TO PROTOCOL
            send_response_to_client(response, client_socket)  # SENDS THE RESPONSE TO CLIENT
        else:
            send_response_to_client("illgal command", client_socket)
    # except Exception as e:
    #     print e
    #     return False
    if request == "QUIT":
        return True
    return False


def receive_client_request(client_socket):
    """ A FUNCTION THAT RECIEVES THE CLIENT'S REQUEST """
    # read from socket
    data = client_socket.recv(4)
    req_and_prms = ""
    if data.isdigit():
        request = client_socket.recv(int(data))
    else:
        return "", None
    # split to request and parameters
    req_and_prms = request.split()
    if len(req_and_prms) > 1:
        return req_and_prms[0], req_and_prms[1:]
    else:
        return req_and_prms[0], None


def check_client_request(request, params):
    """ A FUNCTION THAT CHECKS IF THE REQUEST FROM THE CLIENT IS VALID"""
    request = request.upper()
    print params
    if params is None:
        length = 0
        exist = True
    else:
        length = len(params)
        if request in LST_FILES_FUNCTION:
            exist = valid_file(params[0])
        elif request in LST_FOLDER_FUNCTION:
            exist = valid_folder(params[0])
        elif request == "COPY":
            x = valid_file(params[0])
            y = valid_folder(params[1])
            if valid_file(params[0]) and valid_folder(params[1]):
                exist = True
            else:
                exist = False
        else:
            exist = True
    print exist
    if request in DCT_FUNC and DCT_FUNC[request] == length and exist:
        print request + "is valid"
        return True
    return False


def valid_file(filepath):
    """
    CHECKING IF FILE EXIST
    """
    if os.path.exists(filepath):
        return True
    return False


def valid_folder(folderpath):
    """
    CHECKING IF FOLDER EXIST
    """
    print "checks"
    if os.path.isdir(folderpath):
        return True
    return False


def send_response_to_client(response, client_socket):
    """ A FUNCTION THAT RETURNS THE RESPONS TO CLIENT"""
    # sending the same data
    valid_send = format_answer(response)
    client_socket.send(valid_send)
    if response == "Exiting...":
        client_socket.close()


def execute(parms):
    try:
        subprocess.check_call(parms)
    except WindowsError as e:
        return str(e)
    return "Did Execute"


def copy_files(param, param1):
    shutil.copy(param, param1)
    return "Copied"


def handle_client_request(request, parms, client_socket):
    """ A FUNDTION THAT EXECUTE THE CLIENT REQUEST AND PREPARES A REPLY STRING"""
    request = request.upper()
    response = "Exiting..."
    if request == "TAKE_SCREENSHOT":
        response = take_screenshot()
    elif request == "SEND_FILE":
        response = send_file(parms[0], client_socket)
    elif request == "DIR":
        response = list_folder(parms[0])
    elif request == "DELETE":
        response = delete_file(parms[0])
    elif request == "COPY":
        response = copy_files(parms[0], parms[1])
    elif request == "EXECUTE":
        response = execute(parms[0])
    return response


def format_answer(response):
    """ FORMATING THE ANSWER"""
    valid_send = str(len(str(response))).zfill(4) + str(response)
    return valid_send


def main():
    """
    THE MAIN OF THE SERVER
    """
    # try:
    server_socket = initiate_server_socket(IP, PORT)
    handle_clients(server_socket)
    server_socket.close()
    # except socket.error as msg:
    #     print "socket error: ", msg
    # except Exception as msg:
    #     print "general error: ", msg


if __name__ == '__main__':
    main()
