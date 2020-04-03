#CS 3251 Programming Assignment 2
#Authors: Weixi Li, Mariam Marzouk, Kelly McMaster
#Disclaimer / citation: The class textbook templates were referenced.

from socket import *
import sys
import time
import pickle

from users import User
from messages import Message
from request import Request, Method
from response import Status

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
            if i == '' or int(i) < 0 or int(i) > 255:
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
    request = Request(Method.CHECK_USER, username)
    clientSocket.send(pickle.dumps(request))

    #receive response from server
    response = clientSocket.recv(1024)
    response = pickle.loads(response)
    if response.status == Status.ERROR:
        #the username is already taken; inform the user and exit
        exitGracefully(4)
    else:
        user = User(username)
        print("username legal, connection established.")

#checks the tweet and sends it to the server if it's valid
def sendTweet(userInput):
    startIndex = userInput.find('\"') #the starting index of the tweet message
    #startIndexHash = userInput.find('#') #the starting index of the hashtags
    if startIndex != -1: #i.e. if the first quote was found
        endIndex = userInput.find('\"', startIndex + 1)
        if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
            tweetMessage = userInput[startIndex + 1: endIndex]
            if len(tweetMessage) < 1:
                print("message format illegal.")
            if len(tweetMessage) > 150:
                print("message length illegal, connection refused.")
            else:
                hashPart = userInput[endIndex:] #search for hashtag after the tweet message
                startIndexHash = hashPart.find('#') #the starting index of the hashtags
                if startIndexHash != -1: #hashtags found
                    hashtags = hashPart[startIndexHash + 1:]
                    hashtagList = hashtags.split("#")
                    for hashtag in hashtagList:
                        if not hashtag.isalnum() or len(hashtag) < 1:
                            print("hashtag illegal format, connection refused.")
                    else:
                        #Send the tweet to the server
                        userTweet = Message(tweetMessage, username, hashtagList)
                        request = Request(Method.TWEET, userTweet)
                        clientSocket.send(pickle.dumps(request))
                        response = clientSocket.recv(1024)
                        response = pickle.loads(response)
                        if response.status == Status.ERROR:
                            print(response.body)

#gets the list of all online users from the server
def getUsers():
    request = Request(Method.GET_USERS)
    clientSocket.send(pickle.dumps(request))
    response = clientSocket.recv(1024)
    response = pickle.loads(response)
    listOfOnlineUsers = response.body
    for user in listOfOnlineUsers:
        print(user)

def getTweets(username):
    request = Request(Method.GET_TWEETS, username)
    clientSocket.send(pickle.dumps(request))
    response = getResponse()

    if response.status == Status.ERROR:
        print(response.body)
    else:
        messages = response.body
        for msg in messages:
            print(str(msg))

#logs out the user
def logout(username):
    request = Request(Method.LOGOUT, username)
    clientSocket.send(pickle.dumps(request)) #it's a logout request
    clientSocket.close()
    connected == False
    print("bye bye")
    sys.exit()

def subscribe(tag):
    request = Request(Method.SUB, [tag, username])
    clientSocket.send(pickle.dumps(request))
    response = clientSocket.recv(1024)
    response = pickle.loads(response)
    print(response.body)

def unsubscribe(tag):
    request = Request(Method.UNSUB, [tag, username])
    clientSocket.send(pickle.dumps(request))
    response = clientSocket.recv(1024)
    response = pickle.loads(response)
    print(response.body)

def getTimeline():
    request = Request(Method.TIMELINE, username)
    clientSocket.send(pickle.dumps(request))
    response = getResponse()

    messages = response.body
    for tweet in messages:
        print(str(tweet))

# block until we get the response from the server
def getResponse():
    responseData = b''

    while True:
        data = clientSocket.recv(1024)
        responseData += data

        try:
            response = pickle.loads(responseData)
            break
        except:
            # still need more data to load the pickle object
            continue

    return response

#listens for commands from the user
#"pass" is just there temporarily until functionality is implemented
def listen():
    while connected:
        userInput = input()
        if userInput == "exit":
            logout(username)
        elif userInput[:5] == "tweet":
            sendTweet(userInput[5:])
        elif userInput[:9] == "subscribe":
            subscribe(userInput[11:])
        elif userInput[:11] == "unsubscribe":
            unsubscribe(userInput[13:])
        elif userInput == "timeline":
            getTimeline()
        elif userInput == "getusers":
            getUsers()
        elif userInput[:9] == "gettweets":
            getTweets(userInput[10:])
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


