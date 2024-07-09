import socket


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

if __name__ == '__main__':
    ...
