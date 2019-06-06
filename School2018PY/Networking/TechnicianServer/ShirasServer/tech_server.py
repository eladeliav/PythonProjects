"""
SHIRA NEVO
YUD ALEF 2
SERVER
"""
from PIL import ImageGrab
import socket
import os
from constant import *
import glob


def take_screenshot():
    """ TAKES A SCREENSHOT OF THE SERVER """
    # grab fullscreen
    im = ImageGrab.grab()
    # save image file
    im.save(SCREENSHOT_FILE)
    return 'The screenshot was taken, File name: ' + SCREENSHOT_FILE


def list_folder(folder_path):
    folder_path += "\*"
    files_list = glob.glob(folder_path)
    return " ,".join(files_list)


def exit(client_socket):
    """ CLOSES THE SOCKET OF THE CLIENT """
    client_socket.close()


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
    while request != '' and request != 'QUIT':
        try:
            # receiving data
            request, params = receive_client_request(client_socket)
            valid = check_client_request(request, params)  # CHECKING IF THE REQUEST IS VALID
            if valid:
                response = handle_client_request(request, params, client_socket)  # CHECKING THE RESPONS ACOORDING TO PROTOCOL
                send_response_to_client(response, client_socket)  # SENDS THE RESPONSE TO CLIENT
            else:
                send_response_to_client("illgal command", client_socket)
        except Exception as e:
            print e
            return False
    if request == "QUIT":
        return True


def receive_client_request(client_socket):
    """ A FUNCTION THAT RECIEVES THE CLIENT'S REQUEST """
    # read from socket
    data = client_socket.recv(4)
    req_and_prms = ""
    if data.isdigit():
        request = client_socket.recv(int(data))
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
            exist = valid_file(params)
        elif request in LST_FOLDER_FUNCTION:
            exist = valid_folder(params)
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
    folderpath = folderpath[0]
    if os.path.isdir(folderpath):
        return True
    return False


def send_response_to_client(response, client_socket):
    """ A FUNCTION THAT RETURNS THE RESPONS TO CLIENT"""
    # sending the same data
    valid_send = format_answer(response)
    client_socket.send(valid_send)


def handle_client_request(request, parms, client_socket):
    """ A FUNDTION THAT EXECUTE THE CLIENT REQUEST AND PREPARES A REPLY STRING"""
    request = request.upper()
    response = ""
    if request == "TAKE_SCREENSHOT":
        response = take_screenshot()
    # if request == "SEND FILE":
    #   send_file()
    if request == "DIR":
        response = list_folder(str(parms))
    # if request == "DELETE":
    #   delete()
    # if request == "COPY":
    #  copy()
    # if request == "EXECUTE":
    # execute()
    # if request == "EXIT":
    #     exit()
    return response


def format_answer(response):
    """ FORMATING THE ANSWER"""
    valid_send = str(len(str(response))).zfill(4) + str(response)
    return valid_send


def main():
    """
    THE MAIN OF THE SERVER
    """
    try:
        server_socket = initiate_server_socket(IP, PORT)
        handle_clients(server_socket)
        server_socket.close()
    except socket.error as msg:
        print "socket error: ", msg
    except Exception as msg:
        print "general error: ", msg


if __name__ == '__main__':
    main()
