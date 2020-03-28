import socket               # Import socket module
import hashlib
import time
import threading
import logging
import os

msj = "Thank you for connecting"
port = 50000                    # Reserve a port for your service every new transfer wants a new port or you must wait.
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)            # Create a socket object
host = "localhost"   # Get local machine name
s.bind((host, port))            # Bind to the port
s.listen()                    # Now wait for client connection.
logging.basicConfig(filename= 'server.log', filemode='w' , format = '%(asctime)s - %(message)s', level= logging.DEBUG)
conexiones = []
direcciones = []

print('Numero de clientes que voy a tener')
numeroClientes = input()
print ('Server listening....')

def accepting_connections (numeroClientes):
    for c in conexiones:
        c.close()

    del conexiones[:]
    del direcciones[:]

    while len(conexiones) < int(numeroClientes):
        conn, addr = s.accept()  # Establish connection with client.
        data = conn.recv(1024)
        print('Server received', repr(data))
        s.setblocking(1)
        conexiones.append(conn)
        direcciones.append(addr)
        print('Got connection from', addr)


while True:
    accepting_connections(numeroClientes)
    print ('Ponga el nombre del archivo')
    nombreArchivo = input()
    filename = nombreArchivo    #In the same folder or path is this file running must the file you want to tranfser to be
    i=0
    rutaArchivo = "./"+nombreArchivo
    tamanoArchivo = os.path.getsize(rutaArchivo)

    while i in range(int(numeroClientes)):

        file_hash = hashlib.sha256()  # Create the hash object, can use something other than `.sha256()` if you wish
        fHash = open(filename, 'rb')
        print("HASH: " + file_hash.hexdigest())
        file_hash.update(fHash.read())  # Creates hash of file
        conexiones[i].send(file_hash.hexdigest().encode()) #Sends hash

        f = open(filename, 'rb')
        l = f.read(1024)

        start = time.time()
        numeroPaquetes = 1
        while (l):
            conexiones[i].send(l)
            print('Sent ',repr(l))
              # Update the hash
            l = f.read(1024)
            numeroPaquetes = numeroPaquetes +1
          # conexiones[i].send(b'Thank you or connecting')
        conexiones[i].close()
        end = time.time()
        print("Tiempo " + str(i) + " : "+ str(end - start))
        mensaje = "Se le envió al cliente número " + str(i) + " el archivo : " + nombreArchivo + ". El tiempo de transmision fue: " + str(end - start) + \
                  " El numero de paquetes enviados fue: " + str(numeroPaquetes) + " El tamaño del archivo enviado fue: " + str(tamanoArchivo) + " bytes"
        logging.info(mensaje)
        i += 1
    f.close()

    print('Done sending')

