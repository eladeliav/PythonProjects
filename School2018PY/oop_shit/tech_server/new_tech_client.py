import os
import socket
import sys
from constants import *

class Client(object):
    RECEIVED_FILES_LOCATION = "./ReceivedFiles/"

    def __init__(self, ip, port):
        self.connected = False
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((ip, port))
            self.connected = True
        except socket.error:
            print "Failed to connect"
            exit(1)

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

    @staticmethod
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

    @staticmethod
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

    def receive_multiple_strings(self):
        """
        Receives multiple strings from the server until we get the 'done sending' msg
        """
        done = False
        data = self.read_from_server()
        allReceived = '\n' + data + '\n'
        if data is not False:
            while not done:
                print data
                data = self.read_from_server()
                allReceived += data + '\n'
                if data is not False:
                    if data == PRINT_DIR_SEPARATORS:
                        done = True
                        print data
                else:
                    print "Invalid data size"
        else:
            print "Invalid data size"
        return allReceived

    def receive_file(self, params):
        """
        Loop to read chunk from server, save to file and repeat until done
        :param params: file we're receiving
        """
        total_file_size = self.read_from_server()
        params = params[0]
        file_name = os.path.basename(params[:params.rfind('.')])
        file_extension = params[params.rfind('.'):]
        if total_file_size is False:
            print "Invalid data_size"
            return
        done = False
        params = params[0]
        with open(Client.RECEIVED_FILES_LOCATION + file_name + "_copy" + file_extension, 'wb') as f:
            data = self.read_from_server()
            if data is False:
                print "Invalid data_size"
                return
            while not done:
                f.write(data)
                downloaded_bytes = os.path.getsize(f.name)
                Client.progress(downloaded_bytes, total_file_size, status="Downloading File")
                data = self.read_from_server()
                if data is False:
                    print "Invalid data_size"
                    return
                if data == "FILE_SENT":
                    done = True
                    print '\n', data
                    return '\n' + data

    def read_from_server(self):
        """
        Gets data from server socket
        :return: data if read, False it couldn't read
        """
        data_size = self.sock.recv(SIZE_HEADER)
        if data_size.isdigit():
            to_return = self.sock.recv(int(data_size))
        else:
            to_return = False
        return to_return

    def handle_user_input(self):
        """
        handles user input
        :param my_socket: client socket
        """
        while self.connected:
            # TODO: remove this comment
            # print PRINT_DIR_SEPARATORS
            # for key in COMMANDS_WITH_PARAMS:
            #     print key
            # print PRINT_DIR_SEPARATORS
            request, params = self.receive_user_input()
            if Client.valid_request(request, params):
                self.send_request_to_server(request, params)
                self.handle_server_response(params)
            else:
                print 'Illegal command or wrong use of parameters'
        print 'exiting...'

    def shutdown_socket(self):
        """
        Tries to shutdown a given socket
        :param sock: socket to shutdown
        """
        try:
            self.sock.close()
        except socket.error as e:
            print "Couldn't shutdown socket properly"
            print e

    def send_command(self, request):
        rsp = "Invalid Request"
        command, params = Client.split_req_and_params(request)
        if self.valid_request(command, params):
            self.send_request_to_server(command, params)
            rsp = self.handle_server_response(params)
        return rsp

    def send_request_to_server(self, request, params):
        """
        sends request to server
        :param request: request to send to server
        :param params: params to send to server
        """
        request = request.upper()
        try:
            size = sys.getsizeof(request) + sys.getsizeof(params)
            to_send = str(size).zfill(SIZE_HEADER)
            to_send += request
            if params is not None:
                for item in params:
                    to_send += " " + item
            self.sock.send(to_send)
        except socket.error as e:
            print "Couldn't send request to server"
            print e
            return
        if request == 'EXIT' or request == 'QUIT':
            self.connected = False

    def handle_server_response(self, params):
        """
        receives data size of whatever the server sent us and, if it's valid,
        read whatever data size we received
        then print it out
        :param params: params to pass
        """
        data = self.read_from_server()
        allData = data
        if data is not False:
            if data == PREPARE_FOR_FILE_MSG:
                print data
                return self.receive_file(params)
            if data == PRINT_DIR_SEPARATORS:
                print data
                allData += self.receive_multiple_strings()
                return allData
            print data
        else:
            print 'invalid data size'
            data = "invalid data size"
            return data
        return allData

    def receive_user_input(self):
        """
        Receiving user input, splitting request and params, and returning it
        :param sock: socket to close in case of keyboard interrupt
        :return:
        """
        request_and_params = ""
        while request_and_params == "":
            try:
                request_and_params = raw_input("> ")
            except KeyboardInterrupt:
                print "\nExiting..."
                self.shutdown_socket()
                exit()

        return Client.split_req_and_params(request_and_params)

    @staticmethod
    def split_req_and_params(request_and_params):
        request_and_params = request_and_params.split()
        if len(request_and_params) > 1:
            request = request_and_params[FIRST_ELEMENT]
            params = request_and_params[SECOND_ELEMENT:]
        else:
            request = request_and_params[FIRST_ELEMENT]
            params = None
        return request, params

    def run(self):
        try:
            if self.sock is not None:
                self.handle_user_input()
                self.shutdown_socket()
        except socket.error as e:
            print "exiting..."
            self.shutdown_socket()


def main():
    client = Client(IP, PORT)
    client.run()


if __name__ == '__main__':
    main()
