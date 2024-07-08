import socket


def running_client_on_tcp_socket(server_ip_address, port_number):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip_address, port_number))

    print(f'Connected to server on (ip : {server_ip_address}, port : {port_number})')

    while True:
        data_to_server = input('Insert message : ')
        encoded_data_to_server = data_to_server.encode()
        client_socket.send(encoded_data_to_server)

        if data_to_server == 'Disconnect':
            break



running_client_on_tcp_socket('127.0.0.1', 44111)
