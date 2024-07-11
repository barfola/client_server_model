import socket
import threading
from helper import send_data, receive_data, create_file, send_file_through_socket_connection
import os

server_database_path = 'C:\\Users' # Insert the database directory


def handle_client_upload_command(client_socket: socket.socket):

    client_file_name = receive_data(client_socket)
    if client_file_name != '':
        file_data = receive_data(client_socket)
        create_file(file_path=server_database_path + client_file_name, data=file_data)


def handle_client_download_command(client_socket: socket.socket):
    available_files_for_download_list = os.listdir(server_database_path)
    available_file_for_download = ','.join(available_files_for_download_list)
    send_data(client_socket, available_file_for_download)
    client_file_name_to_download = receive_data(client_socket)

    if client_file_name_to_download in available_files_for_download_list:
        send_file_through_socket_connection(client_socket, server_database_path + client_file_name_to_download)


def handle_client_command(client_socket: socket.socket, client_command):
    global server_database_path

    if client_command == 'Upload':
        handle_client_upload_command(client_socket)

    else:
        handle_client_download_command(client_socket)


def handle_each_client(client_socket: socket.socket, client_address):
    welcome_message = ('> Welcome client, for Upload file insert [Upload] for Download file insert [Download].\n'
                       'for Disconnect insert [Disconnect].')
    send_data(client_socket, welcome_message)

    while True:
        client_command = receive_data(client_socket)

        if client_command == 'Disconnect':
            print(f'Client {client_address} Disconnect.')
            break

        else:
            handle_client_command(client_socket, client_command)

    client_socket.close()


def running_server_on_tcp_socket(server_ip_address, port_number, number_of_listeners):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip_address, port_number))
    server_socket.listen(number_of_listeners)

    print(f'> Server is up and running on ip : {server_ip_address} and port : {port_number}.')

    while True:
        client_socket, client_address = server_socket.accept()
        print(f'> Server got connection from {client_address}')
        client_thread = threading.Thread(target=handle_each_client, args=(client_socket, client_address))
        client_thread.start()


if __name__ == '__main__':
    running_server_on_tcp_socket('127.0.0.1', 44111, 5)
