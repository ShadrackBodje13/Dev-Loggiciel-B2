import socket
from _thread import *
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = '192.168.1.92' #on pourrait essayer plutard avec serveur en ligne
port = 5555

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port)) #le bind utilise l'adresse du serveur et le port pour la connexion reseau

except socket.error as e: #si erreur ou exception afficher erreur
    print(str(e))

s.listen(2) #le serveur est en ecoute de la deuxieme connexion
print("Waiting for a connection")

currentId = "0"
pos = ["0:50,50", "1:100,100"]
def threaded_client(conn):
    global currentId, pos
    conn.send(str.encode(currentId))
    currentId = "1"
    reply = ''
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode('utf-8')
            if not data:
                conn.send(str.encode("Goodbye"))
                break
            else:
                print("Recieved: " + reply)
                arr = reply.split(":")
                id = int(arr[0])
                pos[id] = reply

                if id == 0: nid = 1
                if id == 1: nid = 0

                reply = pos[nid][:]
                print("Sending: " + reply)

            conn.sendall(str.encode(reply))
        except:
            break

    print("Connection Closed")
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn,))