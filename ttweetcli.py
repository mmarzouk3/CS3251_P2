#CS 3251 Programming Assignment 2
#Authors: Weixi Li, Mariam Marzouk, Kelly McMaster
#Disclaimer / citation: The class textbook templates were referenced.

from socket import *
import sys
import time

from users import User
from messages import Message

#client changes this to False when they want to close the conxn
global connected


#prints an error message and exits gracefully
#errorType is the error code, the data field is optional
def exitGracefully(errorType, data = ''):
    #invalid IP addr
    if errorType == 1:
        print("error: server ip invalid, connection refused.")
    #invalid port
    elif errorType == 2:
        print("error: server port invalid, connection refused.")
    #invalid username
    elif errorType == 3:
        print("error: username has wrong format, connection refused.")
    #user already logged in
    elif errorType == 4:
        print("username illegal, connection refused.")
    #Wrong number of parameters
    elif errorType == 5:
        print("error: args should contain <ServerIP> <ServerPort> <Username>")
    #Illegal message length(>150)
    elif errorType == 6:
        print("message length illegal, connection refused.")
    #Illegal message length(=0 or None)
    elif errorType == 7:
        print("message format illegal.")
    #Illegal hashtag
    elif errorType == 8:
        print("hashtag illegal format, connection refused.")
    #Maximum hashtags reached
    elif errorType == 9:
        print(data) #print error msg sent from server
    else:
        pass #remove later
    sys.exit()

#checks that the first command from the user has valid args
def checkInput(serverIP, serverPort, username):
    ### Check the server IP addr
    octets = serverIP.split('.')
    if len(octets) == 4:
        for i in octets:
            #ip octet out of range
            if int(i) < 0 or int(i) > 255:
                exitGracefully(1)
    else:
        exitGracefully(1)
    ###
    ### Check the server port
    try:
        port = int(serverPort)
    except:
        exitGracefully(2)
    if port < 1024 or port > 65535:
        exitGracefully(2)
    ###
    ### Check the username
    #checks that the username is an alphanumeric string
    if not username.isalnum():
        exitGracefully(3)

    return serverIP, port, username

#checks if the port is valid
def checkPortValid(input_):
    try:
        port = int(input_)
        return port
    except:
        exitGracefully(2)

#logs in the user
def login(username):
    #the message contains the request type + the client's username to be checked
    message = "check_user" + username
    clientSocket.send(message.encode()) 

    #receive response from server
    response = clientSocket.recv(1024)
    response = response.decode()
    if response == "invalid":
        #the username is already taken; inform the user and exit
        exitGracefully(4)
    if response == "valid":
        user = User(username)
        print("username legal, connection established.")

#sends the tweet request to the server
def sendTweet(userInput):
    message = "tweet....." + username + userInput
    clientSocket.send(message.encode())
    response = clientSocket.recv(1024)
    response = response.decode()
    if response != 'success':
        print(response)

#gets the list of all online users from the server
def getUsers():
    message = "get_users."
    clientSocket.send(message.encode())
    response = clientSocket.recv(1024)
    response = response.decode()
    listOfOnlineUsers = response.split(" ")
    for user in listOfOnlineUsers:
        print(str(user))
    listOfOnlineUsers = [] #does this qualify as "clearing from client memory" ??
    

#logs out the user
def logout(username):
    message = "logout...." + username
    clientSocket.send(message.encode()) #it's a logout request
    clientSocket.close()
    connected == False
    print("bye bye")
    sys.exit()

#listens for commands from the user
#"pass" is just there temporarily until functionality is implemented
def listen():
    while connected:
        userInput = input()
        if userInput == "exit":
            logout(username)
        elif userInput[:5] == "tweet":
            sendTweet(userInput[5:])
        elif userInput == "subscribe":
            pass
        elif userInput == "unsubscribe":
            pass
        elif userInput == "timeline":
            pass
        elif userInput == "getusers":
            getUsers()
        elif userInput == "gettweets":
            pass
        else:
            print("Not a recognized command. Try again.")

#------------------------------
#-----MAIN CLIENT CODE---------
#------------------------------
#parsing command args and checking for validity
if not len(sys.argv) == 4:
    exitGracefully(5)
else:
    #args need to be checked
    #serverIP = sys.argv[1]
    #serverPort = checkPortValid(sys.argv[2])
    #username = sys.argv[3]
    serverIP, serverPort, username = checkInput(sys.argv[1], sys.argv[2], sys.argv[3])

#This line creates the client socket for the TCP connection.
clientSocket = socket(AF_INET, SOCK_STREAM)

#If the following doesn't work, there must be a problem
#with the ip address, server port, or both. Inform the 
#user and exit gracefully.

#try:
connected = True
clientSocket.connect((serverIP, serverPort))
login(username)
#listens for commands typed in by the user
listen()

#except:
    #print("oops") #remove later
    #pass


