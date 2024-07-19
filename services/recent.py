from data import *
from datetime import datetime

class Tweet:
    def __init__(self, username: str, time: str, content: str, url: str):
        self.username = username
        self.time = time
        self.content = content
        self.url = url

    def is_recent(self, signal_time):
        current_time = datetime.utcnow()
        if self.time and self.time != 'Time not found':
            tweet_time = datetime.strptime(self.time, "%Y-%m-%d %H:%M:%S")
            time_diff = current_time - tweet_time
            return time_diff.total_seconds() < signal_time
        return False
