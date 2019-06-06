# HTTP Server Shell
# Author: royi levin
# Purpose: Provide a basis for Ex. 4.4
# Note: The code is written in a simple way, without classes,
# log files or other utilities, for educational purpose
# Usage: Fill the missing functions and constants

import os
import socket

SOCKET_TIMEOUT = 1
WEBROOT = "G:\\webroot"
DEFAULT_FILE_PATH = WEBROOT + "\\index.html"
HTTP_VERSION_STR = "HTTP/1.1"
IP = "127.0.0.1"
PORT = 80
MSG_SIZE = 1024
EOL = "\r\n"

REDIRECTION_DICTIONARY = {'/js/box1.js': '/js/box.js'}


def calculate_next(params):
    num_str = "num="
    num = params[params.find(num_str) + len(num_str):]  # [num=345345345
    print "Number found: " + num
    if num_str in params and str(num).isdigit():
        return int(num) + 1
    return None


def calculate_area(params):
    height_str = "height="
    width_str = "width="
    height = params[params.find(height_str) + len(height_str):params.find('&')]
    width = params[params.find(width_str) + len(width_str):]
    print "Width: " + width + ", Height: " + height
    if height_str in params and width_str in params and str(width).isdigit() and str(height).isdigit():
        return float(width) * float(height) / 2
    return None


def get_file_data(filename):
    """ Get data from file """
    try:
        with open(filename, 'rb') as f:
            data = f.read()
            return data
    except IOError as e:
        print None


def get_file_type(resource):
    """

    :param resource:
    :return:
    """
    return resource[resource.rfind('.') + 1:]


def get_content_type(filetype):
    """

    :param filetype:
    :return:
    """
    if filetype == "txt":
        return "text/html; charsest=utf-8"
    if filetype == "html":
        return "text/html; charsest=utf-8"
    if filetype == "css":
        return "text/css"
    if filetype == "jpg" or filetype == "png" or filetype == "ico" or filetype == "gif":
        return "image/jpeg"
    return "text/plain"


def handle_client_request(resource, client_socket):
    """
    Check the required resource,
    generate proper HTTP response and send to client
    """
    # TO DO : add code that given a resource (URL and parameters)
    # generates the proper response

    if "calculate-next" in resource:
        data = calculate_next(resource)
        if not data:
            client_socket.sendall(HTTP_VERSION_STR + " 500 Server Internal Error\r\n\r\n")
            return
        else:
            http_response = HTTP_VERSION_STR + " 200 OK" + EOL \
                          + "Content-Length: " + str(len(str(data))) + EOL \
                          + "Content-Type: text/plain" + EOL \
                          + EOL + str(data)
            client_socket.sendall(http_response)
            return

    if "calculate-area" in resource:
        data = calculate_area(resource)
        if not data:
            client_socket.sendall(HTTP_VERSION_STR + " 500 Server Internal Error\r\n\r\n")
            return
        else:
            http_response = HTTP_VERSION_STR + " 200 OK" + EOL \
                          + "Content-Length: " + str(len(str(data))) + EOL \
                          + "Content-Type: text/plain" + EOL \
                          + EOL + str(data)
            client_socket.sendall(http_response)
            return

    if resource in REDIRECTION_DICTIONARY:
        # we got a redirection woo
        http_response = HTTP_VERSION_STR + " 302 Moved Temporarily" + EOL \
                        + "Location: " + REDIRECTION_DICTIONARY[resource] + \
                        EOL + EOL
        client_socket.send(http_response)
        return

    if resource == '/':
        file_path = DEFAULT_FILE_PATH
    else:
        file_path = WEBROOT + resource
    print "File Path: " + file_path

    if not valid_file(file_path):
        reply_404(client_socket)
        return

    filetype = get_file_type(file_path)
    data = get_file_data(file_path)
    content_type = get_content_type(filetype)
    http_header = HTTP_VERSION_STR + " 200 OK" + EOL \
                  + "Content-Length: " + str(len(data)) + EOL \
                  + "Content-Type: " + str(content_type) + EOL \
                  + EOL
    # TO DO: check if file_path had been redirected,
    # not available or other error code. For example:
    # if file_path in REDIRECTION_DICTIONARY:
    # TO DO: send 302 redirection response

    # TO DO: extract requested file tupe from URL (html, jpg etc)

    # TO DO: handle all other headers

    # TO DO: read the data from the file

    http_response = http_header + data
    client_socket.sendall(http_response)


def valid_file(file_path):
    """vulnerable to directory traversal"""
    return os.path.isfile(file_path)


def validate_http_request(request):
    """
    Check if request is a valid HTTP request
    and returns TRUE / FALSE and the requested URL
    """
    # GET /someFile HTTP/1.1
    # GET / HTTP/1.1
    lines = request.split('\r\n')
    first_line = lines[0].split(' ')
    if len(first_line) != 3:
        return False, None

    if first_line[0] != "GET":
        return False, None

    if first_line[-1] != HTTP_VERSION_STR:
        return False, None

    return True, first_line[1]


def reply_404(client_socket):
    """

    :param client_socket:
    :param resource:
    :return:
    """
    client_socket.sendall("HTTP/1.1 404 Not Found\r\n" \
                          "Content-Length: 0\r\n" \
                          "Connection: close\r\n\r\n")


def handle_client(client_socket):
    """
    Handles client requests: verifies client's requests are legal HTTP,
    calls function to handle the requests
    """
    print 'Client connected'
    while True:
        # TO DO: insert code that receives client request
        # ...
        try:
            client_request = client_socket.recv(MSG_SIZE)
        except socket.timeout:
            print "Timed out"
            break
        valid_http, resource = validate_http_request(client_request)
        if valid_http:
            print 'Got a valid HTTP request'
            handle_client_request(resource, client_socket)
        else:
            print 'Error 500 Server Internal Error'
            client_socket.send(HTTP_VERSION_STR + " 500 Server Internal Error\r\n\r\n")
            break
    print 'Closing connection'
    client_socket.close()


def main():
    """

    :return:
    """
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen(10)
    print "Listening for connections on port {}".format(PORT)

    while True:
        client_socket, client_address = server_socket.accept()
        print 'New connection received'
        client_socket.settimeout(SOCKET_TIMEOUT)
        handle_client(client_socket)


if __name__ == "__main__":
    # Call the main handler function
    main()
