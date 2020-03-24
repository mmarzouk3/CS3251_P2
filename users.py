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
    def subscribe_hashtag(tag):
        if len(self.sub_hashtag < 3):
            self.sub_hashtag.add(tag)
            return "You've successfully subcribed!"
        else:
            return "You already are subscribed to three hashtags"

    # This function takes in a string tag and removes it from the user's
    # subscribed hashtags
    def remove_hashtag(tag):
        if tag in sub_hashtag:
            self.sub_hashtag.remove()
            return "You've successfully remove the tag!"
        else:
            return "You are not subscribed to this hashtag"

    # Make sure that everything in tweet is of object Message
    # This function will add a single Message object to the list of Messages
    def add_tweets(tweet):
        self.messages.add(tweet)

    #Get functions or we can delete this and just use the attributes either is fine
    def get_username():
        return self.username

    def get_subhashtasg():
        return self.sub_hashtag

    def get_messages():
        return self.get_messages

