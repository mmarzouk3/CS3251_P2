#CS 3251 Programming Assignment 2
#Authors: Weixi Li, Mariam Marzouk, Kelly McMaster
#Disclaimer / citation: The class textbook templates were referenced.

from socket import *
from _thread import start_new_thread
import sys

onlineUsers = []

#checks whether user input is valid
def checkInput(input_):
    pass #(remove later)
    #if something
        #exitGracefully()

#checks whether the username is valid (i.e. not taken)
def notTaken(username):
    for user in onlineUsers:
        if username == user:
            return False
    return True

#logs the user in if the username is valid
def loginUserIfValid(username):
    #add it to the list of online users if the username is valid
    if notTaken(username):
        onlineUsers.append(username)
        response = "valid"
    else:
        response = "invalid"
    return response

#prints an error message and exits gracefully
#error 1 = too many arguments
def exitGracefully(errorType):
    #if error is blah
        #print message
    sys.exit()

#processes the client's requests
#The first 10 characters are reserved to
#indicate the request type; the 10th char
#onwards contains the actual client message
def processClientRequests(data):
    print("req recevd")
    request_type = data[:10] #first 10 characters reserved for request type
    message = data[10:] #10th character onwards is the actual client data
    if request_type == "check_user":
        username = message
        response = loginUserIfValid(username)
        print("user check")
        return response
    elif request_type == "logout....":
        username = message
        try:
            onlineUsers.remove(username)
        except:
            pass
        response = "logged_out"
        return response
    else:
        response = "what" #change
    return response

#creates a thread for the new client trying to log in
def client_thread(connectionSocket):
    connected = True
    while connected:
        data = connectionSocket.recv(1024)
        data = data.decode()
        if not data:
            break
        reply = processClientRequests(data)
        if reply == 'logged_out': 
            connectionSocket.close()
            connected = False
        else:
            connectionSocket.sendall(reply.encode())

#------------------------------
#-----MAIN SERVER CODE---------
#------------------------------
#command line arg parsing and error checks
if not len(sys.argv) == 2:
    exitGracefully(1)
else:
    portArg = sys.argv[1]
    checkInput(portArg)

serverPort = int(portArg) 

#This creates the server socket for the TCP connection.
serverSocket = socket(AF_INET, SOCK_STREAM)
#binding server socket to localhost and the user-inputted port
serverSocket.bind(('', serverPort))
serverSocket.listen()
print('The server is ready to receive...')

#This loop keeps the server live for continous listening.
while True:
    #blocking call, waits to accept a connection
    connectionSocket, addr = serverSocket.accept()
    #opens a connection for the new client
    start_new_thread(client_thread, (connectionSocket,))

serverSocket.close()
