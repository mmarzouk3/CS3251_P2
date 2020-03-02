#CS 3251 Programming Assignment 2
#Authors: Weixi Li, Mariam Marzouk, Kelly McMaster
#Disclaimer / citation: The class textbook templates were referenced.

from socket import *
import sys

#checks whether user input is valid
def checkInput(input_):
    pass #(remove later)
    #if something
        #exitGracefully()

#prints an error message and exits gracefully
#error 1 = too many arguments
def exitGracefully(errorType):
    #if error is blah
        #print message
    sys.exit()


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
serverSocket.bind(('0.0.0.0', serverPort))
serverSocket.listen(1)
print('The server is ready to receive...')

#This loop keeps the server live for continous listening.
while True:
    connectionSocket, addr = serverSocket.accept()

    message = connectionSocket.recv(1024).decode()
    sendBack = "You username is: " + message #echos back username to client
    connectionSocket.send(sendBack.encode())

    #Closes the connection socket, but server socket remains open
    #this line should only run when the client decides to terminate the conxn
    connectionSocket.close()