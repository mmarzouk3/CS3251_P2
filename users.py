class User:
    def __init__(self, username):
        # username should be a string
        self.username = username

        # sub_hashtag is short for subscribed hashtags (strings)
        self.sub_hashtag = []

        # messages is a list of Message objects
        self.messages = []

    # This function takes in a string tag and subscribes the user to the hastag
    # if their hastag subscribe has not hit 3 yet
    def subscribe_hashtag(self, tag):
        if len(self.sub_hashtag < 3):
            if not tag in self.sub_hashtag:
                self.sub_hashtag.add(tag)
                return "operation success" #message as per pdf guidelines
        else:
            return "operation failed: sub " +  tag + " failed, already exists or exceeds 3 limitation"

    # This function takes in a string tag and removes it from the user's
    # subscribed hashtags
    def remove_hashtag(self, tag):
        if tag in sub_hashtag:
            self.sub_hashtag.remove()
            return "operation success"
        else:
            return "You are not subscribed to this hashtag bub"

    # Make sure that everything in tweet is of object Message
    # This function will add a single Message object to the list of Messages
    def add_tweets(self, tweet):
        self.messages.append(tweet)

    #Get functions or we can delete this and just use the attributes either is fine
    def get_username(self):
        return self.username

    def get_subhashtasg(self):
        return self.sub_hashtag

    def get_messages(self):
        return self.get_messages

