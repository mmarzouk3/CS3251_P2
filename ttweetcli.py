#CS 3251 Programming Assignment 2
#Authors: Weixi Li, Mariam Marzouk, Kelly McMaster
#Disclaimer / citation: The class textbook templates were referenced.

from socket import *
import sys
import time

#client changes this to true when they want to close the conxn
clientTerminatesConxn = False 

#Basic error checking; change as needed
#prints an error message and exits gracefully
#type 1 error is an argument format error
def exitGracefully(errorType):
    if errorType == 1:
        print("Invalid command format. Try again.\n\n"
              "Acceptable command formats are:\n"
              "$ python3 ttweetcli.py <ServerIP> <ServerPort> <Username>\n")
    sys.exit()

#checks if the port is valid
def checkPortValid(input_):
    try:
        port = int(input_)
        return port
    except:
        exitGracefully(2)

#parsing command args and checking for validity
if not len(sys.argv) == 4:
    exitGracefully(1)
else:
    #args need to be checked
    serverIP = sys.argv[1]
    serverPort = checkPortValid(sys.argv[2])
    username = sys.argv[3]


#This line creates the client socket for the TCP connection.
clientSocket = socket(AF_INET, SOCK_STREAM)

#currently setting message to be sent as the username (just for basic functionality; change later)
message = username

#If the following doesn't work, there must be a problem
#with the ip address, server port, or both. Inform the 
#user and exit gracefully.

try:
    clientSocket.connect((serverIP, serverPort))

    clientSocket.send(message.encode())
    print('Your username has been uploaded!')

    #receive response from server
    response = clientSocket.recv(1024)
    response = response.decode()
    print(response)

    #Closes the TCP connection
    if clientTerminatesConxn == True:
        clientSocket.close()

except:
    print("oops")
    #exitGracefully(4)

