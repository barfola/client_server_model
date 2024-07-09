import socket
import threading
from helper import send_data, receive_data


def handle_each_client(client_socket: socket.socket, client_address):
    while True:
        data_from_client = receive_data(client_socket)

        if data_from_client == 'Disconnect':
            print(f'Client {client_address} Disconnect.')
            break
        else:
            print(f'Received data : {data_from_client}, from {client_address}.')
            data_to_client = f'Client {client_address}, server got your message.'
            send_data(client_socket, data_to_client)

    client_socket.close()


def running_server_on_tcp_socket(server_ip_address, port_number, number_of_listeners):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip_address, port_number))
    server_socket.listen(number_of_listeners)

    print(f'Server is up and running on ip : {server_ip_address} and port : {port_number}.')

    while True:
        client_socket, client_address = server_socket.accept()
        print(f'Server got connection from {client_address}')
        client_thread = threading.Thread(target=handle_each_client, args=(client_socket, client_address))
        client_thread.start()


if __name__ == '__main__':
    running_server_on_tcp_socket('127.0.0.1', 44111, 5)
