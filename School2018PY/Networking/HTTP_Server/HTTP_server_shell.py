# coding=utf-8
"""
Elad Eliav
HTTP Server Shell
"""
import socket
import os

server_socket = socket.socket()

# socket constants
IP = '127.0.0.1'
PORT = 80
SOCKET_TIMEOUT = 1

# http headers
DEFAULT_URL = './webroot/index.html'
WEBROOT_PATH = './webroot/'
HTTP_HEADER = 'HTTP/1.1 200 OK\r\n'
HTTP_302 = 'HTTP/1.1 302 Moved Temporarily\r\n'
HTTP_404 = 'HTTP/1.1 404 Not Found\r\n'
HTTP_500 = 'HTTP/1.1 500 Server Internal Error\r\n'

# http content type constants
HTTP_TEXT_TYPE = 'text/html; charset=utf-8'
HTTP_IMAGE_TYPE = 'image/jpeg'
HTTP_CSS_TYPE = 'text/css'
HTTP_JS_TYPE = 'application/javascript'
HTTP_PLAIN = 'text/plain'

# file types
TEXT_TYPE = ('html', 'txt')
IMAGE_TYPE = ("jpg", "ico", "gif", "png", "jfif", "svg")
JS_TYPE = 'js'
CSS_TYPE = 'css'

# dictionary to match between file type and content type
TYPE_DICT = {
    TEXT_TYPE: HTTP_TEXT_TYPE,
    IMAGE_TYPE: HTTP_IMAGE_TYPE,
    JS_TYPE: HTTP_JS_TYPE,
    CSS_TYPE: HTTP_CSS_TYPE,
}

# header fields
HTTP_EMPTY = '\r\n'
CONTENT_TYPE = "Content-Type: {}\r\n"
CONTENT_LENGTH = "Content-Length: {}\r\n"

MESSAGE_404 = "Error 404 File Not Found ¯\_(ツ)_/¯"

REDIRECTION_DICTIONARY = {
    'js/box1.js': 'box.js'
}


def calculate_next(params):
    """
    receives list of params and returns the num + 1
    """
    param_str = "num="
    num = params[params.find(param_str) + len(param_str):]
    print "Number received from calculate next param: " + num
    if param_str in params and str(num).isdigit():
        return int(num) + 1
    return None


def calculate_area(params):
    """
    receives a list of params and calculates the area with those params
    """
    param_height_str = "height="
    param_width_str = "width="
    height = params[params.find(param_height_str) + len(param_height_str): params.find('&')]
    width = params[params.find(param_width_str) + len(param_width_str):]
    print "Height: {}, Width: {}".format(height, width)
    if param_height_str in params and param_width_str in params and str(height).isdigit() and str(width).isdigit():
        return float(height) * float(width) / 2.0
    return None


COMMANDS_DICT = {'calculate-next': calculate_next, 'calculate-area?': calculate_area}


def get_file_data(filename):
    """ Get data from file """
    try:
        with open(filename, 'rb') as f:
            data = f.read()
            return len(data), data
    except IOError as e:
        return 0, None


def get_file_type(filename):
    """
    returns the file extension of a given file
    :param filename: checked file
    :return: file extension string
    """
    file_extension = filename[filename.rfind('.') + 1:]
    return file_extension


def get_content_type(resource):
    """
    Checks with the TYPE_DICT the given resource and returns the needed content type
    :param resource: checked resource
    """
    filetype = get_file_type(resource)
    for key in TYPE_DICT:
        if filetype in key:
            return TYPE_DICT[key]
    return HTTP_TEXT_TYPE


def valid_file(filepath):
    """
    checks if file is valid
    :param filepath: checked file
    :return: True/False
    """
    return os.path.isfile(filepath)


def format_http_response(header, ctype, length, content):
    """
    Generates a valid http response with the received params.
    :param ctype: content type
    :param header: http header
    :param type: content type
    :param length: content length
    :param content: the content
    :return: generated response
    """
    return_msg = header
    return_msg += CONTENT_TYPE.format(ctype)
    return_msg += CONTENT_LENGTH.format(length)
    return_msg += HTTP_EMPTY + content
    return return_msg


def format_http_redirect(header, location):
    """
    Generates a valid http response for a redirection
    :param header: The header
    :param location: new file location (redirect)
    :return:
    """
    response = "{}Location: {}\r\n"
    return response.format(header, location)


def handle_client_request(resource, client_socket):
    """
    Check the required resource,
    generate proper HTTP response and sends to client
    """
    resource = resource[1:]
    for command_key in COMMANDS_DICT:
        if command_key in resource:
            command = command_key
            data = COMMANDS_DICT[command](resource)
            if not data:
                client_socket.send(HTTP_500 + HTTP_EMPTY)  # sending 500
                return
            else:
                data = str(data)
            http_response = format_http_response(HTTP_HEADER, HTTP_PLAIN, len(data), data)
            client_socket.send(http_response)
            return

    url = resource
    if url == '':
        url = DEFAULT_URL
    else:
        url = WEBROOT_PATH + url

    print "Not command, here is url " + url

    if resource in REDIRECTION_DICTIONARY:
        print "about to send 302"
        http_response = format_http_redirect(HTTP_302, REDIRECTION_DICTIONARY[resource])
        print http_response
        client_socket.send(http_response)
        return

    # Dear Ayelet,
    # I can send MESSAGE_404 as data.
    # Every website ever has some .html with a custom 404 message because they add the .html
    # as the data of http response.
    # for example www.amazon.com/whatever.txt, has a 404 page that they sent as the data in the http response
    # as the data in the 404 message.
    if not valid_file(url):
        # http_response = format_http_response(HTTP_404, HTTP_TEXT_TYPE, len(MESSAGE_404), MESSAGE_404)
        http_response = HTTP_404 + HTTP_EMPTY
        print http_response
        client_socket.send(http_response)
        return

    content_type = get_content_type(url)
    content_length, file_data = get_file_data(url)
    http_response = format_http_response(HTTP_HEADER, content_type, content_length, file_data)
    print HTTP_HEADER, '\n', content_type, '\n', content_length
    client_socket.send(http_response)


def validate_http_request(request):
    """
    Check if request is a valid HTTP request
    and returns TRUE / FALSE and the requested URL
    """
    lines = request.split('\n')

    method_line = lines[0].strip()
    if method_line.startswith("GET"):
        method_line = method_line.split()
        if len(method_line) < 2:
            return True, DEFAULT_URL
        return True, method_line[1]
    return False, None


def handle_client(client_socket):
    """
    Handles client requests: verifies client's requests are legal HTTP,
    calls function to handle the requests
    """
    global server_socket
    print 'Client connected'
    while True:
        try:
            client_request = client_socket.recv(1024)
        except KeyboardInterrupt:
            print "Shutting Down"
            server_socket.close()
            client_socket.close()
            exit()
        except socket.timeout:
            break
        except socket.error as e:
            print e
            break
        # ...
        valid_http, resource = validate_http_request(client_request)
        if valid_http:
            print 'Got a valid HTTP request'
            handle_client_request(resource, client_socket)
        else:
            print 'Error: Not a valid HTTP request'
            client_socket.send(HTTP_500 + HTTP_EMPTY)  # sending 500
    print 'Closing connection'
    client_socket.close()


def main():
    """
    Creates and starts to listen on a socket and calls handle_client(for the new accepted socket)
    :return:
    """
    global server_socket
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen(1)
    listening = True
    print "Listening for connections on port %d" % PORT
    while True:
        client_socket, client_address = server_socket.accept()
        listening = False
        print 'New connection received'
        client_socket.settimeout(SOCKET_TIMEOUT)
        handle_client(client_socket)


if __name__ == "__main__":
    # Call the main handler function
    main()
