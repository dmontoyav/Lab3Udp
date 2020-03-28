from socket import *
import sys
import select
import socket
import hashlib
import logging
import time

UDP_IP_ADDRESS = "127.0.0.1"  # Server Address
UDP_PORT = 12345
buffer = 4096
address = (UDP_IP_ADDRESS, UDP_PORT)
socket_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
logging.basicConfig(filename='cliente.log', filemode='w', format='%(asctime)s - %(message)s', level=logging.DEBUG)
nombreArchivo = ""
numeroPaquetes = 0
def hacerHash (filename):
    file_hash = hashlib.sha256()  # Create the hash object, can use something other than `.sha256()` if you wish
    fHash = open(filename, 'rb')
    print("HASH: " + file_hash.hexdigest())
    #file_hash.update(fHash.read())  # Creates hash of file
    return file_hash.hexdigest()


while True:
    message = input('Enter your message > ')
    if message == "exit":
        break
    socket_client.sendto(message.encode(), address)
    data, addr = socket_client.recvfrom(buffer)
    start = time.time()
    nombreArchivo = data.strip()
    print("Received File:", nombreArchivo)
    f = open(data.strip(), 'wb')
    data, addr = socket_client.recvfrom(buffer)
    hashRecibido = data.decode()
    try:
        while (data):
            f.write(data)
            socket_client.settimeout(2)
            data, addr = socket_client.recvfrom(buffer)
            numeroPaquetes += 1
    except timeout:
        f.close()
        end = time.time()
        socket_client.close()
        print("File Downloaded")
        break
hashArchivoRecibido = hacerHash(nombreArchivo)
hashRecibido = str(hashRecibido)
print(hashRecibido)
if hashRecibido == hashArchivoRecibido:
    completo = True
    mensaje = "Se recibieron " + str(numeroPaquetes) + " paquetes del archivo" +  nombreArchivo.decode() +", el tiempo de recepcion fue: " + \
              str(end - start) + "y el archivo estaba correcto"
else:
    completo = False
    mensaje = "Se recibieron " + str(numeroPaquetes) + " paquetes del archivo"+ nombreArchivo.decode()+ ", el tiempo de recepcion fue: " + \
              str(end - start) + "y el archivo estaba correcto"
logging.info(mensaje)
print("Finished")
