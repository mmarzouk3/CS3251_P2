#CS 3251 Programming Assignment 2
#Authors: Weixi Li, Mariam Marzouk, Kelly McMaster
#Disclaimer / citation: The class textbook templates were referenced.

from socket import *
from _thread import start_new_thread
import sys

from users import User
from messages import Message

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
    response = ''
    for user in onlineUsers:
        response += str(user.get_username()) + " " #usernames separated by spaces
    return response

def sendTweetsList(username):
    # if the user exists, first character in response will be 1
    # else first character will be 0
    for user in onlineUsers:
        if user.username == username:
            response = '1'
            for message in user.messages:
                # message guaranteed to not have " character so we will use
                # this to separate full messages
                # hashtags are alphanumeric so we will split the tweet and hashtag
                # using @ symbol
                response += message.tweet + '@#' + "#".join(message.hashtags) + '"'
            return response
    # the requested username is not logged on
    response = "0no user " + username + " in the system"
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
                return "message length illegal, connection refused."
            else:
                if startIndexHash != -1: #hashtags found
                    hashtags = userInput[startIndexHash + 1:]
                    hashtagList = hashtags.split("#")
                    for hashtag in hashtagList:
                        if not hashtag.isalnum() or len(hashtag) < 1:
                            return "hashtag illegal format, connection refused."
                    else:
                        #Store message in the user's profile
                        userMessage = Message(tweetMessage, username, hashtagList)
                        for user in onlineUsers:
                            if user.get_username() == username:
                                user.add_tweets(userMessage)

                        #Store tweet
                        tweets.append(userMessage)
                        return 'success' #all's well

#processes the client's requests
#The first 10 characters are reserved to
#indicate the request type; the 10th char
#onwards contains the actual client message
def processClientRequests(data):
    request_type = data[:10] #first 10 characters reserved for request type
    message = data[10:] #10th character onwards is the actual client data
    print(request_type + message) #delete later
    if request_type == "check_user":
        username = message
        response = loginUserIfValid(username)
        return response
    elif request_type == "logout....":
        username = message
        deleteUser(username)
        response = "logged_out"
        return response
    elif request_type == "tweet.....":
        response = tweet(message)
    elif request_type == "get_users.":
        response = sendUserList()
    elif request_type == "get_tweets":
        username = message
        response = sendTweetsList(username)
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
            if reply:
                connectionSocket.sendall(reply.encode())

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
