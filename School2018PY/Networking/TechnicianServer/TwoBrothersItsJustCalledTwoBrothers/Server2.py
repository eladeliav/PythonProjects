import socket
from Constants import *
from PIL import ImageGrab
import os.path
im = ImageGrab.grab()
client_socket = None

FILE_SENT_MSG = "FILE_SENT"  # a message to let the client know it's done sending the file

def take_screenshot():
    """
    takes a screenshot and returns to the the client "screenshot take"
    """
    im.save(SCREENSHOT_PATH)
    return "screenshot taken: " + SCREENSHOT_PATH


def quit():
    return "quitting..."


def send_file_info(filepath):
    """
    Sends info about a given file to the given client (size of file, name and extension)
    :param filepath: file to send info on
    """
    total_file_size = os.path.getsize(filepath)
    send_response_to_client(PREPARE_FOR_FILE_MSG)
    send_response_to_client(total_file_size)


def send_file(filepath):
    """
    Sends the given file to the client (if valid)
    :param filepath: file to send to client
    :return: finished sending file msg
    """
    if filepath is None:
        return "Wrong use of paramaters"
    if not valid_file(filepath):
        return "File doesn't exist"

    send_file_info(filepath)

    with open(filepath, "rb")as f:
        data = f.read(CHUNKSIZE)
        while len(data) > ZERO_BYTES:
            send_response_to_client(data)
            data = f.read(CHUNKSIZE)
    return FILE_SENT_MSG


def valid_file(file_name):
    return os.path.exists(file_name)


def initiate_server_socket(ip, port):
    """
    the function gets ip and port, creates the socket, starts to listen
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ALL_IFS, PORT))
    server_socket.listen(1)
    return server_socket


def receive_client_request(client_socket):
    """
    the function reads the commands from the socket
    """
    data_size = client_socket.recv(MSG_HEADER)
    if data_size.isdigit():
        data = client_socket.recv(int(data_size))
    else:
        return None, None
    request_and_params = data.split()
    if len(request_and_params) > 1:
        return request_and_params[0], request_and_params[1:]
    else:
        return request_and_params[0], None


def check_client_request(request, params):
    """
    checks if the request is valid
    """
    params_dict = {"TAKE_SCREENSHOT": 0, "SEND_FILE": 1, "DIR": 1, "DELETE": 1, "COPY": 2, "EXECUTE": 1, "QUIT": 0}
    file_check_needed = ["SEND_FILE", "DIR", "DELETE", "COPY"]
    if request in file_check_needed:
        for file in params:
            if not valid_file(file):
                return False
    if params is None and params_dict[request] == 0:
        return True
    return request.upper() in COMMAND_LIST and len(params) == params_dict[request.upper()]


def send_response_to_client(response):
    """
    sends the response of the server back to the client
    """
    response = str(response)
    to_send = ''
    size = str(len(str(response))).zfill(4)
    to_send += size
    to_send += response
    client_socket.send(to_send)


def handle_client_request(request, params):
    """
    checks what command to perform
    """
    command_dict = {"TAKE_SCREENSHOT": take_screenshot, "QUIT": quit, "SEND_FILE": send_file}
    if not params:
        return command_dict[request]()
    if len(params) == 1:
        return command_dict[request](params[0])
    if len(params) == 2:
        return command_dict[request](params[0], params[1])


def handle_single_client(client_socket):
    request = " "
    while request != '' and request != 'QUIT':  # checks if the request (below) is not nothing (" ") or quit
        request, params = receive_client_request(client_socket)  # requests the client for a command
        valid = check_client_request(request, params)  # checks if the command is included in the command list
        if valid:
            response = handle_client_request(request, params)  # the response is the returned value from one of the commands in list
            send_response_to_client(response)  # sends the response to the client
        else:
            send_response_to_client("Illegal Command")  # if not valid send in response illegal to the client


def handle_clients(server_socket):
    global client_socket
    client_socket, address = server_socket.accept()  # accepting a connect request
    handle_single_client(client_socket)  # calls the function above
    client_socket.close()  # close the socket


def main():
    try:
        handle_clients(initiate_server_socket(IP, PORT))
    except socket.error as msg:
        print MESSAGE, msg
    #except Exception as msg:
        #print MESSAGE, msg


if __name__ == '__main__':
    main()
