import socket, sys
import hashlib
import time
import threading
import logging
import os

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT = 12345
buffer = 4096
socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
socket_server.bind((UDP_IP_ADDRESS, UDP_PORT))
direcciones = []
logging.basicConfig(filename='server.log', filemode='w', format='%(asctime)s - %(message)s', level=logging.DEBUG)

numeroClientes = input("Cuantos clientes va a atender? ")
file_name = input("Direccion del archivo: ")
numeroPaquetes = 1
rutaArchivo = "./"+file_name
tamanoArchivo = os.path.getsize(rutaArchivo)

def esperarClientes ():
    i = 0
    while i < int(numeroClientes):
        data, address = socket_server.recvfrom(buffer)
        data = data.strip()
        print("Address received from client ", i + 1, "is: ", address)
        print("Message: ", data)
        direcciones.append(address)
        i = i + 1


def enviarArchivo (pfile_name, addr, s,pfilehash):
    file_name = str.encode(pfile_name)
    s.sendto(file_name, addr)
    s.sendto(pfilehash.encode(),addr)
    f = open(file_name, "rb")
    data = f.read(buffer)
    numeroPaquetes = 0
    while data:
        s.sendto(data, addr)
        #print("sending ...")
        data = f.read(buffer)
        numeroPaquetes = numeroPaquetes + 1
    # s.close()
    f.close()
    print("File was completely sent")
    return numeroPaquetes


def hacerHash (filename):
    file_hash = hashlib.sha256()  # Create the hash object, can use something other than `.sha256()` if you wish
    fHash = open(filename, 'rb')
    print("HASH: " + file_hash.hexdigest())
    #file_hash.update(fHash.read())  # Creates hash of file
    return file_hash.hexdigest()


while True:
    esperarClientes()
    filehash = hacerHash(file_name)
    print(len(direcciones))
    for d in direcciones:
        start = time.time()
        numpaq = enviarArchivo(file_name, d, socket_server,filehash)
        end = time.time()
        mensaje = "Se le envió a la dirección " + str(d[0]) + " , el archivo : " + file_name + ". El tiempo de transmision fue: " + str(end - start) + \
                  " segundos. El numero de paquetes enviados fue: " + str(numpaq) + " El tamaño del archivo enviado fue: " + str(tamanoArchivo) + " bytes"
        logging.info(mensaje)
    break
socket_server.close()