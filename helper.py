import socket
import os


def send_file_content_through_socket_connection(socket_connection: socket.socket, file_path):
    """
    This function sends threw socket connection file content.
    :param socket_connection:
    :param file_path:
    :return None:
    """
    with open(file_path, 'r') as client_file:
        file_data = client_file.read()
        send_data(socket_connection, file_data)


def create_file(file_path, data):
    """
    This function create a file in a given file path and data.
    :param file_path:
    :param data:
    :return None:
    """
    with open(file_path, 'w') as file:
        file.write(data)


def send_data(socket_connection: socket.socket, data: str):
    """
    This function sends data threw socket connection according protocol.
    According to the protocol first 4 bytes represents the data size.

    :param socket_connection:
    :param data:
    :return None:
    """
    data_length_in_binary = len(data).to_bytes(4, byteorder='big')
    encoded_data = data.encode()
    try:
        socket_connection.sendall(data_length_in_binary)
        socket_connection.sendall(encoded_data)
    except ConnectionAbortedError:
        print('> Connection error during data delivering.')

    except Exception:
        print('> Connection error during data delivering.')


def receive_data(socket_connection: socket.socket):
    """
    This function receive data according protocol.
    :param socket_connection:
    :return decode_data:
    :rtype str:
    """
    data_length_in_decimal = int.from_bytes(socket_connection.recv(4), byteorder='big')
    data = b''

    while len(data) < data_length_in_decimal:
        try:
            data_chunk = socket_connection.recv(min(1024, data_length_in_decimal - len(data)))
            data += data_chunk

        except RuntimeError:
            print('> Data is not sent fully, connection closed before full message was sent.')
            return None

        except Exception:
            print('> Error occurred when receiving data.')
            return None

    decoded_data = data.decode()
    return decoded_data


def get_fixed_string(user_string, lower=False, strip=True, capitalize=False):
    """
    This function fixes str according user parameters such as lower, strip, capitalize.
    :param user_string:
    :param lower:
    :param strip:
    :param capitalize:
    :return user string:
    :rtype str:
    """
    if lower is True:
        user_string = user_string.lower()

    if strip is True:
        user_string = user_string.strip()

    if capitalize is True:
        user_string = user_string.capitalize()

    return user_string


def get_file_path(message):
    """
    This function get from user file path.
    :param message:
    :return file_path:
    :rtype str:
    """
    file_path = input(f'> {message}')
    return file_path


def get_directory_path(message):
    """
    This function get directory path from user.
    :param message:
    :return directory_path:
    :rtype str:
    """
    directory_path = input(f'> {message}')
    return directory_path


def is_file_path_valid(file_path):
    """
    This function checks if file path is valid.
    :param file_path:
    :rtype boolean:
    """
    return os.path.isfile(file_path)


def is_directory_path_valid(directory_path):
    """
    This function checks if directory path is valid.
    :param directory_path:
    :rtype boolean:
    """
    return os.path.isdir(directory_path)


def get_server_database_directory():
    """
    This function gets directory path from user, this path will serve as a database path.
    from this path files will be downloaded, or uploaded to this path.
    :return server_database_directory:
    :rtype str:
    """
    while True:
        server_database_directory = get_directory_path(message='Insert server database directory : ')
        if is_directory_path_valid(server_database_directory) is True:
            break

    return server_database_directory



if __name__ == '__main__':
    ...