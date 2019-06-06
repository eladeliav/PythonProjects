import os
import shutil
import socket
import subprocess

from PIL import ImageGrab

from constants import *

SERVER_NAME = "Elad's Amazing Server"  # name of server

TOOLBAR_WIDTH = 40  # constant for progress bar width
CLIENT_DC_MSG = "Client Disconnected"
CLIENT_C_MSG = "Client Connected"
ILLEGAL_COMMAND_MSG = "ILLEGAL COMMAND"
FILE_SENT_MSG = "FILE_SENT"  # a message to let the client know it's done sending the file
ZERO_BYTES = 0
SCREENSHOT_PATH = "./screenshot.png"  # where to save screenshot
FILE_CHUNK_SIZE = 1024  # size of chunks to send/receive

# list to keep track of which commands need a socket as a param as well
COMMANDS_NEED_SOCK = {'SEND_FILE', 'DIR', 'HELP'}


class Server(object):
    def __init__(self, ip, port):
        self.sock = socket.socket()
        self.client_socket = socket.socket()
        self.connected = False
        self.server_exit = False
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind((ip, port))
            self.sock.listen(1)
        except socket.error as e:
            print "Couldn't initialize server socket"
            print e
            exit(1)

    @staticmethod
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

    @staticmethod
    def check_client_request(request, params):
        """
        Makes sure client request is valid
        :param request: request to check
        :param params: params to check
        :return: True or False
        """
        request = request.upper()
        if params is None:
            params = {}
        if request in COMMANDS_WITH_PARAMS and COMMANDS_WITH_PARAMS[request] == len(params):
            return True
        return False

    @staticmethod
    def valid_file(filepath):
        """
        Checks if file exists
        :param filepath: file to check
        :return: True of False depending on if file exists
        """
        return os.path.exists(filepath)

    @staticmethod
    def valid_folder(folder_path):
        """
        Checks if folder exists
        :param folder_path: folder to check
        :return: True of False depending on if folder exists
        """
        if os.path.isdir(folder_path):
            return True
        return False

    @staticmethod
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

    def get_name(self):
        """
        Functions simply returns server name
        :return: server name
        """
        return SERVER_NAME

    def delete_file(self, filepath):
        """
        deletes a given file
        :param filepath: given file
        :return: File deleted confirmation msg
        """
        if not filepath:
            return "Wrong use of parameters"
        filepath = filepath[0]
        if not Server.valid_file(filepath):
            return "File doesn't exist"
        os.remove(filepath)
        return "File deleted"

    def copy_file(self, params):
        """
        copies a given file to a given path
        :param params: give
        :return: either file/folder doesn't exist msg, or file copies msg
        """
        if not params:
            return "Wrong use of parameters"
        filepath1 = params[FIRST_ELEMENT]
        filepath2 = params[SECOND_ELEMENT]
        if not Server.valid_file(filepath1):
            to_send = ""
            to_send += filepath1
            to_send += " Doesn't exist"
            return to_send
        if not Server.valid_file(filepath2):
            to_send = ""
            to_send += filepath2
            to_send += " Doesn't exist"
            return to_send
        shutil.copy(filepath1, filepath2)
        return "File Copied"

    def open_exe(self, params):
        """
        Opens a given exe file
        :param params: path to exe
        :return: command ran confirmation msg
        """
        if not params:
            return "Wrong use of parameters"
        command = params[0]
        try:
            subprocess.check_call(command)
        except WindowsError as e:
            return str(e)
        return "Command Ran"

    def take_screenshot(self):
        """
        Takes a screenshot and returns a phrase to the client that says a screenshot was take.
        :return: 'screenshot taken'
        """
        im = ImageGrab.grab()
        im.save(SCREENSHOT_PATH)
        return 'Screenshot taken. File name: ' + SCREENSHOT_PATH

    def print_commands(self):
        """
        Help command to print out the list of commands
        :return: string version of the command list
        """
        self.send_response_to_client(PRINT_DIR_SEPARATORS)
        command_keys = Server.COMMANDS.keys()
        for name in command_keys:
            self.send_response_to_client(name)
        return PRINT_DIR_SEPARATORS

    def server_shutdown(self):
        """
        Shutsdown client and server
        :return: shutdown msg to send to client
        """
        self.connected = False
        self.server_exit = True
        print CLIENT_DC_MSG
        print 'SHUTTING DOWN CLIENT AND SERVER'
        return 'SHUTTING DOWN CLIENT AND SERVER'

    def exit_client(self):
        """
        Sets the connected variable to False which will eventually disconnect the client
        :return: a string of shutting down the client to send to the client
        """
        self.connected = False
        print CLIENT_DC_MSG
        return 'SHUTTING DOWN CLIENT'

    def send_file_info(self, filepath):
        """
        Sends info about a given file to the given client (size of file, name and extension)
        :param filepath: file to send info on
        :param client_socket: client to send info to
        """
        total_file_size = os.path.getsize(filepath)
        self.send_response_to_client(PREPARE_FOR_FILE_MSG)
        self.send_response_to_client(total_file_size)

    def send_file(self, filepath):
        """
        Sends the given file to the client (if valid)
        :param filepath: file to send to client
        :param client_socket: client to send file to
        :return: finished sending file msg
        """
        if filepath is None:
            return "Wrong use of paramaters"
        filepath = filepath[FIRST_ELEMENT]
        if not Server.valid_file(filepath):
            return "File doesn't exist"

        self.send_file_info(filepath)

        with open(filepath, 'rb')as f:
            data = f.read(FILE_CHUNK_SIZE)
            while len(data) > ZERO_BYTES:
                self.send_response_to_client(data)
                data = f.read(FILE_CHUNK_SIZE)
        return FILE_SENT_MSG

    def list_folder(self, params):
        """
        Sends a list of folders in the given folder path to the client
        :param params: filepath to list
        :return: done sending info msg
        """
        if not params:
            return "Wrong use of parameters"
        params = str(params[0])
        if not Server.valid_folder(params):
            return "Folder doesn't exist"
        self.send_response_to_client(PRINT_DIR_SEPARATORS)
        files = os.listdir(params)
        for name in files:
            self.send_response_to_client(name)
        return PRINT_DIR_SEPARATORS

    # Commands dictionary where the keys are command strings and
    # the keys are pointers to functions
    COMMANDS = {
        'NAME': get_name,
        'HELP': print_commands,
        'QUIT': server_shutdown,
        'EXIT': exit_client,
        'TAKE_SCREENSHOT': take_screenshot,
        'SEND_FILE': send_file,
        'DIR': list_folder,
        'DELETE': delete_file,
        'COPY': copy_file,
        'EXECUTE': open_exe
    }

    def send_response_to_client(self, response):
        """
        Properly send a response to client by formatting it with
        the response size and wrapped in a try.
        :param response: response to send
        """
        try:
            to_send = Server.format_response(response)
            self.client_socket.send(to_send)
        except socket.error:
            print "Couldn't send response to client"
            self.connected = False
            print CLIENT_DC_MSG

    def receive_client_request(self):
        """
        Receives client request
        """
        data_size = None
        try:
            data_size = self.client_socket.recv(SIZE_HEADER)
        except KeyboardInterrupt:
            print "\n SHUTTING DOWN"
            Server.shutdown_socket(self.sock)
            Server.shutdown_socket(self.client_socket)
            exit()
        except socket.error as e:
            print "Couldn't receive client data size"
            self.connected = False
            return None, None
        if data_size.isdigit():
            try:
                data = self.client_socket.recv(int(data_size))
            except socket.error as e:
                print "Couldn't receive client data"
                print e
                self.connected = False
                return None, None
        else:
            return None, None
        request_and_params = data.split()
        if len(request_and_params) > 1:
            return request_and_params[FIRST_ELEMENT], request_and_params[SECOND_ELEMENT:]
        else:
            return request_and_params[FIRST_ELEMENT], None

    def handle_client_request(self, request, params):
        """
        Handles the client request by calling the corresponding function in the commands
        dictionary
        :param request: request to handle
        :param params: params to pass if needed
        """
        request = request.upper()
        if COMMANDS_WITH_PARAMS[request] > 0:  # request has params?
            return Server.COMMANDS[request](self, params)  # needs params but not socket

        return Server.COMMANDS[request](self)  # doesn't need anything

    def handle_client(self):
        """
        Handles client by receiving his request, processing, and returning a response
        """
        while self.connected and not self.server_exit:
            request, params = self.receive_client_request()
            if not request and not params:
                print CLIENT_DC_MSG
                return
            valid = Server.check_client_request(request, params)
            if valid:
                response = self.handle_client_request(request, params)
                self.send_response_to_client(response)
            else:
                self.send_response_to_client(ILLEGAL_COMMAND_MSG)

    def listen_for_client(self):
        """
        Loop to keep accepting client, handle client and wait for his exit, and looping.
        """
        while not self.connected and not self.server_exit:  # while we don't need to exit
            try:
                self.client_socket, address = self.sock.accept()
                self.connected = True
                print CLIENT_C_MSG
            except socket.error as e:
                print "Couldn't accept client socket"
                print e
                return
            except KeyboardInterrupt:
                print "\nShutting Down"
                Server.shutdown_socket(self.sock)
                Server.shutdown_socket(self.client_socket)
                exit()
            self.handle_client()
            Server.shutdown_socket(self.client_socket)
            self.connected = False
        Server.shutdown_socket(self.sock)
        Server.shutdown_socket(self.client_socket)

    def run(self):
        if self.sock is not None:
            self.listen_for_client()


def main():
    server = Server(IP, PORT)
    server.run()


if __name__ == "__main__":
    main()
