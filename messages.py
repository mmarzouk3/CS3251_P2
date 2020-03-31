class Message:
    def __init__(self, tweet, username, hashtags):
        self.tweet = tweet
        self.username = username

        # Hashtags is a list of strings that contain all the hashtags of the tweet
        self.hashtags = hashtags

    # This function checks whether or a string tag exists in our hashtags list for the message
    def check_tag_exists(self, tag):
        return tag in self.hashtags

    # Once again, just get function, we can keep them or delete them

    def get_tweet(self):
        return self.tweet

    def get_username(self):
        return self.username

    def get_hashtags(self):
        return self.hashtags

    def __str__(self):
        return self.username + ': "' + self.tweet + '" #' + '#'.join(self.hashtags)
