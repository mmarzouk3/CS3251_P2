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

#logs in the user
def login(username):
    request_type = "check_username"
    clientSocket.send(request_type.encode()) #it's a check username request
    #wait 1/100th of second (give the server time to process the first message)
    time.sleep(0.01) 
    clientSocket.send(username.encode()) #send username of user to check
    #receive response from server
    response = clientSocket.recv(1024)
    response = response.decode()
    if response == "invalid":
        print("error: username has wrong format, connection refused.")
    if response == "valid":
        print("username legal, connection established.")

#logs out the user
def logout(username):
    request_type = "logout"
    clientSocket.send(request_type.encode()) #it's a logout request
    #wait 1/100th of second (give the server time to process the first message)
    time.sleep(0.01) 
    clientSocket.send(username.encode()) #send username of user to log out
    #clientSocket.close()
    clientTerminatesConxn == True
    print("bye bye")
    sys.exit()

#listens for commands from the user
#"pass" is just there temporarily until functionality is implemented
def listen():
    while not clientTerminatesConxn:
        command = input()
        if command == "exit":
            logout(username)
        elif command == "tweet":
            pass
        elif command == "subscribe":
            pass
        elif command == "unsubscribe":
            pass
        elif command == "timeline":
            pass
        elif command == "getusers":
            pass
        elif command == "gettweets":
            pass
        else:
            print("Not a recognized command. Try again.")


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

#If the following doesn't work, there must be a problem
#with the ip address, server port, or both. Inform the 
#user and exit gracefully.

#try:
clientSocket.connect((serverIP, serverPort))
login(username)

listen()

#except:
    #print("oops")
    #exitGracefully(4)

