#CS 3251 Programming Assignment 2
#Authors: Weixi Li, Mariam Marzouk, Kelly McMaster
#Disclaimer / citation: The class textbook templates were referenced.

from socket import *
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
#The first message received from the client
#always indicated the request type.
#If a second message is sent, it contains
#data.
def processClientRequests():
    request_type = connectionSocket.recv(1024).decode()
    print("req recevd")
    if request_type == "check_username":
        username = connectionSocket.recv(1024).decode()
        response = loginUserIfValid(username)
        connectionSocket.send(response.encode())
        print("user check")
    elif request_type == "logout":
        username = connectionSocket.recv(1024).decode()
        onlineUsers.remove(username)
        response = "removed"
        connectionSocket.send(response.encode())
        connectionSocket.close()
        print("logout")
        print(onlineUsers)
    else:
        response = "what"
        connectionSocket.send(response.encode())



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
serverSocket.listen(1)
print('The server is ready to receive...')

#This loop keeps the server live for continous listening.
while True:
    connectionSocket, addr = serverSocket.accept()

    processClientRequests()
    request_type = connectionSocket.recv(1024).decode()
    if request_type == "logout":
        username = connectionSocket.recv(1024).decode()
        onlineUsers.remove(username)
        response = "removed"
        connectionSocket.send(response.encode())
        connectionSocket.close()
        print("logout")
        print(onlineUsers)

    
