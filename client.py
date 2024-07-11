import socket
from helper import send_data, receive_data, get_fixed_string, get_file_path, is_file_valid, \
 send_file_through_socket_connection, create_file, get_directory_path,  is_directory_valid
import os




def handle_client_command(client_socket: socket.socket, client_command):
    client_command = get_fixed_string(client_command, lower=True, strip=True, capitalize=True)

    if client_command == 'Disconnect':
        send_data(client_socket, client_command)

    elif client_command == 'Upload':

        send_data(client_socket, client_command)
        client_file_path = get_file_path()

        if is_file_valid(client_file_path) is True:
            file_name = os.path.basename(client_file_path)
            send_data(client_socket, data=file_name)
            send_file_through_socket_connection(client_socket, client_file_path)

        else:
            print('File path is not valid.')

    elif client_command == 'Download':

        send_data(client_socket, client_command)
        available_file_for_download = receive_data(client_socket)

        if len(available_file_for_download) != 0:
            print(f'The available files for download are : {available_file_for_download}.')
            file_to_download = input('Insert a file name to download : ')
            available_files_for_download_list = available_file_for_download.split(',')

            if file_to_download in available_files_for_download_list:
                directory_path_to_download = get_directory_path()
                print(is_directory_valid(directory_path_to_download))
                if is_directory_valid(directory_path_to_download):
                    print('Directory valid.')
                    send_data(client_socket, file_to_download)
                    file_data = receive_data(client_socket)
                    print(f'file data {file_data}')
                    create_file(directory_path_to_download+'\\'+file_to_download, file_data)

            else:
                send_data(client_socket, '')
                print("This file name is not available.")

        else:
            print('There are no available files for download.')

    else:
        print('Invalid command, must be [Upload/Download/Disconnect].')


def running_client_on_tcp_socket(server_ip_address, port_number):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip_address, port_number))

    print(f'Connected to server on (ip : {server_ip_address}, port : {port_number})')
    receive_welcome_message_from_server = receive_data(client_socket)
    print(receive_welcome_message_from_server)

    while True:
        client_command = input('> Insert command [Upload/Download/Disconnect] : ')
        handle_client_command(client_socket, client_command)

        if client_command == 'Disconnect':
            break


running_client_on_tcp_socket('127.0.0.1', 44111)

if __name__ == '__main__':
    ...
