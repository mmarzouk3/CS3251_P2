###CS3251_P2 README  

###CS 3251 Programming Assignment 2  
#Authors: Weixi Li, Mariam Marzouk, Kelly McMaster  

###High Level Description:  
We used multi-threading (the python _thread library) to handle multiple clients contacting the server.
We used pickle, a python library that allows the sending and receiving of objects, to help reduce the 
need for string parsing. 

On the client side, our implementation is centered around a continuously listening while loop. This loop
listens for commands entered by the user. Lots of the error-checking is done client-side for efficieny,
so that we don't waste resources sending the server invalid input.

On the server side, a new thread is created for each new client connection. 
To avoid the issue of IO blocking, the server keeps track of timeline messages for each user.
Then, when the user invokes the timeline command, the server sends over the relevant messages.

###Division of Labor:  
---Weixi handled subscribe/unsubscribe, implemented the user & message data structures, and designed the user and message objects.  
---Mariam handled the multiple-client functionality (multi-threading), logging on/off, and tweeting.  
---Kelly handled implementing pickle, gettweets, timeline, and desgined request/response objects for use with pickle. 

###How to Use the Code:
1) Open a terminal, and type $python3 ttweetser.py <ServerPort>
2) Open another terminal and type $python3 ttweetcli.py <ServerIP> <ServerPort> <Username>
3) Test the different commands

###Dependencies:
All 3rd party libraries used are standard; we did not have to specifically install anything extra.
For pickle to work, make sure your python version is >= 3.6.

