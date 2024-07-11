import socket
import os


def send_file_through_socket_connection(socket_connection: socket.socket, file_path):
    with open(file_path, 'r') as client_file:
        file_data = client_file.read()
        send_data(socket_connection, file_data)


def create_file(file_path, data):
    with open(file_path, 'w') as file:
        file.write(data)


def send_data(socket_connection: socket.socket, data: str):
    data_length_in_binary = len(data).to_bytes(4, byteorder='big')
    socket_connection.sendall(data_length_in_binary)
    encoded_data = data.encode()
    socket_connection.sendall(encoded_data)


def receive_data(socket_connection: socket.socket):
    data_length_in_decimal = int.from_bytes(socket_connection.recv(4), byteorder='big')
    data = b''

    while len(data) < data_length_in_decimal:
        try:
            data_chunk = socket_connection.recv(min(1024, data_length_in_decimal - len(data)))
            data += data_chunk

        except RuntimeError:
            print('Data is not sent fully, connection closed before full message was sent.')
            return None

        except Exception:
            print('Error occurred when receiving data.')
            return None

    decoded_data = data.decode()
    return decoded_data


def get_fixed_string(user_string, lower=False, strip=True, capitalize=False):
    if lower is True:
        user_string = user_string.lower()

    if strip is True:
        user_string = user_string.strip()

    if capitalize is True:
        user_string = user_string.capitalize()

    return user_string


def get_file_path():
    file_path = input('Insert file path : ')
    return file_path


def get_directory_path():
    directory_path = input('Insert directory path : ')
    return directory_path


def is_file_valid(file_path):
    return os.path.isfile(file_path)


def is_directory_valid(directory_path):
    return os.path.isdir(directory_path)


if __name__ == '__main__':
    ...