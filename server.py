import socket
import time


def running_server_on_tcp_socket(server_ip_address, port_number, number_of_listeners):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip_address, port_number))
    server_socket.listen(number_of_listeners)

    print(f'Server is up and running on ip : {server_ip_address} and port : {port_number}.')

    return server_socket





