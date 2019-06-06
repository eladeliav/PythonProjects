# HTTP Server Shell
# Author: Barak Gonen
# Purpose: Provide a basis for Ex. 4.4
# Note: The code is written in a simple way, without classes,
# log files or other utilities, for educational purpose
# Usage: Fill the missing functions and constants

# TO DO: import modules

# TO DO: set constants

from Constants import *
import socket
import os.path


def valid_file(file_name):
    """
    checks if file exists
    """
    return os.path.exists(file_name)


def get_file_data(filename):
    """
    Get data from file
    """
    try:
        with open(filename, 'rb') as filename:
            data = filename.read()
            return len(data), data
    except IOError:
        return 0, None


def get_content_type(filename):
    """
    get the type of the file (html\image\css)
    """
    parts = filename[filename.rfind('.') + 1:]
    if parts == "html" or parts == "txt":
        return "text/html; charset=utf-8"
    if parts == "jpg" or parts == "ico" or parts == "gif" or parts == "png":
        return "image/jpeg"
    if parts == "css":
        return "text/css"
    if parts == "js":
        return "application/javascript"
    return "text/plain"


def send_error(client_socket, status):
    http_response = VERSION + "" + status + EOL + EOL
    client_socket.send(http_response)


def handle_client_request(resource, client_socket):
    """
    Check the required resource,
    generate proper HTTP response and send to client
    """
    # TO DO : add code that given a resource (URL and parameters)
    # generates the proper response
    """
    # TO DO: check if URL had been redirected,
    # not available or other error code. For example:
    if url in REDIRECTION_DICTIONARY:
        # TO DO: send 302 redirection response
    """
    url = ""
    if resource == '/':
        url = DEFAULT_URL
    else:
        url = WEBROOT_PATH + resource
    print "Url: " + url

    if not valid_file(url):
        send_error(client_socket, "HTTP/1.1 " + "404 Not Found\r\n\r\n")
        return
    # TO DO: extract requested file tupe from URL (html, jpg etc)

    content_len, data = get_file_data(url)
    filetype = get_content_type(url)
    http_response = "{} {}\r\nContent-Length: {}\r\nContent-Type: {}\r\n\r\n{}".format(VERSION, "200 ok", content_len, filetype, data)
    print http_response
    client_socket.send(http_response)


def validate_http_request(request):
    """
    Check if request is a valid HTTP request
    and returns TRUE / FALSE and the requested URL
    """
    # TO DO: write function
    lines = request.split()
    command_line = lines[0].strip()
    if command_line.startswith("GET"):
        command_line = command_line.split()
        if len(command_line) < 2:
            return True, lines[1], "200 ok"
    if not valid_file(request):
        return False, None, "404 Not Found"
    else:
        return False, None, "500 Server Internal Error"


def handle_client(client_socket):
    """
    Handles client requests: verifies client's requests are legal HTTP,
    calls function to handle the requests
    """
    print 'Client connected'
    while True:
        # TO DO: insert code that receives client request
        client_request = client_socket.recv(MSG_SIZE)
        valid_http, resource, status = validate_http_request(client_request)
        if valid_http:
            print 'Got a valid HTTP request'
            handle_client_request(resource, client_socket)
        else:
            print status
            send_error(client_socket, "HTTP/1.1 " + status + "\r\n\r\n")
            break
    print 'Closing connection'
    client_socket.close()


def main():
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen(10)
    print ("Listening for connections on port %d" % PORT)

    while True:
        try:
            client_socket, client_address = server_socket.accept()
            print 'New connection received'
            client_socket.settimeout(SOCKET_TIMEOUT)
            handle_client(client_socket)
        except socket.error, e:
            print e


if __name__ == "__main__":
    # Call the main handler function
    main()
