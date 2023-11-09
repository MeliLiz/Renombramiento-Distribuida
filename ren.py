import socket
import threading
import socketserver
from random import randrange
import time

direccion_ip = "172.20.6.11" #Para cada proceso cambiar la ip
mi_nombre = '1' # Para cada proceso cambiar el nombre
r = 1 # Las rondas comienzan en 1
nombres = []
vecinos = ["172.20.6.12","172.20.6.13","172.20.6.14"] # Para cada proceso cambiar a los vecinos

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = str(self.request.recv(1024), 'ascii')
        nombres.append(data)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


def client(ip, message, port=12345):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((ip, port))
            sock.sendall(bytes(message, 'ascii'))
            sock.close()
            return 1
    except:
        return 6
    
# Funcion para escribir en el archivo de texto
def escribirMsj(cadena):
    with open("log.txt", "a") as f:
        f.write(cadena + "\n")
        f.close()

def ronda():
    global r
    global mi_nombre
    global nombres
    n = len(vecinos) + 1
    while True:
        if int(time.time() % 30) == 0: #epoch segundos desde 1 de enero de 1970. int % 30 = 0,  
            for vecino in vecinos:
                client(vecino, mi_nombre)
            try:
                time.sleep(3) #esperar 3 segundos, []
                mensaje = "Mensajes recibidos: "+ str(len(nombres))
                print(mensaje)
                escribirMsj(mensaje)#Escribimos en el archivo el numero de mensajes recibidos
                if len(nombres) == n-r: #Como el proceso no se envia mensaje a si mismo, la longitud debe ser n-r y no n-r+1
                    nombres.append(mi_nombre)
                    if max(nombres) == mi_nombre:
                        mi_nombre = r
            except:
                time.sleep(1)
                nombres = []
                break
            time.sleep(1)
            nombres = []
            break
        else:
            continue


if __name__ == "__main__":
    HOST, PORT = direccion_ip, 12345
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    with server:
        ip, port = server.server_address
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        nombre_inicial = mi_nombre
        mensaje = "Nombre inicial: " + mi_nombre #Escribimos en el archivo el nombre inicial del proceso
        print(mensaje)
        escribirMsj(mensaje)
        for _ in range(6):
            print("Ronda: ", r)
            escribirMsj("Ronda:"+str(r)) #Escribimos en el archivo el numero de ronda
            ronda()
            r = r+1
            if nombre_inicial != mi_nombre:
                break
        mensaje = "Nuevo nombre:"+ str(mi_nombre)
        print(mensaje)
        escribirMsj(mensaje) #Escribimos en el archivo el nuevo nombre del proceso
        server.shutdown()