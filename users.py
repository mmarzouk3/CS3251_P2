class User:
    def __init__(self, username):
        # username should be a string
        self.username = username

        # sub_hashtag is short for subscribed hashtags (strings)
        self.sub_hashtag = []

        # messages is a list of Message objects
        self.messages = []

        # list of timeline messages
        self.timelineMessages = []

    # This function takes in a string tag and subscribes the user to the hastag
    # if their hastag subscribe has not hit 3 yet
    def subscribe_hashtag(self, tag):
        if len(self.sub_hashtag) < 3:
            if not tag in self.sub_hashtag:
                self.sub_hashtag.append(tag)
                print(self.sub_hashtag)
                return "operation success" #message as per pdf guidelines
            else:
                return "operation failed: sub " +  tag + " failed, already exists or exceeds 3 limitation"
        else:
            return "operation failed: sub " +  tag + " failed, already exists or exceeds 3 limitation"

    # This function takes in a string tag and removes it from the user's
    # subscribed hashtags
    def remove_hashtag(self, tag):
        if tag == "ALL":
            self.sub_hashtag.clear() #delete all subbed hashtags
            return "operation success"
        if tag in self.sub_hashtag:
            self.sub_hashtag.remove(tag)
            return "operation success"
        else:
            return "operation success" #pdf states "no effect", i.e it counts as a success?

    def has_subscription(self, tags):
        if "ALL" in self.sub_hashtag:
            return True

        for tag in tags:
            if tag in self.sub_hashtag:
                #print("user: " + self.username + "has subscription: " + tag)
                return True
        return False

    # Make sure that everything in tweet is of object Message
    # This function will add a single Message object to the list of Messages
    def add_tweets(self, tweet):
        self.messages.append(tweet)

    def add_to_timeline(self, tweet):
        self.timelineMessages.append(tweet)

    #Get functions or we can delete this and just use the attributes either is fine
    def get_username(self):
        return self.username

    def get_subhashtasg(self):
        return self.sub_hashtag

    def get_messages(self):
        return self.messages

