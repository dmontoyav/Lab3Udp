from socket import *
import sys
import select
import socket

UDP_IP_ADDRESS = "127.0.0.1"  # Server Address
UDP_PORT = 12345
buffer = 4096
address = (UDP_IP_ADDRESS, UDP_PORT)
socket_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
    message = input('Enter your message > ')
    if message == "exit":
        break
    socket_client.sendto(message.encode(), address)
    data, addr = socket_client.recvfrom(buffer)
    print("Received File:", data.strip())
    f = open(data.strip(), 'wb')
    data, addr = socket_client.recvfrom(buffer)
    try:
        while (data):
            f.write(data)
            socket_client.settimeout(2)
            data, addr = socket_client.recvfrom(buffer)
    except timeout:
        f.close()
        socket_client.close()
        print("File Downloaded")
