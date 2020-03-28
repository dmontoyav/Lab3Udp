import socket                   # Import socket module
import hashlib
import time
import logging
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)           # Create a socket object
host = 'localhost'  #Ip address that the TCPServer  is there
port = 50000                     # Reserve a port for your service every new transfer wants a new port or you must wait.
logging.basicConfig(filename= 'cliente.log', filemode='w' , format = '%(asctime)s - %(message)s', level= logging.DEBUG)
s.connect((host, port))
s.send(b'Hello server! Connection succesful ready to receive')

hashFile = s.recv(8000)
print("HASH " + hashFile.decode())

with open('received_file', 'wb') as f:
    print ('file opened')
    start = time.time()
    numeroPaquetes = 0
    while True:
        print('receiving data...')
        data = s.recv(1024)
        print('data=%s', (data))
        numeroPaquetes = numeroPaquetes + 1
        if not data:
            end = time.time()
            print("Tiempo: " + str(end - start))
            break
        # write data to a file
        f.write(data)

f.close()

#Calcula el hash del archivo recibido
filename = 'received_file'
file_hash = hashlib.sha256()  # Create the hash object, can use something other than `.sha256()` if you wish
fHash = open(filename, 'rb')
file_hash.update(fHash.read())  # Creates hash of file
correcto = False
if file_hash.hexdigest() == hashFile.decode():
    print('Successfully get the file')
    correcto = True
    s.send(b'Succesfully get the file')
else:
    print('Hash del archivo no corresponde')
    s.send(b'Hash del archivo no corresponde')

s.close()
if correcto:
    mensaje = "Se recibieron " + str(numeroPaquetes) + " paquetes del archivo received_file, el tiempo de recepcion fue: " + \
              str(end-start) + "y el archivo estaba correcto"
else:
    mensaje =  "Se recibieron " + str(numeroPaquetes) + " paquetes del archivo received_file, el tiempo de recepcion fue: " +\
               str(end-start) + "y el archivo estaba incorrecto"

logging.info(mensaje)
print('connection closed')