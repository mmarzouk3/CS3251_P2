#CS 3251 Programming Assignment 2
#Authors: Weixi Li, Mariam Marzouk, Kelly McMaster
#Disclaimer / citation: The class textbook templates were referenced.

from socket import *
from _thread import start_new_thread
import sys
import pickle

from users import User
from messages import Message
from request import Method
from response import Response, Status

# list of User objects
onlineUsers = []

# list of Message Objects
tweets = []

#checks whether user input is valid
def checkInput(input_):
    pass #(remove later)
    #if something
    #exitGracefully()

#checks whether the username is valid (i.e. not taken)
def notTaken(username):
    for user in onlineUsers:
        if username == user.username:
            return False
    return True

#logs the user in if the username is valid
def loginUserIfValid(username):
    #add it to the list of online users if the username is valid
    if notTaken(username):
        onlineUsers.append(User(username))
        status = Status.OK
    else:
        status = Status.ERROR
    return Response(status)

#prints an error message and exits gracefully
#error 1 = too many arguments
def exitGracefully(errorType):
    #if error is blah
    #print message
    sys.exit()

#delete the user account and all associated messages
def deleteUser(username):
    try:
        for user in onlineUsers:
            if user.get_username() == username:
                break
        onlineUsers.remove(user)

        #delete the user's messages from the tweets list
        for tweet in tweets:
            if tweet.get_username() == username:
                tweets.remove(tweet)
    except:
        print("oops")
        pass

def sendUserList():
    userList = []
    for user in onlineUsers:
        userList.append(user.username)
    return Response(Status.OK, userList)

def sendTweetsList(username):
    # if the user exists, first character in response will be 1
    # else first character will be 0
    for user in onlineUsers:
        if user.username == username:
            response = Response(Status.OK, user.messages)
            return response

    # the requested username is not logged on
    response = Response(Status.ERROR, "no user " + username + " in the system")
    return response

#parses the tweet information from the user and stores it
def tweet(userInput):
    startIndex = userInput.find('\"') #the starting index of the tweet message
    startIndexHash = userInput.find('#') #the starting index of the hashtags
    username = userInput[:startIndex - 1]
    if startIndex != -1: #i.e. if the first quote was found
        endIndex = userInput.find('\"', startIndex + 1)
        if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
            tweetMessage = userInput[startIndex + 1: endIndex]
            if len(tweetMessage) < 1 or len(tweetMessage) > 150:
                return Response(Status.ERROR, "message length illegal, connection refused.")
            else:
                if startIndexHash != -1: #hashtags found
                    hashtags = userInput[startIndexHash + 1:]
                    hashtagList = hashtags.split("#")
                    for hashtag in hashtagList:
                        if not hashtag.isalnum() or len(hashtag) < 1:
                            return Response(Status.ERROR, "hashtag illegal format, connection refused.")
                    else:
                        #Store message in the user's profile
                        userMessage = Message(tweetMessage, username, hashtagList)
                        for user in onlineUsers:
                            if user.get_username() == username:
                                user.add_tweets(userMessage)

                        #Store tweet
                        tweets.append(userMessage)

                        return Response(Status.OK) #all's well

def subscribeToTag(tag, username):
    for user in onlineUsers:
        if user.username == username:
            break
    return Response(Status.OK, user.subscribe_hashtag(tag))

def unsubscribeToTag(tag, username):
    for user in onlineUsers:
        if user.username == username:
            break
    return Response(Status.OK, user.remove_hashtag(tag))


#processes the client's requests
#The first 10 characters are reserved to
#indicate the request type; the 10th char
#onwards contains the actual client message
def processClientRequests(request):
    if request.method == Method.CHECK_USER:
        # login request will have username in the body
        response = loginUserIfValid(request.body)
    elif request.method == Method.LOGOUT:
        # logout request will have username in body
        deleteUser(request.body)
        response = Response(Status.OK, "logged_out")
    elif request.method == Method.TWEET:
        response = tweet(request.body)
    elif request.method == Method.SUB:
        response = subscribeToTag(request.body[0], request.body[1])
    elif request.method == Method.UNSUB:
        response = unsubscribeToTag(request.body[0], request.body[1])
    elif request.method == Method.GET_USERS:
        response = sendUserList()
    elif request.method == Method.GET_TWEETS:
        response = sendTweetsList(request.body)
    else:
        response = Response(Status.ERROR, "unrecognized request")

    return response

#creates a thread for the new client trying to log in
def client_thread(connectionSocket):
    connected = True
    while connected:
        request = connectionSocket.recv(1024)
        request = pickle.loads(request)
        if not request:
            break
        reply = processClientRequests(request)
        if reply.body == 'logged_out':
            connectionSocket.close()
            connected = False
        else:
            if reply:
                connectionSocket.sendall(pickle.dumps(reply))

#------------------------------
#-----MAIN SERVER CODE---------
#------------------------------
#command line arg parsing and error checks
if __name__ == "__main__":
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
